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

        # connections
        self.connect(self.ui.recordButton, QtCore.SIGNAL('toggled(bool)'), self.capture)
        self.connect(self.ui.videoDeviceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_video_device)
        self.connect(self.ui.videoSourceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_video_device)
        self.connect(self.ui.audioSourceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_audio_device)
        
        self.core.preview(True, self.ui.previewWidget.winId())

        # default to v4l2src with /dev/video0
        self.core.change_videosrc('v4l2src', '/dev/video0')

    def change_video_device(self):
        print 'changing video device'
        dev = str(self.ui.videoDeviceList.currentText())
        src = str(self.ui.videoSourceList.currentText())
        self.core.change_videosrc(src, dev)
        
    def change_audio_device(self):
        print 'changing video device'
        src = str(self.ui.audioSourceList.currentText())
        self.core.change_soundsrc(src)

    def capture(self):
        if not (self.ui.recordButton.isChecked()):
            self.core.stop()
            self.ui.recordButton.setText('Record')
            self.ui.videoDeviceList.setEnabled(True)
            self.ui.videoSourceList.setEnabled(True)
            self.ui.audioSourceList.setEnabled(True)
            return
        self.core.record(self.ui.talkList.currentText())
        self.ui.recordButton.setText('Stop')
        self.ui.videoDeviceList.setEnabled(False)
        self.ui.videoSourceList.setEnabled(False)
        self.ui.audioSourceList.setEnabled(False)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())