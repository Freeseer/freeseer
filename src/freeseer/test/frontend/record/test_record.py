#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2011 Free and Open Source Software Learning Centre
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
import time

from PyQt4 import QtGui, QtTest, Qt
from freeseer.frontend.record.record import RecordApp

from freeseer.framework.gstreamer import Gstreamer


class TestRecordApp(unittest.TestCase):
	'''
	Test suite to verify the functionality of the RecordApp	class.

	Tests interact like an end user (using QtTest). Expect the app to be rendered.

	'''

	def setUp(self):
		'''
		Stardard init method: runs before each test_* method

		Initializes a QtGui.QApplication and RecordApp object.
		RecordApp.show() causes the UI to be rendered.

		'''

		self.app = QtGui.QApplication([])
		self.record_app = RecordApp()
		self.record_app.show()

	def test_init_conditions(self):
		'''
		Tests the initial state of the RecordApp
		'''

		pass

	def test_standby_to_recording(self):
		'''
		Tests pre and post conditions when entering Standby, Record, Stop modes
		
		'''

		# TODO: ROADBLOCK
		# The Gstreamer takes a while to initialize the preview.
		# Due to this, when the unitest clicks "Record", the preview has not yet been initialized
		# and Freeseer freezes
		# It is not trivial or clear how to detect whether or not the preview has loaded
		# It turns out that even if the state is GStreamer.PAUSE, the preview has not quite loaded

#		self.assertTrue(self.record_app.mainWidget.standbyPushButton.isVisible(), "[PRE STANDBY] Expected Standby button to be visible")
#		self.assertFalse(self.record_app.mainWidget.recordPushButton.isVisible(), "[PRE STANDBY] Expected Record button to be invisible")	

		# Click the Standby button with the left mouse button
#		QtTest.QTest.mouseClick(self.record_app.mainWidget.standbyPushButton, Qt.Qt.LeftButton)

#		self.assertFalse(self.record_app.mainWidget.standbyPushButton.isVisible(), "[STANDBY] Expected Standby button to be invisible")
#		self.assertTrue(self.record_app.mainWidget.recordPushButton.isVisible(), "[STANDBY] Expected Record button to be visible")

		# TODO: Check if preview has loaded
		
		# Click the Record button with the left mouse button
#		QtTest.QTest.mouseClick(self.record_app.mainWidget.recordPushButton, Qt.Qt.LeftButton)
		
#		self.assertFalse(self.record_app.mainWidget.standbyPushButton.isVisible(), "[RECORDING] Expected Standby button to be invisible")
#		self.assertTrue(self.record_app.mainWidget.recordPushButton.isVisible(), "[RECORDING] Expected Record button to be visible")
#		self.assertTrue(self.record_app.mainWidget.recordPushButton.text() == self.record_app.stopString, "[RECORDING] Incorrect button text for this phase")

		# Click the Record button again in 5 seconds with the left mouse button
#		QtTest.QTest.mouseClick(self.record_app.mainWidget.recordPushButton, Qt.Qt.LeftButton)


	def test_reset_timer(self):	
		'''
		Tests RecordApp.reset_timer()
		'''		

		self.record_app.time_minutes = 15
		self.record_app.time_seconds = 30

		self.record_app.reset_timer()

		self.assertTrue(self.record_app.time_minutes == 0 and self.record_app.time_seconds == 0)


