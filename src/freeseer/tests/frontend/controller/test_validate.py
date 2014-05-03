#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2014 Free and Open Source Software Learning Centre
# http://fosslc.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

import unittest

from freeseer.frontend.controller import validate


class TestServerApp(unittest.TestCase):
    '''
    Test cases for validate.
    '''

    def setUp(self):
        '''
        Stardard init method: runs before each test_* method
        '''
        self.test_form_data = {}

    def test_valid_control_recording_data(self):
        '''
        Tests validating the request form for controlling a recording with valid data
        '''
        self.test_form_data["command"] = "start"
        self.assertTrue(validate.validate_control_recording_request_form(self.test_form_data))

    def test_invalid_control_recording_data(self):
        '''
        Tests validating the request form for controlling a recording with invalid data
        '''
        self.test_form_data["command"] = 1
        self.assertFalse(validate.validate_control_recording_request_form(self.test_form_data))
        self.test_form_data["command"] = "invalid-command"
        self.assertFalse(validate.validate_control_recording_request_form(self.test_form_data))

    def test_invalid_control_recording_data_structure(self):
        '''
        Tests validating the request form for controlling a recording with an invalid data structure
        '''
        invalid_structure = {"test": "should fail"}

        self.assertFalse(validate.validate_control_recording_request_form(None))
        self.assertFalse(validate.validate_control_recording_request_form(invalid_structure))

    def test_valid_create_recording_data(self):
        '''
        Tests validating the request form for creating a recording with valid data
        '''
        self.test_form_data["filename"] = "valid_filename"
        self.assertTrue(validate.validate_create_recording_request_form(self.test_form_data))

    def test_invalid_create_recording_data(self):
        '''
        Tests validating the request form for creating a recording with invalid data
        '''
        self.test_form_data["filename"] = "invalid/filename"
        self.assertFalse(validate.validate_create_recording_request_form(self.test_form_data))
        self.test_form_data["filename"] = 1
        self.assertFalse(validate.validate_create_recording_request_form(self.test_form_data))
        self.test_form_data["filename"] = ""
        self.assertFalse(validate.validate_create_recording_request_form(self.test_form_data))

    def test_invalid_create_recording_data_structure(self):
        '''
        Tests validating the request form for controlling a recording with an invalid data structure
        '''
        invalid_structure = {"test": "should fail"}

        self.assertFalse(validate.validate_create_recording_request_form(None))
        self.assertFalse(validate.validate_create_recording_request_form(invalid_structure))
