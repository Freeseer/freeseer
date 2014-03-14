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
import tempfile

from freeseer.framework.config import options
from freeseer.framework.config.core import Config


class TestConfig(Config):
    option1 = options.StringOption('hello')
    option2 = options.IntegerOption(1337)


class ConfigStorageTest(object):
    """Base class for testing filesystem-based ConfigStorage classes."""

    CONFIG_STORAGE_CLASS = None
    INITIAL_LOAD_CONFIG = ''
    AFTER_STORE_CONFIG = ''

    def setUp(self):
        fd_int, self.filepath = tempfile.mkstemp()
        os.close(fd_int)
        os.remove(self.filepath)

        self.storage = self.CONFIG_STORAGE_CLASS(self.filepath)
        self.config = TestConfig()

    def tearDown(self):
        os.remove(self.filepath)

    def test_load(self):
        """Tests that load(...) correctly populates a TestConfig instance using a CONFIG_STORAGE_CLASS instance."""
        self.storage.load(self.config, 'this_section')
        self.assertEqual(self.config.option1, 'hello')
        self.assertEqual(self.config.option2, 1337)

        with open(self.filepath, 'w') as fd:
            fd.write(self.INITIAL_LOAD_CONFIG)

        self.storage.load(self.config, 'this_section')
        self.assertEqual(self.config.option1, 'othello')
        self.assertEqual(self.config.option2, 0)

    def test_store(self):
        """Tests that store(...) correctly persists a TestConfig instance using a CONFIG_STORAGE_CLASS instance."""
        self.config.option1 = 'something_new'
        self.config.option2 = 10

        self.storage.store(self.config, 'this_section')
        with open(self.filepath) as fd:
            self.assertEqual(fd.read(), self.AFTER_STORE_CONFIG)
