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

import unittest

from freeseer.framework.config import options
from freeseer.framework.config.core import Config
from freeseer.framework.config.exceptions import InvalidOptionValueError
from freeseer.framework.config.exceptions import OptionValueNotSetError
from freeseer.framework.config.exceptions import StorageNotSetError


class MyConfig(Config):
    option1 = options.IntegerOption(1337)
    option2 = options.StringOption()


class TestConfigNoStorage(unittest.TestCase):
    """Tests that ConfigBase is setting up the Config subclass properly."""

    def setUp(self):
        self.config = MyConfig()

    def test_set_defaults(self):
        """Tests that the default values of the Config options were set correctly."""
        self.assertEqual(self.config.values['option1'], 1337)
        self.assertNotIn('option2', self.config.values)

    def test_get_value_missing(self):
        """Tests that get_value(...) fails if the option's value has never been set before."""
        name = 'option2'
        option = self.config.options[name]

        self.assertRaises(OptionValueNotSetError, self.config.get_value, name, option)
        self.assertNotIn(name, self.config.values)

    def test_get_value_success(self):
        """Tests that get_value(...) succeeds if the option's value has been set before."""
        name = 'option1'
        option = self.config.options[name]
        value = self.config.values[name]

        self.assertEqual(self.config.get_value(name, option), value)

    def test_set_value_invalid(self):
        """Tests that set_value(...) fails if it tries to set an invalid value for an option."""
        name = 'option1'
        option = self.config.options[name]
        value = 'invalid'
        initial_value = self.config.values[name]

        self.assertRaises(InvalidOptionValueError, self.config.set_value, name, option, value)
        self.assertEqual(self.config.values[name], initial_value)

    def test_set_value_valid(self):
        """Tests that set_value(...) succeeds if it tries to set a valid value for an option."""
        name = 'option2'
        option = self.config.options[name]
        value = 'hello'

        self.config.set_value(name, option, value)
        self.assertEqual(self.config.values[name], value)

    def test_get_property_missing(self):
        """Tests that getting the property for an option fails if its value has not been set before."""
        try:
            value = self.config.option2
            assert value
        except Exception as e:
            self.assertIsInstance(e, OptionValueNotSetError)
            self.assertNotIn('option2', self.config.values)

    def test_get_property_success(self):
        """Tests that getting the property for an option succeeds if its value has been set before."""
        self.assertEqual(self.config.option1, 1337)

    def test_set_property_invalid(self):
        """Tests that setting the property for an option fails if the value is not valid."""
        try:
            initial_value = self.config.values['option1']
            self.config.option1 = 'invalid'
        except Exception as e:
            self.assertIsInstance(e, InvalidOptionValueError)
            self.assertEqual(self.config.values['option1'], initial_value)

    def test_set_property_success(self):
        """Tests that setting the property for an option succeeds if the value is valid."""
        self.config.option1 = 9001
        self.assertEqual(self.config.values['option1'], 9001)

        self.config.option2 = 'bar'
        self.assertEqual(self.config.values['option2'], 'bar')

    def test_save(self):
        """Tests that saving a Config without a ConfigStorage instance attached to it fails."""
        self.assertRaises(StorageNotSetError, self.config.save)


class MockStorage(object):
    """A mock ConfigStorage class. It simply stores whether its store method was called at least once."""

    def __init__(self):
        self.store_args = []
        self.store_called = False

    def store(self, *args):
        self.store_args = args
        self.store_called = True


class TestConfigWithStorage(TestConfigNoStorage):

    def setUp(self):
        self.storage = MockStorage()
        self.config = MyConfig(self.storage, ['global'])
        self.store_args = (self.config, 'global')

    def test_save(self):
        """Tests that saving a Config with a ConfigStorage instance attached to it "succeeds"."""
        self.config.save()
        self.assertEqual(self.storage.store_args, self.store_args)
        self.assertTrue(self.storage.store_called)
