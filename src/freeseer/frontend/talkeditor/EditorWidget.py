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

import sys

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTableView
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget

from freeseer.frontend.qtcommon.Resource import resource_rc


class EditorWidget(QWidget):
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

        #
        # Import Layout
        #
        self.importLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.importLayout)

        self.importTypeComboBox = QComboBox()
        self.importTypeComboBox.addItem("RSS")
        self.importTypeComboBox.addItem("CSV")
        self.importLayout.addWidget(self.importTypeComboBox)

        #
        # RSS Layout
        #
        self.rssWidget = QWidget()
        self.rssLayout = QHBoxLayout()
        self.rssWidget.setLayout(self.rssLayout)

        self.rssLabel = QLabel("URL")
        self.rssLineEdit = QLineEdit()
        if hasattr(QLineEdit(), 'setPlaceholderText'):
            self.rssLineEdit.setPlaceholderText("http://www.example.com/rss")
        self.rssLabel.setBuddy(self.rssLineEdit)
        self.rssPushButton = QPushButton("Load talks from RSS")
        rss_icon = QIcon()
        rss_icon.addPixmap(QPixmap(":/multimedia/rss.png"), QIcon.Normal, QIcon.Off)
        self.rssPushButton.setIcon(rss_icon)

        self.rssLayout.addWidget(self.rssLabel)
        self.rssLayout.addWidget(self.rssLineEdit)
        self.rssLayout.addWidget(self.rssPushButton)
        self.importLayout.addWidget(self.rssWidget)

        #
        # CSV Layout
        #
        self.csvWidget = QWidget()
        self.csvWidget.hide()
        self.csvLayout = QHBoxLayout()
        self.csvWidget.setLayout(self.csvLayout)

        self.csvLabel = QLabel("File")
        self.csvLineEdit = QLineEdit()

        if sys.platform == 'win32':
            if hasattr(QLineEdit(), 'setPlaceholderText'):
                self.csvLineEdit.setPlaceholderText("C:\Example\Freeseer2011.csv")
        else:
            if hasattr(QLineEdit(), 'setPlaceholderText'):
                self.csvLineEdit.setPlaceholderText("/home/freeseer/Example/Freeseer2011.csv")
        self.csvLabel.setBuddy(self.csvLineEdit)
        self.csvFileSelectButton = QToolButton()
        self.csvFileSelectButton.setText("...")
        self.csvPushButton = QPushButton("Load talks from CSV")

        self.csvLayout.addWidget(self.csvLabel)
        self.csvLayout.addWidget(self.csvLineEdit)
        self.csvLayout.addWidget(self.csvFileSelectButton)
        self.csvLayout.addWidget(self.csvPushButton)
        self.importLayout.addWidget(self.csvWidget)

        #
        # Editor Layout
        #
        self.editorLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.editorLayout)

        self.buttonsLayout = QVBoxLayout()
        self.editorLayout.addLayout(self.buttonsLayout)

        addIcon = QIcon.fromTheme("list-add")
        removeIcon = QIcon.fromTheme("list-remove")
        clearIcon = QIcon.fromTheme("edit-clear")
        closeIcon = QIcon.fromTheme("application-exit")

        self.addButton = QPushButton("Add")
        self.addButton.setIcon(addIcon)
        self.removeButton = QPushButton("Remove")
        self.removeButton.setIcon(removeIcon)
        self.clearButton = QPushButton("Clear")
        self.clearButton.setIcon(clearIcon)
        self.closeButton = QPushButton("Close")
        self.closeButton.setIcon(closeIcon)
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.removeButton)
        self.buttonsLayout.addWidget(self.clearButton)
        self.buttonsLayout.addStretch(0)
        self.buttonsLayout.addWidget(self.closeButton)

        self.editor = QTableView()
        self.editor.setAlternatingRowColors(True)
        self.editor.setSortingEnabled(True)
        self.editorLayout.addWidget(self.editor)

        #
        # Widget Connections
        #

        self.connect(self.importTypeComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.switch_import_plugin)

    def switch_import_plugin(self, plugin):
        self.rssWidget.hide()
        self.csvWidget.hide()

        if plugin == "RSS":
            self.rssWidget.show()
        elif plugin == "CSV":
            self.csvWidget.show()

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = EditorWidget()
    main.show()
    sys.exit(app.exec_())
