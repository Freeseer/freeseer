'''
Created on Jun 4, 2012

@author: borasabuncu
'''
from PyQt4 import QtNetwork, QtCore, QtGui
from PyQt4.QtNetwork import QTcpSocket, QAbstractSocket
from PyQt4.QtNetwork import QHostAddress
from PyQt4.QtCore import QObject, QDataStream
import sys

PORT = 56763
class Client(QtCore.QObject):
    socket = None
    addr = None
    port = None
    blockSize = None
    currentFortune = ''
    def __init__(self, addr, portin):
        print 'Starting client'
        self.socket = QTcpSocket() 
        #self.connect(self.socket, QtCore.SIGNAL('connected()'), self.requestNewFortune)
        #self.connect(self.socket, QtCore.SIGNAL('readyRead()'), self.readFortune)
        self.connect(self.socket, QtCore.SIGNAL('error(QAbstractSocket::SocketError)'), self.displayError)
        self.addr = addr
        self.port = portin
        
    def readFortune(self):
        print 'Reading fortune'
        datain = QtCore.QDataStream(self.socket)
        datain.setVersion(QtCore.QDataStream.Qt_4_0)
        
        if self.blockSize == 0:
            #if self.socket.bytesAvailable() < int(len(quint16)):
                #return
            datain.writeInt(self.blockSize)
        if self.socket.bytesAvailable() < self.blockSize:
            return
        nextFortune = QtCore.QString()
        datain.writeString(nextFortune)
        self.currentFortune = nextFortune
        print self.socket.read(1024)
        print 'End reading fortune'
        
        
    
    def requestNewFortune(self):
        print 'Requesting new fortune'
        self.blockSize = 0
        self.socket.abort()
        print 'Connecting to ', self.addr, self.port
        self.connectTo('address', 2000)
        print 'End requesting new fortune'
        
        
    def connectTo(self, address, portin):
        addr = QHostAddress(self.addr)
        print 'Trying to connect to ', self.addr, self.port
        self.socket.connectToHost(addr, self.port)
        if self.socket.waitForConnected(1000) is False :
            print 'Socket creation failed: ', self.socket.errorString()
        else:
            print 'Connected'
            print self.socket.state()
        
    def displayError(self, socketError):
        if socketError == QAbstractSocket.HostNotFoundError:
            print 'The host was not found'
        elif socketError == QAbstractSocket.ConnectionRefusedError:
            print 'The connection was refused'
        else:
            print 'Unknown error'
    
    def close(self):
        self.socket.close()




        
class ClientG(QtGui.QWidget):
    pushButton = None
    connectButton = None
    label = None
    status = 'Not connected'
    ipAddress = ''
    hostLabelEdit = None
    portLabelEdit = None
    label4 = None
    socket = None
    addr = None
    port = None
    blockSize = None
    currentFortune = ''
    passPhraseEdit = None
    def __init__(self,):
        super(ClientG, self).__init__()
        print 'Starting client'
        
        self.socket = QTcpSocket() 
        self.connect(self.socket, QtCore.SIGNAL('error(QAbstractSocket::SocketError)'), self.displayError)
        self.connect(self.socket, QtCore.SIGNAL('readyRead()'), self.readMessage)
        self.connect(self.socket, QtCore.SIGNAL('connected()'), self.connected)
        
        self.label = QtGui.QLabel('Client status:' + self.status, self)
        self.label.move(10, 20)
        self.label.resize(200, 25)
        label2 = QtGui.QLabel('IP:', self)
        label2.move(10, 50)
        
        self.hostLabelEdit = QtGui.QLineEdit('0.0.0.0' ,self)
        self.hostLabelEdit.move(10,75)
        
        label3 = QtGui.QLabel('Port:', self)
        label3.move(10, 105)
        
        
        self.portLabelEdit = QtGui.QLineEdit('55441',self)
        self.portLabelEdit.move(10, 125)
        
        self.pushButton = QtGui.QPushButton('Connect', self)
        self.pushButton.move(10, 175)  
        self.connect(self.pushButton, QtCore.SIGNAL('pressed()'), self.startClient)
         
        self.connectButton = QtGui.QPushButton('Connect', self)
        self.connectButton.move(100, 175)
        #self.connectButton.setEnabled(False)
        self.connect(self.connectButton, QtCore.SIGNAL('pressed()'), self.connectTo) 
        
        self.passPhraseEdit = QtGui.QLineEdit(self)
        self.passPhraseEdit.move(250, 125)
        #self.connect(self.passPhraseEdit,  QtCore.SIGNAL('textChanged(QString)'), self.enableConnectButton)
        
        self.setGeometry(300, 300, 450, 250)
        self.setWindowTitle('Client')
        self.show()
    
    def enableConnectButton(self):
        self.connectButton.setEnabled(True)
    
    def stateChanged(self):
        print 'State changed'
    
    def connected(self):
        print 'Connected'
    
    def sendMessage(self):
        print 'Sending message!'
        block = QtCore.QByteArray()
        block.append('sagas')
        self.socket.write(block)
        
    def readMessage(self):
        message = self.socket.read(self.socket.bytesAvailable())   
        print 'Server said:', message
    
    def connectTo(self):
        addr = QHostAddress(self.addr)
        print 'Trying to connect to ', self.addr, self.port
        self.socket.connectToHost(addr, self.port)
        if self.socket.waitForConnected(1000) is False :
            print 'Socket creation failed: ', self.socket.errorString()
        else:
            print 'Connected'
            print self.socket.state()
        
        
    def displayError(self, socketError):
        messageBox = QtGui.QMessageBox.critical(self, QtCore.QString('Error!'), 
                                                   QtCore.QString(self.socket.errorString()))
        print 'Error:', self.socket.errorString()
        
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
        self.label.setText('Client status:' + self.status)
        
    def startClient(self):  
        #connect the status to self.client.state()  
        #check for empty port and ip
        if self.status == 'Not connected':
            self.addr = self.hostLabelEdit.text()
            self.port = int(self.portLabelEdit.text())
            self.pushButton.setText(QtCore.QString('Stop'))      
        elif self.status != 'Not connected':
            self.close()
            self.pushButton.setText(QtCore.QString('Start'))
        self.updateStatus()
    
    def close(self):
        self.socket.close()
def Main():
    app = QtGui.QApplication(sys.argv)
    c = ClientG()
    return app.exec_()

Main()