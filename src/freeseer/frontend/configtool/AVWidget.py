#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

Copyright (C) 2011  Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/Freeseer/freeseer/

@author: Thanh Ha
'''

from PyQt4 import QtCore, QtGui

class AVWidget(QtGui.QWidget):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        #
        # Audio Input
        #
        
        self.audioLayout = QtGui.QGridLayout()
        self.audioGroupBox = QtGui.QGroupBox("Audio Input")
        self.audioGroupBox.setLayout(self.audioLayout)
        self.mainLayout.addWidget(self.audioGroupBox)
        
        self.audioGroupBox.setCheckable(True)
        self.audioGroupBox.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        
        self.audioMixerLabel = QtGui.QLabel("Audio Mixer")
        self.audioMixerLabel.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.audioMixerComboBox = QtGui.QComboBox()
        self.audioMixerLabel.setBuddy(self.audioMixerComboBox)
        self.audioMixerSetupPushButton = QtGui.QPushButton("Setup")
        self.audioMixerSetupPushButton.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.audioLayout.addWidget(self.audioMixerLabel, 0, 0)
        self.audioLayout.addWidget(self.audioMixerComboBox, 0, 1)
        self.audioLayout.addWidget(self.audioMixerSetupPushButton, 0, 2)
        
        #
        # Video Input
        #
        
        self.videoLayout = QtGui.QGridLayout()
        self.videoGroupBox = QtGui.QGroupBox("Video Input")
        self.videoGroupBox.setLayout(self.videoLayout)
        self.mainLayout.addWidget(self.videoGroupBox)
        
        self.videoGroupBox.setCheckable(True)
        self.videoGroupBox.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        
        self.videoMixerLabel = QtGui.QLabel("Video Mixer")
        self.videoMixerLabel.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.videoMixerComboBox = QtGui.QComboBox()
        self.videoMixerLabel.setBuddy(self.videoMixerComboBox)
        self.videoMixerSetupPushButton = QtGui.QPushButton("Setup")
        self.videoMixerSetupPushButton.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.videoLayout.addWidget(self.videoMixerLabel, 0, 0)
        self.videoLayout.addWidget(self.videoMixerComboBox, 0, 1)
        self.videoLayout.addWidget(self.videoMixerSetupPushButton, 0, 2)
        
        #
        # Record to File
        #
        
        self.fileLayout = QtGui.QGridLayout()
        self.fileGroupBox = QtGui.QGroupBox("Record to File")
        self.fileGroupBox.setLayout(self.fileLayout)
        self.mainLayout.addWidget(self.fileGroupBox)
        
        self.fileGroupBox.setCheckable(True)
        self.fileGroupBox.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        
        self.fileLabel = QtGui.QLabel("File Format")
        self.fileLabel.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.fileComboBox = QtGui.QComboBox()
        self.fileLabel.setBuddy(self.fileComboBox)
        self.fileSetupPushButton = QtGui.QPushButton("Setup")
        self.fileSetupPushButton.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.fileLayout.addWidget(self.fileLabel, 0, 0)
        self.fileLayout.addWidget(self.fileComboBox, 0, 1)
        self.fileLayout.addWidget(self.fileSetupPushButton, 0, 2)
        
        #
        # Record to Stream
        #
        
        self.streamLayout = QtGui.QGridLayout()
        self.streamGroupBox = QtGui.QGroupBox("Record to Stream")
        self.streamGroupBox.setLayout(self.streamLayout)
        self.mainLayout.addWidget(self.streamGroupBox)
        
        self.streamGroupBox.setCheckable(True)
        self.streamGroupBox.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        
        self.streamLabel = QtGui.QLabel("Stream Format")
        self.streamLabel.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.streamComboBox = QtGui.QComboBox()
        self.streamLabel.setBuddy(self.streamComboBox)
        self.streamSetupPushButton = QtGui.QPushButton("Setup")
        self.streamSetupPushButton.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.streamLayout.addWidget(self.streamLabel, 0, 0)
        self.streamLayout.addWidget(self.streamComboBox, 0, 1)
        self.streamLayout.addWidget(self.streamSetupPushButton, 0, 2)
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = AVWidget()
    main.show()
    sys.exit(app.exec_())