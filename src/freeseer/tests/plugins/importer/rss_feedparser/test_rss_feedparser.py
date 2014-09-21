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

import json
import os

import httpretty
import pytest

from freeseer.plugins.importer.rss_feedparser import FeedParser


@pytest.yield_fixture
def presentation_feed():
    httpretty.enable()
    rss_data_relative_path = '../../../resources/sample_rss_data/'
    rss_file = os.path.join(os.path.dirname(__file__), rss_data_relative_path, 'summercamp2010.rss')
    with open(rss_file, 'r') as presentation_rss_file:
        rss_feed = presentation_rss_file.read()

    json_file = os.path.join(os.path.dirname(__file__), rss_data_relative_path, 'summercamp2010.json')
    with open(json_file, 'r') as presentation_json_file:
        json_data = json.load(presentation_json_file)

    feed_data = {"feedurl": "http://fosslc.org/drupal/presentations_rss/summercamp2010", "json_data": json_data}
    httpretty.register_uri(httpretty.GET, feed_data['feedurl'], body=rss_feed, content_type="application/rss+xml")

    yield feed_data
    httpretty.disable()


@pytest.mark.xfail(reason="Expected to fail until issue GH-555 is fixed")
def test_get_presentations(presentation_feed):
    NUMBER_OF_PRESENTATIONS = 20
    feedparser = FeedParser()
    presentations = feedparser.get_presentations(presentation_feed['feedurl'])

    assert presentations == presentation_feed['json_data']["presentations"]
    assert len(presentations) == NUMBER_OF_PRESENTATIONS
