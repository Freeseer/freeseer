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
from PyQt4.QtCore import QDate

from PyQt4.QtGui import QDateEdit
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTimeEdit
from PyQt4.QtGui import QWidget


class TalkDetailsWidget(QWidget):

    def __init__(self, parent=None):
        super(TalkDetailsWidget, self).__init__(parent)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.buttonLayout = QHBoxLayout()

        self.layout.addLayout(self.buttonLayout, 0, 1, 1, 1)

        self.titleLabel = QLabel('Title')
        self.titleLineEdit = QLineEdit()
        self.layout.addWidget(self.titleLabel, 1, 0, 1, 1)
        self.layout.addWidget(self.titleLineEdit, 1, 1, 1, 3)

        self.presenterLabel = QLabel('Presenter')
        self.presenterLineEdit = QLineEdit()

        self.categoryLabel = QLabel('Category')
        self.categoryLineEdit = QLineEdit()

        self.layout.addWidget(self.presenterLabel, 2, 0, 1, 1)
        self.layout.addWidget(self.presenterLineEdit, 2, 1, 1, 1)
        self.layout.addWidget(self.categoryLabel, 2, 2, 1, 1)
        self.layout.addWidget(self.categoryLineEdit, 2, 3, 1, 1)

        self.eventLabel = QLabel('Event')
        self.eventLineEdit = QLineEdit()
        self.roomLabel = QLabel('Room')
        self.roomLineEdit = QLineEdit()

        self.layout.addWidget(self.eventLabel, 3, 0, 1, 1)
        self.layout.addWidget(self.eventLineEdit, 3, 1, 1, 1)
        self.layout.addWidget(self.roomLabel, 3, 2, 1, 1)
        self.layout.addWidget(self.roomLineEdit, 3, 3, 1, 1)

        self.dateLayout = QHBoxLayout()
        self.timeLayout = QHBoxLayout()
        self.dateLabel = QLabel('Date')
        self.dateEdit = QDateEdit()
        currentDate = QDate()
        self.dateEdit.setDate(currentDate.currentDate())
        self.dateEdit.setCalendarPopup(True)
        self.timeLabel = QLabel('Time')
        self.timeEdit = QTimeEdit()

        self.dateLayout.addWidget(self.dateEdit)
        self.timeLayout.addWidget(self.timeEdit)
        self.layout.addWidget(self.dateLabel, 4, 0, 1, 1)
        self.layout.addLayout(self.dateLayout, 4, 1, 1, 1)
        self.layout.addWidget(self.timeLabel, 4, 2, 1, 1)
        self.layout.addLayout(self.timeLayout, 4, 3, 1, 1)

        self.descriptionLabel = QLabel('Description')
        self.descriptionLabel.setAlignment(Qt.AlignTop)
        self.descriptionTextEdit = QPlainTextEdit()
        self.layout.addWidget(self.descriptionLabel, 5, 0, 1, 1)
        self.layout.addWidget(self.descriptionTextEdit, 5, 1, 1, 3)

    def enable_input_fields(self):
        self.titleLineEdit.setPlaceholderText("Enter Talk Title")
        self.presenterLineEdit.setPlaceholderText("Enter Presenter Name")
        self.categoryLineEdit.setPlaceholderText("Enter Category Type")
        self.eventLineEdit.setPlaceholderText("Enter Event Name")
        self.roomLineEdit.setPlaceholderText("Enter Room Location")
        self.titleLineEdit.setEnabled(True)
        self.presenterLineEdit.setEnabled(True)
        self.categoryLineEdit.setEnabled(True)
        self.eventLineEdit.setEnabled(True)
        self.roomLineEdit.setEnabled(True)
        self.dateEdit.setEnabled(True)
        self.timeEdit.setEnabled(True)
        self.descriptionTextEdit.setEnabled(True)

    def disable_input_fields(self):
        self.titleLineEdit.setPlaceholderText("")
        self.presenterLineEdit.setPlaceholderText("")
        self.categoryLineEdit.setPlaceholderText("")
        self.eventLineEdit.setPlaceholderText("")
        self.roomLineEdit.setPlaceholderText("")
        self.titleLineEdit.setEnabled(False)
        self.presenterLineEdit.setEnabled(False)
        self.categoryLineEdit.setEnabled(False)
        self.eventLineEdit.setEnabled(False)
        self.roomLineEdit.setEnabled(False)
        self.dateEdit.setEnabled(False)
        self.timeEdit.setEnabled(False)
        self.descriptionTextEdit.setEnabled(False)

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = TalkDetailsWidget()
    main.show()
    sys.exit(app.exec_())
