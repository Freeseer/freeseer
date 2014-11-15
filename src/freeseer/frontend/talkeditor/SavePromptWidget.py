#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014  Free and Open Source Software Learning Centre
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

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QVBoxLayout


class SavePromptWidget(QDialog):
    """Dialog warning the user if there are unsaved changes to the current talk"""
    def __init__(self, parent=None):
        super(SavePromptWidget, self).__init__(parent)

        self.resize(600, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bottomButtonLayout = QHBoxLayout()

        self.label = QLabel("This is a test. Click the button below to continue.")
        self.saveButton = QPushButton('Save Changes')
        self.discardButton = QPushButton('Discard Changes')
        self.continueButton = QPushButton('Continue Editing')

        self.layout.addWidget(self.label)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.saveButton)
        self.buttonLayout.addWidget(self.discardButton)
        self.buttonLayout.addWidget(self.continueButton)

        self.layout.addLayout(self.buttonLayout)

        self.setWindowTitle("Unsaved Changes Exist")
