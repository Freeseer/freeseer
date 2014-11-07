#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2013, 2014 Free and Open Source Software Learning Centre
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

import os
import shutil
import tempfile
import unittest

from jsonschema import validate
from jsonschema import ValidationError

from freeseer.framework.config.profile import ProfileManager
from freeseer import settings


class TestConfig(unittest.TestCase):

    def setUp(self):
        '''
        Stardard init method: runs before each test_* method

        Initializes a PluginManager

        '''
        self.profile_manager = ProfileManager(tempfile.mkdtemp())
        self.profile = self.profile_manager.get('testing')
        self.config = self.profile.get_config('freeseer.conf',
                                              settings.FreeseerConfig,
                                              ['Global'],
                                              read_only=False)

    def tearDown(self):
        '''
        Generic unittest.TestCase.tearDown()
        '''
        shutil.rmtree(self.profile_manager._base_folder)

    def test_save(self):
        '''
        Tests that the config file was created after being saved.
        '''
        filepath = self.profile.get_filepath('freeseer.conf')
        self.config.save()
        self.assertTrue(os.path.exists(filepath))

    def test_schema(self):
        """Tests that the settings Config returns the correct schema based on all its options."""
        settings_schema = {
            'type': 'object',
            'properties': {
                'videodir': {
                    'default': '~/Videos',
                    'type': 'string',
                },
                'auto_hide': {
                    'default': False,
                    'type': 'boolean',
                },
                'enable_audio_recording': {
                    'default': True,
                    'type': 'boolean',
                },
                'enable_video_recording': {
                    'default': True,
                    'type': 'boolean',
                },
                'videomixer': {
                    'default': 'Video Passthrough',
                    'type': 'string',
                },
                'audiomixer': {
                    'default': 'Audio Passthrough',
                    'type': 'string',
                },
                'record_to_file': {
                    'default': True,
                    'type': 'boolean',
                },
                'record_to_file_plugin': {
                    'default': 'Ogg Output',
                    'type': 'string',
                },
                'record_to_stream': {
                    'default': False,
                    'type': 'boolean',
                },
                'record_to_stream_plugin': {
                    'default': 'RTMP Streaming',
                    'type': 'string',
                },
                'audio_feedback': {
                    'default': False,
                    'type': 'boolean',
                },
                'video_preview': {
                    'default': True,
                    'type': 'boolean',
                },
                'default_language': {
                    'default': 'tr_en_US.qm',
                    'type': 'string',
                },
            },
        }
        self.assertDictEqual(self.config.schema(), settings_schema)

    def test_schema_validate(self):
        """Tests that schemas validate valid configs."""
        config = {
            'default_language': 'tr_en_US.qm',
            'auto_hide': True
        }
        self.assertIsNone(validate(config, self.config.schema()))

    def test_schema_invalidate(self):
        """Tests that schemas invalidate an invalid config."""
        config = {
            'default_language': False,
            'auto_hide': 5
        }
        self.assertRaises(ValidationError, validate, config, self.config.schema())
