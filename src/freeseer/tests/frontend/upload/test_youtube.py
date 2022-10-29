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
import os
import mock
import sys
import unittest
import pytest
from io import StringIO

from freeseer.framework.youtube import Response
from freeseer.frontend.upload import youtube
from freeseer.tests.framework.test_youtube import TestYoutubeService


class TestYoutubeFrontend(unittest.TestCase):
    TEST_RESPONSE = {
        "id": "test",
        "status": "test",
        "content": "test",
    }

    def setUp(self):
        """Stardard init method: runs before each test_* method"""
        self.saved_stdout = sys.stdout
        self.out = StringIO()

    def test_get_defaults(self):
        """Test get_defaults, should always return a dict"""
        home = os.getenv('HOME')
        expected = {
            'client_secrets': '{}/.freeseer/client_secrets.json'.format(home),
            'video_directory': '{}/Videos'.format(home),
            'oauth2_token': '{}/.freeseer/oauth2_token.json'.format(home)
        }
        actual = youtube.get_defaults()
        self.assertDictEqual(actual, expected)

    def test_prompt_user_not_yes(self):
        """Test output prompting user if they want to upload (assume yes was not specified)"""
        test_videos = {"v1", "v2", "v3"}
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
        self.assertTrue(youtube.prompt_user({"v1", "v2", "v3"}, confirmation=True))


@pytest.mark.parametrize("expected, path", [
    ("/path/that/does/not/exist does not exist, please specify a valid token file", "/path/that/does/not/exist"),
    ("Nothing to upload", TestYoutubeService.SAMPLE_VIDEO),
])
def test_upload(capsys, expected, path):
    """
    Test the responses from the upload test cases.
    """
    youtube.upload([], path, False)
    out, err = capsys.readouterr()
    assert expected == out.strip()


@pytest.mark.parametrize("expected, response", [
    ("The file was successfully uploaded with video id: {}".format(TestYoutubeFrontend.TEST_RESPONSE['id']),
     Response.SUCCESS),
    ("The file failed to upload with unexpected response: {}".format(TestYoutubeFrontend.TEST_RESPONSE),
     Response.UNEXPECTED_FAILURE),
    ("An unretriable HTTP error {} occurred:\n{}".format(TestYoutubeFrontend.TEST_RESPONSE['status'],
                                                         TestYoutubeFrontend.TEST_RESPONSE['content']),
     Response.UNRETRIABLE_ERROR),
    ("The maximum number of retries has been reached",
     Response.MAX_RETRIES_REACHED),
    ("The access token has expired or been revoked, please run python -m freeseer config youtube",
     Response.ACCESS_TOKEN_ERROR),
])
def test_handle_response(capsys, expected, response):
    """
    Test the actual response vs the expected response from response_test_cases.
    """
    youtube.handle_response(response, TestYoutubeFrontend.TEST_RESPONSE)
    out, err = capsys.readouterr()
    assert expected == out.strip()
