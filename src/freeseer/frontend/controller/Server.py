'''
Created on Jun 4, 2012

@author: borasabuncu
'''
from PyQt4 import QtCore, QtGui, QtNetwork
from PyQt4.QtCore import QString
from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4.QtNetwork import QHostAddress
from PyQt4.QtNetwork import QTcpServer, QAbstractSocket
import sys
PORT = 55441
    
class ServerG(QtGui.QWidget):
    server = None
    pushButton = None
    label = None
    label2 = None
    status = 'Off' 
    client = None
    message = ''
    messageLine = None 
    messageButton = None
    clients = []
    passPhrase = 'dog'
    qListWidget = None
    def __init__(self):
        super(ServerG, self).__init__()
        self.server = QTcpServer(self)
        self.connect(self.server, QtCore.SIGNAL('newConnection()'), self.acceptConnection)  
        
        self.pushButton = QtGui.QPushButton('Start', self)
        self.pushButton.move(10, 70)
        self.connect(self.pushButton, QtCore.SIGNAL('pressed()'), self.startServer)
        
        self.label = QtGui.QLabel('Server status:' + self.status, self)
        self.label.move(10, 20)
        self.label.resize(200, 25)
        
        self.label2 = QtGui.QLabel('', self)
        self.label2.move(10, 45)
        self.label2.resize(200, 25)
        
        self.messageLine = QtGui.QLineEdit(self)
        self.messageLine.move(200, 20)
        self.connect(self.messageLine, QtCore.SIGNAL('textEdited(QString)'), self.enableMessageButton)
        
        self.messageButton = QtGui.QPushButton('Send Message', self)
        self.connect(self.messageButton, QtCore.SIGNAL('pressed()'), self.sendCustomMessage)
        self.messageButton.setEnabled(False)
        self.messageButton.move(200, 45)
        
        self.qListWidget = QtGui.QListWidget(self)
        self.qListWidget.move(10, 100)
        self.qListWidget.resize(256, 192)
        
        self.setGeometry(300, 300, 450, 250)
        self.setWindowTitle('Server')
        self.show()
    
    def startServer(self):    
        if self.status == 'Off':
            self.server.listen(QHostAddress.Any, PORT)    
            self.pushButton.setText(QString('Stop'))
            self.status = 'Running' 
            string = 'IP:' + self.server.serverAddress().toString() + ' Port:' + str(self.server.serverPort())
            print string
            self.label2.setText(QString(string))
        elif self.status == 'Running':
            self.server.close()
            self.pushButton.setText(QString('Start'))
            self.status = 'Off'
        self.label.setText('Server status:' + self.status)
    
    def enableMessageButton(self):
        if self.messageLine == '':
            self.messageButton.setEnabled(False)
        else:
            self.messageButton.setEnabled(True)
    
    def startRead(self):
        #self.client.writeData('Hello Client!')
        message = self.client.read(self.client.bytesAvailable())   
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
    
    def acceptConnection(self):
        client = self.server.nextPendingConnection() 
        self.clients.append(client)
        listItem = QtGui.QListWidgetItem(client.localAddress().toString())
        self.qListWidget.addItem(listItem)
        
        
def Main():
        app = QtGui.QApplication(sys.argv)
        s = ServerG()
        return app.exec_()
Main() 

