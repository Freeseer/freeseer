#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2013 Free and Open Source Software Learning Centre
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
import shutil
import tempfile
import unittest

from PyQt4 import QtSql

from freeseer.framework.config.profile import Profile
from freeseer.framework.database import QtDBConnector
from freeseer.framework.plugin import PluginManager
from freeseer.framework.presentation import Presentation


class TestDatabase(unittest.TestCase):
    def setUp(self):
        '''
        Stardard init method: runs before each test_* method

        Initializes a PluginManager

        '''
        self.profile_path = tempfile.mkdtemp()
        profile = Profile(self.profile_path, 'testing')

        dirname = os.path.dirname(__file__)
        self._csvfile = os.path.join(dirname, 'sample_talks.csv')

        db_file = os.path.join(self.profile_path, 'presentations.db')
        self.db = QtDBConnector(db_file, PluginManager(profile))

    def tearDown(self):
        '''
        Generic unittest.TestCase.tearDown()
        '''
        shutil.rmtree(self.profile_path)

    def test_get_talks(self):
        """Simply test that a query is returned"""
        self.assertIsInstance(self.db.get_talks(), QtSql.QSqlQuery)

    def test_get_events(self):
        """Simply test that a query is returned"""
        self.assertIsInstance(self.db.get_events(), QtSql.QSqlQuery)

    def test_get_talk_ids(self):
        """Simply test that a query is returned"""
        self.assertIsInstance(self.db.get_talk_ids(), QtSql.QSqlQuery)

    def test_get_talks_by_event(self):
        """Simply test that a query is returned"""
        self.assertIsInstance(self.db.get_talks_by_event("SC2011"), QtSql.QSqlQuery)

    def test_get_talks_by_room(self):
        """Simply test that a query is returned"""
        self.assertIsInstance(self.db.get_talks_by_room("T105"), QtSql.QSqlQuery)

    def test_get_presentation(self):
        """Simply test that a presentation is returned"""
        self.assertIsInstance(self.db.get_presentation(1), Presentation)

    def test_get_presentations_model(self):
        """Simply test that a model is returned"""
        self.assertIsInstance(self.db.get_presentations_model(), QtSql.QSqlTableModel)

    def test_get_events_model(self):
        """Simply test that a model is returned"""
        self.assertIsInstance(self.db.get_events_model(), QtSql.QSqlQueryModel)

    def test_get_rooms_model(self):
        """Simply test that a model is returned"""
        self.assertIsInstance(self.db.get_rooms_model("SC2011"), QtSql.QSqlQueryModel)

    def test_get_talks_model(self):
        """Simply test that a model is returned"""
        self.assertIsInstance(self.db.get_talks_model("SC2011", "T105"), QtSql.QSqlQueryModel)

    def test_add_talks_from_rss(self):
        """Test that talks are retrieved from the RSS feed"""

        feed1 = "http://fosslc.org/drupal/presentations_rss/summercamp2010"
        feed2 = "http://fosslc.org/drupal/presentations_rss/sc2011"

        presentation1 = Presentation("Managing map data in a database", "Andrew Ross")
        presentation2 = Presentation("Building NetBSD", "David Maxwell")

        self.db.add_talks_from_rss(feed1)
        self.assertTrue(self.db.presentation_exists(presentation1))

        self.db.add_talks_from_rss(feed2)
        self.assertTrue(self.db.presentation_exists(presentation2))

    def test_add_talks_from_csv(self):
        """Test that talks are retrieved from the CSV file"""

        fname = self._csvfile

        presentation = Presentation("Building NetBSD", "David Maxwell")

        self.db.add_talks_from_csv(fname)
        self.assertTrue(self.db.presentation_exists(presentation))
