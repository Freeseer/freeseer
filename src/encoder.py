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


import sys
from PyQt4 import QtGui, QtCore

CONFIG = dict()
CMD_FFMPEG = ("ffmpeg -i \"%(FILENAME)s.avi\" -async 3 -acodec libvorbis \"%(FILENAME)s.ogg\"")

class MainApp(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.ffmpeg = QtCore.QProcess()
        
        # layout
        layout = QtGui.QVBoxLayout()
        
        self.encode = QtGui.QPushButton("Encode")
        self.encode.setCheckable(True)
        layout.addWidget(self.encode)
        
        self.list = QtGui.QListWidget()
        layout.addWidget(self.list)
        
        self.setLayout(layout)
        
        # connectors
        self.connect(self.encode, QtCore.SIGNAL('toggled(bool)'), self.Encode)
        self.connect(self.ffmpeg, QtCore.SIGNAL('readyReadStandardOutput()'), self.ffmpegReadOutput)
        self.connect(self.ffmpeg, QtCore.SIGNAL('finished(int)'), self.EncodeFin)
        
        # Add values
        dir = QtCore.QDir()
        dir.setFilter(QtCore.QDir.Files)
        list = dir.entryList()
        while (not list.isEmpty()):
            self.list.addItem(list.takeFirst())        

    def ffmpegReadOutput(self):
        print QtCore.QString(self.ffmpeg.readAllStandardOutput())
            
    def Encode(self):
        if not (self.encode.isChecked()):
            self.stopEncoding()
            return

        self.startEncoding()
    
    def startEncoding(self):
        CONFIG['FILENAME'] = self.list.currentItem().text().remove(".avi")
        self.ffmpeg.start(CMD_FFMPEG % CONFIG)
        self.encode.setText('Stop')
        print 'Started encoding'
    
    def stopEncoding(self):
        self.ffmpeg.close()
        self.encode.setText('Encode')
        print 'Stopped encoding'        

    def EncodeFin(self):
        print 'Encoding completed'
        self.encode.setChecked(False)

#######################
# Program starts here #
#######################
app = QtGui.QApplication(sys.argv)

widget = MainApp()
widget.show()
widget.resize(480, 320)

sys.exit(app.exec_())
