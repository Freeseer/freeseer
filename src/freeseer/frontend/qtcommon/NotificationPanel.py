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

import collections

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QWidget


class NotificationPanel(QWidget):
    """Widget containing notification queue"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.n_manager = collections.OrderedDict()
        self.error_keyword = None
        self.current_keyword = 0

        # message label
        self.message = QLabel(self)
        self.message.resize(214, 75)
        self.message.setWordWrap(True)

        # "up" and "down" buttons
        self.bUp = QPushButton("u", self)
        self.bUp.resize(35, 35)
        self.bUp.move(215, 0)
        self.bDown = QPushButton("d", self)
        self.bDown.resize(35, 35)
        self.bDown.move(215, 35)

        # Window settings
        self.setGeometry(300, 300, 250, 75)
        self.setMaximumSize(250, 75)
        self.setWindowTitle('Notifications')
        #self.setWindowFlags(Qt.FramelessWindowHint)

        # button connections
        self.connect(self.bUp, SIGNAL('clicked()'), self.next_notification)
        self.connect(self.bDown, SIGNAL('clicked()'), self.prev_notification)

    def add_warning(self, name, message):
        self.n_manager[name] = message
        self.update()

    def add_error(self, name, message):
        self.n_manager[name] = message
        self.error_keyword = name
        self.current_keyword = len(self.n_manager) - 1
        self.update()

    def delete_notification(self, name):
        if len(self.n_manager) and name in self.n_manager:
            if self.n_manager.items()[self.current_keyword][0] == name:
                if self.current_keyword == len(self.n_manager) - 1:
                    self.current_keyword = 0
                else:
                    self.current_keyword = self.current_keyword + 1

            del self.n_manager[name]
            if self.error_keyword == name:
                self.error_keyword = None
        self.update()

    def next_notification(self):
        if self.current_keyword == len(self.n_manager) - 1:
            self.current_keyword = 0
        else:
            self.current_keyword = self.current_keyword + 1
        self.update()

    def prev_notification(self):
        if self.current_keyword == 0:
            self.current_keyword = len(self.n_manager) - 1
        else:
            self.current_keyword = self.current_keyword - 1
        self.update()

    def update(self):
        if len(self.n_manager):
            if self.error_keyword is None and self.n_manager.items()[self.current_keyword][0] == self.error_keyword:
                self.message.setText("ERROR: {}".format(self.n_manager.items()[self.current_keyword][1]))
                self.message.setStyleSheet("QLabel { background-color : red; color : black; }")
            else:
                self.message.setText("WARNING: {}".format(self.n_manager.items()[self.current_keyword][1]))
                self.message.setStyleSheet("QLabel { background-color : yellow; color : black; }")

            self.show()
        else:
            self.hide()

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = NotificationPanel()
    sys.exit(app.exec_())
