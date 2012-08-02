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
import sqlite3

from PyQt4 import QtNetwork, QtCore, QtGui

from PyQt4.QtNetwork import QTcpSocket

    
class ClientG(QtGui.QWidget):
    
    
    
    def __init__(self):
        QtGui.QWidget.__init__(self) 
        
        self.socket = QTcpSocket() 
        
        self.addr = ''
        self.port = 0
        self.status = 'Not connected'
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        logging.info("Starting Client")
        
        self.statusLabel = QtGui.QLabel('Client status:' + self.status, self)
        self.statusLabel.move(10, 20)
        self.statusLabel.resize(200, 25)
        self.mainLayout.addWidget(self.statusLabel)
        
        self.ipLabel = QtGui.QLabel('IP:', self)
        self.ipLabel.move(10, 50)
        self.mainLayout.addWidget(self.ipLabel)
        
        self.hostLabelEdit = QtGui.QLineEdit('0.0.0.0' ,self)
        self.hostLabelEdit.move(10,75)
        self.mainLayout.addWidget(self.hostLabelEdit)
        
        self.portLabel = QtGui.QLabel('Port:', self)
        self.portLabel.move(10, 105)
        self.mainLayout.addWidget(self.portLabel)
        
        self.portLabelEdit = QtGui.QLineEdit('0',self)
        self.portLabelEdit.move(10, 125)
        self.mainLayout.addWidget(self.portLabelEdit)
        
        self.startButton = QtGui.QPushButton('Start', self)
        self.startButton.move(10, 175)  
        self.mainLayout.addWidget(self.startButton)
        
        self.connectButton = QtGui.QPushButton('Connect', self)
        self.connectButton.move(100, 175)
        self.connectButton.setEnabled(False)
        self.mainLayout.addWidget(self.connectButton)
        
        self.passPhraseLabel = QtGui.QLabel('Passphrase:', self)
        self.mainLayout.addWidget(self.passPhraseLabel)
        
        self.passPhraseEdit = QtGui.QLineEdit(self)
        self.passPhraseEdit.move(250, 125)
        self.mainLayout.addWidget(self.passPhraseEdit)
        
        self.serverListLabel = QtGui.QLabel('Recent connections', self)
        self.serverListLabel.move(300, 150)
        self.mainLayout.addWidget(self.serverListLabel)
        
        self.recentListWidget = QtGui.QListWidget(self)
        self.recentListWidget.move(300, 125)
        self.mainLayout.addWidget(self.recentListWidget)
        
        self.propertyLabel = QtGui.QTextEdit(self)
        self.propertyLabel.move(25, 350)
        self.propertyLabel.resize(256, 80)
        self.propertyLabel.setText('Host Instance:\nIP:\nPort:\nPassphrase:')
        self.mainLayout.addWidget(self.propertyLabel)
        
        self.pushButton = QtGui.QPushButton('Add Properties',self)
        self.mainLayout.addWidget(self.pushButton)
        
        #Connections
        self.connect(self.socket, QtCore.SIGNAL('error(QAbstractSocket::SocketError)'), self.displayError)
        self.connect(self.socket, QtCore.SIGNAL('connected()'), self.connected)
        self.connect(self.startButton, QtCore.SIGNAL('pressed()'), self.startClient)
        self.connect(self.connectButton, QtCore.SIGNAL('pressed()'), self.connectToServer) 
        self.connect(self.passPhraseEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connect(self.portLabelEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connect(self.hostLabelEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connect(self.recentListWidget, QtCore.SIGNAL('itemSelectionChanged()'), self.recentListHandler)
        self.connect(self.pushButton, QtCore.SIGNAL('pressed()'), self.addProperties)
         
        self.resize(300, 300)
        self.hide()
    
    def addProperties(self):
        input = self.propertyLabel.toPlainText()
        list = input.split("\n")
        ip = list[1].split(":")[1]
        port = list[2].split(":")[1]
        passPhrase =  list[3].split(":")[1]
        
        if ip is not None:
            self.hostLabelEdit.setText(ip)
        if port is not None:
            self.portLabelEdit.setText(port)
        if passPhrase is not None:
            self.passPhraseEdit.setText(passPhrase)
        
        
    
        
    def enableConnectButton(self):
        if self.passPhraseEdit.text() == '' or self.hostLabelEdit.text() == '' or self.portLabelEdit.text() == '':
            self.connectButton.setEnabled(False)
        else:
            self.connectButton.setEnabled(True)
    
    def connected(self):
        logging.info("Connected to %s %s", self.addr, self.port)
        self.sendPassphrase()
        self.connectButton.setText("Disconnect")
        self.disconnect(self.connectButton, QtCore.SIGNAL('pressed()'), self.connectToServer) 
        self.disconnect(self.passPhraseEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connect(self.connectButton, QtCore.SIGNAL('pressed()'), self.disconnectFromHost)
        self.connect(self.socket, QtCore.SIGNAL("disconnected()"), self.disconnectFromHost)
    
    '''
    Function for sending message to the connected server
    '''  
    def sendMessage(self, message):
        logging.info("Sending message: %s", message)
        block = QtCore.QByteArray()
        block.append(message)
        self.socket.write(block)
    
    '''
    This function is for sending the passphrase to the server. It uses the sendMessage function
    '''
    def sendPassphrase(self):
        passPhrase = base64.b64encode(self.passPhraseEdit.text())
        #self.sendMessage(self.passPhraseEdit.text())
        self.sendMessage(passPhrase)
    
    '''
    This function is for reading message from the server
    '''
    def readMessage(self):
        message = self.socket.read(self.socket.bytesAvailable()) 
        logging("Server said:%s", message)  
        return message
    
    def connectToServer(self):
        self.addr = self.hostLabelEdit.text()
        self.port = int(self.portLabelEdit.text())
        addr = QtNetwork.QHostAddress(self.addr)
        logging.info("Connecting to %s %s", self.addr, self.port)
        self.socket.connectToHost(addr, self.port)
        if self.socket.waitForConnected(1000) is False :
            logging.error("Socket error %s", self.socket.errorString())
        
    '''
    When there is a socket error this function is called to show the error in a QMessageBox
    '''    
    def displayError(self, socketError):
        messageBox = QtGui.QMessageBox.critical(self, QtCore.QString('Error!'), 
                                                   QtCore.QString(self.socket.errorString()))
        logging.error("Socket error %s" % self.socket.errorString())
    
    '''
    This function is for updating the sockets status and the statusLabel. It's called when a stateChanged signal is triggered.
    '''
    def updateStatus(self):
        state = self.socket.state()
        if state == 0:
            self.status = 'Not connected'
        elif state == 1:
            self.status = 'Host lookup'
        elif state == 2:
            self.status = 'Establishing connection'
        elif state == 3:
            self.status = 'Connected'
        elif state == 4:
            self.status = 'The socket is bound to an address and port'
        elif state == 5:
            self.status = 'For internal use only'
        elif state == 6:
            self.status = 'Socket is about to close'
        self.statusLabel.setText('Client status:' + self.status)
    
    def startClient(self):  
        if self.status == 'Not connected':
            self.addr = self.hostLabelEdit.text()
            self.port = int(self.portLabelEdit.text())
            self.startButton.setText(QtCore.QString('Stop'))
            self.getRecentConnections()      
        elif self.status != 'Not connected':
            self.close()
            self.startButton.setText(QtCore.QString('Start'))
        self.connect(self.socket, QtCore.SIGNAL('stateChanged(QAbstractSocket::SocketState)'), self.updateStatus)
        
    
    '''
    Function for disconnecting the client from the host.
    '''
    def disconnectFromHost(self):
        logging.info("Disconnected from host")
        self.socket.disconnectFromHost()
        self.disconnect(self.connectButton, QtCore.SIGNAL('pressed()'), self.disconnectFromHost) 
        self.connect(self.connectButton, QtCore.SIGNAL('pressed()'), self.connectToServer)
        self.connect(self.passPhraseEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connectButton.setText('Connect')
        self.addToRecentConnections()
    
    def close(self):
        self.socket.close()
    
    '''
    This function is for getting the recent connections from the database and load it to the list
    '''    
    def getRecentConnections(self):
        logging.info("Getting recent connections from database")
        con = sqlite3.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute('select * from recentConnections')
            data = cur.fetchone()
            if data is not None:
                print 'Decoding passphrase', base64.b64decode(data[2])
                listItem = ClientListWidget(data[0], data[1], data[2])
                self.recentListWidget.addItem(listItem)
    
    '''
    This function is for adding a new connection to the recent connections. It checks whether it exists in the database or not.
    '''   
    def addToRecentConnections(self):
        con = sqlite3.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute('''SELECT * FROM recentconnections WHERE ip = "%s" and port = "%d" and passphrase = "%s" ''' %
                            (self.addr,
                             self.port,
                             self.passPhraseEdit.text()
                             )
                        )
            data = cur.fetchone()
            if data is not None:
                logging.info("Connection already exists")
                return
            elif data is None:
                cur.execute('''INSERT INTO recentConnections VALUES("%s" , "%d", "%s")''' %
                            (self.addr,
                             self.port,
                             self.passPhraseEdit.text()
                             )
                            )
                logging.info("Recent connection %s %d added ", self.addr, self.port)
                self.getRecentConnections()
        
    '''
    Handler for the recent connections list. When you click on a recent connection the details of the connection are loaded 
    '''
    def recentListHandler(self):
        self.hostLabelEdit.setText(self.recentListWidget.selectedItems()[0].ip)
        port = str(self.recentListWidget.selectedItems()[0].port)
        self.portLabelEdit.setText(port)
        self.passPhraseEdit.setText(self.recentListWidget.selectedItems()[0].passPhrase)
        
'''
Custom QListWidgetItem
It is used for the recent connections list. 
'''
class ClientListWidget(QtGui.QListWidgetItem):
    
    def __init__(self, ip, port, passPhrase):
        QtGui.QWidgetItem.__init__(self)
        self.ip = ip
        self.port = port
        self.passPhrase = passPhrase
        self.setText(self.ip + ' '  + str(port))
        
       
def Main(self):
    app = QtGui.QApplication(sys.argv)
    c = ClientG()
    sys.exit(app.exec_())

if __name__ == "__main__":
    Main()
