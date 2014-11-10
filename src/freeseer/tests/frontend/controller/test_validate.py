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

import pytest

from freeseer.frontend.controller import validate
from freeseer.frontend.controller import recording
from freeseer.frontend.controller.server import HTTPError


class TestValidationApp:
    '''
    Test cases for validate.
    '''

    def test_valid_control_recording_data(self):
        '''
        Tests validating the request form for controlling a recording with valid data
        '''
        form_data = {'command': 'start'}
        validate.validate_form(form_data, recording.form_schema['control_recording'])

    @pytest.mark.parametrize('control', [1, 'invalid-command'])
    def test_invalid_control_recording_data(self, control):
        '''
        Tests validating the request form for controlling a recording with invalid data
        '''
        form_data = {'command': control}
        with pytest.raises(HTTPError):
            validate.validate_form(form_data, recording.form_schema['control_recording'])

    @pytest.mark.parametrize('invalid_form', [None, {'test': 'should fail'}])
    def test_invalid_control_recording_data_structure(self, invalid_form):
        '''
        Tests validating the request form for controlling a recording with an invalid data structure
        '''
        with pytest.raises(HTTPError):
            validate.validate_form(invalid_form, recording.form_schema['control_recording'])

    def test_valid_create_recording_data(self):
        '''
        Tests validating the request form for creating a recording with valid data
        '''
        form_data = {'filename': 'valid_filename'}
        validate.validate_form(form_data, recording.form_schema['create_recording'])

    @pytest.mark.parametrize('filename', ['invalid/filename', 1, ''])
    def test_invalid_create_recording_data(self, filename):
        '''
        Tests validating the request form for creating a recording with invalid data
        '''
        form_data = {'filename': filename}
        with pytest.raises(HTTPError):
            validate.validate_form(form_data, recording.form_schema['create_recording'])

    @pytest.mark.parametrize('invalid_form', [None, {'test': 'should fail'}])
    def test_invalid_create_recording_data_structure(self, invalid_form):
        '''
        Tests validating the request form for controlling a recording with an invalid data structure
        '''
        with pytest.raises(HTTPError):
            validate.validate_form(invalid_form, recording.form_schema['create_recording'])
