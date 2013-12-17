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

from freeseer.framework.config.options import IntegerOption
from freeseer.tests.framework.config.options import TestOption


class TestIntegerOptionNoDefault(unittest.TestCase, TestOption):
    """Tests IntegerOption without a default value."""

    valid_success = range(-1000, 1000)

    encode_success = zip(valid_success, map(str, valid_success))

    decode_success = zip(map(str, valid_success), valid_success)
    decode_failure = [
        'hello',
        '1world',
        'test2',
    ]

    def setUp(self):
        self.option = IntegerOption()


class TestIntegerOptionWithDefault(TestIntegerOptionNoDefault):
    """Tests IntegerOption with a default value."""

    def setUp(self):
        self.option = IntegerOption(1234)

    def test_default(self):
        """Tests that the default was set correctly."""
        self.assertEqual(self.option.default, 1234)
