#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2014 Free and Open Source Software Learning Centre
# http://fosslc.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

import json
import os

import pytest

from freeseer import settings
from freeseer.framework.config.profile import ProfileManager
from freeseer.framework.multimedia import Multimedia
from freeseer.framework.plugin import PluginManager
from freeseer.frontend.controller import server


class MockMedia:
    def __init__(self):
        self.current_state = Multimedia.NULL
        self.num_times_record_called = 0
        self.num_times_stop_called = 0
        self.num_times_pause_called = 0

    def record(self):
        self.num_times_record_called += 1

    def pause(self):
        self.num_times_pause_called += 1

    def stop(self):
        self.num_times_stop_called += 1


class TestServerApp:
    '''
    Test cases for Server.
    '''

    @pytest.fixture(scope='module')
    def test_client(self):
        server.app.config['TESTING'] = True
        server.app.storage_file_path = "test_storage_file"
        return server.app.test_client()

    @pytest.fixture(scope='function', autouse=True)
    def recording(self, request, test_client, monkeypatch, tmpdir):

        recording = server.app.blueprints['recording']

        monkeypatch.setattr(settings, 'configdir', str(tmpdir.mkdir('configdir')))
        test_client.get('/recordings')

        profile_manager = ProfileManager(str(tmpdir.mkdir('profile')))
        recording.profile = profile_manager.get('testing')
        recording.config = recording.profile.get_config('freeseer.conf', settings.FreeseerConfig, ['Global'], read_only=True)
        recording.config.videodir = str(tmpdir.mkdir('Videos'))
        recording.plugin_manager = PluginManager(recording.profile)

        return recording

    @pytest.fixture(scope='function')
    def mock_media_dict(self, request, recording):
        mock_media_1 = MockMedia()
        mock_media_2 = MockMedia()

        filepath1 = os.path.join(recording.config.videodir, 'mock_media_1')
        filepath2 = os.path.join(recording.config.videodir, 'mock_media_2')

        recording.media_info['1'] = {
            'status': Multimedia.NULL,
            'filename': 'mock_media_1',
            'filepath': filepath1,
        }
        recording.media_info['2'] = {
            'status': Multimedia.NULL,
            'filename': 'mock_media_2',
            'filepath': filepath2,
        }

        recording.media_dict = {
            1: mock_media_1,
            2: mock_media_2,
        }

        def clear_media():
            recording.media_info.clear()
            recording.media_dict = {}
        request.addfinalizer(clear_media)

        return recording.media_dict

    def test_get_all_recordings_empty_media_dict(self, test_client):
        '''
        Tests GET request retrieving all recordings with from an empty media dict
        '''
        response = test_client.get('/recordings')
        response_data = json.loads(response.data)
        assert response_data == {'recordings': []}

    def test_get_nonexistent_recording_id(self, test_client):
        '''
        Tests GET request retrieving non-existent recording
        '''
        response = test_client.get('/recordings/1')
        response_data = json.loads(response.data)
        assert response_data['error_code'] == 404
        assert response.status_code == 404

    def test_get_all_recordings(self, test_client, mock_media_dict):
        '''
        Tests GET request all recordings with 2 entries in media dict
        '''
        response = test_client.get('/recordings')
        response_data = json.loads(response.data)
        assert response_data == {'recordings': [1, 2]}

    def test_get_recording_id(self, test_client, mock_media_dict):
        '''
        Tests GET request specific valid recording
        '''
        response = test_client.get('/recordings/1')
        response_data = json.loads(response.data)
        assert response.status_code == 200

        assert response_data == {
            'filename': 'mock_media_1',
            'filesize': 'NA',
            'id': 1,
            'status': 'NULL',
        }

    def test_get_invalid_recording_id(self, test_client, mock_media_dict):
        '''
        Tests GET request with an invalid id (a non integer id)
        '''
        response = test_client.get('/recordings/abc')
        assert response.status_code == 404

        response = test_client.get('/recordings/1.0')
        assert response.status_code == 404

    def test_patch_no_id(self, test_client):
        '''
        Tests a PATCH request without a recording id
        '''
        response = test_client.patch('/recordings')
        assert response.status_code == 405

    def test_patch_nonexistant_id(self, test_client, mock_media_dict):
        '''
        Tests a PATCH request with non-existant recording id
        '''
        response = test_client.patch('/recordings/100', data={'command': 'start'})
        assert response.status_code == 404

    def test_patch_no_command(self, test_client, mock_media_dict):
        '''
        Tests a PATCH request without a command
        '''
        response = test_client.patch('/recordings/1')
        assert response.status_code == 400

    def test_patch_invalid_command(self, test_client, mock_media_dict):
        '''
        Tests a Patch request with an invalid command
        '''
        response = test_client.patch('/recordings/1', data={'command': 'invalid command'})
        assert response.status_code == 400

    @pytest.mark.parametrize("current_state", [Multimedia.NULL, Multimedia.PAUSE])
    def test_patch_start(self, test_client, recording, mock_media_dict, current_state):
        '''
        Tests a Patch request to start a recording
        '''
        mock_media_dict[1].current_state = current_state
        response = test_client.patch('/recordings/1', data={'command': 'start'})
        assert response.status_code == 200
        assert mock_media_dict[1].num_times_record_called == 1

    @pytest.mark.parametrize("current_state", [Multimedia.STOP, Multimedia.RECORD])
    def test_patch_start_invalid(self, test_client, mock_media_dict, current_state):
        '''
        Tests a Patch request to start a recording with an invalid media state
        '''
        mock_media_dict[1].current_state = current_state
        response = test_client.patch('/recordings/1', data={'command': 'start'})
        assert response.status_code == 400
        assert mock_media_dict[1].num_times_record_called == 0

    def test_patch_pause(self, test_client, mock_media_dict):
        '''
        Tests a Patch request to pause a recording
        '''
        mock_media_dict[1].current_state = Multimedia.RECORD
        response = test_client.patch('/recordings/1', data={'command': 'pause'})
        assert response.status_code == 200
        assert mock_media_dict[1].num_times_pause_called == 1

    @pytest.mark.parametrize("current_state", [Multimedia.NULL, Multimedia.PAUSE, Multimedia.STOP])
    def test_patch_pause_invalid(self, test_client, mock_media_dict, current_state):
        '''
        Tests a Patch request to pause a recording with an invalid media state
        '''
        mock_media_dict[1].current_state = current_state
        response = test_client.patch('/recordings/1', data={'command': 'pause'})
        assert response.status_code == 400
        assert mock_media_dict[1].num_times_pause_called == 0

    @pytest.mark.parametrize("current_state", [Multimedia.PAUSE, Multimedia.RECORD])
    def test_patch_stop(self, test_client, mock_media_dict, current_state):
        '''
        Tests a Patch request to stop a recording
        '''
        mock_media_dict[1].current_state = current_state
        response = test_client.patch('/recordings/1', data={'command': 'stop'})
        assert response.status_code == 200
        assert mock_media_dict[1].num_times_stop_called == 1

    @pytest.mark.parametrize("current_state", [Multimedia.STOP, Multimedia.NULL])
    def test_patch_stop_invalid(self, test_client, mock_media_dict, current_state):
        '''
        Tests a Patch request to stop a recording with an invalid media state
        '''
        mock_media_dict[1].current_state = current_state
        response = test_client.patch('/recordings/1', data={'command': 'stop'})
        assert response.status_code == 400
        assert mock_media_dict[1].num_times_stop_called == 0

    def test_post_no_filename(self, test_client):
        '''
        Tests a POST request without a filename
        '''
        response = test_client.post('/recordings')
        assert response.status_code == 400

    def test_post_empty_filename(self, test_client):
        '''
        Tests a POST request with an empty filename
        '''
        response = test_client.post('/recordings', data={'filename': ''})
        assert response.status_code == 400

    def test_post_invalid_filename(self, test_client):
        '''
        Tests a POST request with an invalid filename
        '''
        response = test_client.post('/recordings', data={'filename': 'abc/123'})
        assert response.status_code == 400

    def test_post(self, test_client, recording):
        '''
        Tests a regular POST request
        '''
        assert len(recording.media_dict) == 0
        response = test_client.post('/recordings', data={'filename': 'test'})
        assert response.status_code == 201
        assert list(recording.media_dict.keys()) == [1]
        assert recording.media_info['1']['filename'] == 'test.ogg'

    def test_delete_no_recording_id(self, test_client):
        '''
        Tests a DELETE request without a provided recording id
        '''
        response = test_client.delete('/recordings')
        assert response.status_code == 405

    def test_delete_nonexistent_recording_id(self, test_client):
        '''
        Tests a DELETE request with a recording id that doesn't exist
        '''
        response = test_client.delete('/recordings/100')
        assert response.status_code == 404

    @pytest.mark.parametrize("invalid_id", ['abc', '1.0'])
    def test_delete_invalid_recording_id(self, test_client, invalid_id):
        '''
        Tests a DELETE request with an invalid recording id
        '''
        response = test_client.delete('/recordings/{0}'.format(invalid_id))
        assert response.status_code == 404

    @pytest.mark.parametrize("current_state", [Multimedia.RECORD, Multimedia.PAUSE])
    def test_delete_in_progress_recording(self, test_client, recording, mock_media_dict, current_state):
        '''
        Tests a DELETE request for a recording that is paused or in progress
        '''

        # delete a recording that is in the middle of recording
        mock_media_dict[1].current_state = current_state
        del_media = mock_media_dict[1]
        response = test_client.delete('/recordings/1')
        assert response.status_code == 204
        assert del_media.num_times_stop_called == 1
        assert list(recording.media_dict.keys()) == [2]

    def test_delete_recording_id_and_file(self, test_client, recording, mock_media_dict):
        '''
        Tests a DELETE request where the recording has a specified file
        '''

        # setup - create the file to be deleted
        file_base_name = 'testDeleteFile'
        file_to_delete = file_base_name
        file_to_delete_path = os.path.join(recording.config.videodir, file_to_delete)
        test_file = open(file_to_delete_path, 'a')
        test_file.close()

        # assert the file exists
        assert os.path.isfile(file_to_delete_path)

        # set mock_media filepath to filepath of file to be deleted
        recording.media_info['1']['filepath'] = file_to_delete_path

        response = test_client.delete('/recordings/1')
        assert response.status_code == 204
        assert list(recording.media_dict.keys()) == [2]

        # assert the file no longer exists
        assert not os.path.isfile(file_to_delete_path)
