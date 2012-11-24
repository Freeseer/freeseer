#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2012  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

from PyQt4 import QtGui

#from freeseer.frontend.qtcommon.Resource import resource_rc

class ControllerServerWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(400, 300)
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.statusLabel = QtGui.QLabel("Status: ")
        self.mainLayout.addWidget(self.statusLabel)
        
        #
        # Configuration Layout
        #
        self.configLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(self.configLayout)
        
        self.settingsEdit = QtGui.QLineEdit()
        self.settingsEdit.setReadOnly(True)
        self.mainLayout.addWidget(self.settingsEdit)
        
        self.toolBox = QtGui.QToolBox()
        self.mainLayout.addWidget(self.toolBox)
        
        #
        # Server Configuration
        #
        
        self.connWidget = QtGui.QWidget()
        self.connLayout = QtGui.QGridLayout()
        self.connWidget.setLayout(self.connLayout)
        self.toolBox.addItem(self.connWidget, "Server Settings")
        
        self.hostLabel = QtGui.QLabel("IP Address")
        self.hostCombo = QtGui.QComboBox()
        self.hostCombo.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.hostLabel.setBuddy(self.hostCombo)
        self.portLabel = QtGui.QLabel("Port")
        self.portEdit = QtGui.QSpinBox()
        self.portEdit.setMaximum(65535)
        self.portEdit.setValue(55441)
        self.portLabel.setBuddy(self.portEdit)
        self.connLayout.addWidget(self.hostLabel, 0, 0)
        self.connLayout.addWidget(self.portLabel, 0, 1)
        self.connLayout.addWidget(self.hostCombo, 1, 0)
        self.connLayout.addWidget(self.portEdit, 1, 1)
        
        self.passLabel = QtGui.QLabel("Passphrase")
        self.passEdit = QtGui.QLineEdit()
        self.passEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.passLabel.setBuddy(self.passEdit)
        self.startButton = QtGui.QPushButton("Start Server")
        self.connLayout.addWidget(self.passLabel, 2, 0)
        self.connLayout.addWidget(self.passEdit, 3, 0)
        self.connLayout.addWidget(self.startButton, 3, 1)
        
        #
        # Connected Clients
        #
        
        self.clientListWidget = QtGui.QWidget()
        self.toolBox.addItem(self.clientListWidget, "Control Clients")
        
        self.clientListLayout = QtGui.QHBoxLayout()
        self.clientListWidget.setLayout(self.clientListLayout)
        self.clientList = QtGui.QListWidget()
        self.clientList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.clientListLayout.addWidget(self.clientList)
        
        self.clientListButtonsLayout = QtGui.QVBoxLayout()
        self.clientListLayout.addLayout(self.clientListButtonsLayout)
        
        self.clientStartButton = QtGui.QPushButton("Start Recording")
        self.clientStopButton = QtGui.QPushButton("Stop Recording")
        self.clientDisconnectButton = QtGui.QPushButton("Disconnect")
        self.clientListButtonsLayout.addWidget(self.clientStartButton)
        self.clientListButtonsLayout.addWidget(self.clientStopButton)
        self.clientListButtonsLayout.addWidget(self.clientDisconnectButton)
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = ControllerServerWidget()
    main.show()
    sys.exit(app.exec_())
