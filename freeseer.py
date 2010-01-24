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
VERSION = "2010.01"

import os, sys, time, alsaaudio, audioop
import gobject, pygst
pygst.require("0.10")
import gst
from PyQt4 import QtGui, QtCore

CONFIG = dict()

# Commandline processes
CMD_GSTLAUNCH = ("%(VODRIVER)s name=videosrc device=%(VODEVICE)s ! tee name=vid ! queue ! autovideosink sync=false vid. ! theoraenc ! queue ! mux. alsasrc ! queue ! audioconvert ! queue ! vorbisenc ! queue ! mux. matroskamux name=mux ! filesink name=filesink location=\"%(FILENAME)s\"")

# Initialize some defaults
PWD = os.getcwd()
TALKSFILE = sys.path[0] + '/talks.txt'
CONFIG['FILENAME'] = 'default.mkv'
CONFIG['FILE_INDEX'] = 0
CONFIG['VODEVICE'] = '/dev/video0'
CONFIG['VODRIVER'] = 'v4lsrc'

# Find video devices
viddevs=0
dev='/dev/video' + str(viddevs)
while QtCore.QFile.exists(dev):
    print 'Video device ' + str(viddevs) + ' found.'
    viddevs=viddevs+1
    dev='/dev/video'+str(viddevs)
print 'Found ' + str(viddevs) + ' video devices.'
 
###########################################
#
# Widget to hold GST Player window instance
#
###########################################
class GSTPlayerWidget(QtGui.QWidget):
       
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.player = gst.parse_launch(CMD_GSTLAUNCH % CONFIG)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(self.winId())

    def change_videosrc(self):    
        oldsrc = self.player.get_by_name("videosrc")
        self.player.remove(oldsrc)
        newsrc = gst.element_factory_make(str(CONFIG['VODRIVER']), "videosrc")
        newsrc.set_property("device", CONFIG['VODEVICE'])
        self.player.add(newsrc)
        vidtee = self.player.get_by_name("vid")
        gst.element_link_many(newsrc, vidtee)

    def record(self):
        filesink = self.player.get_by_name("filesink")
        filesink.set_property("location", CONFIG['FILENAME'])
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.player.set_state(gst.STATE_NULL)

class volcheck(QtCore.QThread):
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
        file = QtCore.QFile(TALKSFILE)
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
        file = QtCore.QFile(TALKSFILE)
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

        #############################
        # Begin Layout
        #############################
        layout = QtGui.QVBoxLayout()
        playerbox = QtGui.QHBoxLayout()

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
        self.videoDrivers.addItem('v4lsrc')
        self.videoDrivers.addItem('v4l2src')
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

        self.playerWidget = GSTPlayerWidget(self)
        playerbox.addWidget(self.playerWidget)

        self.volume = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.volume.setFocusPolicy(QtCore.Qt.NoFocus)
        self.volume.setRange(1, 32768)
        playerbox.addWidget(self.volume)

        layout.addLayout(playerbox)

        self.logger = QtGui.QTextBrowser(self)
        self.logger.setMaximumHeight(30)
        layout.addWidget(self.logger)

        self.setLayout(layout)
        ##############################
        # End layout
        ##############################

        # Connections
        self.connect(self.record, QtCore.SIGNAL('toggled(bool)'), self.Capture)
        self.connect(self.talkEditButton, QtCore.SIGNAL('clicked()'), self.editTalks)
        self.connect(self.videoDevices, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeVideoDevice)
        self.connect(self.videoDrivers, QtCore.SIGNAL('currentIndexChanged(int)'), self.changeVideoDevice)

        self.volcheck = volcheck(self)
        self.volcheck.start()
        
        # Add talks
        file = QtCore.QFile(TALKSFILE)
        file.open(QtCore.QIODevice.ReadOnly)
        
        txtStream = QtCore.QTextStream(file)
        while not txtStream.atEnd():
            text = txtStream.readLine()
            self.talk.addItem(text)
        file.close()

    def changeVideoDevice(self):
        print 'Changing video devices'
        self.playerWidget.stop()
        CONFIG['VODEVICE'] = self.videoDevices.currentText()
        CONFIG['VODRIVER'] = self.videoDrivers.currentText()
        self.playerWidget.change_videosrc()

    def closeEvent(self, event):
        print 'Exiting freeseer...'
        self.volcheck.run = False
        self.playerWidget.stop()
        event.accept()

    def editTalks(self):
        self.talkEdit = EditTalks()
        self.talkEdit.show()
        self.talkEdit.resize(480, 320)

    # Check capture status, sets filename, and begin capture.
    def Capture(self):

        if not (self.record.isChecked()):
            self.stopCapture()
            return
        
        self.checkFileExists()
        self.startCapture()

    # checks if a filename exists or not and increments index until it finds
    # at filename that is not taken
    def checkFileExists(self):
        i = 0
        while True:
            CONFIG['FILENAME'] = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate) + " " + self.talk.currentText() + " (" + str(i) + ").mkv"
            rfile = QtCore.QFileInfo(CONFIG['FILENAME'])

            if (rfile.exists()):
                i += 1
                print "File Exists.  Incrementing index to " + str(i)
            else:
                break

    def startCapture(self):
        self.playerWidget.record()
        self.record.setText('Stop')
        self.videoDevices.setEnabled(False)
        self.videoDrivers.setEnabled(False)
        self.talk.setEnabled(False)
        print 'Started capture'
        
    def stopCapture(self):
        self.record.setText('Record')
        self.playerWidget.stop()
        self.videoDevices.setEnabled(True)
        self.videoDrivers.setEnabled(True)
        self.talk.setEnabled(True)
        print 'Stopped capture'
                


#######################
# Program starts here #
#######################
gobject.threads_init()
app = QtGui.QApplication(sys.argv)

widget = MainApp()
widget.show()
widget.resize(480, 320)

sys.exit(app.exec_())

