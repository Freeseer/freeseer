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


class AboutWidget(QtGui.QWidget):
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
        # About
        #

        self.MiscLayout = QtGui.QVBoxLayout()
        self.MiscGroupBox = QtGui.QGroupBox("About")
        self.MiscGroupBox.setLayout(self.MiscLayout)
        self.mainLayout.addWidget(self.MiscGroupBox)

        self.languageLayout = QtGui.QHBoxLayout()
        self.MiscLayout.addLayout(self.languageLayout)
        self.languageLabel = QtGui.QLabel("Default Language")
        self.languageComboBox = QtGui.QComboBox()
        self.languageComboBox.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.languageLabel.setBuddy(self.languageComboBox)
        self.languageLayout.addWidget(self.languageLabel)
        self.languageLayout.addWidget(self.languageComboBox)

        self.recordDirLayout = QtGui.QHBoxLayout()
        self.MiscLayout.addLayout(self.recordDirLayout)

        self.recordDirLabel = QtGui.QLabel("Record Directory")
        self.recordDirLineEdit = QtGui.QLineEdit()
        self.recordDirLabel.setBuddy(self.recordDirLineEdit)
        self.recordDirPushButton = QtGui.QPushButton("...")
        self.recordDirLayout.addWidget(self.recordDirLabel)
        self.recordDirLayout.addWidget(self.recordDirLineEdit)
        self.recordDirLayout.addWidget(self.recordDirPushButton)

        self.autoHideCheckBox = QtGui.QCheckBox("Enable Auto-Hide")
        self.MiscLayout.addWidget(self.autoHideCheckBox)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = AboutWidget()
    main.show()
    sys.exit(app.exec_())
