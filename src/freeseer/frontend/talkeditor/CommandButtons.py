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

from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QWidget

class CommandButtons(QWidget):

    def __init__(self, parent=None):
        super(CommandButtons, self).__init__(parent)
        self.setWindowTitle('Unlock Talk Details')

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.addButton = QPushButton('Add')
        self.duplicateButton = QPushButton('Duplicate')
        self.importButton = QPushButton('Import')
        self.exportButton = QPushButton('Export')
        self.removeButton = QPushButton('Remove')
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.duplicateButton)
        self.layout.addWidget(self.importButton)
        self.layout.addWidget(self.exportButton)
        self.layout.addWidget(self.removeButton)
        self.layout.addStretch()

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = CommandButtons()
    main.show()
    sys.exit(app.exec_())
