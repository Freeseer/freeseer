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

import shlex
import shutil
import sys
import tempfile
import unittest

from mock import patch
from PyQt4 import QtSql

from freeseer.framework.config.profile import Profile
from freeseer.framework.presentation import Presentation
from freeseer.frontend import cli


class TestCli(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.presentations = []
        cls.presentations.append(Presentation("test title 1", "test speaker", "test room", "test event",))
        cls.presentations.append(Presentation("test title 2", "test speaker", "test room", "test event",))

    def setUp(self):
        self.parser = cli.setup_parser()
        self.profile_path = tempfile.mkdtemp()
        profile = Profile(self.profile_path, 'testing')
        self.db = profile.get_database()
        for talk in self.presentations:
            self.db.insert_presentation(talk)

    def tearDown(self):
        shutil.rmtree(self.profile_path)

    @patch.object(Profile, 'get_database')
    def test_add_talk(self, mock_profile):
        """Test adding a talk"""
        mock_profile.return_value = self.db
        args = shlex.split('talk add -t "test title" -s "john doe" -e testing -r rm123')
        sys.argv[1:] = args
        cli.parse_args(self.parser, args)
        talks = self.db.get_talks()
        talks.next()  # Point to talk data
        talks.next()  # Skip first test entry
        talks.next()  # Skip second test entry
        record = talks.record()

        self.assertEqual(talks.value(record.indexOf('title')).toString(), u'test title')
        self.assertEqual(talks.value(record.indexOf('speaker')).toString(), u'john doe')
        self.assertEqual(talks.value(record.indexOf('event')).toString(), u'testing')
        self.assertEqual(talks.value(record.indexOf('room')).toString(), u'rm123')

    def test_remove_talk(self):
        """Test removing a talk"""
        args = shlex.split("talk remove -i 1")
        sys.argv[1:] = args
        cli.parse_args(self.parser, args)
        talks = QtSql.QSqlQuery('SELECT COUNT(*) FROM presentations WHERE title="test title 1" AND speaker="test speaker"')
        self.assertEqual(talks.value(0).toInt()[0], 0)

    def test_clear_talks(self):
        """Test clearing all talks"""
        args = shlex.split("talk clear")
        sys.argv[1:] = args
        cli.parse_args(self.parser, args)
        count = QtSql.QSqlQuery('SELECT COUNT(*) FROM presentations')
        self.assertEqual(count.value(0).toInt()[0], 0)
