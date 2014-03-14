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

from freeseer.framework.config.options import StringOption
from freeseer.tests.framework.config.options import OptionTest


class TestStringOptionNoDefault(unittest.TestCase, OptionTest):
    """Tests StringOption without a default value."""

    valid_success = [
        'testing',
        True,
        0,
    ]

    encode_success = [
        ('testing', 'testing'),
        (True, 'True'),
    ]

    decode_success = [
        ('testing', 'testing'),
        ('True', 'True'),
    ]

    def setUp(self):
        self.option = StringOption()


class TestStringOptionWithDefault(TestStringOptionNoDefault):
    """Tests StringOption with a default value."""

    def setUp(self):
        self.option = StringOption('testing')

    def test_default(self):
        """Tests that the default was set correctly."""
        self.assertEqual(self.option.default, 'testing')
