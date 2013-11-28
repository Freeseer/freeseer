#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

Copyright (C) 2011, 2013 Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/Freeseer/freeseer/

@author: Michael Brawn, Thanh Ha
'''

from PyQt4 import QtCore, QtGui
import sys


class ImportTalksWidget(QtGui.QWidget):

    '''classdocs'''
    def __init__(self, parent=None):
        '''Constructor'''
        QtGui.QWidget.__init__(self, parent)
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.importTalksGroupBox = QtGui.QGroupBox("Import Talks")

        self.importTalksLayout = QtGui.QFormLayout()
        self.importTalksGroupBox.setLayout(self.importTalksLayout)

        # Buttons
        self.importButton = QtGui.QPushButton("Import")
        self.cancelButton = QtGui.QPushButton("Cancel")

        # Radio Button Group
        self.buttonGroup = QtGui.QButtonGroup(self.mainLayout)
        self.csvRadioButton = QtGui.QRadioButton("CSV File")
        self.csvRadioButton.setChecked(True)
        self.rssRadioButton = QtGui.QRadioButton("RSS URL")
        self.buttonGroup.addButton(self.csvRadioButton)
        self.buttonGroup.addButton(self.rssRadioButton)

        # CSV Layout
        self.csvLayout = QtGui.QHBoxLayout()
        self.csvWidget = QtGui.QWidget()
        self.csvWidget.setLayout(self.csvLayout)
        self.csvLineEdit = QtGui.QLineEdit()

        if sys.platform == 'win32':
            if hasattr(QtGui.QLineEdit(), 'setPlaceholderText'):
                self.csvLineEdit.setPlaceholderText("C:\Example\Freeseer2011.csv")
        else:
            if hasattr(QtGui.QLineEdit(), 'setPlaceholderText'):
                self.csvLineEdit.setPlaceholderText("/home/freeseer/Example/Freeseer2011.csv")
        self.csvFileSelectButton = QtGui.QToolButton()
        csvFileSelectButton = QtGui.QIcon.fromTheme("folder")
        self.csvFileSelectButton.setIcon(csvFileSelectButton)

        self.csvLayout.addWidget(self.csvRadioButton)
        self.csvLayout.addWidget(self.csvLineEdit)
        self.csvLayout.addWidget(self.csvFileSelectButton)

        #
        # RSS Layout
        #
        self.rssWidget = QtGui.QWidget()
        self.rssLayout = QtGui.QHBoxLayout()
        self.rssWidget.setLayout(self.rssLayout)

        self.rssLineEdit = QtGui.QLineEdit()
        self.rssLineEdit.setEnabled(False)
        if hasattr(QtGui.QLineEdit(), 'setPlaceholderText'):
            self.rssLineEdit.setPlaceholderText("http://www.example.com/rss")
        self.rssLayout.addWidget(self.rssRadioButton)
        self.rssLayout.addWidget(self.rssLineEdit)

        #
        # Layout
        #
        self.mainLayout.addWidget(self.importTalksGroupBox)
        self.mainLayout.addWidget(self.csvWidget)
        self.mainLayout.addWidget(self.rssWidget)

        self.importCommandButtonsWidget = QtGui.QWidget()
        self.importCommandButtonsLayout = QtGui.QHBoxLayout()
        self.importCommandButtonsWidget.setLayout(self.importCommandButtonsLayout)
        self.importCommandButtonsLayout.addStretch()
        self.importCommandButtonsLayout.addWidget(self.importButton)
        self.importCommandButtonsLayout.addWidget(self.cancelButton)
        self.mainLayout.addWidget(self.importCommandButtonsWidget)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = ImportTalksWidget()
    main.show()
    sys.exit(app.exec_())
