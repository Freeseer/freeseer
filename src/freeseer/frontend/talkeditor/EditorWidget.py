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
http://wiki.github.com/fosslc/freeseer/

@author: Thanh Ha
'''

from PyQt4 import QtCore, QtGui

import resource_rc

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
        # RSS Layout
        #
        self.rssLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.rssLayout)
        
        self.rssLabel = QtGui.QLabel(self.tr("URL"))
        self.rssLineEdit = QtGui.QLineEdit()
        self.rssLabel.setBuddy(self.rssLineEdit)
        self.rssPushButton = QtGui.QPushButton(self.tr("Load talks from RSS"))
        rss_icon = QtGui.QIcon()
        rss_icon.addPixmap(QtGui.QPixmap(":/multimedia/rss.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rssPushButton.setIcon(rss_icon)
        
        self.rssLayout.addWidget(self.rssLabel)
        self.rssLayout.addWidget(self.rssLineEdit)
        self.rssLayout.addWidget(self.rssPushButton)
        
        #
        # Editor Layout
        #
        self.editorLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.editorLayout)
        
        self.buttonsLayout = QtGui.QVBoxLayout()
        self.editorLayout.addLayout(self.buttonsLayout)
        
        self.addButton = QtGui.QPushButton(self.tr("Add"))
        self.removeButton = QtGui.QPushButton(self.tr("Remove"))
        self.clearButton = QtGui.QPushButton(self.tr("Clear"))
        self.closeButton = QtGui.QPushButton(self.tr("Close"))
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.removeButton)
        self.buttonsLayout.addWidget(self.clearButton)
        self.buttonsLayout.addStretch(0)
        self.buttonsLayout.addWidget(self.closeButton)
        
        self.editor = QtGui.QTableView()
        self.editorLayout.addWidget(self.editor)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = EditorWidget()
    main.show()
    sys.exit(app.exec_())
