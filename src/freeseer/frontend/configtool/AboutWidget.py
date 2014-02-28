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

import os
from PyQt4 import QtCore, QtGui


class AboutWidget(QtGui.QWidget):
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
        self.mainLayout.addStretch(0)

        #
        # About
        #
        self.AboutLayout = QtGui.QVBoxLayout()
        self.AboutGroupBox = QtGui.QGroupBox("About")
        self.AboutGroupBox.setLayout(self.AboutLayout)
        self.mainLayout.insertWidget(0,self.AboutGroupBox)

        # freeser info
        self.FreeseerInfo = QtGui.QHBoxLayout()
        self.AboutLayout.insertWidget(0,QtGui.QLabel("<b>Freeseer</b>"))
        self.AboutLayout.insertLayout(1,self.FreeseerInfo)
          
        # freeseer logo
        self.FreeseerLogo = QtGui.QLabel()
        self.FreeseerLogo.setGeometry(0,0,48,48)
        self.FreeseerLogo.setPixmap(QtGui.QPixmap(os.getcwd() + "/data/freeseer_48x48.png"))
        self.FreeseerInfo.insertWidget(0,self.FreeseerLogo)

        # freeseer description
        self.LeftBox = QtGui.QVBoxLayout()
        self.FreeseerInfo.insertLayout(1,self.LeftBox)
        self.FreeseerDescription = QtGui.QLabel("A screencaster built for conferences")
        self.LeftBox.insertWidget(0, self.FreeseerDescription)


        # Buttons
        self.ButtonLayout = QtGui.QHBoxLayout()
        self.HelpButton = QtGui.QPushButton("Get help with Freeser")
        self.ButtonLayout.insertWidget(0,self.HelpButton)
        self.IssueButton = QtGui.QPushButton("Report an issue")
        self.ButtonLayout.insertWidget(1,self.IssueButton)
        self.LeftBox.insertLayout(1,self.ButtonLayout)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = AboutWidget()
    main.show()
    sys.exit(app.exec_())
