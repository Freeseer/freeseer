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

from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QWidget

class ConfigWidget(QWidget):
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QGridLayout()
        self.setLayout(layout)
        
        self.mainInputLabel = QLabel("Main Source")
        self.mainInputComboBox = QComboBox()
        self.mainInputSetupButton = QPushButton("Setup")
        layout.addWidget(self.mainInputLabel, 0, 0)
        layout.addWidget(self.mainInputComboBox, 0, 1)
        layout.addWidget(self.mainInputSetupButton, 0, 2)
        
        self.pipInputLabel = QLabel("PIP Source")
        self.pipInputComboBox = QComboBox()
        self.pipInputSetupButton = QPushButton("Setup")
        layout.addWidget(self.pipInputLabel, 1, 0)
        layout.addWidget(self.pipInputComboBox, 1, 1)
        layout.addWidget(self.pipInputSetupButton, 1, 2)
