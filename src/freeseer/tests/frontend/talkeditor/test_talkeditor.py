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

from PyQt4 import Qt
from PyQt4 import QtGui
from PyQt4 import QtTest

from freeseer.framework.config.profile import ProfileManager
from freeseer.frontend.talkeditor.talkeditor import TalkEditorApp
from freeseer import settings


class TestTalkEditorApp(unittest.TestCase):
    '''
    Test suite to verify the functionality of the TalkEditorApp class.

    Tests interact like an end user (using QtTest). Expect the app to be rendered.

    '''

    def setUp(self):
        '''
        Stardard init method: runs before each test_* method

        Initializes a QtGui.QApplication and TalkEditorApp object.
        TalkEditorApp.show() causes the UI to be rendered.
        '''
        self.profile_manager = ProfileManager(tempfile.mkdtemp())
        profile = self.profile_manager.get('testing')
        config = profile.get_config('freeseer.conf', settings.FreeseerConfig,
                                    storage_args=['Global'], read_only=True)
        db = profile.get_database()

        self.app = QtGui.QApplication([])
        self.talk_editor = TalkEditorApp(config, db)
        self.talk_editor.show()

    def tearDown(self):
        '''
        Standard tear down method. Runs after each test_* method.

        This method closes the TalkEditorApp by clicking the "close" button
        '''
        shutil.rmtree(self.profile_manager._base_folder)

        QtTest.QTest.mouseClick(self.talk_editor.editorWidget.closeButton, Qt.Qt.LeftButton)
        del self.app
        del self.talk_editor.app

    def test_add_talk(self):
        '''
        Tests a user creating a talk and adding it.
        '''

        QtTest.QTest.mouseClick(self.talk_editor.editorWidget.addButton, Qt.Qt.LeftButton)
        self.assertFalse(self.talk_editor.editorWidget.isVisible())
        self.assertTrue(self.talk_editor.addTalkWidget.isVisible())

        mTitle = "This is a test"
        mPresenter = "Me, myself, and I"
        mEvent = "0 THIS St."
        mRoom = "Room 13"

        # populate talk data (date and time are prepopulated)
        self.talk_editor.addTalkWidget.titleLineEdit.setText(mTitle)
        self.talk_editor.addTalkWidget.presenterLineEdit.setText(mPresenter)
        self.talk_editor.addTalkWidget.eventLineEdit.setText(mEvent)
        self.talk_editor.addTalkWidget.roomLineEdit.setText(mRoom)

        # add in the talk
        QtTest.QTest.mouseClick(self.talk_editor.addTalkWidget.addButton, Qt.Qt.LeftButton)

        # find our talk (ensure it was added)
        found = False
        row_count = self.talk_editor.editorWidget.editor.model().rowCount() - 1
        while row_count >= 0 and not found:  # should be at the end, but you never know
            if self.talk_editor.editorWidget.editor.model().index(row_count, 1).data() == mTitle and \
                    self.talk_editor.editorWidget.editor.model().index(row_count, 2).data() == mPresenter and \
                    self.talk_editor.editorWidget.editor.model().index(row_count, 5).data() == mEvent and \
                    self.talk_editor.editorWidget.editor.model().index(row_count, 6).data() == mRoom:
                    found = True
                    # TODO: Select this row
            row_count -= 1

        self.assertTrue(found, "Couldn't find talk just inserted...")

        # now delete the talk we just created
        QtTest.QTest.mouseClick(self.talk_editor.editorWidget.removeButton, Qt.Qt.LeftButton)

    def test_add_talk_cancel(self):
        '''
        Tests a user creating a talk, but cancelling it instead of adding it.
        '''

        QtTest.QTest.mouseClick(self.talk_editor.editorWidget.addButton, Qt.Qt.LeftButton)
        self.assertFalse(self.talk_editor.editorWidget.isVisible())
        self.assertTrue(self.talk_editor.addTalkWidget.isVisible())

        QtTest.QTest.mouseClick(self.talk_editor.addTalkWidget.cancelButton, Qt.Qt.LeftButton)
        self.assertFalse(self.talk_editor.addTalkWidget.isVisible())
        self.assertTrue(self.talk_editor.editorWidget.isVisible())

    def test_close_talkeditor(self):
        '''
        Tests the "close" button.
        Although we close the app using this button after every test (in tearDown()),
        we are not guaranteed a valid test case in tearDown().
        '''

        QtTest.QTest.mouseClick(self.talk_editor.editorWidget.closeButton, Qt.Qt.LeftButton)
        self.assertFalse(self.talk_editor.editorWidget.isVisible())

    def test_clear_all_talks(self):
        '''
        Tests the "clear" button on the main window.
        '''

        if self.talk_editor.editorWidget.editor.model().rowCount() == 0:
            QtTest.QTest.mouseClick(self.talk_editor.editorWidget.addButton, Qt.Qt.LeftButton)
            mTitle = "This is a test"
            mPresenter = "Me, myself, and I"
            mEvent = "0 THIS St."
            mRoom = "Room 13"
            # populate talk data
            self.talk_editor.addTalkWidget.titleLineEdit.setText(mTitle)
            self.talk_editor.addTalkWidget.presenterLineEdit.setText(mPresenter)
            self.talk_editor.addTalkWidget.eventLineEdit.setText(mEvent)
            self.talk_editor.addTalkWidget.roomLineEdit.setText(mRoom)

            # date and time are prepopulated

            # add in the talk
            QtTest.QTest.mouseClick(self.talk_editor.addTalkWidget.addButton, Qt.Qt.LeftButton)

        # we need at least 1 talk
        self.assertTrue(self.talk_editor.editorWidget.editor.model().rowCount() > 0)

        # TODO: ROADBLOCK
        # Clicking "clear" causes a pop-up confirmation box to appear.
        # However, there is no link to this popup from inside the talk_editor

        # hit the clear button, hit no. No changes
        #QtTest.QTest.mouseClick(self.talk_editor.editorWidget.clearButton, Qt.Qt.LeftButton)
        # TODO: get the pop-up box's focus and click the button

        # hit the clear button, hit yes. Empty DB
        #QtTest.QTest.mouseClick(self.talk_editor.editorWidget.clearButton, Qt.Qt.LeftButton)
        # TODO: get the pop-up box's focus and click the button

    def test_file_menu_quit(self):
        '''
        Tests TalkEditorApp's File->Quit
        '''

        self.assertTrue(self.talk_editor.isVisible())

        # File->Quit
        self.talk_editor.actionExit.trigger()
        self.assertFalse(self.talk_editor.isVisible())

    def test_help_menu_about(self):
        '''
        Tests TalkEditorApp's Help->About
        '''

        self.assertTrue(self.talk_editor.isVisible())

        # Help->About
        self.talk_editor.actionAbout.trigger()
        self.assertFalse(self.talk_editor.hasFocus())
        self.assertTrue(self.talk_editor.aboutDialog.isVisible())

        # Click "Close"
        QtTest.QTest.mouseClick(self.talk_editor.aboutDialog.closeButton, Qt.Qt.LeftButton)
        self.assertFalse(self.talk_editor.aboutDialog.isVisible())
