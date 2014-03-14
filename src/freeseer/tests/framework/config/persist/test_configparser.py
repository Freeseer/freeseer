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

import unittest

from freeseer.framework.config.persist import ConfigParserStorage
from freeseer.tests.framework.config.persist import ConfigStorageTest

initial_config = '''\
[this_section]
option1 = othello
option2 = 0

'''
after_config = '''\
[this_section]
option1 = something_new
option2 = 10

'''


class TestConfigParserStorage(ConfigStorageTest, unittest.TestCase):
    """Tests that ConfigParserStorage works with a generic Config subclass."""

    CONFIG_STORAGE_CLASS = ConfigParserStorage
    INITIAL_LOAD_CONFIG = initial_config
    AFTER_STORE_CONFIG = after_config
