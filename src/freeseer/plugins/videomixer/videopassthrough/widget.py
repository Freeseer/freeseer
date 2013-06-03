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
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QSlider
from PyQt4.QtGui import QSpinBox
from PyQt4.QtGui import QWidget

class ConfigWidget(QWidget):
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QFormLayout()
        self.setLayout(layout)
        
        self.inputLabel = QLabel("Video Input")
        self.inputCombobox = QComboBox()
        layout.addRow(self.inputLabel, self.inputCombobox)
        
        self.videocolourLabel = QLabel(self.tr("Colour Format"))
        self.videocolourComboBox = QComboBox()
        self.videocolourComboBox.addItem("video/x-raw-rgb")
        self.videocolourComboBox.addItem("video/x-raw-yuv")
        self.videocolourComboBox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        layout.addRow(self.videocolourLabel, self.videocolourComboBox)
        
        self.framerateLabel = QLabel("Framerate")
        self.framerateLayout = QHBoxLayout()
        self.framerateSlider = QSlider()
        self.framerateSlider.setOrientation(Qt.Horizontal)
        self.framerateSlider.setMinimum(0)
        self.framerateSlider.setMaximum(60)
        self.framerateSpinBox = QSpinBox()
        self.framerateSpinBox.setMinimum(0)
        self.framerateSpinBox.setMaximum(60)
        self.framerateLayout.addWidget(self.framerateSlider)
        self.framerateLayout.addWidget(self.framerateSpinBox)
        layout.addRow(self.framerateLabel, self.framerateLayout)
        
        self.videoscaleLabel = QLabel("Video Scale")
        self.videoscaleComboBox = QComboBox()
        self.videoscaleComboBox.addItem("NOSCALE")
        self.videoscaleComboBox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        layout.addRow(self.videoscaleLabel, self.videoscaleComboBox)
