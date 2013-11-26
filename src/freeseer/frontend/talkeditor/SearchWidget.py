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

@author: Michael Brawn
'''

from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QIcon


class SearchWidget(QWidget):

    def __init__(self, parent=None):
        super(SearchWidget, self).__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.searchLineEdit = QLineEdit()
        self.searchIcon = QIcon.fromTheme("edit-find")
        self.searchButton = QPushButton('Search')
        self.searchButton.setIcon(self.searchIcon)
        
        self.layout.addStretch()
        self.layout.addWidget(self.searchLineEdit)
        self.layout.addWidget(self.searchButton)

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = SearchWidget()
    main.show()
    sys.exit(app.exec_())
