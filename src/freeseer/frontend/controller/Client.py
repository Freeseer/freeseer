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

import os
import logging
import sys
import sqlite3

from PyQt4 import QtNetwork, QtCore, QtGui
from PyQt4.QtNetwork import QTcpSocket

from ClientWidget import ControllerClientWidget
    
class ClientDialog(QtGui.QDialog):

    STATUS = ["Not Connected",
              "Host Lookup",
              "Establishing connection",
              "Connected",
              "The socket is bound to an address and port",
              "For internal use only",
              "Socket is about to close"]
    
    def __init__(self, configdir, recentconndb_file="recentconn.db"):
        QtGui.QDialog.__init__(self)
        
        # Variables
        self.configdir = configdir
        self.recentconndb_file = os.path.abspath("%s/%s" % (self.configdir, recentconndb_file))
        
        self.socket = QTcpSocket() 
        self.addr = ''
        self.port = 0
        self.status = self.STATUS[0]
        
        logging.info("Starting Client")

        # Properties        
        self.setModal(True)
        
        # Setup Widget
        self.layout = QtGui.QVBoxLayout()
        self.mainWidget = ControllerClientWidget()
        self.layout.addWidget(self.mainWidget)
        self.setLayout(self.layout)
          
        #Connections
        self.connect(self.socket, QtCore.SIGNAL('error(QAbstractSocket::SocketError)'), self.displayError)
        self.connect(self.socket, QtCore.SIGNAL('connected()'), self.connected)
        self.connect(self.mainWidget.connectButton, QtCore.SIGNAL('pressed()'), self.connectToServer) 
        self.connect(self.mainWidget.hostEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connect(self.mainWidget.portEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connect(self.mainWidget.passEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connect(self.mainWidget.recentConnList, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem *)'), self.recentListHandler)

        self.getRecentConnections()
        self.enableConnectButton()
        self.hide()
        
    ##
    ## UI Related
    ##
    
    def enableConnectButton(self):
        if self.mainWidget.passEdit.text() == '' or self.mainWidget.hostEdit.text() == '' or self.mainWidget.portEdit.text() == '':
            self.mainWidget.connectButton.setEnabled(False)
        else:
            self.mainWidget.connectButton.setEnabled(True)
    
    def connected(self):
        logging.info("Connected to %s %s", self.addr, self.port)
        self.sendPassphrase()
        self.mainWidget.connectButton.setText("Disconnect")
        self.disconnect(self.mainWidget.connectButton, QtCore.SIGNAL('pressed()'), self.connectToServer) 
        self.disconnect(self.mainWidget.passEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connect(self.mainWidget.connectButton, QtCore.SIGNAL('pressed()'), self.disconnectFromHost)
        self.connect(self.socket, QtCore.SIGNAL("disconnected()"), self.disconnectedFromHost)
        
    '''
    This function is for updating the sockets status and the statusLabel. It's called when a stateChanged signal is triggered.
    '''
    def updateStatus(self):
        state = self.socket.state()
        self.status = self.STATUS[state]
        self.mainWidget.statusLabel.setText('Client status:' + self.status)
        
    '''
    When there is a socket error this function is called to show the error in a QMessageBox
    '''    
    def displayError(self, socketError):
        messageBox = QtGui.QMessageBox.critical(self, QtCore.QString('Error!'), 
                                                   QtCore.QString(self.socket.errorString()))
        logging.error("Socket error %s" % self.socket.errorString())

    ##
    ## Connection Related
    ##
        
    '''
    Function that is called when connect button is pressed.
    '''
    def connectToServer(self):
        self.addr = self.mainWidget.hostEdit.text()
        self.port = int(self.mainWidget.portEdit.text())
        self.getRecentConnections()      
        
        self.connect(self.socket, QtCore.SIGNAL('stateChanged(QAbstractSocket::SocketState)'), self.updateStatus)

        addr = QtNetwork.QHostAddress(self.addr)
        logging.info("Connecting to %s %s", self.addr, self.port)
        self.socket.connectToHost(addr, self.port)
        if self.socket.waitForConnected(1000) is False :
            logging.error("Socket error %s", self.socket.errorString())    
    
    def disconnectFromHost(self):
        self.socket.disconnectFromHost()
        
    '''
    Function for disconnecting the client from the host.
    '''
    def disconnectedFromHost(self):
        logging.info("Disconnected from host")
        self.disconnect(self.mainWidget.connectButton, QtCore.SIGNAL('pressed()'), self.disconnectFromHost)
        self.connect(self.mainWidget.connectButton, QtCore.SIGNAL('pressed()'), self.connectToServer)
        self.connect(self.mainWidget.passEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.mainWidget.connectButton.setText('Connect')
        self.addToRecentConnections()
      
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
        self.sendMessage(self.mainWidget.passEdit.text())
    
    '''
    This function is for reading message from the server
    '''
    def readMessage(self):
        message = self.socket.read(self.socket.bytesAvailable()) 
        logging("Server said:%s", message)  
        return message

    ##
    ## Recent Connections Related
    ##
    
    '''
    This function is for getting the recent connections from the database and load it to the list
    '''    
    def getRecentConnections(self):
        logging.info("Getting recent connections from database")
        if os.path.isfile(self.recentconndb_file) is False:
            logging.info("Database doesn't exist, creating database")
            con = sqlite3.connect(self.recentconndb_file)
            with con:
                cur = con.cursor()
                cur.execute('create table recentconnections(ip varchar(15), port int, passphrase varchar(150))') 
        else:
            con = sqlite3.connect(self.recentconndb_file)
            with con:
                cur = con.cursor()
                cur.execute('select * from recentConnections')
                data = cur.fetchone()
                self.mainWidget.recentConnList.clear()
                if data is not None:
                    listItem = ClientListWidget(data[0], data[1], data[2])
                    self.mainWidget.recentConnList.addItem(listItem)
                
    '''
    This function is for adding a new connection to the recent connections. It checks whether it exists in the database or not.
    '''   
    def addToRecentConnections(self):
        con = sqlite3.connect(self.recentconndb_file)
        with con:
            cur = con.cursor()
            cur.execute('''SELECT * FROM recentconnections WHERE ip = "%s" and port = "%d" and passphrase = "%s" ''' %
                            (self.addr,
                             self.port,
                             self.mainWidget.passEdit.text()
                             )
                        )
            data = cur.fetchone()
            if data is not None:
                logging.info("Connection already exists in the database")
                return
            elif data is None:
                cur.execute('''INSERT INTO recentConnections VALUES("%s" , "%d", "%s")''' %
                            (self.addr,
                             self.port,
                             self.mainWidget.passEdit.text()
                             )
                            )
                logging.info("Recent connection %s %d added to the database ", self.addr, self.port)
                self.getRecentConnections()
        
    '''
    Handler for the recent connections list. When you click on a recent connection the details of the connection are loaded 
    '''
    def recentListHandler(self, connection):
        chost = self.mainWidget.recentConnList.selectedItems()[0].ip
        cport = self.mainWidget.recentConnList.selectedItems()[0].port
        cpass = self.mainWidget.recentConnList.selectedItems()[0].passPhrase
        self.mainWidget.hostEdit.setText(chost)
        self.mainWidget.portEdit.setValue(cport)
        self.mainWidget.passEdit.setText(cpass)
        self.mainWidget.toolBox.setCurrentWidget(self.mainWidget.connWidget)
        
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
        self.setText("%s:%s" % (ip, port))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
    c = ClientDialog(configdir)
    c.show()
    sys.exit(app.exec_())
