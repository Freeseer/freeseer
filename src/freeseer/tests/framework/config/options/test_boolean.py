#!/usr/bin/env python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2013, 2014 Free and Open Source Software Learning Centre
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

from jsonschema import validate
from jsonschema import ValidationError

from freeseer.framework.config.options import BooleanOption
from freeseer.tests.framework.config.options import OptionTest


class TestBooleanOptionNoDefault(unittest.TestCase, OptionTest):
    """Tests BooleanOption without a default value."""

    valid_success = [
        True,
        False,
    ]
    valid_failure = [
        'True',
        1337,
    ]

    encode_success = [
        (True, 'true'),
        (False, 'false'),
    ]

    decode_success = [
        ('true', True),
        ('false', False),
    ]

    def setUp(self):
        self.option = BooleanOption()

    def test_schema(self):
        """Tests BooleanOption schema method."""
        self.assertRaises(ValidationError, validate, 4, self.option.schema())
        self.assertIsNone(validate(True, self.option.schema()))
        self.assertDictEqual(self.option.schema(), {'type': 'boolean'})


class TestBooleanOptionWithDefault(TestBooleanOptionNoDefault):
    """Test BooleanOption with a default value."""

    def setUp(self):
        self.option = BooleanOption(False)

    def test_default(self):
        """Tests that the default was set correctly."""
        self.assertEqual(self.option.default, False)

    def test_schema(self):
        """Tests BooleanOption schema method."""
        self.assertRaises(ValidationError, validate, 4, self.option.schema())
        self.assertIsNone(validate(True, self.option.schema()))
        self.assertDictEqual(self.option.schema(), {'default': False, 'type': 'boolean'})
