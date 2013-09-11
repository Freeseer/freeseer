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

import unittest

import pep8

from freeseer.tests import pep8_options
from freeseer.tests import pep8_report


class TestFramework(unittest.TestCase):
    def test_pep8(self):
        '''Ensure framework conforms to pep8'''
        checker = pep8.StyleGuide(**pep8_options)
        report = checker.check_files(['freeseer/tests/framework',
                                      'freeseer/framework',
                                      'freeseer/tests/__init__.py'])  # Need to ensure __init__.py is also checked
        pep8_report(self, report)
