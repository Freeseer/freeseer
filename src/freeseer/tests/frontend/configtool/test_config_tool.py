#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2012, 2013, 2014 Free and Open Source Software Learning Centre
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

from mock import MagicMock
import shutil
import tempfile
import unittest

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtTest

from freeseer.framework.config.profile import ProfileManager
from freeseer.frontend.configtool.configtool import ConfigToolApp
from freeseer import settings


class TestConfigToolApp(unittest.TestCase):
    """
    Test suite to verify the functionality of the ConfigToolApp class.

    Tests interact like an end user (using QtTest). Expect the app to be rendered.

    NOTE: most tests will follow this format:
        1. Get current config setting
        2. Make UI change (config change happens immediately)
        3. Reparse config file
        4. Test that has changed (using the previous and new)
    """

    def setUp(self):
        """
        Stardard init method: runs before each test_* method

        Initializes a QtGui.QApplication and ConfigToolApp object.
        ConfigToolApp.show() causes the UI to be rendered.
        """
        self.profile_manager = ProfileManager(tempfile.mkdtemp())
        profile = self.profile_manager.get('testing')
        config = profile.get_config('freeseer.conf', settings.FreeseerConfig, storage_args=['Global'], read_only=False)

        self.app = QtGui.QApplication([])
        self.config_tool = ConfigToolApp(profile, config)
        self.config_tool.show()

    def tearDown(self):
        """
        Standard tear down method. Runs after each test_* method.

        This method closes the ConfigToolApp by clicking the "close" button
        """

        QtTest.QTest.mouseClick(self.config_tool.mainWidget.closePushButton, Qt.Qt.LeftButton)
        shutil.rmtree(self.profile_manager._base_folder)
        del self.config_tool.app
        self.app.deleteLater()

    def test_default_widget(self):
        self.assertEqual(self.config_tool.currentWidget, self.config_tool.generalWidget)

    def check_combobox_corner_cases_frontend(self, combobox_widget):
        """
        Tests that a given QtComboBox has:
        - a default selected item
        - does not blow up on the minimum and maximum index item in the combobox list
        """
        index = combobox_widget.currentIndex()
        combobox_widget.setCurrentIndex(0)
        self.assertEqual(combobox_widget.currentIndex(), 0)
        self.assertIsNot(combobox_widget.currentText(), None)
        combobox_widget.setCurrentIndex(combobox_widget.count() - 1)
        self.assertEqual(combobox_widget.currentIndex(), (combobox_widget.count() - 1))
        self.assertIsNot(combobox_widget.currentText(), None)
        combobox_widget.setCurrentIndex(index)
        self.assertEqual(combobox_widget.currentIndex(), index)
        self.assertIsNot(combobox_widget.currentText(), None)

    def select_general_settings_tab(self):
        # Select "General" tab
        item = self.config_tool.mainWidget.optionsTreeWidget.findItems(self.config_tool.generalString,
                                                                       QtCore.Qt.MatchExactly)
        self.assertFalse(not item or item[0] is None)
        self.config_tool.mainWidget.optionsTreeWidget.setCurrentItem(item[0])
        QtTest.QTest.mouseClick(self.config_tool.mainWidget.optionsTreeWidget, Qt.Qt.LeftButton)

    def test_general_settings_checkbox(self):
        """
        Test the config tool's General Tab auto-hide system tray icon checkbox with simulated user input
        """
        self.select_general_settings_tab()
        # Test disabled checkbox
        self.config_tool.currentWidget.autoHideCheckBox.setChecked(False)
        self.assertEqual(self.config_tool.currentWidget.autoHideCheckBox.checkState(), QtCore.Qt.Unchecked)
        self.assertFalse(self.config_tool.config.auto_hide)

        # Test enabled checkbox
        self.config_tool.currentWidget.autoHideCheckBox.setChecked(True)
        self.assertEqual(self.config_tool.currentWidget.autoHideCheckBox.checkState(), QtCore.Qt.Checked)
        self.assertTrue(self.config_tool.config.auto_hide)

    def test_general_settings_dropdown_menu(self):
        """
        Test the config tool's General Tab language selection drop down menu with simulated user input
        """
        self.select_general_settings_tab()
        # Test dropdown menu
        language_combo_box = self.config_tool.generalWidget.languageComboBox
        self.check_combobox_corner_cases_frontend(language_combo_box)

        QtTest.QTest.keyClick(language_combo_box, QtCore.Qt.Key_PageUp)  # Test simulated user interaction with drop down list
        for i in range(language_combo_box.count() - 2):
            last_language = self.config_tool.config.default_language
            QtTest.QTest.keyClick(language_combo_box, QtCore.Qt.Key_Down)
            current_language = self.config_tool.config.default_language
            self.assertNotEqual(last_language, current_language)

        # Test frontend constants
        self.assertNotEqual(language_combo_box.findText('Deutsch'), -1)  # Assert there are multiple languages in the menu
        self.assertNotEqual(language_combo_box.findText('English'), -1)
        self.assertNotEqual(language_combo_box.findText('Nederlands'), -1)

    def test_general_settings_help_reset(self):
        """
        Test the config tool's General Tab help link and reset button with simulated user input
        """
        self.select_general_settings_tab()
        # Test that Help us translate tries to open a web url.
        QtGui.QDesktopServices.openUrl = MagicMock(return_value=None)
        self.config_tool.open_translate_url()
        QtGui.QDesktopServices.openUrl.assert_called_with(
            QtCore.QUrl("http://freeseer.readthedocs.org/en/latest/contribute/translation.html")
        )

        # Reset
        # The reset test should set the backend config_tool values, simulate a user clicking through the reset popup and
        # verify that the backend config_tool values have been set to defaults.
        # TODO: FIXME. Related to gh#631. The buttons on the dialog cause segfaults in the test environment and prevent
        # the test from being implemented at the present time.
        # self.config_tool.confirm_reset()

    def select_recording_tab(self):
        """
        Helper function used to open up the recording tab for recording tab related tests
        """
        item = self.config_tool.mainWidget.optionsTreeWidget.findItems(self.config_tool.avString,
                                                                       QtCore.Qt.MatchExactly)
        self.assertFalse(not item or item[0] is None)
        self.config_tool.mainWidget.optionsTreeWidget.setCurrentItem(item[0])
        QtTest.QTest.mouseClick(self.config_tool.mainWidget.optionsTreeWidget, Qt.Qt.LeftButton)
        self.assertEqual(self.config_tool.currentWidget, self.config_tool.avWidget)

    def test_recording_settings_file(self):
        """
        Simulates a user interacting with the config tool record to file settings.
        """
        self.select_recording_tab()
        # Test disabled checkbox
        self.config_tool.currentWidget.fileGroupBox.setChecked(False)
        self.assertFalse(self.config_tool.config.record_to_file)

        # Test enabled checkbox
        self.config_tool.currentWidget.fileGroupBox.setChecked(True)
        self.assertTrue(self.config_tool.config.record_to_file)
        self.assertIn(self.config_tool.config.record_to_file_plugin, ['Ogg Output', 'WebM Output', 'Raw Output'])

        # Test combo box
        file_combo_box = self.config_tool.avWidget.fileComboBox
        self.check_combobox_corner_cases_frontend(file_combo_box)
        QtTest.QTest.keyClick(file_combo_box, QtCore.Qt.Key_PageUp)  # Simulate user input to test backend and frontend
        for i in range(file_combo_box.count() - 2):
            last_plugin = self.config_tool.config.record_to_file_plugin
            QtTest.QTest.keyClick(file_combo_box, QtCore.Qt.Key_Down)
            current_plugin = self.config_tool.config.record_to_file_plugin
            self.assertNotEqual(last_plugin, current_plugin)

        # Test frontend text values
        self.assertNotEqual(file_combo_box.findText('Ogg Output'), -1)
        self.assertNotEqual(file_combo_box.findText('WebM Output'), -1)
        self.assertNotEqual(file_combo_box.findText('Raw Output'), -1)

    def test_recording_settings_stream(self):
        """
        Simulates a user interacting with the config tool record to output stream settings.
        """
        self.select_recording_tab()
        # Test disabled checkbox
        self.config_tool.currentWidget.streamGroupBox.setChecked(False)
        self.assertFalse(self.config_tool.config.record_to_stream)

        # Test enabled checkbox
        self.config_tool.currentWidget.streamGroupBox.setChecked(True)
        self.assertTrue(self.config_tool.config.record_to_stream)

        # Test combo box
        stream_combo_box = self.config_tool.avWidget.streamComboBox
        self.check_combobox_corner_cases_frontend(stream_combo_box)
        QtTest.QTest.keyClick(stream_combo_box, QtCore.Qt.Key_PageUp)  # Simulate user input to test backend and frontend
        for i in range(stream_combo_box.count() - 2):
            last_plugin = self.config_tool.plugman.get_plugin_by_name(stream_combo_box.currentText(), 'Output')
            QtTest.QTest.keyClick(stream_combo_box, QtCore.Qt.Key_Down)
            current_plugin = self.config_tool.plugman.get_plugin_by_name(stream_combo_box.currentText(), 'Output')
            self.assertNotEqual(last_plugin, current_plugin)

        # Test frontend text values
        self.assertNotEqual(stream_combo_box.findText('RTMP Streaming'), -1)
        self.assertNotEqual(stream_combo_box.findText('Ogg Icecast'), -1)

    def test_recording_settings_video_input(self):
        """
        Simulates a user interacting with the config tool record to video input setting.
        """

        self.select_recording_tab()
        # Test disabled checkbox
        self.config_tool.currentWidget.videoGroupBox.setChecked(False)
        self.assertFalse(self.config_tool.config.enable_video_recording)

        # Test enabled checkbox
        self.config_tool.currentWidget.videoGroupBox.setChecked(True)
        self.assertTrue(self.config_tool.config.enable_video_recording)
        self.assertIn(self.config_tool.config.videomixer, ['Video Passthrough', 'Picture-In-Picture'])

        # Test combo box
        video_mixer_combo_box = self.config_tool.avWidget.videoMixerComboBox
        self.check_combobox_corner_cases_frontend(video_mixer_combo_box)
        QtTest.QTest.keyClick(video_mixer_combo_box, QtCore.Qt.Key_PageUp)  # Simulate user to test backend/frontend
        for i in range(video_mixer_combo_box.count() - 2):
            last_plugin = self.config_tool.videomixer
            QtTest.QTest.keyClick(video_mixer_combo_box, QtCore.Qt.Key_Down)
            current_plugin = self.config_tool.videomixer
            self.assertNotEqual(last_plugin, current_plugin)

        # Test frontend text values
        self.assertTrue(video_mixer_combo_box.findText('Video Passthrough') != -1)
        self.assertTrue(video_mixer_combo_box.findText('Picture-In-Picture') != -1)

    def test_recording_settings_audio_input(self):
        """
        Simulates a user interacting with the config tool record to audio input settings.
        """
        self.select_recording_tab()
        # Test disabled checkbox
        self.config_tool.currentWidget.audioGroupBox.setChecked(False)
        self.assertFalse(self.config_tool.config.enable_audio_recording)

        # Test enabled checkbox
        self.config_tool.currentWidget.audioGroupBox.setChecked(True)
        self.assertTrue(self.config_tool.config.enable_audio_recording)
        self.assertIn(self.config_tool.config.audiomixer, ['Audio Passthrough', 'Multiple Audio Inputs'])

        # Test combo box
        audio_mixer_combo_box = self.config_tool.avWidget.audioMixerComboBox
        self.check_combobox_corner_cases_frontend(audio_mixer_combo_box)
        QtTest.QTest.keyClick(audio_mixer_combo_box, QtCore.Qt.Key_PageUp)  # Simulate user to test backend/frontend
        for i in range(audio_mixer_combo_box.count() - 2):
            last_plugin = self.config_tool.audiomixer
            QtTest.QTest.keyClick(audio_mixer_combo_box, QtCore.Qt.Key_Down)
            current_plugin = self.config_tool.audiomixer
            self.assertNotEqual(last_plugin, current_plugin)

        # Test frontend text values
        self.assertNotEqual(audio_mixer_combo_box.findText('Audio Passthrough'), -1)
        self.assertNotEqual(audio_mixer_combo_box.findText('Multiple Audio Inputs'), -1)

    def test_plugin_settings(self):
        """
        Simulate a user going through the list of plugins in the plugin settings page of the config tool.

        This test builds a dictionary value based on a traversal of the QTreeWidget that contains the plugins displayed
        in the GUI. The dictionary is then used to assert that plugins exist in the appropriate categories. This test
        also uses a map to relate the GUI's category names to the backend's category names since the two differ.
        """
        item = self.config_tool.mainWidget.optionsTreeWidget.findItems(self.config_tool.pluginsString,
                                                                       QtCore.Qt.MatchExactly)
        self.assertFalse(not item or item[0] is None)
        self.config_tool.mainWidget.optionsTreeWidget.setCurrentItem(item[0])
        QtTest.QTest.mouseClick(self.config_tool.mainWidget.optionsTreeWidget, Qt.Qt.LeftButton)
        self.assertEqual(self.config_tool.currentWidget, self.config_tool.pluginWidget)

        # GUI names categories are different than the backend. Define a translation from GUI -> backend
        gui_category_to_backend_category = {
            'Audio Input': 'AudioInput',
            'Audio Mixer': 'AudioMixer',
            'Video Input': 'VideoInput',
            'Video Mixer': 'VideoMixer',
            'Output': 'Output',
            'Input': 'Importer'
        }
        QtTest.QTest.keyClick(self.config_tool.pluginWidget.list, QtCore.Qt.Key_PageUp)
        root = self.config_tool.pluginWidget.list.invisibleRootItem()
        plugin_category = {}  # A dictionary of plugin -> category
        for category_index in range(root.childCount()):
            category = str(self.config_tool.pluginWidget.list.currentItem().text(0))
            QtTest.QTest.keyClick(self.config_tool.pluginWidget.list, QtCore.Qt.Key_Down)
            for plugin_index in range(root.child(category_index).childCount()):
                plugin_name = str(self.config_tool.pluginWidget.list.currentItem().text(0))
                plugin_category[plugin_name] = gui_category_to_backend_category[category]
                QtTest.QTest.keyClick(self.config_tool.pluginWidget.list, QtCore.Qt.Key_Down)

        # Assert expected categories exist.
        self.assertIn('AudioInput', list(plugin_category.values()))
        self.assertIn('AudioMixer', list(plugin_category.values()))
        self.assertIn('VideoInput', list(plugin_category.values()))
        self.assertIn('VideoMixer', list(plugin_category.values()))
        self.assertIn('Output', list(plugin_category.values()))
        self.assertIn('Importer', list(plugin_category.values()))

        for category in ['AudioInput', 'AudioMixer', 'VideoInput', 'VideoMixer', 'Output', 'Importer']:
            for plugin in self.config_tool.get_plugins(category):
                self.assertIn(plugin.plugin_object.name, plugin_category)
                self.assertEqual(plugin_category[plugin.plugin_object.name], category)
                self.assertEqual(category, plugin.plugin_object.CATEGORY)

    def test_logger_settings(self):
        """
        Tests for config tool's Logger tab

        Needs to be tested differently since the
        Config instance isn't affected by changes in this tab.
        """

        # TODO
        pass

    def test_close_configtool(self):
        """
        Tests for config tool's close button
        """

        self.assertTrue(self.config_tool.mainWidget.isVisible())
        QtTest.QTest.mouseClick(self.config_tool.mainWidget.closePushButton, Qt.Qt.LeftButton)
        self.assertFalse(self.config_tool.mainWidget.isVisible())

    def test_file_menu_quit(self):
        """
        Tests for config tool's File->Quit
        """

        self.assertTrue(self.config_tool.isVisible())

        # File->Quit
        self.config_tool.actionExit.trigger()
        self.assertFalse(self.config_tool.isVisible())

    def test_help_menu_about(self):
        """
        Tests for config tool's Help->About
        """

        self.assertTrue(self.config_tool.isVisible())

        # Help->About
        self.config_tool.actionAbout.trigger()
        self.assertFalse(self.config_tool.hasFocus())
        self.assertTrue(self.config_tool.aboutDialog.isVisible())

        # Click "Close"
        QtTest.QTest.mouseClick(self.config_tool.aboutDialog.closeButton, Qt.Qt.LeftButton)
        self.assertFalse(self.config_tool.aboutDialog.isVisible())
