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
        self.mainLayout.addStretch(0)
        self.setLayout(self.mainLayout)

        self.fontSize = self.font().pixelSize()
        self.fontUnit = "px"
        if self.fontSize == -1:  # Font is set as points, not pixels.
            self.fontUnit = "pt"
            self.fontSize = self.font().pointSize()
        #
        # General
        #

        self.boxStyle = "QGroupBox {{ font-weight: bold; font-size: {}{} }}".format(self.fontSize + 1, self.fontUnit)
        self.miscLayout = QtGui.QVBoxLayout()
        self.miscGroupBox = QtGui.QGroupBox("General")
        self.miscGroupBox.setLayout(self.miscLayout)
        self.miscGroupBox.setStyleSheet(self.boxStyle)
        self.mainLayout.insertWidget(0, self.miscGroupBox)

        self.languageLayout = QtGui.QHBoxLayout()
        self.miscLayout.addLayout(self.languageLayout)
        self.languageLabel = QtGui.QLabel("Default Language")
        self.languageComboBox = QtGui.QComboBox()
        self.languageComboBox.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.languageLabel.setBuddy(self.languageComboBox)
        self.languageLayout.addWidget(self.languageLabel)
        self.languageLayout.addWidget(self.languageComboBox)

        self.autoHideCheckBox = QtGui.QCheckBox("Enable Auto-Hide")
        self.miscLayout.addWidget(self.autoHideCheckBox)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = GeneralWidget()
    main.show()
    sys.exit(app.exec_())
