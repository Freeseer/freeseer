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

NAME = "freeseer"
VERSION = "2009.11"

import sys, time, alsaaudio, audioop
from PyQt4 import QtGui, QtCore

CONFIG = dict()

# Commandline processes
CMD_MPLAYER = ("mplayer -slave -quiet -noconsolecontrols -nomouseinput -wid %(WID)s -tv driver=%(VODRIVER)s:outfmt=rgb24:device=%(VODEVICE)s -fps 10 tv://")
CMD_MENCODER = ("mencoder -tv driver=%(VODRIVER)s:outfmt=bgr24:device=%(VODEVICE)s:forceaudio:alsa -fps 10 tv:// -oac lavc -ovc lavc -lavcopts vcodec=mpeg4:keyint=100:vbitrate=8000:vhq:acodec=vorbis -o \"%(FILENAME)s\"")

# Initialize some defaults
CONFIG['FILENAME'] = 'default'
CONFIG['FILE_INDEX'] = 0
CONFIG['VODEVICE'] = '/dev/video0'
CONFIG['VODRIVER'] = 'v4l'

# Find video devices
viddevs=0
dev='/dev/video' + str(viddevs)
while QtCore.QFile.exists(dev):
    print 'Video device ' + str(viddevs) + ' found.'
    viddevs=viddevs+1
    dev='/dev/video'+str(viddevs)
print 'Found ' + str(viddevs) + ' video devices.'
 
########################################
#
# Widget to hold mplayer instance in
#
########################################
class MPlayerWidget(QtGui.QWidget):
       
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        CONFIG["WID"] = self.winId()
        self.mplayer = QtCore.QProcess()
        self.mplayer.start(CMD_MPLAYER % CONFIG)
        self.connect(self.mplayer, QtCore.SIGNAL('readyReadStandardOutput()'), self.mpStdOut)
    
    def __del__(self):
        self.mplayer.close()
    
    def mpstart(self):
        self.mplayer.start(CMD_MPLAYER % CONFIG)

    def mpStdOut(self):
        print QtCore.QString(self.mplayer.readAllStandardOutput())

