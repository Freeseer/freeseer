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
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QIcon


class CommandButtons(QWidget):

    def __init__(self, parent=None):
        super(CommandButtons, self).__init__(parent)
        self.setWindowTitle('Unlock Talk Details')

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        #addIcon = QIcon.fromTheme("list-add")
        duplicateIcon = QIcon.fromTheme("go-jump")
        importIcon = QIcon.fromTheme("document-open")
        exportIcon = QIcon.fromTheme("document-save")
        removeIcon = QIcon.fromTheme("list-remove")
        removeAllIcon = QIcon.fromTheme("window-close")

        self.importButton = QPushButton('Import')
        self.importButton.setIcon(importIcon)
        self.exportButton = QPushButton('Export')
        self.exportButton.setIcon(exportIcon)
        self.removeButton = QPushButton('Remove')
        self.removeButton.setIcon(removeIcon)
        self.removeAllButton = QPushButton('Remove All')
        self.removeAllButton.setIcon(removeAllIcon)
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText("Search...")
        self.searchIcon = QIcon.fromTheme("edit-find")
        self.searchButton = QPushButton('Search')
        self.searchButton.setIcon(self.searchIcon)
        self.layout.addWidget(self.importButton)
        self.layout.addWidget(self.exportButton)
        self.layout.addWidget(self.removeButton)
        self.layout.addWidget(self.removeAllButton)
        self.layout.addStretch()
        self.layout.addWidget(self.searchLineEdit)
        self.layout.addWidget(self.searchButton)
        self.layout.addStretch()

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = CommandButtons()
    main.show()
    sys.exit(app.exec_())
