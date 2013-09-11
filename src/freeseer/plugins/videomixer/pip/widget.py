#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

Copyright (C) 2013  Free and Open Source Software Learning Centre
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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QWidget


class ConfigWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QGridLayout()
        self.setLayout(layout)

        self.mainInputLabel = QLabel("Main Source")
        self.mainInputComboBox = QComboBox()
        self.mainInputSetupButton = QToolButton()
        self.mainInputSetupButton.setText("Settings")
        configIcon = QIcon.fromTheme("preferences-other")
        self.mainInputSetupButton.setIcon(configIcon)
        self.mainInputSetupButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.mainInputSetupButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.mainInputSetupStack = QStackedWidget()
        blankWidget = QWidget()
        self.mainInputSetupStack.addWidget(blankWidget)
        self.mainInputSetupStack.addWidget(self.mainInputSetupButton)
        layout.addWidget(self.mainInputLabel, 0, 0)
        layout.addWidget(self.mainInputComboBox, 0, 1)
        layout.addWidget(self.mainInputSetupStack, 0, 2)

        self.pipInputLabel = QLabel("PIP Source")
        self.pipInputComboBox = QComboBox()
        self.pipInputSetupButton = QToolButton()
        self.pipInputSetupButton.setText("Settings")
        self.pipInputSetupButton.setIcon(configIcon)  # reuse the one from main input
        self.pipInputSetupButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.pipInputSetupButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.pipInputSetupStack = QStackedWidget()
        blankWidget = QWidget()
        self.pipInputSetupStack.addWidget(blankWidget)
        self.pipInputSetupStack.addWidget(self.pipInputSetupButton)
        layout.addWidget(self.pipInputLabel, 1, 0)
        layout.addWidget(self.pipInputComboBox, 1, 1)
        layout.addWidget(self.pipInputSetupStack, 1, 2)
