#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2013  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

from PyQt4.QtCore import QString
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QFormLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer.frontend.qtcommon import resource  # noqa


class ReportDialog(QDialog):
    """Failure report dialog for Freeseer"""
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        icon = QIcon()
        icon.addPixmap(QPixmap(_fromUtf8(":/freeseer/logo.png")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        boldFont = QFont()
        boldFont.setBold(True)

        self.infoLayout = QFormLayout()
        self.mainLayout.addLayout(self.infoLayout)
        self.reportLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.reportLayout)
        self.buttonLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        # Talk infomation
        self.titleLabel = QLabel("Title:")
        self.titleLabel2 = QLabel()
        self.titleLabel2.setFont(boldFont)
        self.speakerLabel = QLabel("Speaker:")
        self.speakerLabel2 = QLabel()
        self.speakerLabel2.setFont(boldFont)
        self.eventLabel = QLabel("Event:")
        self.eventLabel2 = QLabel()
        self.eventLabel2.setFont(boldFont)
        self.roomLabel = QLabel("Room:")
        self.roomLabel2 = QLabel()
        self.roomLabel2.setFont(boldFont)
        self.timeLabel = QLabel("Time:")
        self.timeLabel2 = QLabel()
        self.timeLabel2.setFont(boldFont)
        self.infoLayout.addRow(self.titleLabel, self.titleLabel2)
        self.infoLayout.addRow(self.speakerLabel, self.speakerLabel2)
        self.infoLayout.addRow(self.eventLabel, self.eventLabel2)
        self.infoLayout.addRow(self.roomLabel, self.roomLabel2)
        self.infoLayout.addRow(self.timeLabel, self.timeLabel2)

        #Report
        self.commentLabel = QLabel("Comment")
        self.commentEdit = QLineEdit()

        self.reportCombo = QComboBox()
        # Prototype for report options. Please define these in the
        # record.py logic file under retranslate() so that translations
        # work.
#        self.options = ['No Audio', 'No Video', 'No Audio/Video']
#        for i in self.options:
#            self.reportCombo.addItem(i)

        self.releaseCheckBox = QCheckBox("Release Received")

        self.reportLayout.addWidget(self.commentLabel)
        self.reportLayout.addWidget(self.commentEdit)
        self.reportLayout.addWidget(self.reportCombo)
        self.reportLayout.addWidget(self.releaseCheckBox)

        #Buttons
        self.reportButton = QPushButton("Report")
        self.closeButton = QPushButton("Close")

        self.buttonLayout.addWidget(self.closeButton)
        self.buttonLayout.addWidget(self.reportButton)
        self.connect(self.closeButton, SIGNAL("clicked()"), self.close)
