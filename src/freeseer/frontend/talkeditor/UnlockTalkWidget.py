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
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QVBoxLayout


class UnlockTalkWidget(QDialog):

    def __init__(self, parent=None):
        super(UnlockTalkWidget, self).__init__(parent)
        self.setWindowTitle('Unlock Talk Details')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.information = QLabel('Enter the password to unlock the talks')
        self.layout.addWidget(self.information)

        self.passwordBox = QLineEdit()
        self.layout.addWidget(self.passwordBox)

        self.buttonBox = QDialogButtonBox(Qt.Horizontal)
        self.layout.addWidget(self.buttonBox)

        self.unlockButton = QPushButton('Unlock')
        self.cancelButton = QPushButton('Cancel')
        self.buttonBox.addButton(
            self.unlockButton, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(
            self.cancelButton, QDialogButtonBox.RejectRole)

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = UnlockTalkWidget()
    main.show()
    sys.exit(app.exec_())
