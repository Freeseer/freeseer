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

import mock
import sys
import unittest
from StringIO import StringIO

from freeseer.framework.youtube import Response
from freeseer.frontend.upload import youtube
from freeseer.tests.framework.test_youtube import TestYoutubeService


class TestYoutubeFrontend(unittest.TestCase):
    def setUp(self):
        """Stardard init method: runs before each test_* method"""
        self.test_response = {
            "id": "test",
            "status": "test",
            "content": "test"
        }
        self.saved_stdout = sys.stdout
        self.out = StringIO()

    def test_handle_response_success(self):
        """Test Response.SUCCESS"""
        expected = "The file was successfully uploaded with video id: {}".format(self.test_response['id'])
        try:
            sys.stdout = self.out
            youtube.handle_response(Response.SUCCESS, self.test_response)
            output = self.out.getvalue().strip()
            self.assertEqual(expected, output)
        finally:
            sys.stdout = self.saved_stdout

    def test_handle_response_failure(self):
        """Test Response.UNEXPECTED_FAILURE"""
        expected = "The file failed to upload with unexpected response: {}".format(self.test_response)
        try:
            sys.stdout = self.out
            youtube.handle_response(Response.UNEXPECTED_FAILURE, self.test_response)
            output = self.out.getvalue().strip()
            self.assertEqual(expected, output)
        finally:
            sys.stdout = self.saved_stdout

    def test_handle_response_unretriable(self):
        """Test Response.UNRETRIABLE_ERROR"""
        expected = "An unretriable HTTP error {} occurred:\n{}".format(self.test_response['status'], self.test_response['content'])
        try:
            sys.stdout = self.out
            youtube.handle_response(Response.UNRETRIABLE_ERROR, self.test_response)
            output = self.out.getvalue().strip()
            self.assertEqual(expected, output)
        finally:
            sys.stdout = self.saved_stdout

    def test_handle_response_max_retries(self):
        """Test Response.MAX_RETRIES_REACHED"""
        expected = "The maximum number of retries has been reached"
        try:
            sys.stdout = self.out
            youtube.handle_response(Response.MAX_RETRIES_REACHED, self.test_response)
            output = self.out.getvalue().strip()
            self.assertEqual(expected, output)
        finally:
            sys.stdout = self.saved_stdout

    def test_handle_response_token_error(self):
        """Test Response.ACCESS_TOKEN_ERROR"""
        expected = "The access token has expired or been revoked, please run python -m freeseer config youtube"
        try:
            sys.stdout = self.out
            youtube.handle_response(Response.ACCESS_TOKEN_ERROR, self.test_response)
            output = self.out.getvalue().strip()
            self.assertEqual(expected, output)
        finally:
            sys.stdout = self.saved_stdout

    def test_get_defaults(self):
        """Test get_defaults, should always return a dict"""
        self.assertTrue(youtube.get_defaults())

    def test_upload_missing_token_file(self):
        """Test missing token file on upload"""
        token_path = "/path/that/does/not/exist"
        expected = "{} does not exist, please specify a valid token file".format(token_path)
        try:
            sys.stdout = self.out
            youtube.upload([], token_path, False)
            output = self.out.getvalue().strip()
            self.assertEqual(expected, output)
        finally:
            sys.stdout = self.saved_stdout

    def test_upload_nothing_to_upload(self):
        """Test nothing to upload"""
        # Just pass a filepath that exists
        token_path = TestYoutubeService.SAMPLE_VIDEO
        expected = "Nothing to upload"
        try:
            sys.stdout = self.out
            youtube.upload([], token_path, False)
            output = self.out.getvalue().strip()
            self.assertEqual(expected, output)
        finally:
            sys.stdout = self.saved_stdout

    def test_prompt_user_not_yes(self):
        """Test output prompting user if they want to upload (assume yes was not specified)"""
        test_videos = set(["v1", "v2", "v3"])
        expected = "Found videos:\n"
        joined = "\n".join(test_videos)
        expected += joined
        try:
            sys.stdout = self.out
            with mock.patch('__builtin__.raw_input', return_value='no'):
                youtube.prompt_user(test_videos, confirmation=False)
            output = self.out.getvalue().strip()
            self.assertEqual(expected, output)
        finally:
            sys.stdout = self.saved_stdout

    def test_prompt_user_yes(self):
        """Test assume yes (assume yes was not specified)"""
        self.assertTrue(youtube.prompt_user(set(["v1", "v2", "v3"]), confirmation=True))
