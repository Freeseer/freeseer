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

from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QGroupBoxWithDpi
from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QWidgetWithDpi


class GeneralWidget(QWidgetWithDpi):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(GeneralWidget, self).__init__(parent)

        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addStretch(0)
        self.setLayout(self.mainLayout)

        fontSize = self.font().pixelSize()
        fontUnit = "px"
        if fontSize == -1:  # Font is set as points, not pixels.
            fontUnit = "pt"
            fontSize = self.font().pointSize()

        boxStyle = "QGroupBox {{ font-weight: bold; font-size: {}{} }}".format(fontSize + 1, fontUnit)
        BOX_WIDTH = 400
        BOX_HEIGHT = 60

        #
        # Heading
        #

        self.title = QtGui.QLabel(u"{0} General {1}".format(u'<h1>', u'</h1>'))
        self.mainLayout.insertWidget(0, self.title)
        self.mainLayout.insertSpacerItem(1, QtGui.QSpacerItem(0, fontSize * 2))

        #
        # Language
        #

        languageBoxLayout = QtGui.QVBoxLayout()
        self.languageGroupBox = QGroupBoxWithDpi("Language")
        self.languageGroupBox.setLayout(languageBoxLayout)
        self.languageGroupBox.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.languageGroupBox.setFixedSize(BOX_WIDTH, BOX_HEIGHT)
        self.languageGroupBox.setStyleSheet(boxStyle)
        self.mainLayout.insertWidget(2, self.languageGroupBox)

        languageLayout = QtGui.QHBoxLayout()
        languageBoxLayout.addLayout(languageLayout)
        self.translateButton = QtGui.QPushButton("Help us translate")
        self.languageComboBox = QtGui.QComboBox()
        self.languageComboBox.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        languageLayout.addWidget(self.languageComboBox, 2)
        languageLayout.addSpacerItem(self.qspacer_item_with_dpi(40, 0))
        languageLayout.addWidget(self.translateButton, 1)

        #
        # Appearance
        #

        appearanceBoxLayout = QtGui.QVBoxLayout()
        self.appearanceGroupBox = QGroupBoxWithDpi("Appearance")
        self.appearanceGroupBox.setLayout(appearanceBoxLayout)
        self.appearanceGroupBox.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.appearanceGroupBox.setFixedSize(BOX_WIDTH, BOX_HEIGHT)
        self.appearanceGroupBox.setStyleSheet(boxStyle)
        self.mainLayout.insertWidget(3, self.appearanceGroupBox)

        self.autoHideCheckBox = QtGui.QCheckBox("Auto-Hide to system tray on record")
        appearanceBoxLayout.addWidget(self.autoHideCheckBox)

        #
        # Reset
        #

        resetBoxLayout = QtGui.QVBoxLayout()
        self.resetGroupBox = QGroupBoxWithDpi("Reset")
        self.resetGroupBox.setLayout(resetBoxLayout)
        self.resetGroupBox.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.resetGroupBox.setFixedSize(BOX_WIDTH / 2, BOX_HEIGHT)
        self.resetGroupBox.setStyleSheet(boxStyle)
        self.mainLayout.addWidget(self.resetGroupBox)
        self.mainLayout.addSpacerItem(self.qspacer_item_with_dpi(0, 20))

        resetLayout = QtGui.QHBoxLayout()
        resetBoxLayout.addLayout(resetLayout)
        self.resetButton = QtGui.QPushButton("Reset settings to defaults")
        resetLayout.addWidget(self.resetButton)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = GeneralWidget()
    main.show()
    sys.exit(app.exec_())
