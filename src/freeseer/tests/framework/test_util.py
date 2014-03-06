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

import mock
import os
import shutil
import tempfile
import unittest

from freeseer.framework.config.profile import ProfileManager
from freeseer.framework.util import reset
from freeseer.framework.util import reset_configuration
from freeseer.framework.util import reset_database


class TestUtil(unittest.TestCase):

    def setUp(self):
        self.config_dir = tempfile.mkdtemp()
        self.profile_manager = ProfileManager(os.path.join(self.config_dir, 'profiles'))

    def tearDown(self):
        shutil.rmtree(self.config_dir)

    def test_reset(self):
        """Test Resetting the configuration directory"""
        profile = self.profile_manager.get('default')
        open(profile.get_filepath('freeseer.conf'), 'w+')
        open(profile.get_filepath('plugin.conf'), 'w+')
        open(profile.get_filepath('presentations.db'), 'w+')
        self.assertTrue(os.path.exists(self.config_dir))
        with mock.patch('__builtin__.raw_input', return_value='yes'):
            reset(self.config_dir)
        self.assertFalse(os.path.exists(self.config_dir))

        # recreate the config_dir for tearDown()
        # while we're at it test that passing a none "yes" answer results in directory not removed
        os.makedirs(self.config_dir)
        with mock.patch('__builtin__.raw_input', return_value='no'):
            reset(self.config_dir)
        self.assertTrue(os.path.exists(self.config_dir))

    def test_reset_configuration(self):
        """Test Resetting configuration files"""
        # Test resetting the default profile (no profile arguments passed)
        profile = self.profile_manager.get('default')
        open(profile.get_filepath('freeseer.conf'), 'w+')
        open(profile.get_filepath('plugin.conf'), 'w+')
        self.assertTrue(os.path.exists(profile.get_filepath('plugin.conf')))
        self.assertTrue(os.path.exists(profile.get_filepath('freeseer.conf')))
        reset_configuration(self.config_dir)
        self.assertFalse(os.path.exists(profile.get_filepath('plugin.conf')))
        self.assertFalse(os.path.exists(profile.get_filepath('freeseer.conf')))

        # Test resetting a non-default profile
        profile = self.profile_manager.get('not-default')
        open(profile.get_filepath('freeseer.conf'), 'w+')
        open(profile.get_filepath('plugin.conf'), 'w+')
        self.assertTrue(os.path.exists(profile.get_filepath('plugin.conf')))
        self.assertTrue(os.path.exists(profile.get_filepath('freeseer.conf')))
        reset_configuration(self.config_dir, 'not-default')
        self.assertFalse(os.path.exists(profile.get_filepath('plugin.conf')))
        self.assertFalse(os.path.exists(profile.get_filepath('freeseer.conf')))

    def test_reset_database(self):
        """Test Resetting database file"""
        # Test resetting the default profile (no profile arguments passed)
        profile = self.profile_manager.get('default')
        open(profile.get_filepath('presentations.db'), 'w+')
        self.assertTrue(os.path.exists(profile.get_filepath('presentations.db')))
        reset_database(self.config_dir)
        self.assertFalse(os.path.exists(profile.get_filepath('presentations.db')))

        # Test resetting a non-default profile
        profile = self.profile_manager.get('not-default')
        open(profile.get_filepath('presentations.db'), 'w+')
        self.assertTrue(os.path.exists(profile.get_filepath('presentations.db')))
        reset_database(self.config_dir, 'not-default')
        self.assertFalse(os.path.exists(profile.get_filepath('presentations.db')))
