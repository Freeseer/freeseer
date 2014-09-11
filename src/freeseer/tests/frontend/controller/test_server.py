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
import shutil
import tempfile
import unittest

from freeseer import settings
from freeseer.framework.config.profile import ProfileManager
from freeseer.framework.multimedia import Multimedia
from freeseer.framework.plugin import PluginManager
from freeseer.frontend.controller import server


class MockMedia():
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


class TestServerApp(unittest.TestCase):
    '''
    Test cases for Server.
    '''

    def setUp(self):
        '''
        Stardard init method: runs before each test_* method
        '''
        server.app.config['TESTING'] = True
        server.app.storage_file_path = "test_storage_file"
        self.app = server.app.test_client()
        self.recording = server.app.blueprints['recording']

        # token call to fire configuration logic
        self.app.get('/recordings')
        print self.recording.record_config.videodir

        self.profile_manager = ProfileManager(tempfile.mkdtemp())
        self.temp_video_dir = tempfile.mkdtemp()
        self.recording.record_config.videodir = self.temp_video_dir
        self.recording.record_profile = self.profile_manager.get('testing')
        self.recording.record_config = self.recording.record_profile.get_config('freeseer.conf', settings.FreeseerConfig, ['Global'], read_only=True)
        self.recording.record_plugin_manager = PluginManager(self.recording.record_profile)
        self.recording.media_dict = {}

        # mock media
        self.mock_media_1 = MockMedia()
        self.mock_media_2 = MockMedia()

        self.test_media_dict_1 = {}
        filepath1 = os.path.join(self.recording.record_config.videodir, 'mock_media_1')
        filepath2 = os.path.join(self.recording.record_config.videodir, 'mock_media_1')
        self.test_media_dict_1[1] = {'media': self.mock_media_1, 'filename': 'mock_media_1', 'filepath': filepath1}
        self.test_media_dict_1[2] = {'media': self.mock_media_2, 'filename': 'mock_media_2', 'filepath': filepath2}

    def tearDown(self):
        '''
        Generic unittest.TestCase.tearDown()
        '''
        shutil.rmtree(self.profile_manager._base_folder)
        shutil.rmtree(self.temp_video_dir)
        del self.app

    def test_get_all_recordings_empty_media_dict(self):
        '''
        Tests GET request retrieving all recordings with from an empty media dict
        '''
        response = self.app.get('/recordings')
        response_data = json.loads(response.data)
        self.assertTrue('recordings' in response_data)
        self.assertTrue(response_data['recordings'] == [])

    def test_get_nonexistent_recording_id(self):
        '''
        Tests GET request retrieving non-existent recording
        '''
        response = self.app.get('/recordings/1')
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error_message'], "recording id could not be found")
        self.assertEqual(response_data['error_code'], 404)
        self.assertEqual(response.status_code, 404)

    def test_get_all_recordings(self):
        '''
        Tests GET request all recordings with 2 entries in media dict
        '''
        self.recording.media_dict = self.test_media_dict_1
        response = self.app.get('/recordings')
        response_data = json.loads(response.data)
        self.assertTrue('recordings' in response_data)
        self.assertTrue(response_data['recordings'] == [1, 2])

    def test_get_recording_id(self):
        '''
        Tests GET request specific valid recording
        '''
        self.recording.media_dict = self.test_media_dict_1
        response = self.app.get('/recordings/1')
        response_data = json.loads(response.data)
        self.assertTrue('recordings' not in response_data)
        self.assertTrue('filename' in response_data)
        self.assertTrue('filesize' in response_data)
        self.assertTrue('status' in response_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['filename'], 'mock_media_1')
        self.assertEqual(response_data['filesize'], 'NA')
        self.assertEqual(response_data['id'], 1)
        self.assertEqual(response_data['status'], 'NULL')

    def test_get_invalid_recording_id(self):
        '''
        Tests GET request with an invalid id (a non integer id)
        '''
        self.recording.media_dict = self.test_media_dict_1
        response = self.app.get('/recordings/abc')
        self.assertEqual(response.status_code, 404)

        response = self.app.get('/recordings/1.0')
        self.assertEqual(response.status_code, 404)

    def test_patch_no_id(self):
        '''
        Tests a PATCH request without a recording id
        '''
        response = self.app.patch('/recordings')
        self.assertEqual(response.status_code, 405)

    def test_patch_nonexistant_id(self):
        '''
        Tests a PATCH request with non-existant recording id
        '''
        self.recording.media_dict = self.test_media_dict_1
        response = self.app.patch('/recordings/100')
        self.assertEqual(response.status_code, 404)

    def test_patch_no_command(self):
        '''
        Tests a PATCH request without a command
        '''
        self.recording.media_dict = self.test_media_dict_1
        response = self.app.patch('/recordings/1')
        self.assertEqual(response.status_code, 400)

    def test_patch_invalid_command(self):
        '''
        Tests a Patch request with an invalid command
        '''
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'invalid command'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 400)

    def test_patch_start(self):
        '''
        Tests a Patch request to start a recording
        '''
        self.mock_media_1.current_state = Multimedia.NULL
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'start'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.mock_media_1.num_times_record_called, 1)

        self.mock_media_1.num_times_record_called = 0
        self.mock_media_1.current_state = Multimedia.PAUSE
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'start'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.mock_media_1.num_times_record_called, 1)

    def test_patch_start_invalid(self):
        '''
        Tests a Patch request to start a recording with an invalid media state
        '''
        self.mock_media_1.current_state = Multimedia.STOP
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'start'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.mock_media_1.num_times_record_called, 0)

        self.mock_media_1.num_times_record_called = 0
        self.mock_media_1.current_state = Multimedia.RECORD
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'start'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.mock_media_1.num_times_record_called, 0)

    def test_patch_pause(self):
        '''
        Tests a Patch request to pause a recording
        '''
        self.mock_media_1.current_state = Multimedia.RECORD
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'pause'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.mock_media_1.num_times_pause_called, 1)

    def test_patch_pause_invalid(self):
        '''
        Tests a Patch request to pause a recording with an invalid media state
        '''
        self.mock_media_1.current_state = Multimedia.NULL
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'pause'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.mock_media_1.num_times_pause_called, 0)

        self.mock_media_1.current_state = Multimedia.PAUSE
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'pause'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.mock_media_1.num_times_pause_called, 0)

        self.mock_media_1.current_state = Multimedia.STOP
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'pause'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.mock_media_1.num_times_pause_called, 0)

    def test_patch_stop(self):
        '''
        Tests a Patch request to stop a recording
        '''
        self.mock_media_1.current_state = Multimedia.RECORD
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'stop'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.mock_media_1.num_times_stop_called, 1)

        self.mock_media_1.num_times_stop_called = 0
        self.mock_media_1.current_state = Multimedia.PAUSE
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'stop'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.mock_media_1.num_times_stop_called, 1)

    def test_patch_stop_invalid(self):
        '''
        Tests a Patch request to stop a recording with an invalid media state
        '''
        self.mock_media_1.current_state = Multimedia.STOP
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'stop'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.mock_media_1.num_times_stop_called, 0)

        self.mock_media_1.num_times_stop_called = 0
        self.mock_media_1.current_state = Multimedia.NULL
        self.recording.media_dict = self.test_media_dict_1
        data_to_send = {'command': 'stop'}
        response = self.app.patch('/recordings/1', data=data_to_send)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.mock_media_1.num_times_stop_called, 0)

    def test_post_no_filename(self):
        '''
        Tests a POST request without a filename
        '''
        response = self.app.post('/recordings')
        self.assertEqual(response.status_code, 400)

    def test_post_empty_filename(self):
        '''
        Tests a POST request with an empty filename
        '''
        data_to_send = {'filename': ''}
        response = self.app.post('/recordings', data=data_to_send)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_filename(self):
        '''
        Tests a POST request with an invalid filename
        '''
        data_to_send = {'filename': 'abc/123'}
        response = self.app.post('/recordings', data=data_to_send)
        self.assertEqual(response.status_code, 400)

    def test_post(self):
        '''
        Tests a regular POST request
        '''
        self.assertTrue(len(self.recording.media_dict.keys()) == 0)
        data_to_send = {'filename': 'test'}
        response = self.app.post('/recordings', data=data_to_send)
        self.assertTrue(len(self.recording.media_dict.keys()) == 1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.recording.media_dict.keys(), [1])
        self.assertEqual(self.recording.media_dict[1]['filename'], 'test.ogg')

    def test_delete_no_recording_id(self):
        '''
        Tests a DELETE request without a provided recording id
        '''
        response = self.app.delete('/recordings')
        self.assertEqual(response.status_code, 405)

    def test_delete_nonexistant_recording_id(self):
        '''
        Tests a DELETE request with a recording id that doesn't exist
        '''
        response = self.app.delete('/recordings/100')
        self.assertEqual(response.status_code, 404)

    def test_delete_invalid_recording_id(self):
        '''
        Tests a DELETE request with an invalid recording id
        '''
        response = self.app.delete('/recordings/abc')
        self.assertEqual(response.status_code, 404)
        response = self.app.delete('/recordings/1.0')
        self.assertEqual(response.status_code, 404)

    def test_delete_in_progress_recording(self):
        '''
        Tests a DELETE request for a recording that is paused or in progress
        '''
        self.recording.media_dict = self.test_media_dict_1

        # delete a recording that is in the middle of recording
        self.mock_media_1.current_state = Multimedia.RECORD
        response = self.app.delete('/recordings/1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.mock_media_1.num_times_stop_called, 1)
        self.assertEqual(self.recording.media_dict.keys(), [2])

        # delete a recording that is paused
        self.mock_media_2.current_state = Multimedia.PAUSE
        response = self.app.delete('/recordings/2')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.mock_media_2.num_times_stop_called, 1)
        self.assertEqual(self.recording.media_dict.keys(), [])

    def test_delete_recording_id_and_file(self):
        '''
        Tests a DELETE request where the recording has a specified file
        '''

        # setup - create the file to be deleted
        file_base_name = 'testDeleteFile'
        file_to_delete = file_base_name
        file_to_delete_path = os.path.join(self.recording.record_config.videodir, file_to_delete)
        counter = 1
        while os.path.isfile(file_to_delete_path):
            file_to_delete = file_base_name + str(counter)
            file_to_delete_path = os.path.join(self.recording.record_config.videodir, file_to_delete)
            counter += 1
        test_file = open(file_to_delete_path, 'a')
        test_file.close()

        # assert the file exists
        self.assertTrue(os.path.isfile(file_to_delete_path))

        # setup - set the file as the file for the Media instance
        self.recording.media_dict[1] = {'media': self.mock_media_1, 'filename': file_to_delete, 'filepath': file_to_delete_path}

        response = self.app.delete('/recordings/1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.recording.media_dict.keys(), [])

        # assert the file no longer exists
        self.assertFalse(os.path.isfile(file_to_delete_path))
