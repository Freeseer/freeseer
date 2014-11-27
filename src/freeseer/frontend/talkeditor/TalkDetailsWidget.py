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
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QPushButton


class TalkDetailsWidget(QWidget):

    def __init__(self, parent=None):
        super(TalkDetailsWidget, self).__init__(parent)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.buttonLayout = QHBoxLayout()

        saveIcon = QIcon.fromTheme("document-save")
        self.saveButton = QPushButton('Save Talk')
        self.saveButton.setIcon(saveIcon)
        self.buttonLayout.addWidget(self.saveButton)

        self.layout.addLayout(self.buttonLayout, 0, 1, 1, 1)

        self.titleLabel = QLabel('Title')
        self.titleLineEdit = QLineEdit()
        self.presenterLabel = QLabel('Presenter')
        self.presenterLineEdit = QLineEdit()
        self.layout.addWidget(self.titleLabel, 1, 0, 1, 1)
        self.layout.addWidget(self.titleLineEdit, 1, 1, 1, 1)
        self.layout.addWidget(self.presenterLabel, 1, 2, 1, 1)
        self.layout.addWidget(self.presenterLineEdit, 1, 3, 1, 1)

        self.eventLabel = QLabel('Event')
        self.eventLineEdit = QLineEdit()
        self.categoryLabel = QLabel('Category')
        self.categoryLineEdit = QLineEdit()

        self.layout.addWidget(self.eventLabel, 2, 0, 1, 1)
        self.layout.addWidget(self.eventLineEdit, 2, 1, 1, 1)
        self.layout.addWidget(self.categoryLabel, 2, 2, 1, 1)
        self.layout.addWidget(self.categoryLineEdit, 2, 3, 1, 1)

        self.roomLabel = QLabel('Room')
        self.roomLineEdit = QLineEdit()
        self.dateLayout = QHBoxLayout()
        self.dateLabel = QLabel('Date')
        self.dateEdit = QDateEdit()
        currentDate = QDate()
        self.dateEdit.setDate(currentDate.currentDate())
        self.dateEdit.setCalendarPopup(True)

        self.layout.addWidget(self.roomLabel, 3, 0, 1, 1)
        self.layout.addWidget(self.roomLineEdit, 3, 1, 1, 1)
        self.dateLayout.addWidget(self.dateEdit)
        self.layout.addWidget(self.dateLabel, 3, 2, 1, 1)
        self.layout.addLayout(self.dateLayout, 3, 3, 1, 1)

        self.startTimeLayout = QHBoxLayout()
        self.startTimeLabel = QLabel('Start Time')
        self.startTimeEdit = QTimeEdit()
        self.startTimeLayout.addWidget(self.startTimeEdit)
        self.endTimeLayout = QHBoxLayout()
        self.endTimeLabel = QLabel('End Time')
        self.endTimeEdit = QTimeEdit()
        self.endTimeLayout.addWidget(self.endTimeEdit)

        self.layout.addWidget(self.startTimeLabel, 4, 0, 1, 1)
        self.layout.addLayout(self.startTimeLayout, 4, 1, 1, 1)
        self.layout.addWidget(self.endTimeLabel, 4, 2, 1, 1)
        self.layout.addLayout(self.endTimeLayout, 4, 3, 1, 1)

        self.descriptionLabel = QLabel('Description')
        self.descriptionLabel.setAlignment(Qt.AlignTop)
        self.descriptionTextEdit = QPlainTextEdit()
        self.layout.addWidget(self.descriptionLabel, 5, 0, 1, 1)
        self.layout.addWidget(self.descriptionTextEdit, 5, 1, 1, 3)

        self.fields = [self.titleLineEdit, self.presenterLineEdit, self.categoryLineEdit,
                       self.eventLineEdit, self.roomLineEdit, self.dateEdit, self.startTimeEdit,
                       self.endTimeEdit, self.descriptionTextEdit]

    def toggle_input_fields(self, enable):
        for field in self.fields:
            field.setEnabled(enable)

    def input_fields_enabled(self):
        for field in self.fields:
            if not field.isEnabled():
                return False
        return True

    def enable_input_fields(self):
            self.titleLineEdit.setPlaceholderText("Enter Talk Title")
            self.presenterLineEdit.setPlaceholderText("Enter Presenter Name")
            self.categoryLineEdit.setPlaceholderText("Enter Category Type")
            self.eventLineEdit.setPlaceholderText("Enter Event Name")
            self.roomLineEdit.setPlaceholderText("Enter Room Location")
            self.toggle_input_fields(True)

    def disable_input_fields(self):
            self.titleLineEdit.setPlaceholderText("")
            self.presenterLineEdit.setPlaceholderText("")
            self.categoryLineEdit.setPlaceholderText("")
            self.eventLineEdit.setPlaceholderText("")
            self.roomLineEdit.setPlaceholderText("")
            self.toggle_input_fields(False)

    def clear_input_fields(self):
            self.titleLineEdit.clear()
            self.presenterLineEdit.clear()
            self.categoryLineEdit.clear()
            self.eventLineEdit.clear()
            self.roomLineEdit.clear()
            self.descriptionTextEdit.clear()

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = TalkDetailsWidget()
    main.show()
    sys.exit(app.exec_())
