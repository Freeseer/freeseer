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
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGridLayout

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer.frontend.qtcommon import resource  # noqa
from freeseer.frontend.qtcommon.AboutWidget import AboutWidget

RECORD_BUTTON_ARTIST = 'Sekkyumu'
RECORD_BUTTON_LINK = 'http://sekkyumu.deviantart.com/'
HEADPHONES_ARTIST = 'Ben Fleming'
HEADPHONES_LINK = 'http://mediadesign.deviantart.com/'


class AboutDialog(QDialog):
    """
    Common About Dialog for the Freeseer Project. This should be used for the
    about dialog when including one in GUIs.


    Grid Layout:

    Logo  |  About Infos
    ------|-------------
          |  Close Button
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.aboutWidget = AboutWidget()

        icon = QIcon()
        icon.addPixmap(QPixmap(_fromUtf8(":/freeseer/logo.png")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.aboutWidget)

        # Right Bottom corner of grid, Close Button
        self.buttonBox = QDialogButtonBox()
        self.closeButton = self.buttonBox.addButton("Close", QDialogButtonBox.AcceptRole)
        self.layout.addWidget(self.buttonBox, 1, 1)
        self.connect(self.closeButton, SIGNAL("clicked()"), self.close)

        self.setWindowTitle("About Freeseer")
