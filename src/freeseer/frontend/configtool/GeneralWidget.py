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
http://wiki.github.com/fosslc/freeseer/

@author: Thanh Ha
'''

from PyQt4 import QtCore, QtGui

class GeneralWidget(QtGui.QWidget):
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
        # AV
        #
        
        self.AVLayout = QtGui.QGridLayout()
        self.AVGroupBox = QtGui.QGroupBox(self.tr("Audio / Video Settings"))
        self.AVGroupBox.setLayout(self.AVLayout)
        self.mainLayout.addWidget(self.AVGroupBox)
        
        self.recordAudioCheckbox = QtGui.QCheckBox(self.tr("Record Audio"))
        self.AVLayout.addWidget(self.recordAudioCheckbox, 0, 0)
        
        self.audioMixerLabel = QtGui.QLabel(self.tr("Audio Mixer"))
        self.audioMixerLabel.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.audioMixerComboBox = QtGui.QComboBox()
        self.audioMixerLabel.setBuddy(self.audioMixerComboBox)
        self.audioMixerSetupPushButton = QtGui.QPushButton(self.tr("Setup"))
        self.audioMixerSetupPushButton.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.AVLayout.addWidget(self.audioMixerLabel, 1, 0)
        self.AVLayout.addWidget(self.audioMixerComboBox, 1, 1)
        self.AVLayout.addWidget(self.audioMixerSetupPushButton, 1, 2)
        
        self.recordVideoCheckbox = QtGui.QCheckBox(self.tr("Record Video"))
        self.AVLayout.addWidget(self.recordVideoCheckbox, 2, 0)
        
        self.videoMixerLabel = QtGui.QLabel(self.tr("Video Mixer"))
        self.videoMixerLabel.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.videoMixerComboBox = QtGui.QComboBox()
        self.videoMixerLabel.setBuddy(self.audioMixerComboBox)
        self.videoMixerSetupPushButton = QtGui.QPushButton(self.tr("Setup"))
        self.videoMixerSetupPushButton.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        self.AVLayout.addWidget(self.videoMixerLabel, 3, 0)
        self.AVLayout.addWidget(self.videoMixerComboBox, 3, 1)
        self.AVLayout.addWidget(self.videoMixerSetupPushButton, 3, 2)
        
        
        #
        # Misc
        #
        
        self.MiscLayout = QtGui.QVBoxLayout()
        self.MiscGroupBox = QtGui.QGroupBox(self.tr("Miscellaneous"))
        self.MiscGroupBox.setLayout(self.MiscLayout)
        self.mainLayout.addWidget(self.MiscGroupBox)
        
        self.recordDirLayout = QtGui.QHBoxLayout()
        self.MiscLayout.addLayout(self.recordDirLayout)
        
        self.recordDirLabel = QtGui.QLabel(self.tr("Record Directory"))
        self.recordDirLineEdit = QtGui.QLineEdit()
        self.recordDirLabel.setBuddy(self.recordDirLineEdit)
        self.recordDirPushButton = QtGui.QPushButton("...")
        self.recordDirLayout.addWidget(self.recordDirLabel)
        self.recordDirLayout.addWidget(self.recordDirLineEdit)
        self.recordDirLayout.addWidget(self.recordDirPushButton)
        
        self.autoHideCheckBox = QtGui.QCheckBox(self.tr("Enable Auto-Hide"))
        self.MiscLayout.addWidget(self.autoHideCheckBox)
        
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = GeneralWidget()
    main.show()
    sys.exit(app.exec_())