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

from freeseer.framework.config import Config
from freeseer.framework.logger import Logger
from freeseer.frontend.qtcommon.FreeseerApp import FreeseerApp
from freeseer.frontend.qtcommon.Resource import resource_rc

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

class ServerApp(FreeseerApp):
    
    STATUS = ["Offline",
              "Online"]

    status = STATUS[0]
    clients = []
    passPhrase = ''
    ipAddress = None
    
    def __init__(self):
        FreeseerApp.__init__(self)
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
        self.connect(self.mainWidget.passEdit, QtCore.SIGNAL('textChanged(QString)'), self.onPassChanged)
        
        # Initialize Passphrase Field
        self.mainWidget.passEdit.setPlaceholderText("Passphrase required to start server")
        self.mainWidget.startButton.setEnabled(False)

        # Client Control
        self.connect(self.mainWidget.clientStartButton, QtCore.SIGNAL('pressed()'), self.sendRecordCommand)
        self.connect(self.mainWidget.clientStopButton, QtCore.SIGNAL('pressed()'), self.sendStopCommand)
        self.connect(self.mainWidget.clientDisconnectButton, QtCore.SIGNAL('pressed()'), self.disconnectClients)
        self.connect(self.mainWidget.clientList, QtCore.SIGNAL('itemSelectionChanged()'), self.updateClientButtons)
    
        self.load_settings()
        self.updateStatus(self.status)
        
    ###
    ### Translation Related
    ###
    def retranslate(self):
        self.setWindowTitle(self.uiTranslator.translate("ControllerServerApp", "Controller Server"))
        
        #
        # Reusuable Strings
        #
        self.serverStatusString = self.uiTranslator.translate("ControllerServerApp", "Server status")
        self.startServerString = self.uiTranslator.translate("ControllerServerApp", "Start Server")
        self.stopServerString = self.uiTranslator.translate("ControllerServerApp", "Stop Server")
        self.startRecordingString = self.uiTranslator.translate("ControllerServerApp", "Start Recording")
        self.stopRecordingString = self.uiTranslator.translate("ControllerServerApp", "Stop Recording")
        self.pauseRecordingString = self.uiTranslator.translate("ControllerServerApp", "Pause Recording")
        self.resumeRecordingString = self.uiTranslator.translate("ControllerServerApp", "Resume Recording")
        # --- End Reusable Strings
        
        #
        # Server Settings
        #
        self.mainWidget.toolBox.setItemText(0, self.uiTranslator.translate("ControllerServerApp", "Server Settings"))
        self.mainWidget.hostLabel.setText(self.uiTranslator.translate("ControllerServerApp", "IP Address"))
        self.mainWidget.portLabel.setText(self.uiTranslator.translate("ControllerServerApp", "Port"))
        self.mainWidget.passLabel.setText(self.uiTranslator.translate("ControllerServerApp", "Passphrase"))
        
        # Button
        if self.status == self.STATUS[0]:
            self.mainWidget.startButton.setText(self.startServerString)
        else:
            self.mainWidget.startButton.setText(self.stopServerString)
        # --- End Server Settings
        
        #
        # Control Clients
        #
        self.mainWidget.toolBox.setItemText(1, self.uiTranslator.translate("ControllerServerApp", "Control Clients"))
        self.updateClientButtons()
        self.mainWidget.clientDisconnectButton.setText(self.uiTranslator.translate("ControllerServerApp", "Disconnect"))
        # --- End Control Clients
        
    ###
    ### Server Methods
    ###
    def load_settings(self): 
        logging.info('Loading settings...')
        configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        self.config = Config(configdir)
        
        # Load default language.
        actions = self.menuLanguage.actions()
        for action in actions:
            if action.data().toString() == self.config.default_language:
                action.setChecked(True)
                self.translate(action)
                break
    
    def startServer(self):    
        if self.status == self.STATUS[0]:   # Check if status is Offline
            if self.ipAddress is None:
                self.ipAddress = QHostAddress(self.mainWidget.hostCombo.currentText())
            self.server.listen(self.ipAddress, PORT)    
            self.status = self.STATUS[1]    # Set Running            
            self.mainWidget.hostCombo.setEnabled(False)
            logging.info("Started server %s: %s", self.server.serverAddress().toString(), str(self.server.serverPort()))
            
        elif self.status == self.STATUS[1]:      # Check if status is Online
            self.server.close()
            self.status = self.STATUS[0]         # Set status Offline
            self.disconnectAllClients()
            self.mainWidget.hostCombo.setEnabled(True)
            self.ipAddress = None
            
        self.updateStatus(self.status)
        self.setPassPhrase()
        self.setConnectionLabel()
        self.retranslate()
        
    def updateStatus(self, status):
        self.mainWidget.statusLabel.setText("%s: %s" % (self.serverStatusString, status))
        
    def setConnectionLabel(self):
        text = "%s:%s" % (self.mainWidget.hostCombo.currentText(),
                          self.mainWidget.portEdit.text())
        self.mainWidget.settingsEdit.setText(text)

        if self.mainWidget.passEdit.text():
            self.mainWidget.settingsEdit.setText("%s@%s" % (self.mainWidget.passEdit.text(),
                                                            text))
        
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
    
    def onPassChanged(self):
        """Disable 'Start' button only when the passphrase field is empty."""
        if self.mainWidget.passEdit.text():
            self.mainWidget.startButton.setEnabled(True)
        else:
            self.mainWidget.startButton.setEnabled(False)
            
    def ipComboBoxHandler(self):
        self.ipAddress = QHostAddress(self.ipComboBox.itemText(self.ipComboBox.currentIndex()))
        logging.info("Server IP changed to: %s", self.ipAddress.toString())
    
    ###
    ### Messaging
    ###
    
    def startRead(self):
        client = QtCore.QObject.sender(self)
        message = client.read(client.bytesAvailable())   
        logging.info("Client said: %s", message)
        return message
    
    def sendMessage(self, client, message):
        block = QtCore.QByteArray()
        block.append(message)
        client.write(block)
            
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
        self.updateClientButtons()
    
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
        if buttonText == self.startRecordingString or buttonText == self.resumeRecordingString:
            command = COMMANDS[1]   # Set Record
        elif buttonText == self.pauseRecordingString:
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
                
        self.updateClientButtons()
    
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
            
        self.updateClientButtons()
        
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
            
    def updateClientButtons(self):
        if len(self.mainWidget.clientList.selectedItems()) > 0:
            self.mainWidget.clientDisconnectButton.setEnabled(True)
            self.mainWidget.clientStartButton.setEnabled(True)
            
            for i in range(0, len(self.mainWidget.clientList.selectedItems())):
                clientStatus = self.mainWidget.clientList.selectedItems()[i].status
                logging.debug("Client status: %s", clientStatus)
                
                if clientStatus == CLIENT_STATUS[1]:    # Client is Recording
                    self.mainWidget.clientStartButton.setText(self.pauseRecordingString)
                    self.mainWidget.clientStopButton.setEnabled(True)
                    
                elif clientStatus == CLIENT_STATUS[3]:  # Client is Idle
                    self.mainWidget.clientStartButton.setText(self.startRecordingString)
                    self.mainWidget.clientStopButton.setEnabled(False)
                    
                elif clientStatus == CLIENT_STATUS[2]:  # Client is Paused
                    self.mainWidget.clientStartButton.setText(self.resumeRecordingString)
                    self.mainWidget.clientStopButton.setEnabled(True)
                    
        else:
            self.mainWidget.clientDisconnectButton.setEnabled(False)
            self.mainWidget.clientStartButton.setEnabled(False)
            self.mainWidget.clientStartButton.setText(self.startRecordingString)
            self.mainWidget.clientStopButton.setEnabled(False) 
            self.mainWidget.clientStopButton.setText(self.stopRecordingString)
        
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
        
