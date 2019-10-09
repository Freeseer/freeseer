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

import os
import shutil

from freeseer.framework.config.persist import ConfigParserStorage
from freeseer.framework.config.persist import JSONConfigStorage
from freeseer.framework.database import QtDBConnector
from freeseer.framework.plugin import PluginManager


class ProfileManager(object):
    """Manages Profile instances for the current system user."""

    def __init__(self, base_folder):
        self._base_folder = base_folder
        self._cache = {}
        self._create_if_needed(base_folder)

    def _create_if_needed(self, path):
        try:
            os.makedirs(path)
        except OSError:
            # This is thrown if path already exists.
            pass

    def get(self, name='default', create_if_needed=True):
        """
        Retrieve Profile instances by name. Profiles are cached for future gets.

        Args:
            name: The name of the profile.
            create_if_needed: When True, get creates a new profile instance
                if profile for given name doesn't exist.

        Returns:
            The instance of Profile for the given name.

        Raises:
            ProfileDoesNotExist: If create_if_needed==False and
            the given profile name doesn't exist.
        """
        if name in self._cache:
            return self._cache[name]
        else:
            full_path = os.path.join(self._base_folder, name)
            if os.path.exists(full_path):
                self._cache[name] = Profile(full_path, name)
                return self._cache[name]
            elif create_if_needed:
                return self.create(name)

        raise ProfileDoesNotExist(name)

    def create(self, name):
        """
        Creates a new Profile on file and adds it to the cache.

        Args:
            name: The name of the profile to create.

        Returns:
            The instance for the created Profile.

        Raises:
            ProfileAlreadyExists: If a profile by the same name exists.
        """
        path = os.path.join(self._base_folder, name)
        try:
            os.makedirs(path)
        except OSError:
            raise ProfileAlreadyExists(name)

        self._cache[name] = Profile(path, name)
        return self._cache[name]

    def list_profiles(self):
        """Returns a list of available profiles on file."""
        return os.listdir(self._base_folder)

    def delete(self, name):
        """
        Deletes a profile and its configuration files from disk and cache.

        Args:
            name: The name of the profile to delete.

        Raises:
            ProfileDoesNotExist: If no profile exists for give name.
        """
        path = os.path.join(self._base_folder, name)
        try:
            shutil.rmtree(path)
            del self._cache[name]
        except OSError:
            raise ProfileDoesNotExist(name)
        except KeyError:
            pass


class Profile(object):
    """Represents a profile's config files, databases, and other stuff."""

    STORAGE_MAP = {
        '.conf': ConfigParserStorage,
        '.json': JSONConfigStorage,
    }

    def __init__(self, folder, name):
        self._folder = folder
        self._name = name
        self._storages = {}
        self._databases = {}

    @property
    def name(self):
        return self._name

    def get_filepath(self, name):
        """Returns the absolute path for a file called name.

        The filepath will be prefixed with the profile's base folder.
        """
        return os.path.join(self._folder, name)

    def get_storage(self, name):
        """
        Returns a ConfigStorage instance for a given config file name.

        The ConfigStorage instance is picked based on the file suffix.
        It will also be cached for future invocations of this method.
        """
        if name not in self._storages:
            for suffix, engine in self.STORAGE_MAP.items():
                if name.endswith(suffix):
                    self._storages[name] = engine(self.get_filepath(name))
                    break

        if name in self._storages:
            return self._storages[name]
        else:
            raise KeyError('{} does not have a valid suffix'.format(name))

    def get_config(self, filename, config_class, storage_args=None, read_only=False):
        """Returns an instance of config_class that has be loaded from filename.

        Params:
            filename - name of the file, this will be passed to get_storage(..)
            config_class - Config subclass
            storage_args - an iterable of arguments that will be passed to
                           storage.load(config, ...)
            read_only - if True, the storage will be passed to the Config
                        instance
        """
        storage_args = storage_args if storage_args else []
        storage = self.get_storage(filename)

        if read_only:
            config = config_class()
        else:
            config = config_class(storage, storage_args)

        return storage.load(config, *storage_args)

    def get_database(self, name='presentations.db'):
        """Returns an instance of QtDBConnector for a specific database file.

        It is also cached for future gets.
        """
        if name not in self._databases:
            self._databases[name] = QtDBConnector(self.get_filepath(name), PluginManager(self))
        return self._databases[name]


class ProfileAlreadyExists(Exception):
    def __init__(self, value):
        message = 'Profile already exists: "{}"'.format(value)
        super(Exception, self).__init__(message)


class ProfileDoesNotExist(Exception):
    def __init__(self, value):
        message = 'Profile does not exist: "{}"'.format(value)
        super(Exception, self).__init__(message)
