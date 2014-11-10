#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

import functools
import os
import shelve

from flask import Blueprint
from flask import request

from freeseer import settings
from freeseer.framework.multimedia import Multimedia
from freeseer.framework.plugin import PluginManager
from freeseer.frontend.controller import app
from freeseer.frontend.controller import validate
from freeseer.frontend.controller.server import HTTPError
from freeseer.frontend.controller.server import ServerError
from freeseer.frontend.controller.server import http_response

recording = Blueprint('recording', __name__)

recording.form_schema = {
    'control_recording': {
        'type': 'object',
        'properties': {
            'command': {
                'enum': ['start', 'pause', 'stop']
            }
        },
        'required': ['command']
    },
    'create_recording': {
        'type': 'object',
        'properties': {
            'filename': {
                'type': 'string',
                'pattern': '^\w+$'
            }
        },
        'required': ['filename']
    }
}


def sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response_dict = func(*args, **kwargs)
        recording.media_info.sync()
        return response_dict
    return wrapper


@recording.before_app_first_request
def configure_recording():
    """Configures freeseer to record via REST server.

    Gets recording profiles and configuration and instantiates recording plugins. Then it restores any stored talks.
    Runs upon first call to REST server.
    """
    recording.profile = settings.profile_manager.get()
    recording.config = recording.profile.get_config('freeseer.conf', settings.FreeseerConfig,
                                                    storage_args=['Global'], read_only=True)
    recording.plugin_manager = PluginManager(recording.profile)
    recording.storage_file = os.path.join(settings.configdir, app.storage_file_path)

    media_info = shelve.open(recording.storage_file, writeback=True)

    recording.next_id = 1
    recording.media_dict = {}
    for key, value in media_info.iteritems():
        new_media = Multimedia(recording.config, recording.plugin_manager)
        if value['null_multimeda']:
            new_media.current_state = Multimedia.NULL
        else:
            # if null_multimeda is False, a video exists, set current_state to Multimedia.STOP
            new_media.current_state = Multimedia.STOP

        media_id = int(key)
        if media_id >= recording.next_id:
            recording.next_id = media_id + 1

        if new_media.current_state == Multimedia.NULL:
            filename = value['filename'].split('.ogg')[0]
            success, filename = new_media.load_backend(None, filename)

            if not success:
                raise ServerError('Could not load multimedia backend')

            value['filename'] = filename

            value['filepath'] = new_media.plugman.get_plugin_by_name(new_media.config.record_to_file_plugin, "Output").plugin_object.location

        recording.media_dict[media_id] = new_media

    recording.media_info = media_info
    recording.media_info.sync()


@recording.route('/recordings', methods=['GET'])
@http_response(200)
def get_all_recordings():
    """Returns list of all recordings."""
    return {'recordings': recording.media_dict.keys()}


@recording.route('/recordings/<int:recording_id>', methods=['GET'])
@http_response(200)
def get_specific_recording(recording_id):
    """Returns specific recording by id."""

    key = str(recording_id)
    try:
        retrieved_media_entry = recording.media_info[key]
    except KeyError:
        raise HTTPError(404, 'No recording with id "{}" was found'.format(recording_id))

    current_state = recording.media_dict[recording_id].current_state
    filename = retrieved_media_entry['filename']

    try:
        filesize = os.path.getsize(retrieved_media_entry['filepath'])
    except OSError:
        filesize = 'NA'

    return {
        'id': recording_id,
        'filename': filename,
        'filesize': filesize,
        'status': current_state,
    }


@recording.route('/recordings/<int:recording_id>', methods=['PATCH'])
@http_response(200)
@sync
def control_recording(recording_id):
    """Change the state of a recording."""

    validate.validate_form(request.form, recording.form_schema['control_recording'])

    try:
        retrieved_media = recording.media_dict[recording_id]
    except KeyError:
        raise HTTPError(404, 'No recording with id "{}" was found'.format(recording_id))

    command = request.form['command']
    media_state = retrieved_media.current_state

    if command == 'start' and media_state in [Multimedia.NULL, Multimedia.PAUSE]:
        retrieved_media.record()
    elif command == 'pause' and media_state == Multimedia.RECORD:
        retrieved_media.pause()
    elif command == 'stop' and media_state in [Multimedia.RECORD, Multimedia.PAUSE]:
        retrieved_media.stop()
    else:
        raise HTTPError(400, 'Command "{}" could not be performed'.format(command))

    if media_state is not Multimedia.NULL:
        key = str(recording_id)
        recording.media_info[key]['null_multimeda'] = False

    return ''


@recording.route('/recordings', methods=['POST'])
@http_response(201)
@sync
def create_recording():
    """Initializes a recording and returns its id."""

    validate.validate_form(request.form, recording.form_schema['create_recording'])

    new_filename = request.form['filename']
    new_media = Multimedia(recording.config, recording.plugin_manager)
    success, filename = new_media.load_backend(None, new_filename)

    if not success:
        raise HTTPError(500, 'Could not load multimedia backend')

    filepath = new_media.plugman.get_plugin_by_name(new_media.config.record_to_file_plugin, "Output").plugin_object.location
    new_recording_id = recording.next_id
    key = str(new_recording_id)

    recording.media_dict[new_recording_id] = new_media
    recording.media_info[key] = {
        'filename': filename,
        'filepath': filepath,
        'null_multimeda': True,
    }
    recording.next_id = recording.next_id + 1
    recording.media_info.sync()

    return {'id': new_recording_id}


@recording.route('/recordings/<int:recording_id>', methods=['DELETE'])
@http_response(204)
@sync
def delete_recording(recording_id):
    """Deletes a recording given an id."""
    try:
        retrieved_media = recording.media_dict[recording_id]
    except KeyError:
        raise HTTPError(404, 'No recording with id "{}" was found'.format(recording_id))

    key = str(recording_id)
    retrieved_media_entry = recording.media_info[key]

    if retrieved_media.current_state in [Multimedia.RECORD, Multimedia.PAUSE]:
        retrieved_media.stop()

    # Delete the file if it exists
    try:
        os.remove(retrieved_media_entry['filepath'])
    except OSError:
        pass

    del recording.media_dict[recording_id]
    del recording.media_info[key]
    recording.media_info.sync()

    return ''
