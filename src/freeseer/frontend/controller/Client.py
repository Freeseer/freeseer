'''
Created on Jun 4, 2012

@author: borasabuncu
'''
import logging
import sys
import base64

from PyQt4 import QtNetwork, QtCore, QtGui

from PyQt4.QtNetwork import QTcpSocket

PORT = 56763
    
class ClientG(QtGui.QWidget):
    
    status = 'Not connected'
    socket = None
    
    
    def __init__(self):
        QtGui.QWidget.__init__(self) 
        
        self.socket = QTcpSocket() 
        
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
        
        self.portLabelEdit = QtGui.QLineEdit('55441',self)
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
        
        self.serverListWidget = QtGui.QListWidget(self)
        self.serverListWidget.move(300, 125)
        self.mainLayout.addWidget(self.serverListWidget)
        
        #Connections
        self.connect(self.socket, QtCore.SIGNAL('error(QAbstractSocket::SocketError)'), self.displayError)
        #self.connect(self.socket, QtCore.SIGNAL('readyRead()'), self.readMessage)
        self.connect(self.socket, QtCore.SIGNAL('connected()'), self.connected)
        self.connect(self.startButton, QtCore.SIGNAL('pressed()'), self.startClient)
        self.connect(self.connectButton, QtCore.SIGNAL('pressed()'), self.connectToServer) 
        self.connect(self.passPhraseEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        
        self.resize(300, 300)
        self.hide()
    
    def enableConnectButton(self):
        if self.passPhraseEdit.text() == '':
            self.connectButton.setEnabled(False)
        else:
            self.connectButton.setEnabled(True)
    
    def stateChanged(self):
        print 'State changed'
    
    def connected(self):
        logging.info("Connected to %s %s", self.addr, self.port)
        self.sendPassphrase()
        self.connectButton.setText("Disconnect")
        self.disconnect(self.connectButton, QtCore.SIGNAL('pressed()'), self.connectToServer) 
        self.disconnect(self.passPhraseEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connect(self.connectButton, QtCore.SIGNAL('pressed()'), self.disconnectFromHost)
        self.connect(self.socket, QtCore.SIGNAL("disconnected()"), self.disconnectFromHost)
        
    def sendMessage(self, message):
        print 'Sending message!'
        block = QtCore.QByteArray()
        block.append(message)
        self.socket.write(block)
    
    def sendPassphrase(self):
        self.sendMessage(self.passPhraseEdit.text())
        
    def readMessage(self):
        message = self.socket.read(self.socket.bytesAvailable())   
        #print 'Server said:', message
        return message
    
    def connectToServer(self):
        addr = QtNetwork.QHostAddress(self.addr)
        logging.info("Connecting to %s %s", self.addr, self.port)
        self.socket.connectToHost(addr, self.port)
        if self.socket.waitForConnected(1000) is False :
            logging.error("Socket error %s", self.socket.errorString())
        
        
    def displayError(self, socketError):
        messageBox = QtGui.QMessageBox.critical(self, QtCore.QString('Error!'), 
                                                   QtCore.QString(self.socket.errorString()))
        logging.error("Socket error %s" % self.socket.errorString())
    
    def updateStatus(self):
        state = self.socket.state()
        if state == 0:
            self.status = 'Not connected'
        elif state == 1:
            self.status = 'Host lookup'
        elif state == 2:
            self.status = 'Host lookup'
        elif state == 3:
            self.status = 'Connected'
        elif state == 6:
            self.status = 'Socket is about to close'
        self.statusLabel.setText('Client status:' + self.status)
        
    def startClient(self):  
        #connect the status to self.client.state()  
        #check for empty port and ip
        if self.status == 'Not connected':
            self.addr = self.hostLabelEdit.text()
            self.port = int(self.portLabelEdit.text())
            self.startButton.setText(QtCore.QString('Stop'))      
        elif self.status != 'Not connected':
            self.close()
            self.startButton.setText(QtCore.QString('Start'))
        self.updateStatus()
    
    def disconnectFromHost(self):
        print 'Disconnected'
        self.socket.disconnectFromHost()
        self.disconnect(self.connectButton, QtCore.SIGNAL('pressed()'), self.disconnectFromHost) 
        self.connect(self.connectButton, QtCore.SIGNAL('pressed()'), self.connectToServer)
        self.connect(self.passPhraseEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        self.connectButton.setText('Connect')
    
    def close(self):
        self.socket.close()
def Main(self):
    app = QtGui.QApplication(sys.argv)
    c = ClientG()
    sys.exit(app.exec_())
if __name__ == "__main__":
    Main()
