#!/usr/bin/env python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2013  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

import os
import shutil
import tempfile
import unittest

from freeseer.framework.config.options import FolderOption
from freeseer.tests.framework.config.options import OptionTest


class TestFolderOptionNoDefault(unittest.TestCase, OptionTest):
    """Tests FolderOption without a default value."""

    valid_success = [
        '/tmp',
    ]
    valid_failure = [
        '/tmp/1',
    ]

    encode_success = zip(valid_success, valid_success)

    decode_success = zip(valid_success, valid_success)
    decode_failure = valid_failure

    def setUp(self):
        self.option = FolderOption()

    def test_presentation(self):
        path = tempfile.mkdtemp()
        shutil.rmtree(path)

        presentation_value = self.option.presentation(path)
        self.assertEqual(presentation_value, path)
        self.assertFalse(os.path.exists(presentation_value))


class TestFolderOptionAutoCreate(TestFolderOptionNoDefault):
    """Tests FolderOption without a default value, and with auto_create turned on."""

    valid_failure = []

    decode_failure = []

    def setUp(self):
        self.option = FolderOption(auto_create=True)

    def test_presentation(self):
        path = tempfile.mkdtemp()
        shutil.rmtree(path)

        presentation_value = self.option.presentation(path)
        self.assertEqual(presentation_value, path)
        self.assertTrue(os.path.exists(presentation_value))

        shutil.rmtree(path)


class TestFolderOptionWithDefault(TestFolderOptionNoDefault):
    """Tests FolderOption with a default value."""

    def setUp(self):
        self.option = FolderOption('/tmp')

    def test_default(self):
        """Tests that the default was set correctly."""
        self.assertEqual(self.option.default, '/tmp')
