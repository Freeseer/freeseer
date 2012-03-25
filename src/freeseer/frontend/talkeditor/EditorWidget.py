#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

Copyright (C) 2011  Free and Open Source Software Learning Centre
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

from PyQt4 import QtCore, QtGui

from freeseer.frontend.qtcommon.Resource import resource_rc

class EditorWidget(QtGui.QWidget):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        #
        # Import Layout
        #
        self.importLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.importLayout)
        
        self.importTypeComboBox = QtGui.QComboBox()
        self.importTypeComboBox.addItem("RSS")
        self.importTypeComboBox.addItem("CSV")
        self.importLayout.addWidget(self.importTypeComboBox)
        
        #
        # RSS Layout
        #
        self.rssWidget = QtGui.QWidget()
        self.rssLayout = QtGui.QHBoxLayout()
        self.rssWidget.setLayout(self.rssLayout)
        
        self.rssLabel = QtGui.QLabel("URL")
        self.rssLineEdit = QtGui.QLineEdit()
        self.rssLineEdit.setPlaceholderText("http://www.example.com/rss")
        self.rssLabel.setBuddy(self.rssLineEdit)
        self.rssPushButton = QtGui.QPushButton("Load talks from RSS")
        rss_icon = QtGui.QIcon()
        rss_icon.addPixmap(QtGui.QPixmap(":/multimedia/rss.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rssPushButton.setIcon(rss_icon)
        
        self.rssLayout.addWidget(self.rssLabel)
        self.rssLayout.addWidget(self.rssLineEdit)
        self.rssLayout.addWidget(self.rssPushButton)
        self.importLayout.addWidget(self.rssWidget)
        
        #
        # CSV Layout
        #
        self.csvWidget = QtGui.QWidget()
        self.csvWidget.hide()
        self.csvLayout = QtGui.QHBoxLayout()
        self.csvWidget.setLayout(self.csvLayout)
        
        self.csvLabel = QtGui.QLabel("File")
        self.csvLineEdit = QtGui.QLineEdit()
        self.csvLineEdit.setPlaceholderText("/home/freeseer/Example/Freeseer2011.csv")
        self.csvLabel.setBuddy(self.csvLineEdit)
        self.csvFileSelectButton = QtGui.QPushButton("Select CSV file")
        self.csvPushButton = QtGui.QPushButton("Load talks from CSV")
        
        self.csvLayout.addWidget(self.csvLabel)
        self.csvLayout.addWidget(self.csvLineEdit)
        self.csvLayout.addWidget(self.csvFileSelectButton)
        self.csvLayout.addWidget(self.csvPushButton)
        self.importLayout.addWidget(self.csvWidget)
        
        #
        # Editor Layout
        #
        self.editorLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.editorLayout)
        
        self.buttonsLayout = QtGui.QVBoxLayout()
        self.editorLayout.addLayout(self.buttonsLayout)
        
        addIcon = QtGui.QIcon.fromTheme("list-add")
        removeIcon = QtGui.QIcon.fromTheme("list-remove")
        clearIcon = QtGui.QIcon.fromTheme("edit-clear")
        closeIcon = QtGui.QIcon.fromTheme("application-exit")
        
        self.addButton = QtGui.QPushButton("Add")
        self.addButton.setIcon(addIcon)
        self.removeButton = QtGui.QPushButton("Remove")
        self.removeButton.setIcon(removeIcon)
        self.clearButton = QtGui.QPushButton("Clear")
        self.clearButton.setIcon(clearIcon)
        self.closeButton = QtGui.QPushButton("Close")
        self.closeButton.setIcon(closeIcon)
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.removeButton)
        self.buttonsLayout.addWidget(self.clearButton)
        self.buttonsLayout.addStretch(0)
        self.buttonsLayout.addWidget(self.closeButton)
        
        self.editor = QtGui.QTableView()
        self.editor.setAlternatingRowColors(True)
        self.editor.setSortingEnabled(True)
        self.editorLayout.addWidget(self.editor)
        
        #
        # Widget Connections
        #
        
        self.connect(self.importTypeComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.switch_import_plugin)
        
    def switch_import_plugin(self, plugin):
        self.rssWidget.hide()
        self.csvWidget.hide()
        
        if plugin == "RSS":
            self.rssWidget.show()
        elif plugin == "CSV":
            self.csvWidget.show()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = EditorWidget()
    main.show()
    sys.exit(app.exec_())
