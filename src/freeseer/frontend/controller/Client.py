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
        
        # Translations
        self.uiTranslator = QtCore.QTranslator()
        self.uiTranslator.load(":/languages/tr_en_US.qm")
        self.retranslate()
        self.updateStatus()
        
    ###
    ### Translation Related
    ###
    def retranslate(self):
        self.setWindowTitle(self.uiTranslator.translate("ControllerClientApp", "Controller Client"))                
        #
        # Reusable Strings
        #
        self.clientStatusString = self.uiTranslator.translate("ControllerClientApp", "Status")
        self.connectString = self.uiTranslator.translate("ControllerClientApp", "Connect")
        self.disconnectString = self.uiTranslator.translate("ControllerClientApp", "Disconnect")
        # --- End Reusable Strings
        
        #
        # Connection Settings
        #
        self.mainWidget.toolBox.setItemText(0, self.uiTranslator.translate("ControllerClientApp", "Connection Settings"))
        self.mainWidget.hostLabel.setText(self.uiTranslator.translate("ControllerClientApp", "Host name (or IP Address)"))
        self.mainWidget.portLabel.setText(self.uiTranslator.translate("ControllerClientApp", "Port"))
        self.mainWidget.passLabel.setText(self.uiTranslator.translate("ControllerClientApp", "Passphrase"))
        if self.status == self.STATUS[3]:
            self.mainWidget.connectButton.setText(self.uiTranslator.translate("ControllerClientApp", self.disconnectString))
        else:
            self.mainWidget.connectButton.setText(self.uiTranslator.translate("ControllerClientApp", self.connectString))
        self.updateStatus()
        # --- End Connection Settings
        
        #
        # Recent Connections
        #
        self.mainWidget.toolBox.setItemText(1, self.uiTranslator.translate("ControllerClientApp", "Recent Connections"))
        # --- End Recent Connections
        
    ##
    ## UI Related
    ##
    
    def enableConnectButton(self):
        if self.mainWidget.passEdit.text() == '' or self.mainWidget.hostEdit.text() == '' or self.mainWidget.portEdit.text() == '':
            self.mainWidget.connectButton.setEnabled(False)
        else:
            self.mainWidget.connectButton.setEnabled(True)
    
    def connected(self):
        caddr = self.socket.peerName()
        cport = self.socket.peerPort()
        logging.info("Connected to %s:%s" % (caddr, cport))
        
        self.sendPassphrase()
        self.mainWidget.connectButton.setText(self.disconnectString)
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
        self.mainWidget.statusLabel.setText(self.clientStatusString + ": " + self.status)
        
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
        caddr = self.mainWidget.hostEdit.text()
        cport = int(self.mainWidget.portEdit.text())
        cpass = self.mainWidget.passEdit.text()
        self.getRecentConnections()      
        
        self.connect(self.socket, QtCore.SIGNAL('stateChanged(QAbstractSocket::SocketState)'), self.updateStatus)

        logging.info("Connecting to %s:%s" % (caddr, cport))
        self.socket.connectToHost(caddr, cport)
        
        if not self.socket.waitForConnected(1000):
            logging.error("Socket error %s", self.socket.errorString())
        else:
            # Add to recent connections if connection is successful
            self.addToRecentConnections(caddr, cport, cpass)
    
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
        self.mainWidget.connectButton.setText(self.connectString)
      
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
                    listItem = ClientListItem(data[0], data[1], data[2])
                    self.mainWidget.recentConnList.addItem(listItem)
                
    '''
    This function is for adding a new connection to the recent connections. It checks whether it exists in the database or not.
    '''   
    def addToRecentConnections(self, caddr, cport, cpass):
        con = sqlite3.connect(self.recentconndb_file)
        with con:
            cur = con.cursor()
            cur.execute('''SELECT * FROM recentconnections WHERE ip = "%s" and port = "%d" and passphrase = "%s" ''' %
                            (caddr, cport, cpass))
                            
            data = cur.fetchone()
            if data is not None:
                logging.info("Connection already exists in the database")
                return
            elif data is None:
                cur.execute('''INSERT INTO recentConnections VALUES("%s" , "%d", "%s")''' %
                            (caddr, cport, cpass))
                logging.info("Recent connection %s %d added to the database ", caddr, cport)
                self.getRecentConnections()
        
    '''
    Handler for the recent connections list. When you click on a recent connection the details of the connection are loaded 
    '''
    def recentListHandler(self, connection):
        chost = self.mainWidget.recentConnList.selectedItems()[0].host
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
class ClientListItem(QtGui.QListWidgetItem):
    
    def __init__(self, host, port, passPhrase):
        QtGui.QWidgetItem.__init__(self)
        self.host = host
        self.port = port
        self.passPhrase = passPhrase
        self.setText("%s:%s" % (host, port))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
    c = ClientDialog(configdir)
    c.show()
    sys.exit(app.exec_())
