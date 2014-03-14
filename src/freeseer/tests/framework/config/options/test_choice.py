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

from freeseer.framework.config.options import ChoiceOption
from freeseer.tests.framework.config.options import OptionTest


class TestChoiceOptionNoDefault(unittest.TestCase, OptionTest):
    """Tests ChoiceOption without a default value."""

    valid_success = [
        'hello',
        'world',
    ]
    valid_failure = [
        'hello1',
        '1hello',
        'w0rld',
    ]

    encode_success = zip(valid_success, valid_success)

    decode_success = zip(valid_success, valid_success)
    decode_failure = valid_failure

    def setUp(self):
        self.option = ChoiceOption([
            'hello',
            'world',
        ])


class TestChoiceOptionWithDefault(TestChoiceOptionNoDefault):
    """Tests ChoiceOption with a default value."""

    def setUp(self):
        self.option = ChoiceOption([
            'hello',
            'world',
        ], 'hello')

    def test_default(self):
        """Tests that the default was set correctly."""
        self.assertEqual(self.option.default, 'hello')
