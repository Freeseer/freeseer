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
import json
import os
import signal
import sys

from flask import current_app
from flask import Flask
from flask import jsonify
from flask import request

from freeseer import settings
from freeseer.framework.multimedia import Multimedia
from freeseer.framework.plugin import PluginManager
from freeseer.frontend.controller import validate

app = Flask(__name__)


class HTTPError(Exception):

    def __init__(self, message, status_code):
        super(HTTPError, self).__init__(message)
        self.message = message
        self.status_code = status_code


class ServerError(Exception):

    def __init__(self, message):
        super(ServerError, self).__init__(message)


def catch_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            return e.message, e.status_code
    return wrapper


@app.route('/recordings', methods=['GET'])
def get_all_recordings():
    response = jsonify({'recordings': current_app.media_dict.keys()})
    response.status_code = 200
    return response


@app.route('/recordings/<int:recording_id>', methods=['GET'])
@catch_exceptions
def get_specific_recording(recording_id):
    response = ''

    recording_id = int(recording_id)
    if recording_id in current_app.media_dict:
        retrieved_media_entry = current_app.media_dict[recording_id]
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

        response = jsonify({
            'id': recording_id,
            'filename': retrieved_filename,
            'filesize': filesize,
            'status': state
        })
        response.status_code = 200

    else:
        raise HTTPError('recording id could not be found', 404)

    return response


@app.route('/recordings/<int:recording_id>', methods=['PATCH'])
@catch_exceptions
def control_recording(recording_id):
    response = ''

    recording_id = int(recording_id)
    if recording_id in current_app.media_dict:
        retrieved_media_entry = current_app.media_dict[recording_id]
        retrieved_media = retrieved_media_entry['media']
        if validate.validate_control_recording_request_form(request.form):
            command = request.form['command']
            media_state = retrieved_media.current_state

            if command == 'start' and media_state in [Multimedia.NULL, Multimedia.PAUSE]:
                retrieved_media.record()
                response = '', 200
            elif command == 'pause' and media_state == Multimedia.RECORD:
                retrieved_media.pause()
                response = '', 200
            elif command == 'stop' and media_state in [Multimedia.RECORD, Multimedia.PAUSE]:
                retrieved_media.stop()
                response = '', 200
            else:
                raise HTTPError('command could not be performed', 400)
        else:
            raise HTTPError('Form data was invalid', 400)

    else:
        raise HTTPError('recording id could not be found', 404)

    return response


@app.route('/recordings', methods=['POST'])
@catch_exceptions
def create_recording():
    response = ''

    if validate.validate_create_recording_request_form(request.form):
        new_filename = request.form['filename']
        new_media = Multimedia(current_app.record_config, current_app.record_plugin_manager)
        success, filename = new_media.load_backend(None, new_filename)

        if success:
            filepath = new_media.plugman.get_plugin_by_name(new_media.config.record_to_file_plugin, "Output").plugin_object.location

            new_recording_id = current_app.next_id
            current_app.next_id = current_app.next_id + 1

            if new_recording_id not in current_app.media_dict:
                current_app.media_dict[new_recording_id] = {
                    'media': new_media,
                    'filename': filename,
                    'filepath': filepath
                }

                response = jsonify({'id': new_recording_id})
                response.status_code = 201
            else:
                raise HTTPError('Provided id already in use', 500)
        else:
            raise HTTPError('Could not load multimedia backend', 500)
    else:
        raise HTTPError('Form data was invalid', 400)

    return response


@app.route('/recordings/<int:recording_id>', methods=['DELETE'])
@catch_exceptions
def delete_recording(recording_id):
    recording_id = int(recording_id)
    if recording_id in current_app.media_dict:
        retrieved_media_entry = current_app.media_dict[recording_id]
        retrieved_media = retrieved_media_entry['media']

        if retrieved_media.current_state == Multimedia.RECORD or retrieved_media.current_state == Multimedia.PAUSE:
            retrieved_media.stop()

        # Delete the file if it exists
        if os.path.isfile(retrieved_media_entry['filepath']):
            os.remove(retrieved_media_entry['filepath'])

        del current_app.media_dict[recording_id]
        response = '', 200
    else:
        raise HTTPError('recording id could not be found', 404)

    return response


def exit_gracefully(signum, frame):
    persistant = {}

    # transfer the file information into the dictionary
    for key in app.media_dict:
        entry = app.media_dict[key]
        entry_media = entry['media']

        # stop the recording if it is in progress or paused
        if entry_media.current_state == Multimedia.RECORD or entry_media.current_state == Multimedia.PAUSE:
            entry_media.stop()

        persistant[key] = {
            'filename': entry['filename'],
            'filepath': entry['filepath'],
            'status': entry_media.current_state
        }

    with open(app.storage_file, 'w') as fd:
        fd.write(json.dumps(persistant))

    sys.exit(1)


def configure(storage_file):
    app.record_profile = settings.profile_manager.get()
    app.record_config = app.record_profile.get_config('freeseer.conf', settings.FreeseerConfig, ['Global'], read_only=True)
    app.record_plugin_manager = PluginManager(app.record_profile)
    app.storage_file = os.path.join(settings.configdir, storage_file)
    app.next_id = 1

    # restore talks from storage
    if os.path.isfile(app.storage_file):
        with open(app.storage_file) as fd:
            persistant = json.loads(fd.read())

        app.media_dict = {}
        for key in persistant:
            new_media = Multimedia(app.record_config, app.record_plugin_manager)
            new_media.current_state = persistant[key]['status']
            int_key = int(key)

            if new_media.current_state == Multimedia.NULL:
                filename = persistant[key]['filename'].split(".ogg")[0]
                success, filename = new_media.load_backend(None, filename)

                if success:
                    filepath = new_media.plugman.get_plugin_by_name(new_media.config.record_to_file_plugin, "Output").plugin_object.location
                    app.media_dict[int_key] = {
                        'media': new_media,
                        'filename': filename,
                        'filepath': filepath
                    }
                else:
                    raise ServerError('Could not load multimedia backend')
            else:
                app.media_dict[int_key] = {
                    'media': new_media,
                    'filename': persistant[key]['filename'],
                    'filepath': persistant[key]['filepath']
                }

            if int_key >= app.next_id:
                app.next_id = int_key + 1
    else:
        app.media_dict = {}


def start_server(storage_file):
    # setup the application so it exits gracefully
    signal.signal(signal.SIGINT, exit_gracefully)

    configure(storage_file)
    app.run()
