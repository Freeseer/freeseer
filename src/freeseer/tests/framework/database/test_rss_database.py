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
import pytest

from freeseer.framework.presentation import Presentation


rss_resource_relative_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'resources', 'sample_rss_data')

feed_2010 = (os.path.join(rss_resource_relative_path, 'summercamp2010.rss'),
             'http://fosslc.org/drupal/presentations_rss/summercamp2010')
feed_2011 = (os.path.join(rss_resource_relative_path, 'sc2011.rss'),
             'http://fosslc.org/drupal/presentations/sc2011')

presentation1 = Presentation('Managing map data in a database', 'Andrew Ross')
presentation2 = Presentation('Building NetBSD', 'David Maxwell')
presentation3 = Presentation('Lecture Broadcast and Capture using BigBlueButton', 'Fred Dixon')


@pytest.mark.httpretty
@pytest.mark.parametrize("feed, expected", [
    (feed_2010, [(presentation1, True)]),
    (feed_2011, [
        (presentation1, False),
        (presentation2, True),
        (presentation3, True)
    ]),
    (feed_2011, [(Presentation('Fake Title', 'Fake Speaker'), False)])
])
def test_add_talks_from_rss(db, feed, expected):
    """Assert that presentations can be added from an rss feed"""
    feed_filename, feed_url = feed

    with open(feed_filename) as presentation_rss_file:
        feed_data = presentation_rss_file.read()

    # Monkey patch GET request.
    httpretty.register_uri(httpretty.GET, feed_url, body=feed_data, content_type='application/rss+xml')
    db.add_talks_from_rss(feed_url)
    for presentation, expectation in expected:
        assert db.presentation_exists(presentation) == expectation
