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
import pytest

from freeseer.framework.youtube import Response
from freeseer.framework.youtube import YoutubeService


class TestYoutubeService(unittest.TestCase):
    SAMPLE_VIDEO = os.path.join(os.path.dirname(__file__), 'sample_video.ogg')
    SAMPLE_VIDEO_METADATA = {
        'tags': [
            'Freeseer',
            'FOSSLC',
            'Open Source',
        ],
        'categoryId': 27,
        'description': 'At Test by Alex recorded on 2014-03-09',
        'title': u'Test',
    }

    def test_get_metadata(self):
        """Test retrieval of metadata from video file.

        Case: Returned metadata should be equal to sample video's metadata."""
        metadata = YoutubeService.get_metadata(self.SAMPLE_VIDEO)
        self.assertDictEqual(self.SAMPLE_VIDEO_METADATA, metadata)

    def test_upload_video(self):
        """Test uploading a video file using mocks"""
        youtube = YoutubeService()
        youtube.upload_video = Mock(return_value=(Response.SUCCESS, None))
        response_code, response = youtube.upload_video(self.SAMPLE_VIDEO)
        youtube.upload_video.assert_called_with(self.SAMPLE_VIDEO)
        self.assertEqual(Response.SUCCESS, response_code)


@pytest.mark.parametrize("video, expected", [
    ("/path/to/test.ogg", True),
    ("test.webm", True),
    ("asdfg.qwergb", False),
])
def test_valid_video_file(video, expected):
    """Tests valid_video_file function for all test cases."""
    assert YoutubeService.valid_video_file(video) == expected
