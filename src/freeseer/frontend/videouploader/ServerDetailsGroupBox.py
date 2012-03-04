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

@author: Jordan Klassen
'''

from PyQt4 import QtCore, QtGui
from freeseer.framework import const

class ServerDetailsGroupBox(QtGui.QGroupBox):
    '''
    classdocs
    '''
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QGroupBox.__init__(self, parent)
        
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.formLayout_serverdetails = QtGui.QFormLayout()
        self.formLayout_serverdetails.setObjectName("formLayout_serverdetails")
        
        self.label_username = QtGui.QLabel(self)
        self.label_username.setObjectName("label_username")
        self.formLayout_serverdetails.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_username)
        
        self.label_password = QtGui.QLabel(self)
        self.label_password.setObjectName("label_password")
        self.formLayout_serverdetails.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_password)
        
        self.label_Server = QtGui.QLabel(self)
        self.label_Server.setObjectName("label_Server")
        self.formLayout_serverdetails.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_Server)
        
        self.lineEdit_username = QtGui.QLineEdit(self)
        self.label_username.setBuddy(self.lineEdit_username)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.formLayout_serverdetails.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_username)
        
        self.lineEdit_password = QtGui.QLineEdit(self)
        self.lineEdit_password.setText("")
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.Password)
        self.label_password.setBuddy(self.lineEdit_password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout_serverdetails.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_password)
        
        self.horizontalLayout_serveraddress = QtGui.QHBoxLayout()
        self.horizontalLayout_serveraddress.setObjectName("horizontalLayout_serveraddress")
        
        self.lineEdit_Server = QtGui.QLineEdit(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Server.sizePolicy().hasHeightForWidth())
        self.lineEdit_Server.setSizePolicy(sizePolicy)
        self.lineEdit_Server.setMinimumSize(QtCore.QSize(150, 0))
        self.label_Server.setBuddy(self.lineEdit_Server)
        self.lineEdit_Server.setObjectName("lineEdit_Server")
        self.horizontalLayout_serveraddress.addWidget(self.lineEdit_Server)
        
        self.label_port = QtGui.QLabel(self)
        self.label_port.setObjectName("label_port")
        self.horizontalLayout_serveraddress.addWidget(self.label_port)
        
        self.lineEdit_port = QtGui.QLineEdit(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_port.sizePolicy().hasHeightForWidth())
        self.lineEdit_port.setSizePolicy(sizePolicy)
        self.lineEdit_port.setMinimumSize(QtCore.QSize(50, 0))
        self.label_port.setBuddy(self.lineEdit_port)
        self.lineEdit_port.setText(str(const.SFTP_DEFAULT_PORT))
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.horizontalLayout_serveraddress.addWidget(self.lineEdit_port)
        
        self.text_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r".+"), self)
        self.port_validator = QtGui.QIntValidator(1, 65535, self)
        
        self.formLayout_serverdetails.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_serveraddress)
        
        self.verticalLayout.addLayout(self.formLayout_serverdetails)
        
        self.horizontalLayout_servertype = QtGui.QHBoxLayout()
        self.horizontalLayout_servertype.setObjectName("horizontalLayout_servertype")
        
        self.radioButton_sftp = QtGui.QRadioButton(self)
        self.radioButton_sftp.setObjectName("radioButton_sftp")
        self.horizontalLayout_servertype.addWidget(self.radioButton_sftp)
        
        self.radioButton_drupal = QtGui.QRadioButton(self)
        self.radioButton_drupal.setObjectName("radioButton_drupal")
        self.horizontalLayout_servertype.addWidget(self.radioButton_drupal)
        
        self.buttonGroup_serverType = QtGui.QButtonGroup(self)
        self.buttonGroup_serverType.addButton(self.radioButton_sftp)
        self.buttonGroup_serverType.addButton(self.radioButton_drupal)
        
        self.verticalLayout.addLayout(self.horizontalLayout_servertype)
        
        self.retranslate()
        
        # radiobutton mapping #
        self.serverType_button_mapping = {const.Sftp:   self.radioButton_sftp,
                                          const.Drupal: self.radioButton_drupal}
        
        self.button_serverType_mapping = dict(reversed(item) for item in self.serverType_button_mapping.items())
        
        self.buttonGroup_serverType.buttonClicked.connect(self.onServerTypeChange)
    
    @QtCore.pyqtSlot(QtGui.QAbstractButton)
    def onServerTypeChange(self, button):
        servertype = self.button_serverType_mapping[button]
        self.lineEdit_port.setEnabled(servertype == const.Sftp)
        self.label_port.setEnabled(servertype == const.Sftp)
        
        
    def retranslate(self):
        self.setTitle(self.tr("Server Details"))
        self.label_username.setText(self.tr("&Username"))
        self.label_password.setText(self.tr("&Password"))
        self.label_Server.setText(self.tr("&Server"))
        self.label_port.setText(self.tr("P&ort"))
        self.radioButton_sftp.setText(self.tr("SF&TP/SCP"))
        self.radioButton_drupal.setText(self.tr("&Drupal"))
        
    def getUsername(self):
        return self.lineEdit_username.text()
    def setUsername(self, value):
        self.lineEdit_username.setText(value)
    username = property(getUsername, setUsername)
    
    def getPassword(self):
        return self.lineEdit_password.text()
    password = property(getPassword)
    
    def getServerAddress(self):
        return self.lineEdit_Server.text()
    def setServerAddress(self, value):
        self.lineEdit_Server.setText(value)
    serverAddress = property(getServerAddress, setServerAddress)
    
    def getServerPort(self):
        return self.lineEdit_port.text()
    def setServerPort(self, value):
        self.lineEdit_port.setText(value)
    serverPort = property(getServerPort, setServerPort)
        
    def getServerType(self):
        if self.buttonGroup_serverType.checkedButton() == None:
            return -1 
        return self.button_serverType_mapping[self.buttonGroup_serverType.checkedButton()]
    def setServerType(self, value):
        self.serverType_button_mapping[value].click()
    serverType = property(getServerType, setServerType)
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = ServerDetailsGroupBox()
    main.show()
    sys.exit(app.exec_())