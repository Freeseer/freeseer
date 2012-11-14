
import unittest
import os

from PyQt4 import QtGui, QtTest, Qt, QtCore

from freeseer.framework.config import Config
from freeseer.frontend.configtool.configtool import ConfigToolApp

homedir = os.path.expanduser("~/.freeseer")


class TestConfigToolApp(unittest.TestCase):
	'''
	Test suite to verify the functionality of the ConfigToolApp class.

	Tests interact like an end user (using QtTest). Expect the app to be rendered.

	NOTE: most tests will follow this format:
		1. Get current config setting
		2. Make UI change (config change happens immediately)
		3. Reparse config file
		4. Test that has changed (using the previous and new)
	'''

	def setUp(self):
		'''
		Stardard init method: runs before each test_* method

		Initializes a QtGui.QApplication and ConfigToolApp object.
		ConfigToolApp.show() causes the UI to be rendered.
		'''

		self.app = QtGui.QApplication([])
		self.config_tool = ConfigToolApp()
		self.config_tool.show()
		self.config = Config(homedir)

	def test_general_settings(self):
		self.assertTrue(self.config_tool.currentWidget == self.config_tool.generalWidget)
		self.config.readConfig()			


	def test_recording_settings(self):
		item = self.config_tool.mainWidget.optionsTreeWidget.findItems(self.config_tool.avString, QtCore.Qt.MatchExactly)
		self.assertFalse(len(item) == 0 or item[0] == None)
		self.config_tool.mainWidget.optionsTreeWidget.setCurrentItem(item[0])
		QtTest.QTest.mouseClick(self.config_tool.mainWidget.optionsTreeWidget, Qt.Qt.LeftButton)

		self.assertTrue(self.config_tool.currentWidget == self.config_tool.avWidget)
		self.config.readConfig()			


	def test_plugin_settings(self):
		# TODO
		pass

	def test_plugin_audio_input_settings(self):
		# TODO
		pass

	def test_plugin_audio_mixer_settings(self):
		# TODO
		pass

	def test_plugin_video_input_settings(self):
		# TODO
		pass

	def test_plugin_video_mixer_settings(self):
		# TODO
		pass

	def test_plugin_output_settings(self):
		# TODO
		pass

	def test_logger_settings(self):
		item = self.config_tool.mainWidget.optionsTreeWidget.findItems(self.config_tool.loggerString, QtCore.Qt.MatchExactly)
		self.assertFalse(len(item) == 0 or item[0] == None)
		self.config_tool.mainWidget.optionsTreeWidget.setCurrentItem(item[0])
		QtTest.QTest.mouseClick(self.config_tool.mainWidget.optionsTreeWidget, Qt.Qt.LeftButton)

		self.assertTrue(self.config_tool.currentWidget == self.config_tool.loggerWidget)
		self.config.readConfig()			
	



	def test_close_configtool(self):
		self.assertTrue(self.config_tool.mainWidget.isVisible())
		QtTest.QTest.mouseClick(self.config_tool.mainWidget.closePushButton, Qt.Qt.LeftButton)
		self.assertFalse(self.config_tool.mainWidget.isVisible())


	def tearDown(self):
		'''
		Standard tear down method. Runs after each test_* method.

		This method closes the ConfigToolApp by clicking the "close" button
		'''

		QtTest.QTest.mouseClick(self.config_tool.mainWidget.closePushButton, Qt.Qt.LeftButton)
