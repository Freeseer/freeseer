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

from PyQt4 import QtCore, QtGui


class ControllerClientWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.statusLabel = QtGui.QLabel("Status: ")
        self.mainLayout.addWidget(self.statusLabel)

        #
        # Configuration Layout
        #
        self.configLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(self.configLayout)

        self.toolBox = QtGui.QToolBox()
        self.mainLayout.addWidget(self.toolBox)

        #
        # Connection Settings
        #

        self.connWidget = QtGui.QWidget()
        self.connLayout = QtGui.QGridLayout()
        self.connWidget.setLayout(self.connLayout)
        self.toolBox.addItem(self.connWidget, "Connection Settings")

        self.hostLabel = QtGui.QLabel("Host name (or IP Address)")
        self.hostEdit = QtGui.QLineEdit()
        self.hostEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.hostLabel.setBuddy(self.hostEdit)
        self.portLabel = QtGui.QLabel("Port")
        self.portEdit = QtGui.QSpinBox()
        self.portEdit.setMaximum(65535)
        self.portEdit.setValue(55441)
        self.portLabel.setBuddy(self.portEdit)
        self.connLayout.addWidget(self.hostLabel, 0, 0)
        self.connLayout.addWidget(self.portLabel, 0, 1)
        self.connLayout.addWidget(self.hostEdit, 1, 0)
        self.connLayout.addWidget(self.portEdit, 1, 1)

        self.passLabel = QtGui.QLabel("Passphrase")
        self.passEdit = QtGui.QLineEdit()
        self.passEdit.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.passLabel.setBuddy(self.passEdit)
        self.connectButton = QtGui.QPushButton("Connect")
        self.connLayout.addWidget(self.passLabel, 2, 0)
        self.connLayout.addWidget(self.passEdit, 3, 0)
        self.connLayout.addWidget(self.connectButton, 3, 1)

        #
        # Recent Connections
        #

        self.recentConnList = QtGui.QTableView()
        self.recentConnList.setShowGrid(False)
        self.recentConnList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.toolBox.addItem(self.recentConnList, "Recent Connections")

        #
        # Qt Connections
        #

        self.connect(self.hostEdit, QtCore.SIGNAL("textEdited(const QString &)"), self.copy_settings)

    def copy_settings(self, value):
        """
        Copies settings in the Host field to port and passphrase if the string format is correct

        Format: passphrase@host:port
        """

        if ":" in value and "@" in value:
            splitport = str(value).rsplit(":", 1)
            splitpass = splitport[0].rsplit("@", 1)

            host = splitpass[1]
            port = int(splitport[1])
            passphrase = splitpass[0]

            # set the appropriate config boxes
            self.hostEdit.setText(host)
            self.portEdit.setValue(port)
            self.passEdit.setText(passphrase)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = ControllerClientWidget()
    main.show()
    sys.exit(app.exec_())
