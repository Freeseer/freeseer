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

from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QDoubleSpinBox
from PyQt4.QtGui import QFormLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QSpinBox
from PyQt4.QtGui import QWidget


class ConfigWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QFormLayout()
        self.setLayout(layout)

        #
        # Audio Quality
        #

        self.label_audio_quality = QLabel("Audio Quality")
        self.spinbox_audio_quality = QDoubleSpinBox()
        self.spinbox_audio_quality.setMinimum(0.0)
        self.spinbox_audio_quality.setMaximum(1.0)
        self.spinbox_audio_quality.setSingleStep(0.1)
        self.spinbox_audio_quality.setDecimals(1)
        self.spinbox_audio_quality.setValue(0.3)            # Default value 0.3

        #
        # Video Quality
        #

        self.label_video_quality = QLabel("Video Quality (kb/s)")
        self.spinbox_video_quality = QSpinBox()
        self.spinbox_video_quality.setMinimum(0)
        self.spinbox_video_quality.setMaximum(16777215)
        self.spinbox_video_quality.setValue(2400)           # Default value 2400

        #
        # Misc.
        #
        self.label_matterhorn = QLabel("Matterhorn Metadata")
        self.label_matterhorn.setToolTip("Generates Matterhorn Metadata in XML format")
        self.checkbox_matterhorn = QCheckBox()
        layout.addRow(self.label_matterhorn, self.checkbox_matterhorn)

    def get_video_quality_layout(self):
        layout_video_quality = QHBoxLayout()
        layout_video_quality.addWidget(self.label_video_quality)
        layout_video_quality.addWidget(self.spinbox_video_quality)

        return layout_video_quality

    def get_audio_quality_layout(self):
        layout_audio_quality = QHBoxLayout()
        layout_audio_quality.addWidget(self.label_audio_quality)
        layout_audio_quality.addWidget(self.spinbox_audio_quality)

        return layout_audio_quality
