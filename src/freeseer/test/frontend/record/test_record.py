#!/usr/bin/python


import unittest
import time

from PyQt4 import QtGui, QtTest, Qt
from freeseer.frontend.record.record import RecordApp

class TestResetTimer(unittest.TestCase):
	
	def setUp(self):

		self.app = QtGui.QApplication([])
		self.record_app = RecordApp()

	def test_start_recording(self):
		#self.record_app.record(True)
		#self.record_app.record(False)

		self.record_app.time_minutes = 15
		self.record_app.time_seconds = 30

		self.record_app.reset_timer()

		self.assertTrue(self.record_app.time_minutes == 0 and self.record_app.time_seconds == 0)


	def test_reset_timer(self):	
		self.record_app.time_minutes = 15
		self.record_app.time_seconds = 30

		self.record_app.reset_timer()

		self.assertTrue(self.record_app.time_minutes == 0 and self.record_app.time_seconds == 0)


