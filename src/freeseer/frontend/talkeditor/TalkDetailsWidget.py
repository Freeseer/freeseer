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
from PyQt4.QtCore import QTime
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

        self.titleLabel = QLabel('Title')
        self.titleLineEdit = QLineEdit()
        self.layout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.layout.addWidget(self.titleLineEdit, 0, 1, 1, 3)

        self.presenterLabel = QLabel('Presenter')
        self.presenterLineEdit = QLineEdit()
        self.levelLabel = QLabel('Level')
        self.levelLineEdit = QLineEdit()
        self.layout.addWidget(self.presenterLabel, 1, 0, 1, 1)
        self.layout.addWidget(self.presenterLineEdit, 1, 1, 1, 1)
        self.layout.addWidget(self.levelLabel, 1, 2, 1, 1)
        self.layout.addWidget(self.levelLineEdit, 1, 3, 1, 1)

        self.eventLabel = QLabel('Event')
        self.eventLineEdit = QLineEdit()
        self.roomLabel = QLabel('Room')
        self.roomLineEdit = QLineEdit()
        self.layout.addWidget(self.eventLabel, 2, 0, 1, 1)
        self.layout.addWidget(self.eventLineEdit, 2, 1, 1, 1)
        self.layout.addWidget(self.roomLabel, 2, 2, 1, 1)
        self.layout.addWidget(self.roomLineEdit, 2, 3, 1, 1)

        self.dateLayout = QHBoxLayout()
        self.timeLayout = QHBoxLayout()
        self.dateLabel = QLabel('Date')
        self.dateEdit = QDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.timeLabel = QLabel('Time')
        self.timeEdit = QTimeEdit()

        currentTime = QTime()
        currentDate = QDate()

        self.dateEdit.setDate(currentDate.currentDate())
        self.dateLabel.setBuddy(self.dateEdit)
        self.timeEdit.setTime(currentTime.currentTime())
        self.timeLabel.setBuddy(self.dateEdit)
        
        self.dateLayout.addWidget(self.dateEdit)
        self.timeLayout.addWidget(self.timeEdit)
        self.layout.addWidget(self.dateLabel, 3, 0, 1, 1)
        self.layout.addLayout(self.dateLayout, 3, 1, 1, 1)
        self.layout.addWidget(self.timeLabel, 3, 2, 1, 1)
        self.layout.addLayout(self.timeLayout, 3, 3, 1, 1)



        self.descriptionLabel = QLabel('Description')
        self.descriptionLabel.setAlignment(Qt.AlignTop)
        self.descriptionTextEdit = QPlainTextEdit()
        self.layout.addWidget(self.descriptionLabel, 4, 0, 1, 1)
        self.layout.addWidget(self.descriptionTextEdit, 4, 1, 1, 3)

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = TalkDetailsWidget()
    main.show()
    sys.exit(app.exec_())
