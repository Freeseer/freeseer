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

from freeseer.framework.config.core import Option
from freeseer.framework.config.exceptions import InvalidDecodeValueError


class TestOption(object):
    '''
    "Exhaustively" test many success and failure scenarios for:
        option.is_valid(...)
        option.encode(...)
        option.decode(...)

    Your test classes should subclass both unittest.TestCase and TestOption.
    Then, you have to override the value lists below. The success lists cannot
    be empty.
    '''

    valid_success = []
    valid_failure = []

    encode_success = []
    encode_failure = []

    decode_success = []
    decode_failure = []

    def setUp(self):
        '''
        This should initialize your option class and any other things it needs.
        '''
        self.option = None

    def test_is_valid_success(self):
        '''
        Tests that is_valid succeeds in the correct scenarios.
        '''
        if not self.valid_success:
            self.fail('missing is_valid successful values')
        for value in self.valid_success:
            self.assertTrue(self.option.is_valid(value))

    def test_is_valid_failure(self):
        '''
        Tests that is_valid fails in the correct scenarios.
        '''
        for value in self.valid_failure:
            self.assertFalse(self.option.is_valid(value))

    def test_encode_success(self):
        '''
        Tests that encode succeeds in the correct scenarios.
        '''
        if not self.encode_success:
            self.fail('missing encode successful values')
        for in_value, out_value in self.encode_success:
            self.assertTrue(self.option.is_valid(in_value))
            self.assertEqual(self.option.encode(in_value), out_value)

    def test_encode_failure(self):
        '''
        Tests that encode fails in the correct scenarios.
        '''
        for in_value in self.encode_failure:
            self.assertRaises(Exception, self.option.encode, in_value)

    def test_decode_success(self):
        '''
        Tests that decode succeeds in the correct scenarios.
        '''
        if not self.decode_success:
            self.fail('missing decode successful values')
        for in_value, out_value in self.decode_success:
            decoded = self.option.decode(in_value)
            self.assertTrue(self.option.is_valid(decoded))
            self.assertEqual(decoded, out_value)

    def test_decode_failure(self):
        '''
        Tests that decode fails in the correct scenarios.
        '''
        for in_value in self.decode_failure:
            self.assertRaises(InvalidDecodeValueError, self.option.decode, in_value)

    # Override these if you implement non-default behaviour

    def test_default(self):
        '''
        Tests the option's default value, and ensure that it isn't specificed.

        You need to override this method if your option has a default value.
        '''
        self.assertEqual(self.option.default, Option.NotSpecified)

    def test_presentation(self):
        '''
        Tests that presentation returns the same value that is passed into it.

        You need to override this method if your option presents a different
        value than what it is given.
        '''
        value = ['testing']
        self.assertEqual(value, self.option.presentation(value))
