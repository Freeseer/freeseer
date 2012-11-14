

import unittest
import logging

from freeseer.frontend.reporteditor.reporteditor import ReportEditorApp

from PyQt4 import QtGui, QtTest, Qt

class TestReportEditorApp(unittest.TestCase):
	'''
	Test cases for ReportEditorApp. 
	'''


	def setUp(self):
		'''
		Stardard init method: runs before each test_* method

		Initializes a QtGui.QApplication and ReportEditorApp object.
		ReportEditorApp() causes the UI to be rendered.
		'''

		self.app = QtGui.QApplication([])
		self.report_editor = ReportEditorApp()
		self.report_editor.show()


	def test_close_report_editor(self):
		'''
		Tests closing the ReportEditorApp
		'''

		QtTest.QTest.mouseClick(self.report_editor.editorWidget.closeButton, Qt.Qt.LeftButton)
		self.assertFalse(self.report_editor.editorWidget.isVisible())
