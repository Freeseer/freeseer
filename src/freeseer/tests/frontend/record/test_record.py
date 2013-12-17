#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2012, 2013 Free and Open Source Software Learning Centre
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

import shutil
import tempfile
import unittest

import pep8

from PyQt4 import Qt
from PyQt4 import QtGui
from PyQt4 import QtTest

from freeseer.framework.config.profile import ProfileManager
from freeseer.frontend.record.record import RecordApp
from freeseer import settings

from freeseer.tests import pep8_options
from freeseer.tests import pep8_report


class TestRecordApp(unittest.TestCase):
    '''
    Test suite to verify the functionality of the RecordApp class.

    Tests interact like an end user (using QtTest). Expect the app to be rendered.

    '''

    def setUp(self):
        '''
        Stardard init method: runs before each test_* method

        Initializes a QtGui.QApplication and RecordApp object.
        RecordApp.show() causes the UI to be rendered.
        '''
        self.profile_manager = ProfileManager(tempfile.mkdtemp())
        profile = self.profile_manager.get('testing')
        config = profile.get_config('freeseer.conf', settings.FreeseerConfig, storage_args=['Global'], read_only=False)

        self.app = QtGui.QApplication([])
        self.record_app = RecordApp(profile, config)
        self.record_app.show()

    def tearDown(self):
        '''
        Generic unittest.TestCase.tearDown()
        '''
        shutil.rmtree(self.profile_manager._base_folder)

        self.record_app.actionExit.trigger()
        del self.app

    def test_init_conditions(self):
        '''
        Tests the initial state of the RecordApp
        '''
        # TODO
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
        # It turns out that even if the state is Multimedia.PAUSE, the preview has not quite loaded

#       self.assertTrue(self.record_app.mainWidget.standbyPushButton.isVisible(), "[PRE STANDBY] Expected Standby button to be visible")
#       self.assertFalse(self.record_app.mainWidget.recordPushButton.isVisible(), "[PRE STANDBY] Expected Record button to be invisible")

        # Click the Standby button with the left mouse button
#       QtTest.QTest.mouseClick(self.record_app.mainWidget.standbyPushButton, Qt.Qt.LeftButton)

#       self.assertFalse(self.record_app.mainWidget.standbyPushButton.isVisible(), "[STANDBY] Expected Standby button to be invisible")
#       self.assertTrue(self.record_app.mainWidget.recordPushButton.isVisible(), "[STANDBY] Expected Record button to be visible")

        # TODO: Check if preview has loaded

        # Click the Record button with the left mouse button
#       QtTest.QTest.mouseClick(self.record_app.mainWidget.recordPushButton, Qt.Qt.LeftButton)

#       self.assertFalse(self.record_app.mainWidget.standbyPushButton.isVisible(), "[RECORDING] Expected Standby button to be invisible")
#       self.assertTrue(self.record_app.mainWidget.recordPushButton.isVisible(), "[RECORDING] Expected Record button to be visible")
#       self.assertTrue(self.record_app.mainWidget.recordPushButton.text() == self.record_app.stopString, "[RECORDING] Incorrect button text for this phase")

        # Click the Record button again in 5 seconds with the left mouse button
#       QtTest.QTest.mouseClick(self.record_app.mainWidget.recordPushButton, Qt.Qt.LeftButton)

    def test_reset_timer(self):
        '''
        Tests RecordApp.reset_timer()
        '''

        # set our own values
        self.record_app.time_minutes = 15
        self.record_app.time_seconds = 30

        # reset timer and check that the values are 0
        self.record_app.reset_timer()
        self.assertTrue(self.record_app.time_minutes == 0 and self.record_app.time_seconds == 0)

    def test_file_menu_quit(self):
        '''
        Tests RecordApp's File->Quit
        '''

        self.assertTrue(self.record_app.isVisible())

        # File->Menu
        self.record_app.actionExit.trigger()
        self.assertFalse(self.record_app.isVisible())

    def test_help_menu_about(self):
        '''
        Tests RecordApp's Help->About
        '''

        self.assertTrue(self.record_app.isVisible())

        # Help->About
        self.record_app.actionAbout.trigger()
        self.assertFalse(self.record_app.hasFocus())
        self.assertTrue(self.record_app.aboutDialog.isVisible())

        # Click "Close"
        QtTest.QTest.mouseClick(self.record_app.aboutDialog.closeButton, Qt.Qt.LeftButton)
        self.assertFalse(self.record_app.aboutDialog.isVisible())

    def test_pep8(self):
        checker = pep8.StyleGuide(**pep8_options)
        report = checker.check_files(['freeseer/tests/frontend/record',
                                      'freeseer/frontend/record'])
        pep8_report(self, report)