class volcheck(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent

    def run(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
        inp.setchannels(1)
        inp.setrate(8000)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        
        inp.setperiodsize(160)
        
        while True:
            l,data = inp.read()
            if l:
                #print audioop.max(data, 2)
                self.parent.volume.setValue(audioop.max(data, 2))
            time.sleep(.001)

class EditTalks(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # Layout
        layout = QtGui.QHBoxLayout()
        
        leftside = QtGui.QVBoxLayout()
        self.editBox = QtGui.QLineEdit()
        leftside.addWidget(self.editBox)
        
        self.talkList = QtGui.QListWidget()
        leftside.addWidget(self.talkList)
        
        rightside = QtGui.QVBoxLayout()
        self.addTalkButton = QtGui.QPushButton('add')
        rightside.addWidget(self.addTalkButton)
        self.delTalkButton = QtGui.QPushButton('remove')
        rightside.addWidget(self.delTalkButton)
        self.savTalkButton = QtGui.QPushButton('save')
        rightside.addWidget(self.savTalkButton)
        
        layout.addLayout(leftside)
        layout.addLayout(rightside)
        self.setLayout(layout)
        # End Layout
        
        # Connections
        self.connect(self.addTalkButton, QtCore.SIGNAL('clicked()'), self.addTalk)
        self.connect(self.delTalkButton, QtCore.SIGNAL('clicked()'), self.delTalk)
        self.connect(self.savTalkButton, QtCore.SIGNAL('clicked()'), self.saveTalks)
        
        # Add talks
        file = QtCore.QFile('/home/zxiiro/workspace/Kapture/src/talks.txt')
        file.open(QtCore.QIODevice.ReadOnly)
        
        txtStream = QtCore.QTextStream(file)
        while not txtStream.atEnd():
            text = txtStream.readLine()
            self.talkList.addItem(text)
        file.close()
    
    def addTalk(self):
        self.talkList.addItem(self.editBox.text())
    
    def delTalk(self):
        self.talkList.takeItem(self.talkList.currentRow())
        
    def saveTalks(self):
        file = QtCore.QFile('/home/zxiiro/workspace/Kapture/src/talks.txt')
        file.open(QtCore.QIODevice.WriteOnly)
        
        txtStream = QtCore.QTextStream(file)
        i = 0
        while i < self.talkList.count():
            txtStream << self.talkList.item(i).text() << '\n' 
            i = i+1
            
        txtStream.flush()
        file.flush()
        file.close()

class MainApp(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        ##############################
        # Variable Initialization
        ##############################
        self.mencoder = QtCore.QProcess()

        #############################
        # Begin Layout
        #############################
        layout = QtGui.QVBoxLayout()
        previewbox = QtGui.QHBoxLayout()

        self.record = QtGui.QPushButton("Record")
        self.record.setCheckable(True)
        layout.addWidget(self.record)
        
        videoLabel = QtGui.QLabel('Device:')
        videoLabel.setMaximumWidth(50)
        self.videoDevices = QtGui.QComboBox()
        i = 0
        while i < viddevs:
            self.videoDevices.addItem('/dev/video' + str(i))
            i=i+1
        self.videoDrivers = QtGui.QComboBox()
        self.videoDrivers.addItem('v4l')
        self.videoDrivers.addItem('v4l2')
        viddevLayout = QtGui.QHBoxLayout()
        viddevLayout.addWidget(videoLabel)
        viddevLayout.addWidget(self.videoDevices)
        viddevLayout.addWidget(self.videoDrivers)
        layout.addLayout(viddevLayout)
        
        talkLabel = QtGui.QLabel('Title:')
        talkLabel.setMaximumWidth(50)
        self.talk = QtGui.QComboBox()
        self.talk.addItem('Foo Bar - Test Presentation')
        self.talkEditButton = QtGui.QPushButton("Edit")
        self.talkEditButton.setMaximumWidth(50)
        talkLayout = QtGui.QHBoxLayout()
        talkLayout.addWidget(talkLabel)
        talkLayout.addWidget(self.talk)
        talkLayout.addWidget(self.talkEditButton)
        layout.addLayout(talkLayout)

        self.mplayer = MPlayerWidget(self)
        previewbox.addWidget(self.mplayer)
        self.mplayerp = self.mplayer.mplayer

        self.volume = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.volume.setFocusPolicy(QtCore.Qt.NoFocus)
        self.volume.setRange(1, 32768)
        previewbox.addWidget(self.volume)

        layout.addLayout(previewbox)

        self.logger = QtGui.QTextBrowser(self)
        self.logger.setMaximumHeight(30)
        layout.addWidget(self.logger)

        self.setLayout(layout)
        ##############################
        # End layout
        ##############################

        # Connections
        self.connect(self.record, QtCore.SIGNAL('toggled(bool)'), self.Capture)
        self.connect(self.mencoder, QtCore.SIGNAL('readyReadStandardOutput()'), self.mencoderReadOutput)
        self.connect(self.talkEditButton, QtCore.SIGNAL('clicked()'), self.editTalks)
        self.connect(self.videoDevices, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeVideoDevice)
        self.connect(self.videoDrivers, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeVideoDevice)

        self.volcheck = volcheck(self)
        self.volcheck.start()
        
        # Add talks
        file = QtCore.QFile('/home/zxiiro/workspace/Kapture/src/talks.txt')
        file.open(QtCore.QIODevice.ReadOnly)
        
        txtStream = QtCore.QTextStream(file)
        while not txtStream.atEnd():
            text = txtStream.readLine()
            self.talk.addItem(text)
        file.close()

    def changeVideoDevice(self):
        print 'Changing video devices'
        self.mplayerp.close()
        CONFIG['VODEVICE'] = self.videoDevices.currentText()
        CONFIG['VODRIVER'] = self.videoDrivers.currentText()
        self.mplayer.mpstart()

    def closeEvent(self, event):
        print 'Exiting freeseer...'
        self.mplayer.mplayer.close()
        event.accept()

    def mencoderReadOutput(self):
        self.logger.setText(QtCore.QString(self.mencoder.readAllStandardOutput()))
        
    def editTalks(self):
        self.talkEdit = EditTalks()
        self.talkEdit.show()
        self.talkEdit.resize(480, 320)

    # Code for starting MEncoder
    def Capture(self):
        #print self.mencoder.state()
        if not (self.record.isChecked()):
            self.stopCapture()
            return
        
        self.checkFileExists()
        
        if self.videoDrivers.currentText() == 'v4l2':
            self.mplayerp.close()
            
        self.startCapture()

    # checks if a filename exists or not and increments index until it finds
    # at filename that is not taken
    def checkFileExists(self):
        i = 0
        while True:
            CONFIG['FILENAME'] = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate) + " " + self.talk.currentText() + " (" + str(i) + ").avi"
            rfile = QtCore.QFileInfo(CONFIG['FILENAME'])

            if (rfile.exists()):
                i += 1
                print "File Exists.  Incrementing index to " + str(i)
            else:
                break

    def startCapture(self):
        self.mencoder.start(CMD_MENCODER % CONFIG)
        self.record.setText('Stop')
        print 'Started capture'
        
    def stopCapture(self):
        self.mencoder.close()
        self.record.setText('Record')
        print 'Stopping capture'
                



#######################
# Program starts here #
#######################
app = QtGui.QApplication(sys.argv)

widget = MainApp()
widget.show()
widget.resize(480, 320)

sys.exit(app.exec_())

