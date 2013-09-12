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

        boldFont = QtGui.QFont()
        boldFont.setBold(True)

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

        self.infoLayout = QtGui.QFormLayout()
        self.editorLayout.addLayout(self.infoLayout)

        self.titleLabel = QtGui.QLabel("Title :")
        self.titleLabel2 = QtGui.QLabel()
        self.titleLabel2.setFont(boldFont)
        self.speakerLabel = QtGui.QLabel("Speaker :")
        self.speakerLabel2 = QtGui.QLabel()
        self.speakerLabel2.setFont(boldFont)
        self.descriptionLabel = QtGui.QLabel("Description :")
        self.descriptionLabel2 = QtGui.QLabel()
        self.descriptionLabel2.setFont(boldFont)
        self.levelLabel = QtGui.QLabel("Level :")
        self.levelLabel2 = QtGui.QLabel()
        self.levelLabel2.setFont(boldFont)
        self.eventLabel = QtGui.QLabel("Event :")
        self.eventLabel2 = QtGui.QLabel()
        self.eventLabel2.setFont(boldFont)
        self.roomLabel = QtGui.QLabel("Room :")
        self.roomLabel2 = QtGui.QLabel()
        self.roomLabel2.setFont(boldFont)
        self.timeLabel = QtGui.QLabel("Time :")
        self.timeLabel2 = QtGui.QLabel()
        self.timeLabel2.setFont(boldFont)

        self.infoLayout.addRow(self.titleLabel, self.titleLabel2)
        self.infoLayout.addRow(self.speakerLabel, self.speakerLabel2)
        self.infoLayout.addRow(self.descriptionLabel, self.descriptionLabel2)
        self.infoLayout.addRow(self.levelLabel, self.levelLabel2)
        self.infoLayout.addRow(self.eventLabel, self.eventLabel2)
        self.infoLayout.addRow(self.roomLabel, self.roomLabel2)
        self.infoLayout.addRow(self.timeLabel, self.timeLabel2)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = ReportEditorWidget()
    main.show()
    sys.exit(app.exec_())
