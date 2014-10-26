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

from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QVBoxLayout

from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QDialogWithDpi
from freeseer.frontend.talkeditor.TalkDetailsWidget import TalkDetailsWidget


class NewTalkWidget(QDialogWithDpi):
    """Dialog for adding new talk to database"""
    def __init__(self, parent=None):
        super(NewTalkWidget, self).__init__(parent)

        self.resize(600, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bottomButtonLayout = QHBoxLayout()

        self.talkDetailsWidget = TalkDetailsWidget()
        self.layout.addWidget(self.talkDetailsWidget)

        self.talkDetailsWidget.saveButton.hide()
        addIcon = QIcon.fromTheme("list-add")
        cancelIcon = QIcon.fromTheme("edit-clear")

        self.addButton = QPushButton('Add')
        self.addButton.setIcon(addIcon)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.setIcon(cancelIcon)

        self.talkDetailsWidget.layout.addLayout(self.bottomButtonLayout, 6, 1, 1, 1)

        self.bottomButtonLayout.addWidget(self.addButton)
        self.bottomButtonLayout.addWidget(self.cancelButton)

        self.setWindowTitle("New Talk")

        self.talkDetailsWidget.enable_input_fields()
        self.talkDetailsWidget.dateEdit.setDisplayFormat('dd MMMM, yyyy')
