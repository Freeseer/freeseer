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
import httpretty
import unittest

from freeseer.plugins.importer.rss_feedparser import FeedParser


class TestFeedParser(unittest.TestCase):

    def setUp(self):
        rss_file = os.path.join(os.path.dirname(__file__), 'testrss.rss')
        with open(rss_file, 'r') as f:
            rss_feed = f.read()
        httpretty.enable()
        feedurl = "http://fosslc.org/drupal/presentations_rss/summercamp2010"
        httpretty.register_uri(httpretty.GET, feedurl, body=rss_feed, content_type="application/rss+xml")
        feedparser = FeedParser()
        self.presentation = feedparser.get_presentations(feedurl)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_get_presentations(self):
        self.assertEqual(self.presentation[0]['Title'], u"Managing map data in a database")
        self.assertEqual(self.presentation[0]['Speaker'], u"Andrew Ross")
        self.assertEqual(self.presentation[0]['Level'], u"Intermediate")
        self.assertEqual(self.presentation[0]['Status'], u"Approved")
        self.assertEqual(self.presentation[0]['Time'], u"2010-05-14T10:45")
        self.assertEqual(self.presentation[0]['Event'], u"Summercamp2010")
        self.assertEqual(self.presentation[0]['Room'], u"Rom AB113")
