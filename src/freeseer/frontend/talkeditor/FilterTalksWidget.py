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

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QSizePolicy


class FilterTalksWidget(QWidget):

    def __init__(self, parent=None):
        super(FilterTalksWidget, self).__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        

        self.speakerLabel = QLabel("Speaker")
        self.speakerLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.speakerComboBox = QComboBox()
        self.speakerLabel.setBuddy(self.speakerComboBox)
        self.eventLabel = QLabel("Event")
        self.eventLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.eventComboBox = QComboBox()
        self.eventLabel.setBuddy(self.eventComboBox)
        self.roomLabel = QLabel("Room")
        self.roomLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.roomComboBox = QComboBox()
        self.roomLabel.setBuddy(self.roomComboBox)
        self.dateLabel = QLabel("Date")
        self.dateLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.dateComboBox = QComboBox()
        self.dateLabel.setBuddy(self.dateComboBox)
        self.layout.addWidget(self.speakerLabel)
        self.layout.addWidget(self.speakerComboBox)
        self.layout.addWidget(self.eventLabel)
        self.layout.addWidget(self.eventComboBox)
        self.layout.addWidget(self.roomLabel)
        self.layout.addWidget(self.roomComboBox)
        self.layout.addWidget(self.dateLabel)
        self.layout.addWidget(self.dateComboBox)

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = FilterTalksWidget()
    main.show()
    sys.exit(app.exec_())
