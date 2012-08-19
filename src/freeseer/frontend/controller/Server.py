#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011  Free and Open Source Software Learning Centre
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
import sys

from PyQt4 import QtCore, QtGui, QtNetwork 

from PyQt4.QtNetwork import QTcpServer, QHostAddress, QNetworkInterface

from freeseer.framework.logger import Logger

from passlib.apps import custom_app_context as pwd_context

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

PORT = 55441

class ServerWidget(QtGui.QWidget):
    
    status = 'Off' 
    clients = []
    passPhrase = ''
    ipAddress = None
    
    def __init__(self):
        QtGui.QWidget.__init__(self) 
        self.resize(400, 420)
        
        configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        self.logger = Logger(configdir)
        logging.info("Logger initialized")
        
        self.server = QTcpServer(self)
        logging.info("Starting Freeseer Server")
        self.startButton = QtGui.QPushButton('Start Server', self)
        self.startButton.move(25, 90)
       
        self.statusLabel = QtGui.QLabel('Server status:' + self.status, self)
        self.statusLabel.move(25, 15)
        self.statusLabel.resize(200, 25)
        
        self.iLabel = QtGui.QLabel('IP:', self)
        self.iLabel.move(25, 40)
        
        self.ipComboBox = QtGui.QComboBox(self)
        self.ipComboBox.addItem(QtCore.QString("0.0.0.0"))
        self.ipComboBox.move(50, 35)
        self.ipComboBox.resize(100, 35)
        
        self.portLabel = QtGui.QLabel('Port:', self)
        self.portLabel.move(25, 57)
        self.portLabel.resize(100, 40)
        
        self.statusLabel2 = QtGui.QLabel('', self)
        self.statusLabel2.move(25, 45)
        self.statusLabel2.resize(200, 25)
        
        self.messageLine = QtGui.QLineEdit(self)
        self.messageLine.move(190, 10)
        
        self.messageButton = QtGui.QPushButton('Send Message', self)
        self.messageButton.setEnabled(False)
        self.messageButton.move(320, 10)
        
        self.propertiesLabel = QtGui.QLabel('Properties:', self)
        self.propertiesLabel.move(25, 355)
        
        self.propertiesInfoButton = QtGui.QPushButton('?', self)
        self.propertiesInfoButton.move(120, 352)
        self.propertiesInfoButton.resize(20, 20)
        
        self.propertyLabel = QtGui.QTextEdit(self)
        self.propertyLabel.move(25, 375)
        self.propertyLabel.resize(256, 80)
        self.propertyLabel.setReadOnly(True)
        self.propertyLabel.setText('Host Instance:\nIP:\nPort:\nPassphrase:')
        
        self.passPhraseLabel = QtGui.QLabel('Passphrase:' + self.passPhrase, self)
        self.passPhraseLabel.move(190, 40)
        
        self.passPhraseEdit = QtGui.QLineEdit(self)
        self.passPhraseEdit.move(190, 60)
        
        self.passPhraseEdit.setText('pass')
        self.setPassPhrase()
        
        self.passPhraseButton = QtGui.QPushButton('Set Passphrase', self)
        self.passPhraseButton.setEnabled(False)
        self.passPhraseButton.move(320, 60)
        
        self.ipLabel = QtGui.QLabel('IP Address', self)
        self.ipLabel.move(25, 130)
        
        self.connectionLabel = QtGui.QLabel('Status', self)
        self.connectionLabel.move(115, 130)
        
        self.qListWidget = QtGui.QListWidget(self)
        self.qListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.qListWidget.move(25, 160)
        self.qListWidget.resize(256, 192)
        
        self.startRecordButton = QtGui.QPushButton('Start Recording', self)
        self.startRecordButton.move(300, 160)
        self.startRecordButton.setEnabled(False)
        
        self.stopRecordButton = QtGui.QPushButton('Stop Recording', self)
        self.stopRecordButton.move(300, 210)
        self.stopRecordButton.setEnabled(False)
        
        self.disconnectButton = QtGui.QPushButton('Disconnect', self)
        self.disconnectButton.move(300, 310)
        self.disconnectButton.setEnabled(False)
        
        #Connections
        self.connect(self.server, QtCore.SIGNAL('newConnection()'), self.acceptConnection)  
        self.connect(self.startButton, QtCore.SIGNAL('pressed()'), self.startServer)
        self.connect(self.messageLine, QtCore.SIGNAL('textEdited(QString)'), self.enableMessageButton)
        self.connect(self.messageButton, QtCore.SIGNAL('pressed()'), self.sendCustomMessage)
        self.connect(self.passPhraseEdit, QtCore.SIGNAL('textEdited(QString)'), self.enablePassphraseButton)
        self.connect(self.passPhraseButton, QtCore.SIGNAL('pressed()'), self.setPassPhrase)
        self.connect(self.startRecordButton, QtCore.SIGNAL('pressed()'), self.sendRecordCommand)
        self.connect(self.stopRecordButton, QtCore.SIGNAL('pressed()'), self.sendStopCommand)
        self.connect(self.disconnectButton, QtCore.SIGNAL('pressed()'), self.disconnectClients)
        self.connect(self.qListWidget, QtCore.SIGNAL('itemSelectionChanged()'), self.updateButtons)
        self.connect(self.propertiesInfoButton, QtCore.SIGNAL('pressed()'), self.showPropertiesInfo)
        self.connect(self.ipComboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.ipComboBoxHandler)
        
    def startServer(self):    
        if self.status == 'Off':
            if self.ipAddress is None:
                self.ipAddress = QHostAddress(self.ipComboBox.currentText())
            self.server.listen(self.ipAddress, PORT)    
            self.startButton.setText(QtCore.QString('Stop Server'))
            self.status = 'Running' 
            string = 'IP:' + self.server.serverAddress().toString() + ' Port:' + str(self.server.serverPort())
            self.portLabel.setText("Port:" + str(self.server.serverPort()))
            logging.info("Started server IP:%s Port:%s", self.server.serverAddress().toString(), str(self.server.serverPort()))
            self.ipComboBox.setEnabled(False)
            self.updateProperties()
        elif self.status == 'Running':
            self.server.close()
            self.startButton.setText(QtCore.QString('Start Server'))
            self.status = 'Off'
            self.disconnectAllClients()
            self.ipComboBox.setEnabled(True)
            self.ipAddress = None
        self.statusLabel.setText('Server status:' + self.status)
    
    '''
    This function is for updating the properties box when there is a change in the attributes
    '''
    def updateProperties(self):
        self.propertyLabel.setText('Host Instance:\nIP:' + self.server.serverAddress().toString() + '\nPort:' + str(self.server.serverPort())
                                    + '\nPassphrase:' + self.passPhrase2)
        
    
    def enableMessageButton(self):
        if self.messageLine == '':
            self.messageButton.setEnabled(False)
        else:
            self.messageButton.setEnabled(True)
    
    def enablePassphraseButton(self):
        if self.passPhraseEdit == '':
            self.passPhraseButton.setEnabled(False)
        else:
            self.passPhraseButton.setEnabled(True)
    
    def updateButtons(self):
        if len(self.qListWidget.selectedItems()) > 0:
            self.disconnectButton.setEnabled(True)
            self.startRecordButton.setEnabled(True)
            for i in range(0, len(self.qListWidget.selectedItems())):
                clientStatus = self.qListWidget.selectedItems()[i].status
                logging.info("Client status:%s", clientStatus)
                if clientStatus == 'Recording':
                    logging.info("Client recording")
                    self.startRecordButton.setText('Pause Recording')
                    self.stopRecordButton.setEnabled(True)
                elif clientStatus == 'Idle':
                    self.startRecordButton.setText('Start Recording')
                    self.stopRecordButton.setEnabled(False)
                elif clientStatus == 'Paused':
                    self.startRecordButton.setText('Resume Recording')
                    self.stopRecordButton.setEnabled(True)
        else:
            self.disconnectButton.setEnabled(False)
            self.startRecordButton.setEnabled(False)
            self.startRecordButton.setText('Start Recording')
            self.stopRecordButton.setEnabled(False) 
            self.stopRecordButton.setText('Stop Recording')
    
    def startRead(self):
        client = QtCore.QObject.sender(self)
        message = client.read(client.bytesAvailable())   
        logging.info("Client said: %s", message)
        return message
    
    def sendMessage(self, client, message):
        block = QtCore.QByteArray()
        block.append(message)
        client.write(block)
    
    def sendCustomMessage(self):
        for i in range(0, len(self.clients)):
            client = self.clients.pop(i)
            self.clients.insert(i, client)
            self.sendMessage(client, self.messageLine.text())
        
    '''
    This function is for changing the passphrase. It saves the new passphrase in the self.passPhrase after encoding it.
    '''
    def setPassPhrase(self):
        self.passPhrase = self.passPhraseEdit.text()
        logging.info ("Passphrase changed to %s", self.passPhraseEdit.text())
        self.passPhraseLabel.setText("Passphrase:" + self.passPhrase)
        self.passPhraseEdit.clear()
        #self.passPhrase = base64.b64encode(self.passPhrase)
        self.passPhrase = str(self.passPhrase)
        self.passPhrase2 = self.passPhrase
        self.passPhrase = pwd_context.encrypt(self.passPhrase)
        self.updateProperties()
        
    
    '''
    This function reads the passphrase sent from the client. It decodes the saved passphrase and the one that client sent and compares.
    Client is accepted if the passphrases match. Otherwise client is rejected
    '''  
    def readPassPhrase(self):
        client = QtCore.QObject.sender(self)
        message = client.read(client.bytesAvailable())   
        logging.info("Client said: %s", message)
        if pwd_context.verify(message, self.passPhrase) is False:
            client.disconnectFromHost()
            logging.info("Client rejected")
        else:
            self.clients.append(client)
            self.updateList()
            logging.info("Client accepted")
            self.disconnect(client, QtCore.SIGNAL('readyRead()'), self.readPassPhrase)
            self.connect(client, QtCore.SIGNAL('readyRead()'), self.startRead)
            
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
        self.qListWidget.clear()
        for i in range(0, len(self.clients)):
            client = self.clients[i]
            listItem = ServerListWidget(client)
            self.qListWidget.addItem(listItem)
            clientLabel = QtGui.QLabel('F1', self)
            clientLabel.move(5 + (i * 20), 150)
    
    def addClientToList(self, client):
        self.clients.append(object)
        listItem = ServerListWidget(client)
        self.qListWidget.addItem(listItem)
    
    def removeClientFromTheList(self, client):
        self.clients.remove(client)
        self.updateList()

    '''
    Sends a record command to the selected clients
    '''     
    def sendRecordCommand (self):
        buttonText = self.startRecordButton.text()
        if buttonText == 'Start Recording':
            command = 'Record'
        elif buttonText == 'Pause Recording':
            command = 'Pause'
        elif buttonText == 'Resume Recording':
            command = 'Resume'
        logging.info(command + " send to") 
        for i in range(0, len(self.qListWidget.selectedItems())):
            client = self.qListWidget.selectedItems()[i].client
            self.sendMessage(client, command)
            if command == 'Record' or command == 'Resume':
                self.qListWidget.selectedItems()[i].changeStatus('Recording')
            elif command == 'Pause':
                self.qListWidget.selectedItems()[i].changeStatus('Paused')
        self.updateButtons()
    
    '''
    Sends a stop command to selected clients
    '''
    def sendStopCommand (self):
        logging.info("Stop record send to")
        for i in range(0, len(self.qListWidget.selectedItems())):
            client = self.qListWidget.selectedItems()[i].client
            self.sendMessage(client, 'Stop')
            self.qListWidget.selectedItems()[i].changeStatus('Idle')
        self.updateButtons()
    
    def getClientFromList(self, ip):
        for i in range(0, len(self.clients)):
            if self.clients[i].localAddress().toString() == ip:
                self.sendMessage(self.clients[i], 'Record')
    '''
    Method to disconnect all clients selected from the list
    '''
    def disconnectClients(self):
        for i in range(0, len(self.qListWidget.selectedItems())):
            client = self.qListWidget.selectedItems()[i].client
            client.disconnectFromHost()  
    
    '''
    Method to disconnect all clients that are connected
    '''
    def disconnectAllClients(self):
        for i in range(0, self.qListWidget.count()):
            client = self.qListWidget.item(i).client
            client.disconnectFromHost()    
    
    '''
    This shows a messagebox explaining the properties box
    '''
    def showPropertiesInfo(self):
        infoString = 'This box is for copying the connection info\n for an easy way to enter the conneciton details\non the client side. You can copy this info and send it to the client(s) to connect to this server.'
        QtGui.QMessageBox.information(self, QtCore.QString('Properties Info'), QtCore.QString(infoString))
        
    
    def ipComboBoxHandler(self):
        self.ipAddress = QHostAddress(self.ipComboBox.itemText(self.ipComboBox.currentIndex()))
        logging.info("Server IP changed to:%s", self.ipAddress.toString())
        
        
    
