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

import json
import os
import signal

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


def teardown_recording(signum, frame):
    """Teardown method for recording api.

    Stops any active recordings and saves to disk. Called on server shutdown for graceful exit.
    """
    persistent = {}
    recording = app.blueprints['recording']

    for key in recording.media_dict:
        entry = recording.media_dict[key]
        entry_media = entry['media']

        if entry_media.current_state == Multimedia.RECORD or entry_media.current_state == Multimedia.PAUSE:
            entry_media.stop()

        persistent[key] = {
            'filename': entry['filename'],
            'filepath': entry['filepath'],
            'status': entry_media.current_state
        }
    with open(recording.storage_file, 'w') as fd:
        fd.write(json.dumps(persistent))


@recording.before_app_first_request
def configure_recording():
    """Configures freeseer to record via REST server.

    Gets recording profiles and configuration and instantiates recording plugins. Then it restores any stored talks.
    Runs upon first call to REST server.
    """
    # setup the application so it exits gracefully
    signal.signal(signal.SIGINT, teardown_recording)
    recording.record_profile = settings.profile_manager.get()
    recording.record_config = recording.record_profile.get_config('freeseer.conf', settings.FreeseerConfig,
                                                                  storage_args=['Global'], read_only=True)
    recording.record_plugin_manager = PluginManager(recording.record_profile)
    recording.storage_file = os.path.join(settings.configdir, app.storage_file_path)
    recording.next_id = 1

    # restore talks from storage
    if os.path.isfile(recording.storage_file):
        with open(recording.storage_file) as fd:
            persistent = json.loads(fd.read())

        recording.media_dict = {}
        for key in persistent:
            new_media = Multimedia(recording.record_config, recording.record_plugin_manager)
            new_media.current_state = persistent[key]['status']
            media_id = int(key)

            if new_media.current_state == Multimedia.NULL:
                filename = persistent[key]['filename'].split(".ogg")[0]
                success, filename = new_media.load_backend(None, filename)

                if success:
                    filepath = new_media.plugman.get_plugin_by_name(new_media.config.record_to_file_plugin, "Output").plugin_object.location
                    recording.media_dict[media_id] = {
                        'media': new_media,
                        'filename': filename,
                        'filepath': filepath
                    }
                else:
                    raise ServerError('Could not load multimedia backend')
            else:
                recording.media_dict[media_id] = {
                    'media': new_media,
                    'filename': persistent[key]['filename'],
                    'filepath': persistent[key]['filepath']
                }

        # sets next_id to last index of persistent + 1
        recording.next_id = len(persistent)
    else:
        # if no talks to restore, make empty media_dict, set next_id to 1
        recording.media_dict = {}
        recording.next_id = 1


@recording.route('/recordings', methods=['GET'])
@http_response(200)
def get_all_recordings():
    """Returns list of all recordings."""
    return {'recordings': recording.media_dict.keys()}


@recording.route('/recordings/<int:recording_id>', methods=['GET'])
@http_response(200)
def get_specific_recording(recording_id):
    """Returns specific recording by id."""
    recording_id = int(recording_id)
    if recording_id in recording.media_dict:
        retrieved_media_entry = recording.media_dict[recording_id]
        retrieved_media = retrieved_media_entry['media']
        retrieved_filename = retrieved_media_entry['filename']

        state_indicator = retrieved_media.current_state
        if state_indicator == Multimedia.NULL:
            state = 'NULL'
        elif state_indicator == Multimedia.RECORD:
            state = 'RECORD'
        elif state_indicator == Multimedia.PAUSE:
            state = 'PAUSE'
        elif state_indicator == Multimedia.STOP:
            state = 'STOP'
        else:
            raise HTTPError('recording state could not be determined', 500)

        if os.path.isfile(retrieved_media_entry['filepath']):
            filesize = os.path.getsize(retrieved_media_entry['filepath'])
        else:
            filesize = 'NA'

        return {
            'id': recording_id,
            'filename': retrieved_filename,
            'filesize': filesize,
            'status': state
        }

    else:
        raise HTTPError('recording id could not be found', 404)


@recording.route('/recordings/<int:recording_id>', methods=['PATCH'])
@http_response(200)
def control_recording(recording_id):
    """Change the state of a recording."""
    recording_id = int(recording_id)
    if recording_id in recording.media_dict:
        retrieved_media_entry = recording.media_dict[recording_id]
        retrieved_media = retrieved_media_entry['media']
        if validate.validate_control_recording_request_form(request.form):
            command = request.form['command']
            media_state = retrieved_media.current_state

            if command == 'start' and media_state in [Multimedia.NULL, Multimedia.PAUSE]:
                retrieved_media.record()
            elif command == 'pause' and media_state == Multimedia.RECORD:
                retrieved_media.pause()
            elif command == 'stop' and media_state in [Multimedia.RECORD, Multimedia.PAUSE]:
                retrieved_media.stop()
            else:
                raise HTTPError('command could not be performed', 400)
        else:
            raise HTTPError('Form data was invalid', 400)

    else:
        raise HTTPError('recording id could not be found', 404)

    return ''


@recording.route('/recordings', methods=['POST'])
@http_response(201)
def create_recording():
    """Initializes a recording and returns its id."""
    if validate.validate_create_recording_request_form(request.form):
        new_filename = request.form['filename']
        new_media = Multimedia(recording.record_config, recording.record_plugin_manager)
        success, filename = new_media.load_backend(None, new_filename)

        if success:
            filepath = new_media.plugman.get_plugin_by_name(new_media.config.record_to_file_plugin, "Output").plugin_object.location
            new_recording_id = recording.next_id
            recording.next_id = recording.next_id + 1

            if new_recording_id not in recording.media_dict:
                recording.media_dict[new_recording_id] = {
                    'media': new_media,
                    'filename': filename,
                    'filepath': filepath
                }

                return {'id': new_recording_id}
            else:
                raise HTTPError('Provided id already in use', 500)
        else:
            raise HTTPError('Could not load multimedia backend', 500)
    else:
        raise HTTPError('Form data was invalid', 400)


@recording.route('/recordings/<int:recording_id>', methods=['DELETE'])
@http_response(204)
def delete_recording(recording_id):
    """Deletes a recording given an id."""
    recording_id = int(recording_id)
    if recording_id in recording.media_dict:
        retrieved_media_entry = recording.media_dict[recording_id]
        retrieved_media = retrieved_media_entry['media']

        if retrieved_media.current_state == Multimedia.RECORD or retrieved_media.current_state == Multimedia.PAUSE:
            retrieved_media.stop()

        # Delete the file if it exists
        if os.path.isfile(retrieved_media_entry['filepath']):
            os.remove(retrieved_media_entry['filepath'])

        del recording.media_dict[recording_id]
    else:
        raise HTTPError('recording id could not be found', 404)

    return ''
