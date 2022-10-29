#!/usr/bin/env python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014 Free and Open Source Software Learning Centre
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

from freeseer.framework.config.options import FloatOption
from freeseer.tests.framework.config.options import OptionTest


class TestFloatOptionNoDefault(unittest.TestCase, OptionTest):
    """Tests FloatOption without a default value."""

    valid_success = [x / 10.0 for x in range(-100, 100)]

    encode_success = list(zip(valid_success, list(map(str, valid_success))))

    decode_success = list(zip(list(map(str, valid_success)), valid_success))
    decode_failure = [
        'hello',
        '1world',
        'test2',
    ]

    def setUp(self):
        self.option = FloatOption()

    def test_schema(self):
        """Tests FloatOption schema method."""
        self.assertRaises(ValidationError, validate, 'error', self.option.schema())
        self.assertIsNone(validate(5.5, self.option.schema()))
        self.assertDictEqual(self.option.schema(), {'type': 'number'})


class TestFloatOptionWithDefault(TestFloatOptionNoDefault):
    """Tests FloatOption with a default value."""

    def setUp(self):
        self.option = FloatOption(1234.5)

    def test_default(self):
        """Tests that the default was set correctly."""
        self.assertEqual(self.option.default, 1234.5)

    def test_schema(self):
        """Tests FloatOption schema method."""
        self.assertRaises(ValidationError, validate, 'error', self.option.schema())
        self.assertIsNone(validate(5.0, self.option.schema()))
        self.assertDictEqual(self.option.schema(), {'default': 1234.5, 'type': 'number'})
