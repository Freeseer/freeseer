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

import abc
import collections
import functools

from freeseer.framework.config.exceptions import InvalidOptionValueError
from freeseer.framework.config.exceptions import OptionValueNotSetError
from freeseer.framework.config.exceptions import StorageNotSetError


class Option(object):
    """Represents a Config option."""

    __metaclass__ = abc.ABCMeta

    class NotSpecified(object):
        pass

    def __init__(self, default=NotSpecified):
        self.default = default

    def is_required(self):
        """Returns true iff this option is required."""
        return self.default == self.NotSpecified

    # Override these if you know what you're doing

    def pre_set(self, value):
        """Do something before value is stored for this option."""
        return value

    def presentation(self, value):
        """Returns a modified version of value that will not itself be persisted."""
        return value

    # Override these!

    @abc.abstractmethod
    def is_valid(self, value):
        """Checks if a value is valid for this option."""
        pass

    @abc.abstractmethod
    def encode(self, value):
        """Encodes value into a string.

        Should raise something if unable to encode.
        """
        pass

    @abc.abstractmethod
    def decode(self, value):
        """Decodes value into a proper Option value.

        Should raise something if unable to decode.
        """
        pass


class ConfigBase(abc.ABCMeta):
    """Metaclass for Config subclasses.

    It does some transformations on the options you specify to let them be used as properties.
    """

    def __new__(meta, name, bases, class_attributes):
        """Finds all Options delcared in the subclass and transform them into properties."""
        class_attributes, options = meta.find_options(class_attributes)
        class_attributes['options'] = options
        cls = super(ConfigBase, meta).__new__(meta, name, bases, class_attributes)
        for opt_name, option in options.iteritems():
            opt_get = functools.partial(cls.get_value, name=opt_name, option=option, presentation=True)
            opt_set = functools.partial(cls._set_value, name=opt_name, option=option)
            setattr(cls, opt_name, property(opt_get, opt_set))
        return cls

    @staticmethod
    def find_options(class_attributes):
        """Find all Option subclasses within the class body."""
        new_attributes = {}
        options = collections.OrderedDict()
        for name in sorted(class_attributes.keys()):
            attr = class_attributes[name]
            if name.startswith('_') or not isinstance(attr, Option):
                new_attributes[name] = attr
            else:
                options[name] = attr
        return new_attributes, options


class Config(object):
    """Base class for all custom configs.

    To be useful, its body must contain some number of Option instances.

    Example:
        class MyConfig(Config):
            test = StringOption('default_value')
    """

    __metaclass__ = ConfigBase

    def __init__(self, storage=None, storage_args=None):
        """
        Params:
            storage - an instance of a ConfigStorage
            storage_args - an iterable of arguments that will be passed to
                           storage.load(...)
        """
        self._storage = storage
        self._storage_args = storage_args if storage_args else []

        self.values = {}
        self.set_defaults()

    def _set_value(self, value, name, option):
        """This is just here to make the argument order more logical."""
        self.set_value(name, option, value)

    def set_defaults(self):
        """Sets the values of all options to their default value (if applicable)."""
        for name, option in self.options.iteritems():
            if not option.is_required():
                self.set_value(name, option, option.default)

    # You probably will not need to override these:

    def get_value(self, name, option, presentation=False):
        """Gets the value of an option.

        Params:
            name - the string name of the option instance
            option - the option instance itself
            presentation - boolean

        Returns: the value that the config has stored for this option
        """
        if name in self.values:
            value = self.values[name]
            if presentation:
                return option.presentation(value)
            else:
                return value
        else:
            raise OptionValueNotSetError(name, option)

    def set_value(self, name, option, value):
        """Sets the value of an option.

        Params:
            name - the string name of the option instance
            option - the option instance itself
            value - the value that will be set for the option

        Returns: nothing
        """
        if option.is_valid(value):
            mod_value = option.pre_set(value)
            self.values[name] = mod_value
        else:
            raise InvalidOptionValueError(name, option)

    def save(self):
        """Persist the Config instance.

        This only works if the storage stuff is passed to the Config's constructor.
        """
        if self._storage:
            self._storage.store(self, *self._storage_args)
        else:
            raise StorageNotSetError()


class ConfigStorage(object):
    """Defines an interface for loading and storing Config instances."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, filepath):
        """
        Params:
            filepath - the path to file where the config will be persisted or loaded from
        """
        self._filepath = filepath

    # Override these!

    @abc.abstractmethod
    def load(self, config_instance):
        """Populates the Config instance from somewhere.

        It should iterate over all options in self.options and determine the value to store by using option.decode(..).
        """
        pass

    @abc.abstractmethod
    def store(self, config_instance):
        """Persists the Config to somewhere.

        It should iterate over all options in self.options and determine the value to persis by using option.encode(..).
        """
        pass
