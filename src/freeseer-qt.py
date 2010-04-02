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

__version__=u'1.9.5'

NAME=u'Freeseer'
DESCRIPTION=u'Freeseer is a video capture utility capable of capturing presentation. It captures vga output and audio and mixes them together to produce a video.'
URL=u'http://www.fosslc.org'
COPYRIGHT=u'Copyright (C) 2010 The Free and Open Source Software Learning Centre'
LICENSE_TEXT=u"This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software."
RECORD_BUTTON_ARTIST=u'Sekkyumu'
RECORD_BUTTON_LINK=u'http://sekkyumu.deviantart.com/'
HEADPHONES_ARTIST=u'Ben Fleming'
HEADPHONES_LINK=u'http://mediadesign.deviantart.com/'

ABOUT_INFO = u'<h1>'+NAME+u'</h1>' + \
u'<br><b>Version: ' + __version__ + u'</b>' + \
u'<p>' + DESCRIPTION + u'</p>' + \
u'<p>' + COPYRIGHT + u'</p>' + \
u'<p><a href="'+URL+u'">' + URL + u'</a></p>' \
u'<p>' + LICENSE_TEXT + u'</p>' \
u'<p>Record button graphics by: <a href="' + RECORD_BUTTON_LINK+ u'">' + RECORD_BUTTON_ARTIST + u'</a></p>' \
u'<p>Headphones graphics by: <a href="' + HEADPHONES_LINK+ u'">' + HEADPHONES_ARTIST + u'</a></p>'


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

        # get available video sources
        vidsrcs = self.core.get_video_sources()
        self.videosrc = vidsrcs[0]

        # get available audio sources
        sndsrcs = self.core.get_audio_sources()
        for src in sndsrcs:
            self.ui.audioSourceList.addItem(src)

        # add available talk titles
        self.load_talks()

        # setup systray
        logo = QtGui.QPixmap('logo.png')
        sysIcon = QtGui.QIcon(logo)
        self.systray = QtGui.QSystemTrayIcon(sysIcon)
        self.systray.show()
        self.connect(self.systray, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self._icon_activated)

        # main tab connections
        self.connect(self.ui.recordButton, QtCore.SIGNAL('toggled(bool)'), self.capture)
        self.connect(self.ui.audioFeedbackCheckbox, QtCore.SIGNAL('stateChanged(int)'), self.toggle_audio_feedback)

        # configure tab connections
        self.connect(self.ui.videoDeviceList, QtCore.SIGNAL('activated(int)'), self.change_video_device)
        self.connect(self.ui.audioSourceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_audio_device)
        # connections for video source radio buttons
        self.connect(self.ui.localDesktopButton, QtCore.SIGNAL('clicked()'), self._toggled_video_source)
        self.connect(self.ui.hardwareButton, QtCore.SIGNAL('clicked()'), self._toggled_video_source)
        self.connect(self.ui.usbsrcButton, QtCore.SIGNAL('clicked()'), self._toggled_video_source)
        self.connect(self.ui.firewiresrcButton, QtCore.SIGNAL('clicked()'), self._toggled_video_source)

        # edit talks tab connections
        self.connect(self.ui.addTalkButton, QtCore.SIGNAL('clicked()'), self.add_talk)
        self.connect(self.ui.removeTalkButton, QtCore.SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.ui.saveButton, QtCore.SIGNAL('clicked()'), self.save_talks)
        self.connect(self.ui.resetButton, QtCore.SIGNAL('clicked()'), self.load_talks)

        # Main Window Connections
        self.connect(self.ui.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)

        # setup audio feedback slider
        self.ui.audioFeedbackSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.audioFeedbackSlider.setRange(1, 32768)
        self.volcheck = volcheck(self)
        self.volcheck.start()

        # setup video preview widget
        self.core.preview(True, self.ui.previewWidget.winId())

        # Setup default sources
        self._toggled_video_source()
        self.core.change_soundsrc(str(self.ui.audioSourceList.currentText()))

    def _toggled_video_source(self):
        '''
        Updates the GUI when the user selects a different video source and
        configures core with new video source information
        '''
        # recording the local desktop
        if (self.ui.localDesktopButton.isChecked()): self.videosrc = 'ximagesrc'

        # recording from hardware such as usb or fireware device
        elif (self.ui.hardwareButton.isChecked()):
            if (self.ui.usbsrcButton.isChecked()): self.videosrc = 'v4l2src'
            elif (self.ui.firewiresrcButton.isChecked()): self.videosrc = 'dv1394src'
            else: return

            # add available video devices for selected source
            viddevs = self.core.get_video_devices(self.videosrc)
            self.ui.videoDeviceList.clear()
            for dev in viddevs:
                self.ui.videoDeviceList.addItem(dev)

        # invalid selection (this should never happen)
        else: return

        # finally load the changes into core
        videodev = str(self.ui.videoDeviceList.currentText())
        self.core.change_videosrc(self.videosrc, videodev)

    def change_video_device(self):
        '''
        Function for changing video device
        eg. /dev/video1
        '''
        dev = str(self.ui.videoDeviceList.currentText())
        src = self.videosrc
        self.core.logger.debug('Changing video device to ' + dev)
        self.core.change_videosrc(src, dev)

    def change_audio_device(self):
        src = str(self.ui.audioSourceList.currentText())
        self.core.logger.debug('Changing audio device to ' + src)
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
        else:
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

        # Do not add talks if they are empty strings
        if (len(talk) == 0): return
        
        self.ui.editTalkList.addItem(talk)

        #clean up add title boxes
        self.ui.roomEdit.clear()
        self.ui.presenterEdit.clear()
        self.ui.titleEdit.clear()

    def remove_talk(self):
        self.ui.editTalkList.takeItem(self.ui.editTalkList.currentRow())

    def load_talks(self):
        '''
        This method updates the GUI with the available presentation titles.
        '''
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
        self.core.logger.info('Exiting freeseer...')
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
