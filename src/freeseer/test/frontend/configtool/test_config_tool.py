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

	def tearDown(self):
		'''
		Standard tear down method. Runs after each test_* method.

		This method closes the ConfigToolApp by clicking the "close" button
		'''

		QtTest.QTest.mouseClick(self.config_tool.mainWidget.closePushButton, Qt.Qt.LeftButton)
		del self.app


	def test_general_settings(self):
		'''
		Tests for the config tool's General Tab
		'''
		
		# General tab
		self.assertTrue(self.config_tool.currentWidget == self.config_tool.generalWidget)

		# Language drop-down
		# TODO

		# Record directory
		# TODO

		# AutoHide Checkbox
		for i in range(2):
			state = self.config_tool.currentWidget.autoHideCheckBox.checkState()
			expected_state = QtCore.Qt.Unchecked
			if state == QtCore.Qt.Unchecked:
				expected_state = QtCore.Qt.Checked
			self.config_tool.currentWidget.autoHideCheckBox.click()
			self.assertEquals( \
				self.config_tool.currentWidget.autoHideCheckBox.checkState(), expected_state)	
	
			self.config.readConfig()
			self.assertEquals(self.config.auto_hide, expected_state == QtCore.Qt.Checked)
			
	def test_recording_settings(self):
		'''
		Tests for config tool's Recording tab
		'''

		# Select "Recording" tab
		item = self.config_tool.mainWidget.optionsTreeWidget.findItems(self.config_tool.avString, QtCore.Qt.MatchExactly)
		self.assertFalse(len(item) == 0 or item[0] == None)
		self.config_tool.mainWidget.optionsTreeWidget.setCurrentItem(item[0])
		QtTest.QTest.mouseClick(self.config_tool.mainWidget.optionsTreeWidget, Qt.Qt.LeftButton)

		# Recording tab
		self.assertTrue(self.config_tool.currentWidget == self.config_tool.avWidget)
	
		# Audio Input

		# Checkbox
		for i in range(2):
			self.config.readConfig()
			if self.config_tool.currentWidget.audioGroupBox.isChecked():
				self.assertTrue(self.config.enable_audio_recording)
				self.assertTrue(self.config.audiomixer == "Audio Passthrough" or \
					self.config.audiomixer == "Multiple Audio Inputs")
				self.config_tool.currentWidget.audioGroupBox.setChecked(False)
			else:
				self.assertFalse(self.config.enable_audio_recording)
				self.config_tool.currentWidget.audioGroupBox.setChecked(True)

		# Dropdown
		# TODO


		# Video Input
		# Checkbox
		for i in range(2):
			self.config.readConfig()
			if self.config_tool.currentWidget.videoGroupBox.isChecked():
				self.assertTrue(self.config.enable_video_recording)
				# TODO: Write better test case for this
				self.assertTrue(self.config.videomixer == "Video Passthrough" or \
					self.config.videomixer == "Picture-In-Picture")
				self.config_tool.currentWidget.videoGroupBox.setChecked(False)
			else:
				self.assertFalse(self.config.enable_video_recording)
				self.config_tool.currentWidget.videoGroupBox.setChecked(True)
		
		# Dropdown
		# TODO		


		# Record to File
		
		# Checkbox
		for i in range(2):
			self.config.readConfig()
			if self.config_tool.currentWidget.fileGroupBox.isChecked():
				self.assertTrue(self.config.record_to_file)
				# TODO: Write better test case for this
				self.assertTrue(self.config.record_to_file_plugin == "Ogg Output" or \
					self.config.record_to_file_plugin == "WebM Output")
				self.config_tool.currentWidget.fileGroupBox.setChecked(False)
			else:
				self.assertFalse(self.config.record_to_file)
				self.config_tool.currentWidget.fileGroupBox.setChecked(True)

		# Dropdown
		# TODO

		# Record to Stream	
		
		# Checkbox
		for i in range(2):
			self.config.readConfig()
			if self.config_tool.currentWidget.streamGroupBox.isChecked():
				self.assertTrue(self.config.record_to_stream)
				# TODO: Write better test case for this
				#self.assertTrue(self.config.record_to_stream_plugin == None)
				self.config_tool.currentWidget.streamGroupBox.setChecked(False)
			else:
				self.assertFalse(self.config.record_to_stream)
				self.config_tool.currentWidget.streamGroupBox.setChecked(True)
		
		# Dropdown
		# TODO


	def test_plugin_audio_input_settings(self):
		'''
		Tests for config tool's Plugins->Audio Input tab
		'''

		# TODO
		pass

	def test_plugin_audio_mixer_settings(self):
		'''
		Tests for config tool's Plugins->Audio Mixer tab
		'''
		
		# TODO
		pass

	def test_plugin_video_input_settings(self):
		'''
		Tests for config tool's Plugins->Video Input tab
		'''
		
		# TODO
		pass

	def test_plugin_video_mixer_settings(self):
		'''
		Tests for config tool's Plugins->Video Mixer tab
		'''
		
		# TODO
		pass

	def test_plugin_output_settings(self):
		'''
		Tests for config tool's Plugins->Output tab
		'''
		
		# TODO
		pass

	def test_logger_settings(self):
		'''
		Tests for config tool's Logger tab

		Needs to be tested differently since the
		Config instance isn't affected by changes in this tab.
		'''

		# TODO
		pass

	
	def test_close_configtool(self):
		'''
		Tests for config tool's close button
		'''
		
		self.assertTrue(self.config_tool.mainWidget.isVisible())
		QtTest.QTest.mouseClick(self.config_tool.mainWidget.closePushButton, Qt.Qt.LeftButton)
		self.assertFalse(self.config_tool.mainWidget.isVisible())

	def test_file_menu_quit(self):
		'''
		Tests for config tool's File->Quit
		'''
		
		self.assertTrue(self.config_tool.isVisible())
	
		# File->Quit
		self.config_tool.actionExit.trigger()
		self.assertFalse(self.config_tool.isVisible())

	def test_help_menu_about(self):
		'''
		Tests for config tool's Help->About
		'''
		
		self.assertTrue(self.config_tool.isVisible())

		# Help->About
		self.config_tool.actionAbout.trigger()
		self.assertFalse(self.config_tool.hasFocus())
		self.assertTrue(self.config_tool.aboutDialog.isVisible())

		# Click "Close"
		QtTest.QTest.mouseClick(self.config_tool.aboutDialog.closeButton, Qt.Qt.LeftButton)
		self.assertFalse(self.config_tool.aboutDialog.isVisible())
