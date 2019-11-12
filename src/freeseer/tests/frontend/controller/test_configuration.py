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

import pytest

from freeseer import settings
from freeseer.framework.config.profile import ProfileManager
from freeseer.framework.config.profile import ProfileDoesNotExist
from freeseer.framework.plugin import PluginManager
from freeseer.frontend.controller import server


def pack_schema(config, include):
    """Returns a partial schema from the options in 'include'."""
    schema = {}
    for key in include:
        schema[key] = config.options[key].schema()
    print schema
    return schema


class TestConfigurationApp:
    @pytest.fixture(scope='module')
    def test_client(self):
        server.app.config['TESTING'] = True
        server.app.storage_file_path = "test_storage_file"
        return server.app.test_client()

    @pytest.fixture(scope='function', autouse=True)
    def configuration(self, request, test_client, monkeypatch, tmpdir):
        configuration = server.app.blueprints['configuration']

        monkeypatch.setattr(settings, 'configdir', str(tmpdir.mkdir('configdir')))

        settings.profile_manager = ProfileManager(str(tmpdir.mkdir('profile')))
        configuration.profile = settings.profile_manager.get('testing')
        configuration.config = configuration.profile.get_config('freeseer.conf',
                                                                settings.FreeseerConfig,
                                                                ['Global'],
                                                                read_only=False)
        configuration.plugin_manager = PluginManager(configuration.profile)
        return configuration

    def test_list_profiles(self, test_client):
        response = test_client.get('/profiles')
        expected = {
            'profiles': settings.profile_manager.list_profiles()
        }
        data = json.loads(response.data)
        assert response.status_code == 200
        assert expected == data

    def test_view_profile(self, test_client, configuration):
        response = test_client.get('/profiles/testing')
        configuration.config = configuration.profile.get_config('freeseer.conf',
                                                                settings.FreeseerConfig,
                                                                ['Global'],
                                                                read_only=True)
        expected = {
            'configuration': configuration.config.values,
            'schema': configuration.config.schema(),
        }
        data = json.loads(response.data)
        assert expected == data
        assert response.status_code == 200

    def test_view_profile_nonexistant_id(self, test_client):
        response = test_client.get('/profiles/doesnotexist')
        assert response.status_code == 404

    def test_create_profile(self, test_client):
        response = test_client.post('/profiles',
                                    data={'name': 'new_profile'})
        new_profile = settings.profile_manager.get('new_profile', create_if_needed=False)
        assert response.status_code == 201
        assert new_profile

    def test_create_profile_invalid_args(self, test_client):
        response = test_client.post('/profiles', data={'name': '12@345'})
        data = json.loads(response.data)
        assert response.status_code == 400
        assert data['description'] == 'Invalid Profile Name: 12@345'

    def test_create_profile_already_exists(self, test_client):
        response = test_client.post('/profiles',
                                    data={'name': 'testing'})
        assert response.status_code == 400

    def test_delete_profile(self, test_client):
        response = test_client.delete('/profiles/testing')
        assert response.status_code == 204
        with pytest.raises(ProfileDoesNotExist):
            settings.profile_manager.get('testing', create_if_needed=False)

    def test_modify_profile(self, test_client, configuration):
        response = test_client.patch('/profiles/testing',
                                     data={
                                         'default_language': 'tr_en_FR.qm',
                                     })

        assert response.status_code == 200

        configuration.config = configuration.profile.get_config('freeseer.conf',
                                                                settings.FreeseerConfig,
                                                                ['Global'],
                                                                read_only=True)
        assert configuration.config.default_language == 'tr_en_FR.qm'

    def test_modify_profile_arg_needs_encoding(self, test_client):
        response = test_client.patch('/profiles/testing',
                                     data={
                                         'auto_hide': True
                                     })
        assert response.status_code == 200

    def test_modify_profile_invalid_option(self, test_client):
        response = test_client.patch('/profiles/testing',
                                     data={
                                         'not_a_real_option': True
                                     })
        response_data = json.loads(response.data)
        assert response_data['description'] == 'Invalid Option: not_a_real_option'
        assert response_data['error_code'] == 400

    def test_view_general_configuration(self, test_client, configuration):
        response = test_client.get('/profiles/testing/general')
        response_data = json.loads(response.data)

        general = configuration.profile.get_config('freeseer.conf',
                                                   settings.FreeseerConfig,
                                                   ['Global'],
                                                   read_only=True)
        assert response_data == {
            'configuration': {
                'default_language': general.default_language,
                'auto_hide': general.auto_hide,
            },
            'schema': pack_schema(general, ['default_language', 'auto_hide']),
        }

        assert response.status_code == 200

    def test_modify_general_configuration(self, test_client, configuration):
        response = test_client.patch('/profiles/testing/general',
                                     data={
                                         'default_language': 'tr_en_FR.qm',
                                     })

        assert response.status_code == 200

        configuration.config = configuration.profile.get_config('freeseer.conf',
                                                                settings.FreeseerConfig,
                                                                ['Global'],
                                                                read_only=True)
        assert configuration.config.default_language == 'tr_en_FR.qm'

    def test_view_recording_configuration(self, test_client, configuration):
        response = test_client.get('/profiles/testing/recording')
        data = json.loads(response.data)
        config = configuration.config
        expected = {
            'configuration': {
                'record_to_file': config.record_to_file,
                'videodir': config.videodir,
                'record_to_file_plugin': config.record_to_file_plugin,
                'record_to_stream': config.record_to_stream,
                'record_to_stream_plugin': config.record_to_stream_plugin,
                'enable_audio_recording': config.enable_audio_recording,
                'audiomixer': config.audiomixer,
                'enable_video_recording': config.enable_video_recording,
                'videomixer': config.videomixer,
            },
            'schema': pack_schema(config, [
                'record_to_file',
                'videodir',
                'record_to_file_plugin',
                'record_to_stream',
                'record_to_stream_plugin',
                'enable_audio_recording',
                'audiomixer',
                'enable_video_recording',
                'videomixer',
            ]),
        }
        assert response.status_code == 200
        assert expected['configuration'] == data['configuration']

    def test_list_plugin_category(self, test_client, configuration):
        response = test_client.get('/profiles/testing/recording/audioinput')
        plugin_infos = configuration.plugin_manager.get_plugins_of_category('AudioInput')
        expected = {'plugins': [plugin.name for plugin in plugin_infos]}
        data = json.loads(response.data)
        assert data == expected
        assert response.status_code == 200

    def test_list_plugin_instances(self, test_client, configuration):
        test_client.post('/profiles/testing/recording/audioinput/jackaudiosource')
        test_client.post('/profiles/testing/recording/audioinput/jackaudiosource')
        test_client.post('/profiles/testing/recording/audioinput/pulseaudiosource')
        response = test_client.get('/profiles/testing/recording/audioinput/jackaudiosource')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['instances']) == 2

    def test_view_plugin_instance(self, test_client, configuration):
        response = test_client.get('/profiles/testing/recording/audioinput/jackaudiosource/0')
        plugin = configuration.plugin_manager.get_plugin_by_name('Jack Audio Source', 'AudioInput')
        plugin_object = plugin.plugin_object
        plugin_object.set_instance(0)
        plugin_object.load_config(configuration.plugin_manager)
        expected = {
            'configuration': plugin_object.config.values,
            'schema': plugin_object.config.schema(),
        }
        data = json.loads(response.data)
        assert response.status_code == 200
        assert expected == data

    def test_view_invalid_plugin_name(self, test_client, configuration):
        response = test_client.get('/profiles/testing/recording/audioinput/fakeaudiosource/0')
        data = json.loads(response.data)
        assert data['description'] == 'Invalid Plugin Name: fakeaudiosource'
        assert response.status_code == 400

    def test_view_invalid_plugin_category(self, test_client, configuration):
        response = test_client.get('/profiles/testing/recording/fakeinput/jackaudiosource/0')
        data = json.loads(response.data)
        assert data['description'] == 'Invalid Plugin Category: fakeinput'
        assert response.status_code == 400

    def test_create_plugin_instance(self, test_client, configuration):
        response = test_client.post('/profiles/testing/recording/audioinput/jackaudiosource')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 'id' in data
        id = data['id']
        plugin = configuration.plugin_manager.get_plugin_by_name('Jack Audio Source', 'AudioInput')
        plugin_object = plugin.plugin_object
        plugin_object.set_instance(id)
        config = plugin_object.config
        assert config

    def test_modify_plugin_instance(profile, test_client, configuration):
        response = test_client.patch('/profiles/testing/recording/audioinput/jackaudiosource/0',
                                     data={
                                         'client': 'testclient',
                                         'connect': 'testconnect',
                                     })
        plugin = configuration.plugin_manager.get_plugin_by_name('Jack Audio Source', 'AudioInput')
        plugin_object = plugin.plugin_object
        plugin_object.set_instance(0)

        assert plugin_object.config.client == 'testclient'
        assert plugin_object.config.connect == 'testconnect'
        assert response.status_code == 200
