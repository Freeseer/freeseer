#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2012 Free and Open Source Software Learning Centre
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

from freeseer.framework.presentation import Presentation

class TestPresentation(unittest.TestCase):
	
	def setUp(self):
		'''
		Generic unittest.TestCase.setUp()
		'''

		self.pres = Presentation("John Doe", event="haha", time="NOW")

	def test_correct_time_set(self):
		'''
		Checks that the Presentation's time
		'''

		self.assertTrue(self.pres.time == "NOW")
		self.pres.speaker = "John Doe"

	def test_speaker_not_first_param(self):
		self.assertNotEquals(self.pres.speaker, "John Doe")

	def test_event_is_default(self):
		self.assertTrue(self.pres.event == "haha")
