#!/usr/bin/python

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2010  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# the #fosslc channel on IRC (freenode.net)

from freeseer_core import *
from freeseer_ui_qt import *
import os, sys, time, alsaaudio, audioop
from PyQt4 import QtGui, QtCore

class MainApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_FreeseerMainWindow()
        self.ui.setupUi(self)
        self.statusBar().showMessage('ready')

        self.core = FreeseerCore()

        # get supported devices and sources
        viddevs = self.core.get_video_devices()
        vidsrcs = self.core.get_video_sources()
        sndsrcs = self.core.get_audio_sources()

        # add available video devices
        for dev in viddevs:
            self.ui.videoDeviceList.addItem(dev)

        # add available video sources
        for src in vidsrcs:
            self.ui.videoSourceList.addItem(src)

        # add available audio sources
        for src in sndsrcs:
            self.ui.audioSourceList.addItem(src)

        # add available talk titles
        talklist = self.core.get_talk_titles()
        for talk in talklist:
            self.ui.talkList.addItem(talk)
            self.ui.editTalkList.addItem(talk)
        
        self.core.preview(True, self.ui.previewWidget.winId())

        self.core.change_videosrc('v4l2src', '/dev/video0')
        self.core.record('test.ogg')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())