class ServerG(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        #
        # Translator
        #
        self.current_language = None
        self.uiTranslator = QtCore.QTranslator()
        self.uiTranslator.load(":/languages/tr_en_US.qm")
        self.langActionGroup = QtGui.QActionGroup(self)
        self.langActionGroup.setExclusive(True)
        QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'))
        self.connect(self.langActionGroup, QtCore.SIGNAL('triggered(QAction *)'), self.translate)
        # --- Translator
        
        self.setGeometry(300, 300, 450, 470)
        self.retranslate()
        
        self.mainWidget = ServerWidget()
        
        self.menubar = QtGui.QMenuBar(self.mainWidget)
        self.setMenuBar(self.menubar)
        
        self.menubar.setGeometry(QtCore.QRect(0, 0, 566, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        
        self.menuFile = QtGui.QMenu("File")
        self.menuFile.addMenu(QtGui.QMenu("Quit"))
        self.menu2 = QtGui.QMenu("Edit")
        
        exitIcon = QtGui.QIcon.fromTheme("application-exit")
        self.actionExit = QtGui.QAction(self)
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.setObjectName(QtCore.QString("Exit"))
        self.actionExit.setIcon(exitIcon)
        self.actionExit.setText(self.uiTranslator.translate("RecordApp", "&Quit"))
        
        self.menuFile.addAction(self.actionExit)
        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menu2)
        
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle('Freeseer - Server')
        
    def retranslate(self):
        self.setWindowTitle(self.uiTranslator.translate("RecordApp", "Freeseer - portable presentation recording station"))
    
    def translate(self, action):
        '''
        When a language is selected from the language menu this function is called
        The language to be changed to is retrieved
        '''
        self.current_language = str(action.data().toString()).strip("tr_").rstrip(".qm")
        
        logging.info("Switching language to: %s" % action.text())
        self.uiTranslator.load(":/languages/tr_%s.qm" % self.current_language)
        
        self.retranslate()

'''
Custom QListWidgetItem class
Additionally it includes a client object
'''
class ServerListWidget(QtGui.QListWidgetItem):
    
    def __init__(self, client):
        QtGui.QWidgetItem.__init__(self)
        self.client = client
        self.status = 'Idle'
        self.setText(self.client.localAddress().toString() + ' ' + self.status)
        
    def changeStatus(self, status):
        self.status = status
        self.setText(self.client.localAddress().toString() + ' ' + self.status)
        