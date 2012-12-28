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

import logging
import os

from passlib.apps import custom_app_context as pwd_context

from PyQt4 import QtCore, QtGui
from PyQt4.QtNetwork import QTcpServer, QHostAddress

from freeseer.framework.logger import Logger
from ServerWidget import ControllerServerWidget
from Client import COMMANDS

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

PORT = 55441

CLIENT_STATUS = ["Stopped",
                 "Recording",
                 "Paused",
                 "Idle"]

class ServerApp(QtGui.QMainWindow):
    
    STATUS = ["Offline",
              "Online"]

    status = STATUS[0]
    clients = []
    passPhrase = ''
    ipAddress = None
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(400, 300)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        self.logger = Logger(configdir)
        logging.info("Logger initialized")
        
        self.server = QTcpServer(self)
        logging.info("Starting Freeseer Server")
        
        # Setup Widget
        self.mainWidget = ControllerServerWidget()
        self.setCentralWidget(self.mainWidget)
        
        self.mainWidget.hostCombo.addItem(QtCore.QString("0.0.0.0"))
                
        #Connections
        self.connect(self.server, QtCore.SIGNAL('newConnection()'), self.acceptConnection)  
        self.connect(self.mainWidget.startButton, QtCore.SIGNAL('pressed()'), self.startServer)
        self.connect(self.mainWidget.hostCombo, QtCore.SIGNAL('currentIndexChanged(int)'), self.ipComboBoxHandler)
        
        # Client Control
        self.connect(self.mainWidget.clientStartButton, QtCore.SIGNAL('pressed()'), self.sendRecordCommand)
        self.connect(self.mainWidget.clientStopButton, QtCore.SIGNAL('pressed()'), self.sendStopCommand)
        self.connect(self.mainWidget.clientDisconnectButton, QtCore.SIGNAL('pressed()'), self.disconnectClients)
        self.connect(self.mainWidget.clientList, QtCore.SIGNAL('itemSelectionChanged()'), self.updateButtons)
        
    ###
    ### Server Methods
    ###
    
    def startServer(self):    
        if self.status == self.STATUS[0]:   # Check if status is Offline
            if self.ipAddress is None:
                self.ipAddress = QHostAddress(self.mainWidget.hostCombo.currentText())
            self.server.listen(self.ipAddress, PORT)    
            self.mainWidget.startButton.setText(QtCore.QString('Stop Server'))
            self.status = self.STATUS[1]    # Set Running
            logging.info("Started server %s: %s", self.server.serverAddress().toString(), str(self.server.serverPort()))
            self.mainWidget.hostCombo.setEnabled(False)
            
        elif self.status == self.STATUS[1]:      # Check if status is Online
            self.server.close()
            self.mainWidget.startButton.setText(QtCore.QString('Start Server'))
            self.status = self.STATUS[0]         # Set status Offline
            self.disconnectAllClients()
            self.mainWidget.hostCombo.setEnabled(True)
            self.ipAddress = None
            
        self.mainWidget.statusLabel.setText('Server status: ' + self.status)
        self.setPassPhrase()
        self.setConnectionLabel()
        
    def setConnectionLabel(self):
        text = "%s:%s" % (self.mainWidget.hostCombo.currentText(),
                          self.mainWidget.portEdit.text())
        self.mainWidget.settingsEdit.setText(text)

        if self.mainWidget.passEdit.text():
            self.mainWidget.settingsEdit.setText("%s@%s" % (self.mainWidget.passEdit.text(),
                                                            text))
    
    def updateButtons(self):
        if len(self.mainWidget.clientList.selectedItems()) > 0:
            self.mainWidget.clientDisconnectButton.setEnabled(True)
            self.mainWidget.clientStartButton.setEnabled(True)
            
            for i in range(0, len(self.mainWidget.clientList.selectedItems())):
                clientStatus = self.mainWidget.clientList.selectedItems()[i].status
                logging.debug("Client status: %s", clientStatus)
                
                if clientStatus == CLIENT_STATUS[1]:    # Client is Recording
                    self.mainWidget.clientStartButton.setText('Pause Recording')
                    self.mainWidget.clientStopButton.setEnabled(True)
                    
                elif clientStatus == CLIENT_STATUS[3]:  # Client is Idle
                    self.mainWidget.clientStartButton.setText('Start Recording')
                    self.mainWidget.clientStopButton.setEnabled(False)
                    
                elif clientStatus == CLIENT_STATUS[2]:  # Client is Paused
                    self.mainWidget.clientStartButton.setText('Resume Recording')
                    self.mainWidget.clientStopButton.setEnabled(True)
                    
        else:
            self.mainWidget.clientDisconnectButton.setEnabled(False)
            self.mainWidget.clientStartButton.setEnabled(False)
            self.mainWidget.clientStartButton.setText('Start Recording')
            self.mainWidget.clientStopButton.setEnabled(False) 
            self.mainWidget.clientStopButton.setText('Stop Recording')
    
    def startRead(self):
        client = QtCore.QObject.sender(self)
        message = client.read(client.bytesAvailable())   
        logging.info("Client said: %s", message)
        return message
    
    def sendMessage(self, client, message):
        block = QtCore.QByteArray()
        block.append(message)
        client.write(block)
        
    '''
    This function is for changing the passphrase. It saves the new passphrase in the self.passPhrase after encoding it.
    '''
    def setPassPhrase(self):
        self.passphrase = self.mainWidget.passEdit.text()
        logging.info ("Passphrase set to %s", self.passphrase)
        #self.passPhrase = base64.b64encode(self.passPhrase)
        self.passphrase = str(self.passphrase)
        self.passphrase = pwd_context.encrypt(self.passphrase)
        
    '''
    This function reads the passphrase sent from the client. It decodes the saved passphrase and the one that client sent and compares.
    Client is accepted if the passphrases match. Otherwise client is rejected
    '''  
    def readPassPhrase(self):
        client = QtCore.QObject.sender(self)
        message = client.read(client.bytesAvailable())   
        logging.info("Client said: %s", message)
        if pwd_context.verify(message, self.passphrase) is False:
            client.disconnectFromHost()
            logging.info("Client rejected")
        else:
            self.clients.append(client)
            self.updateList()
            logging.info("Client accepted")
            self.disconnect(client, QtCore.SIGNAL('readyRead()'), self.readPassPhrase)
            self.connect(client, QtCore.SIGNAL('readyRead()'), self.startRead)
            
    def ipComboBoxHandler(self):
        self.ipAddress = QHostAddress(self.ipComboBox.itemText(self.ipComboBox.currentIndex()))
        logging.info("Server IP changed to: %s", self.ipAddress.toString())
            
    ###
    ### Client List Methods
    ###
            
    '''
    This is the function to handle a new connection.
    '''
    def acceptConnection(self):
        client = self.server.nextPendingConnection()
        self.connect(client, QtCore.SIGNAL("disconnected()"), self.clientDisconnected)
        self.connect(client, QtCore.SIGNAL('readyRead()'), self.readPassPhrase)
    
    def clientDisconnected(self):
        client = QtCore.QObject.sender(self)
        logging.info("Client disconnected")
        self.clients.remove(client)
        self.updateList()
        self.updateButtons()
    
    '''
    This method is to update the list
    '''
    def updateList(self):
        self.mainWidget.clientList.clear()
        for i in range(0, len(self.clients)):
            client = self.clients[i]
            listItem = ClientListItem(client)
            self.mainWidget.clientList.addItem(listItem)
            clientLabel = QtGui.QLabel('F1', self)
            clientLabel.move(5 + (i * 20), 150)
    
    def addClientToList(self, client):
        self.clients.append(object)
        listItem = ClientListItem(client)
        self.mainWidget.clientList.addItem(listItem)
    
    def removeClientFromTheList(self, client):
        self.clients.remove(client)
        self.updateList()

    '''
    Sends a record command to the selected clients
    '''     
    def sendRecordCommand (self):
        buttonText = self.mainWidget.clientStartButton.text()
        
        # Find out what command to send
        if buttonText == 'Start Recording' or buttonText == 'Resume Recording':
            command = COMMANDS[1]   # Set Record
        elif buttonText == 'Pause Recording':
            command = COMMANDS[2]   # Set Pause
        
        # Send command
        for i in range(0, len(self.mainWidget.clientList.selectedItems())):
            c_item = self.mainWidget.clientList.selectedItems()[i]
            client = c_item.client
            self.sendMessage(client, command)
            
            if command == COMMANDS[1]:                # Check if command is Record
                c_item.changeStatus(CLIENT_STATUS[1]) # Set Recording
            elif command == COMMANDS[2]:              # Check if command is Pause
                c_item.changeStatus(CLIENT_STATUS[2]) # Set Paused
                
            logging.info("Sent  %s  command to %s" % (command, c_item.address))
                
        self.updateButtons()
    
    '''
    Sends a stop command to selected clients
    '''
    def sendStopCommand (self):
        command = COMMANDS[0]   # Set Stop command
        
        for i in range(0, len(self.mainWidget.clientList.selectedItems())):
            c_item = self.mainWidget.clientList.selectedItems()[i]
            client = c_item.client
            self.sendMessage(client, command)
            c_item.changeStatus(CLIENT_STATUS[3])  # Set Idle
            
            logging.info("Sent  %s  command to %s" % (command, c_item.address))
            
        self.updateButtons()
        
    '''
    Method to disconnect all clients selected from the list
    '''
    def disconnectClients(self):
        for i in range(0, len(self.mainWidget.clientList.selectedItems())):
            client = self.mainWidget.clientList.selectedItems()[i].client
            client.disconnectFromHost()  
    
    '''
    Method to disconnect all clients that are connected
    '''
    def disconnectAllClients(self):
        for i in range(0, self.mainWidget.clientList.count()):
            client = self.mainWidget.clientList.item(i).client
            client.disconnectFromHost()
        
'''
Custom QListWidgetItem class
Additionally it includes a client object
'''
class ClientListItem(QtGui.QListWidgetItem):
    
    def __init__(self, client):
        QtGui.QWidgetItem.__init__(self)
        self.client = client
        self.address = self.client.localAddress().toString()
        self.status = CLIENT_STATUS[3]
        self.setText(self.address + ' ' + self.status)
        
    def changeStatus(self, status):
        self.status = status
        self.setText('%s %s' % (self.address, self.status))
        