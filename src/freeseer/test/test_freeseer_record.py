#!/usr/bin/python


import unittest

from PyQt4 import QtGui, QtTest
from freeseer.frontend.record.record import RecordApp


class TestRecordApp(unittest.TestCase):
	
	def setUp(self):
		self.app = QtGui.QApplication([])
		self.record_app = RecordApp()



	def test_reset_timer(self):
		self.record_app.time_minutes = 15
		self.record_app.time_seconds = 30

		self.record_app.reset_timer()

		self.assertTrue(self.record_app.time_minutes == 0 and self.record_app.time_seconds == 0)
