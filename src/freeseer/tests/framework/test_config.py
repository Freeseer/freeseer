#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2013 Free and Open Source Software Learning Centre
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
