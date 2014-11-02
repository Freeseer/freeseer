#!/usr/bin/env python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2013  Free and Open Source Software Learning Centre
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

import shutil
import tempfile
import unittest

from freeseer.framework.config import Config, options
from freeseer.framework.config.exceptions import StorageNotSetError
from freeseer.framework.config.persist import ConfigParserStorage, JSONConfigStorage
from freeseer.framework.config.profile import Profile, ProfileAlreadyExists, ProfileDoesNotExist, ProfileManager
from freeseer.framework.database import QtDBConnector


class TestConfig(Config):
    option1 = options.StringOption('hello')
    option2 = options.StringOption('world')


class TestProfileManager(unittest.TestCase):
    """Tests the ProfileManager."""

    def setUp(self):
        self.profiles_path = tempfile.mkdtemp()
        self.profile_manager = ProfileManager(self.profiles_path)

    def tearDown(self):
        shutil.rmtree(self.profiles_path)

    def test_get(self):
        """Tests that get returns a Profile instance."""
        profile = self.profile_manager.get('testing')
        self.assertIsInstance(profile, Profile)

    def test_get_non_existent(self):
        """Test for non-existent profile."""
        self.assertRaises(ProfileDoesNotExist, self.profile_manager.get, 'non-existent_profile', create_if_needed=False)

    def test_get_non_existent_creates(self):
        """Test that get creates non-existent profile if create_if_needed=True."""
        self.assertRaises(ProfileDoesNotExist, self.profile_manager.get, 'non-existent_profile', create_if_needed=False)
        profile = self.profile_manager.get('non_existent_profile')
        self.assertIsInstance(profile, Profile)

    def test_get_cache(self):
        """Tests that get caching is working as expected."""
        profile1 = self.profile_manager.get('testing')
        profile2 = self.profile_manager.get('testing')
        self.assertEqual(profile1, profile2)

    def test_list_profiles(self):
        """Tests that list_profiles returns all profiles on file."""
        self.profile_manager.create('testing1')
        self.profile_manager.create('testing2')
        profiles = self.profile_manager.list_profiles()
        self.assertItemsEqual(['testing1', 'testing2'], profiles)

    def test_create_profile(self):
        """Tests that create_profile returns an instance of Profile.."""
        profile = self.profile_manager.create('testing1')
        self.assertIsInstance(profile, Profile)

    def test_create_profile_existing(self):
        """Tests that exception is raised if trying to overwrite existing profile."""
        self.profile_manager.create('testing1')
        self.assertRaises(ProfileAlreadyExists, self.profile_manager.create, 'testing1')

    def test_create_profile_caches(self):
        """Tests that create_profile adds the new Profile instance to cache."""
        self.assertNotIn('testing1', self.profile_manager._cache)
        self.profile_manager.create('testing1')
        self.assertIn('testing1', self.profile_manager._cache)

    def test_delete_profile_existing(self):
        """Tests that delete_profile deletes the profile from cache and file."""
        self.profile_manager.create('testing1')
        self.profile_manager.delete('testing1')
        self.assertRaises(ProfileDoesNotExist, self.profile_manager.get, 'testing1', create_if_needed=False)

    def test_delete_profile_non_existing(self):
        """Non-existent profiles can't be deleted."""
        self.assertRaises(ProfileDoesNotExist, self.profile_manager.delete, 'testing')


class TestProfile(unittest.TestCase):
    """Tests Profile."""

    def setUp(self):
        self.profile_path = tempfile.mkdtemp()
        self.profile = Profile(self.profile_path, 'testing')

    def tearDown(self):
        shutil.rmtree(self.profile_path)

    def test_get_filepath(self):
        """Tests that get_filepath(...) returns a path prefixed with the profile's folder."""
        filepath = self.profile.get_filepath('testing.db')
        self.assertTrue(filepath.startswith(self.profile_path))

    def test_get_storage_valid_suffix(self):
        """Tests that get_storage(...) returns the correct ConfigStorage class for a particular file suffix."""
        json_storage = self.profile.get_storage('testing.json')
        self.assertIsInstance(json_storage, JSONConfigStorage)

        config_parser_storage = self.profile.get_storage('testing.conf')
        self.assertIsInstance(config_parser_storage, ConfigParserStorage)

    def test_get_storage_cache(self):
        """Tests that get_storage(...) caches ConfigStorage instances properly."""
        storage1 = self.profile.get_storage('testing.conf')
        storage2 = self.profile.get_storage('testing.conf')
        self.assertEqual(storage1, storage2)

    def test_get_storage_invalid_suffix(self):
        """Tests that get_storage(...) does not accept an invalid filename suffix."""
        self.assertRaises(KeyError, self.profile.get_storage, ('testing.json,'))

    def test_get_config(self):
        """Tests that get_config(...) returns the correct config instance and that it is .save()-able."""
        config = self.profile.get_config('testing.conf', TestConfig, storage_args=['this_section'])
        self.assertIsInstance(config, TestConfig)
        self.assertIsNone(config.save())

    def test_get_config_read_only(self):
        """Tests that get_config(...) returns a read-only config instance."""
        config = self.profile.get_config('testing.conf', TestConfig, storage_args=['this_section'], read_only=True)
        self.assertIsInstance(config, TestConfig)
        self.assertRaises(StorageNotSetError, config.save)

    def test_get_database(self):
        """Tests that get_database(...) returns an instance of QtDBConnector."""
        database = self.profile.get_database('testing.db')
        self.assertIsInstance(database, QtDBConnector)

    def test_get_database_cache(self):
        """Tests that get_database(...) caches QtDBConnector properly."""
        database1 = self.profile.get_database('testing.db')
        database2 = self.profile.get_database('testing.db')
        self.assertEqual(database1, database2)
