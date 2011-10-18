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

class AddTalkWidget(QtGui.QWidget):
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
        
        self.addTalkGroupBox = QtGui.QGroupBox("Add Talk")
        self.mainLayout.addWidget(self.addTalkGroupBox)
        
        self.addTalkLayout = QtGui.QFormLayout()
        self.addTalkGroupBox.setLayout(self.addTalkLayout)
        
        # Title
        self.titleLabel = QtGui.QLabel("Title")
        self.titleLineEdit = QtGui.QLineEdit()
        self.titleLabel.setBuddy(self.titleLineEdit)
        self.addTalkLayout.addRow(self.titleLabel, self.titleLineEdit)
        
        # Presenter
        self.presenterLabel = QtGui.QLabel("Presenter")
        self.presenterLineEdit = QtGui.QLineEdit()
        self.presenterLabel.setBuddy(self.presenterLineEdit)
        self.addTalkLayout.addRow(self.presenterLabel, self.presenterLineEdit)
        
        # Event
        self.eventLabel = QtGui.QLabel("Event")
        self.eventLineEdit = QtGui.QLineEdit()
        self.eventLabel.setBuddy(self.eventLineEdit)
        self.addTalkLayout.addRow(self.eventLabel, self.eventLineEdit)
        
        # Room
        self.roomLabel = QtGui.QLabel("Room")
        self.roomLineEdit = QtGui.QLineEdit()
        self.roomLabel.setBuddy(self.roomLineEdit)
        self.addTalkLayout.addRow(self.roomLabel, self.roomLineEdit)
        
        # Date 
        self.dateLabel = QtGui.QLabel("Date")
        self.dateEdit = QtGui.QDateEdit()
        self.dateLabel.setBuddy(self.dateEdit)
        self.addTalkLayout.addRow(self.dateLabel, self.dateEdit)
        
        self.dateEdit.setCalendarPopup(True)
        
        # Time
        self.timeLabel = QtGui.QLabel("Time")
        self.timeEdit = QtGui.QTimeEdit()
        self.timeLabel.setBuddy(self.dateEdit)
        self.addTalkLayout.addRow(self.timeLabel, self.timeEdit)
        
        # Buttons
        self.buttonsWidget = QtGui.QHBoxLayout()
        self.addButton = QtGui.QPushButton("Add")
        self.cancelButton = QtGui.QPushButton("Cancel")
        self.buttonsWidget.addWidget(self.addButton)
        self.buttonsWidget.addWidget(self.cancelButton)
        self.addTalkLayout.addRow(None, self.buttonsWidget)
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = AddTalkWidget()
    main.show()
    sys.exit(app.exec_())
