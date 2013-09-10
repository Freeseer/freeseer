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
from PyQt4.QtGui import QFormLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QWidget


class ConfigWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QFormLayout()
        self.setLayout(layout)

        self.label = QLabel("Audio Input")
        self.inputLayout = QHBoxLayout()
        self.combobox = QComboBox()
        self.combobox.setMinimumWidth(150)
        self.inputSettingsToolButton = QToolButton()
        self.inputSettingsToolButton.setText("Settings")
        configIcon = QIcon.fromTheme("preferences-other")
        self.inputSettingsToolButton.setIcon(configIcon)
        self.inputSettingsToolButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.inputSettingsToolButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.inputSettingsStack = QStackedWidget()
        blankWidget = QWidget()
        self.inputSettingsStack.addWidget(blankWidget)
        self.inputSettingsStack.addWidget(self.inputSettingsToolButton)
        self.inputLayout.addWidget(self.combobox)
        self.inputLayout.addWidget(self.inputSettingsStack)
        layout.addRow(self.label, self.inputLayout)
