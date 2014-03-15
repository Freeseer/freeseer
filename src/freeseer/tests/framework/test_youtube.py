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
import unittest
from mock import Mock

from freeseer.framework.youtube import Response
from freeseer.framework.youtube import YoutubeService


class TestYoutubeService(unittest.TestCase):

    SAMPLE_VIDEO = os.path.join(os.path.dirname(__file__), 'sample_video.ogg')

    def test_valid_video_file_ogg(self):
        """Test valid_video_file function

        Case: file ending in .ogg
        """
        self.assertTrue(YoutubeService.valid_video_file("/path/to/test.ogg"))

    def test_valid_video_file_webm(self):
        """Test valid_video_file function

        Case: file ending in .webm
        """
        self.assertTrue(YoutubeService.valid_video_file("test.webm"))

    def test_valid_video_file_invalid(self):
        """Test valid_video_file function

        Case: string not complying to valid file types
        """
        self.assertTrue(not YoutubeService.valid_video_file("asdfg.qwergb"))

    def test_get_metadata(self):
        """Test retrieval of metadata from video file"""
        # a dictionary should always be returned
        self.assertTrue(YoutubeService.get_metadata(self.SAMPLE_VIDEO))

    def test_upload_video(self):
        """Test uploading a video file using mocks"""
        youtube = YoutubeService()
        youtube.upload_video = Mock(return_value=(Response.SUCCESS, None))
        response_code, response = youtube.upload_video(self.SAMPLE_VIDEO)
        youtube.upload_video.assert_called_with(self.SAMPLE_VIDEO)
        self.assertEqual(Response.SUCCESS, response_code)
        