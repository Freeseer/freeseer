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

import os
import sys
import time
import alsaaudio
import audioop

from PyQt4 import QtGui, QtCore

from freeseer_core import *
from freeseer_ui_qt import *
from freeseer_about import *

__version__=u'2.0'

NAME=u'Freeseer'
DESCRIPTION=u'Freeseer is a video capture utility capable of capturing presentation. It captures vga output and audio and mixes them together to produce a video.'
URL=u'http://www.fosslc.org'
COPYRIGHT=u'Copyright (C) 2010 The Free and Open Source Software Learning Centre'
LICENSE_TEXT=u"This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software."

ABOUT_INFO = u'<h1>'+NAME+u'</h1>' + \
u'<br><b>Version: ' + __version__ + u'</b>' + \
u'<p>' + DESCRIPTION + u'</p>' + \
u'<p>' + COPYRIGHT + u'</p>' + \
u'<p><a href="'+URL+u'">' + URL + u'</a></p>' \
u'<p>' + LICENSE_TEXT + u'</p>'


class AboutDialog(QtGui.QDialog):
    '''
    About dialog class for displaying app information.
    '''
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_FreeseerAbout()
        self.ui.setupUi(self)
        self.ui.aboutInfo.setText(ABOUT_INFO)


class MainApp(QtGui.QMainWindow):
    '''
    Freeseer main gui class
    '''
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_FreeseerMainWindow()
        self.ui.setupUi(self)
        self.ui.hardwareBox.hide()
        self.statusBar().showMessage('ready')
        self.aboutDialog = AboutDialog()

        self.core = FreeseerCore()

        # get supported devices and sources
        viddevs = self.core.get_video_devices('all')
        vidsrcs = self.core.get_video_sources()
        sndsrcs = self.core.get_audio_sources()

        self.videosrc = vidsrcs[0]

        # add available video devices
        for dev in viddevs:
            self.ui.videoDeviceList.addItem(dev)

        # add available video sources
        #for src in vidsrcs:
        #    self.ui.videoSourceList.addItem(src)

        # add available audio sources
        for src in sndsrcs:
            self.ui.audioSourceList.addItem(src)

        # add available talk titles
        self.load_talks()

        # systray
        logo = QtGui.QPixmap('logo.png')
        sysIcon = QtGui.QIcon(logo)
        self.systray = QtGui.QSystemTrayIcon(sysIcon)
        self.systray.show()

        # connections
        self.connect(self.ui.recordButton, QtCore.SIGNAL('toggled(bool)'), self.capture)
        self.connect(self.ui.videoDeviceList, QtCore.SIGNAL('activated(int)'), self.change_video_device)
        #self.connect(self.ui.videoSourceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_video_device)
        self.connect(self.ui.audioSourceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_audio_device)
        self.connect(self.ui.addTalkButton, QtCore.SIGNAL('clicked()'), self.add_talk)
        self.connect(self.ui.removeTalkButton, QtCore.SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.ui.saveButton, QtCore.SIGNAL('clicked()'), self.save_talks)
        self.connect(self.ui.resetButton, QtCore.SIGNAL('clicked()'), self.load_talks)
        self.connect(self.ui.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        self.connect(self.ui.audioFeedbackCheckbox, QtCore.SIGNAL('stateChanged(int)'), self.toggle_audio_feedback)
        self.connect(self.systray, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self._icon_activated)

        # connections for video source radio buttons
        self.connect(self.ui.localDesktopButton, QtCore.SIGNAL('clicked()'), self._toggled_video_source)
        self.connect(self.ui.hardwareButton, QtCore.SIGNAL('clicked()'), self._toggled_video_source)
        self.connect(self.ui.v4l2srcButton, QtCore.SIGNAL('clicked()'), self._toggled_video_source)
        self.connect(self.ui.v4lsrcButton, QtCore.SIGNAL('clicked()'), self._toggled_video_source)
        self.connect(self.ui.dv1394srcButton, QtCore.SIGNAL('clicked()'), self._toggled_video_source)

        self.ui.audioFeedbackSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.audioFeedbackSlider.setRange(1, 32768)
        self.volcheck = volcheck(self)
        self.volcheck.start()

        self.core.preview(True, self.ui.previewWidget.winId())

        # default to v4l2src with /dev/video0
        self.core.change_videosrc('v4l2src', '/dev/video0')
        self.core.change_soundsrc(str(self.ui.audioSourceList.currentText()))

    def _toggled_video_source(self):
        # recording the local desktop
        if (self.ui.localDesktopButton.isChecked()): self.videosrc = 'ximagesrc'
        # recording from hardware such as usb or fireware device
        elif (self.ui.hardwareButton.isChecked()):
            if (self.ui.v4l2srcButton.isChecked()): self.videosrc = 'v4l2src'
            elif (self.ui.v4lsrcButton.isChecked()): self.videosrc = 'v4lsrc'
            elif (self.ui.dv1394srcButton.isChecked()): self.videosrc = 'dv1394src'
            else: return
        else: return
        videodev = str(self.ui.videoDeviceList.currentText())
        
        viddevs = self.core.get_video_devices(self.videosrc)
        print viddevs
        # add available video devices
        self.ui.videoDeviceList.clear()
        for dev in viddevs:
            self.ui.videoDeviceList.addItem(dev)
            
        self.core.change_videosrc(self.videosrc, videodev)

    def change_video_device(self):
        '''
        Function for changing video device
        eg. /dev/video1
        '''
        print 'changing video device'
        dev = str(self.ui.videoDeviceList.currentText())
        src = self.videosrc
        self.core.change_videosrc(src, dev)

    def change_audio_device(self):
        print 'changing video device'
        src = str(self.ui.audioSourceList.currentText())
        self.core.change_soundsrc(src)

    def toggle_audio_feedback(self):
        if (self.ui.audioFeedbackCheckbox.isChecked()):
            self.core.audioFeedback(True)
            return
        self.core.audioFeedback(False)

    def capture(self):
        '''
        Function for recording and stopping recording.
        '''
        if not (self.ui.recordButton.isChecked()):
            self.core.stop()
            self.ui.recordButton.setText('Record')
            self.ui.videoConfigBox.setEnabled(True)
            self.ui.soundConfigBox.setEnabled(True)
            self.ui.audioFeedbackCheckbox.setEnabled(True)
            self.statusBar().showMessage('ready')
            return
        self.core.record(self.ui.talkList.currentText())
        self.ui.recordButton.setText('Stop')
        self.ui.videoConfigBox.setEnabled(False)
        self.ui.soundConfigBox.setEnabled(False)
        self.ui.audioFeedbackCheckbox.setEnabled(False)
        self.statusBar().showMessage('recording...')

    def add_talk(self):
        talk = ""
        if (self.ui.roomEdit.isEnabled()): talk += self.ui.roomEdit.text() + " - "
        if (self.ui.presenterEdit.isEnabled()): talk += self.ui.presenterEdit.text() + " - "
        talk += self.ui.titleEdit.text()
        self.ui.editTalkList.addItem(talk)

        #clean up add title boxes
        self.ui.roomEdit.clear()
        self.ui.presenterEdit.clear()
        self.ui.titleEdit.clear()

    def remove_talk(self):
        self.ui.editTalkList.takeItem(self.ui.editTalkList.currentRow())

    def load_talks(self):
        talklist = self.core.get_talk_titles()
        self.ui.talkList.clear()
        self.ui.editTalkList.clear()
        for talk in talklist:
            self.ui.talkList.addItem(talk)
            self.ui.editTalkList.addItem(talk)

    def save_talks(self):
        talk_list = []
        i = 0
        while i < self.ui.editTalkList.count():
            t = self.ui.editTalkList.item(i).text() + '\n'
            talk_list.append(t)
            i = i+1

        self.core.save_talk_titles(talk_list)
        self.load_talks()

    def _icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.show()
            else: self.hide()

    def closeEvent(self, event):
        print 'Exiting freeseer...'
        self.volcheck.run = False
        self.core.stop()
        event.accept()

class volcheck(QtCore.QThread):
    '''
    Threaded class for getting mic volume information and returning the current input from mic.
    '''
    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent

    def run(self):
        self.run = True
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
        inp.setchannels(2)
        inp.setrate(8000)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

        inp.setperiodsize(160)

        while self.run:
            l,data = inp.read()
            if l:
                #print audioop.max(data, 2)
                self.parent.ui.audioFeedbackSlider.setValue(audioop.max(data, 2))
                time.sleep(.02)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())
