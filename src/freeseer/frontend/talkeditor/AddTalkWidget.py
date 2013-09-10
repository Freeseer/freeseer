#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

Copyright (C) 2011, 2013  Free and Open Source Software Learning Centre
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

from PyQt4.QtCore import QDate
from PyQt4.QtCore import QTime
from PyQt4.QtGui import QDateEdit
from PyQt4.QtGui import QFormLayout
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTimeEdit
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget


class AddTalkWidget(QWidget):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QWidget.__init__(self, parent)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.addTalkGroupBox = QGroupBox("Add Talk")
        self.mainLayout.addWidget(self.addTalkGroupBox)

        self.addTalkLayout = QFormLayout()
        self.addTalkGroupBox.setLayout(self.addTalkLayout)

        # Title
        self.titleLabel = QLabel("Title")
        self.titleLineEdit = QLineEdit()
        if hasattr(QLineEdit(), 'setPlaceholderText'):
            self.titleLineEdit.setPlaceholderText("Title of the presentation")
        self.titleLabel.setBuddy(self.titleLineEdit)
        self.addTalkLayout.addRow(self.titleLabel, self.titleLineEdit)

        # Presenter
        self.presenterLabel = QLabel("Presenter")
        self.presenterLineEdit = QLineEdit()
        if hasattr(QLineEdit(), 'setPlaceholderText'):
            self.presenterLineEdit.setPlaceholderText("Name person or people presenting (comma separated)")
        self.presenterLabel.setBuddy(self.presenterLineEdit)
        self.addTalkLayout.addRow(self.presenterLabel, self.presenterLineEdit)

        # Event
        self.eventLabel = QLabel("Event")
        self.eventLineEdit = QLineEdit()
        if hasattr(QLineEdit(), 'setPlaceholderText'):
            self.eventLineEdit.setPlaceholderText("The name of the Event this talk is being presented at")
        self.eventLabel.setBuddy(self.eventLineEdit)
        self.addTalkLayout.addRow(self.eventLabel, self.eventLineEdit)

        # Room
        self.roomLabel = QLabel("Room")
        self.roomLineEdit = QLineEdit()
        if hasattr(QLineEdit(), 'setPlaceholderText'):
            self.roomLineEdit.setPlaceholderText("The Room in which the presentation is taking place")
        self.roomLabel.setBuddy(self.roomLineEdit)
        self.addTalkLayout.addRow(self.roomLabel, self.roomLineEdit)

        # Date
        current_date = QDate()
        self.dateLabel = QLabel("Date")
        self.dateEdit = QDateEdit()
        self.dateEdit.setDate(current_date.currentDate())
        self.dateLabel.setBuddy(self.dateEdit)
        self.addTalkLayout.addRow(self.dateLabel, self.dateEdit)

        self.dateEdit.setCalendarPopup(True)

        # Time
        current_time = QTime()
        self.timeLabel = QLabel("Time")
        self.timeEdit = QTimeEdit()
        self.timeEdit.setTime(current_time.currentTime())
        self.timeLabel.setBuddy(self.dateEdit)
        self.addTalkLayout.addRow(self.timeLabel, self.timeEdit)

        # Buttons
        addIcon = QIcon.fromTheme("list-add")
        cancelIcon = QIcon.fromTheme("edit-clear")

        self.buttonsWidget = QHBoxLayout()
        self.addButton = QPushButton("Add")
        self.addButton.setIcon(addIcon)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setIcon(cancelIcon)
        self.buttonsWidget.addWidget(self.addButton)
        self.buttonsWidget.addWidget(self.cancelButton)
        self.addTalkLayout.addRow(None, self.buttonsWidget)


if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = AddTalkWidget()
    main.show()
    sys.exit(app.exec_())
