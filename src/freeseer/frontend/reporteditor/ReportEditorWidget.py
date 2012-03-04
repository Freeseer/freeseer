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

class ReportEditorWidget(QtGui.QWidget):
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
        # ReportEditor Layout
        #
        self.editorLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.editorLayout)
        
        self.buttonsLayout = QtGui.QVBoxLayout()
        
        self.editorLayout.addLayout(self.buttonsLayout)

        
        addIcon = QtGui.QIcon.fromTheme("list-add")
        removeIcon = QtGui.QIcon.fromTheme("list-remove")
        clearIcon = QtGui.QIcon.fromTheme("edit-clear")
        closeIcon = QtGui.QIcon.fromTheme("application-exit")
        
        #self.addButton = QtGui.QPushButton("Add")
        #self.addButton.setIcon(addIcon)
        self.removeButton = QtGui.QPushButton("Remove")
        self.removeButton.setIcon(removeIcon)
        self.clearButton = QtGui.QPushButton("Clear")
        self.clearButton.setIcon(clearIcon)
        self.closeButton = QtGui.QPushButton("Close")
        self.closeButton.setIcon(closeIcon)
        #self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.removeButton)
        self.buttonsLayout.addWidget(self.clearButton)
        self.buttonsLayout.addStretch(0)
        self.buttonsLayout.addWidget(self.closeButton)
        
        self.editor = QtGui.QTableView()
        self.editor.setAlternatingRowColors(True)
        self.editor.setSortingEnabled(True)
        
        self.tableLayout = QtGui.QGridLayout()
        self.tableLayout.addWidget(self.editor)
        self.editorLayout.addLayout(self.tableLayout)
        
        self.infoLayout = QtGui.QVBoxLayout()
        self.editorLayout.addLayout(self.infoLayout)
        
        self.titleLabel = QtGui.QLabel("Title :")
        self.speakerLabel = QtGui.QLabel("Speaker :")
        self.descriptionLabel = QtGui.QLabel("Description :")
        self.levelLabel = QtGui.QLabel("Level :")
        self.eventLabel = QtGui.QLabel("Event :")
        self.roomLabel = QtGui.QLabel("Room :")
        self.timeLabel = QtGui.QLabel("Time :")
        
        self.emptyLabel = QtGui.QLabel(" "*80)
        self.infoLayout.addWidget(self.titleLabel)
        self.infoLayout.addWidget(self.speakerLabel)
        self.infoLayout.addWidget(self.descriptionLabel)
        self.infoLayout.addWidget(self.levelLabel)
        self.infoLayout.addWidget(self.eventLabel)
        self.infoLayout.addWidget(self.roomLabel)
        self.infoLayout.addWidget(self.timeLabel)
        self.infoLayout.addWidget(self.emptyLabel)
        self.infoLayout.addStretch(0)
        
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = ReportEditorWidget()
    main.show()
    sys.exit(app.exec_())
