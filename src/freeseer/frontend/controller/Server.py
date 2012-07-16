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
import sys
import base64

from PyQt4 import QtCore, QtGui, QtNetwork

from PyQt4.QtNetwork import QTcpServer, QHostAddress

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

PORT = 55441

class ServerWidget(QtGui.QWidget):
    
    status = 'Off' 
    clients = []
    passPhrase = 'pass'
    
    def __init__(self):
        QtGui.QWidget.__init__(self) 
        self.resize(400, 400)
        self.server = QTcpServer(self)
        
        self.startButton = QtGui.QPushButton('Start', self)
        self.startButton.move(25, 70)
        
        self.statusLabel = QtGui.QLabel('Server status:' + self.status, self)
        self.statusLabel.move(25, 20)
        self.statusLabel.resize(200, 10)
        
        self.statusLabel2 = QtGui.QLabel('', self)
        self.statusLabel2.move(25, 45)
        self.statusLabel2.resize(200, 25)
        
        self.messageLine = QtGui.QLineEdit(self)
        self.messageLine.move(190, 10)
        
        self.messageButton = QtGui.QPushButton('Send Message', self)
        self.messageButton.setEnabled(False)
        self.messageButton.move(320, 10)
        
        self.passPhraseLabel = QtGui.QLabel('Passphrase:' + self.passPhrase, self)
        self.passPhraseLabel.move(190, 40)
        
        self.passPhraseEdit = QtGui.QLineEdit(self)
        self.passPhraseEdit.move(190, 60)
        
        self.passPhraseButton = QtGui.QPushButton('Set Passphrase', self)
        self.passPhraseButton.setEnabled(False)
        self.passPhraseButton.move(320, 60)
        
        self.ipLabel = QtGui.QLabel('IP Address', self)
        self.ipLabel.move(25, 110)
        
        self.connectionLabel = QtGui.QLabel('Connection', self)
        self.connectionLabel.move(115, 110)
        
        self.controlLabel = QtGui.QLabel('Control', self)
        self.controlLabel.move(205, 110)
        
        self.qListWidget = QtGui.QListWidget(self)
        self.qListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.qListWidget.move(25, 140)
        self.qListWidget.resize(256, 192)
        
        self.startRecordButton = QtGui.QPushButton('Start Recording', self)
        self.startRecordButton.move(300, 140)
        
        self.pauseRecordButton = QtGui.QPushButton('Pause Recording', self)
        self.pauseRecordButton.move(300, 190)
        
        self.stopRecordButton = QtGui.QPushButton('Stop Recording', self)
        self.stopRecordButton.move(300, 240)
        
        self.disconnectButton = QtGui.QPushButton('Disconnect', self)
        self.disconnectButton.move(300, 290)
        self.disconnectButton.setEnabled(False)
          
        #Connections
        self.connect(self.server, QtCore.SIGNAL('newConnection()'), self.acceptConnection)  
        self.connect(self.startButton, QtCore.SIGNAL('pressed()'), self.startServer)
        self.connect(self.messageLine, QtCore.SIGNAL('textEdited(QString)'), self.enableMessageButton)
        self.connect(self.messageButton, QtCore.SIGNAL('pressed()'), self.sendCustomMessage)
        self.connect(self.passPhraseEdit, QtCore.SIGNAL('textEdited(QString)'), self.enablePassphraseButton)
        self.connect(self.passPhraseButton, QtCore.SIGNAL('pressed()'), self.setPassPhrase)
        self.connect(self.startRecordButton, QtCore.SIGNAL('pressed()'), self.sendRecordCommand)
        self.connect(self.disconnectButton, QtCore.SIGNAL('pressed()'), self.disconnectClients)
        self.connect(self.qListWidget, QtCore.SIGNAL('itemSelectionChanged()'), self.enableDisconnectButton)
        
    def startServer(self):    
        if self.status == 'Off':
            self.server.listen(QHostAddress.Any, PORT)    
            self.startButton.setText(QtCore.QString('Stop'))
            self.status = 'Running' 
            string = 'IP:' + self.server.serverAddress().toString() + ' Port:' + str(self.server.serverPort())
            logging.info("Started server IP:%s Port:%s", self.server.serverAddress().toString(), str(self.server.serverPort()))
            self.statusLabel2.setText(QtCore.QString(string))
        elif self.status == 'Running':
            self.server.close()
            self.startButton.setText(QtCore.QString('Start'))
            self.status = 'Off'
        self.statusLabel.setText('Server status:' + self.status)
    
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
    
    def enableDisconnectButton(self):
        if len(self.qListWidget.selectedItems()) > 0:
            self.disconnectButton.setEnabled(True)
        else:
            self.disconnectButton.setEnabled(False) 
    
    def startRead(self):
        #self.client.writeData('Hello Client!')
        client = QtCore.QObject.sender(self)
        message = client.read(client.bytesAvailable())   
        logging.info("Client said: %s", message)
        print 'Client said:', message
        return message
    
    def disconnected(self):
        print 'Client disconnected' 
    
    def sendMessage(self, client, message):
        block = QtCore.QByteArray()
        block.append(message)
        client.write(block)
    
    def sendCustomMessage(self):
        #block = QtCore.QByteArray()
        #block.append(self.messageLine.text())
        for i in range(0, len(self.clients)):
            client = self.clients.pop(i)
            self.clients.insert(i, client)
            self.sendMessage(client, self.messageLine.text())
            #client.write(block)
    
    def readMessage(self):
        client = self.server.nextPendingConnection()
        passPhrase = client.read(client.bytesAvailable())
        print passPhrase
    
    def setPassPhrase(self):
        self.passPhrase = self.passPhraseEdit.text()
        logging.info ("Passphrase changed to %s", self.passPhraseEdit.text())
        self.passPhraseLabel.setText("Passphrase:" + self.passPhrase)
        self.passPhraseEdit.clear()
    
    def readPassPhrase(self):
        #self.client.writeData('Hello Client!')
        #when successful disconnect and connect
        client = QtCore.QObject.sender(self)
        message = client.read(client.bytesAvailable())   
        logging.info("Client said: %s", message)
        print 'Client said:', message
        if message != self.passPhrase:
            client.disconnectFromHost()
            print 'Client rejected'
        else:
            #self.clients.append(client)
            #self.updateList()
            self.addClientToList(client)
            print 'Client accepted'
            self.disconnect(client, QtCore.SIGNAL('readyRead()'), self.readPassPhrase)
            self.connect(client, QtCore.SIGNAL('readyRead()'), self.startRead)
        
    #
    #This is the function to handle a new connection.
    #
    def acceptConnection(self):
        client = self.server.nextPendingConnection()
        self.connect(client, QtCore.SIGNAL("disconnected()"), self.clientDisconnected)
        self.connect(client, QtCore.SIGNAL('readyRead()'), self.readPassPhrase)
        #self.clients.append(client)
        #self.updateList()
    
    def clientDisconnected(self):
        print 'Client Disconnected'
        client = QtCore.QObject.sender(self)
        self.removeClientFromTheList(client)
        #self.clients.remove(client)
        logging.info("Client %s disconnected", client.localAddress().toString())
        
        #self.updateList()
    #
    #This method is to update the 
    #
    def updateList(self):
        self.qListWidget.clear()
        for i in range(0, len(self.clients)):
            client = self.clients[i]
            listItem = ServerListWidget(client)
            self.qListWidget.addItem(listItem)
            #self.qListWidget.setItemWidget(listItem, QtGui.QCheckBox())
            clientLabel = QtGui.QLabel('F1', self)
            clientLabel.move(5 + (i * 20), 150)
    
    def addClientToList(self, client):
        self.clients.append(object)
        listItem = ServerListWidget(client)
        self.qListWidget.addItem(listItem)
    
    def removeClientFromTheList(self, client):
        #self.clients.remove(client)
        index = 0
        for i in range(0, self.qListWidget.count()):
            item = self.qListWidget.item(i)
            if item.client == client:
                index = i
                break
        self.qListWidget.removeItemWidget(self.qListWidget[i])

    #
    #Sends a record command to the selected clients
    #     
    def sendRecordCommand (self):
        print 'Record sent to', 
        for i in range(0, len(self.qListWidget.selectedItems())):
            client = self.qListWidget.selectedItems()[i].client
            self.sendMessage(client, 'Record')
    #
    #Sends a pause command to the selected clients
    #
    def sendPauseCommand (self):
        print 'Record sent to', 
        for i in range(0, len(self.qListWidget.selectedItems())):
            client = self.qListWidget.selectedItems()[i].client
            self.sendMessage(client, 'Pause')
    
    #
    #Sends a stop command to selected clients
    #
    def sendStopCommand (self):
        print 'Record sent to', 
        for i in range(0, len(self.qListWidget.selectedItems())):
            client = self.qListWidget.selectedItems()[i].client
            self.sendMessage(client, 'Stop')
    
    def getClientFromList(self, ip):
        for i in range(0, len(self.clients)):
            if self.clients[i].localAddress().toString() == ip:
                self.sendMessage(self.clients[i], 'Record')
    #
    #Method to disconnect all clients selected from the list
    #
    def disconnectClients(self):
        for i in range(0, len(self.qListWidget.selectedItems())):
            client = self.qListWidget.selectedItems()[i].client
            client.disconnectFromHost()          
    
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
        
        self.setWindowTitle('Server')
        self.setGeometry(300, 300, 450, 450)
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

#Custom QListWidgetItem class
#Additionally it includes a client object
class ServerListWidget(QtGui.QListWidgetItem):
    def __init__(self, client):
        QtGui.QWidgetItem.__init__(self)
        self.client = client
        self.setText(self.client.localAddress().toString())