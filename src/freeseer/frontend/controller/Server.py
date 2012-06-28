'''
Created on Jun 4, 2012

@author: borasabuncu
'''
import logging
import sys

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
    
    def __init__(self):
        #super(ServerG, self).__init__()
        QtGui.QWidget.__init__(self) 
        self.resize(400, 400)
        
        self.server = QTcpServer(self)
        
        self.startButton = QtGui.QPushButton('Start', self)
        self.startButton.move(35, 70)
        
        self.statusLabel = QtGui.QLabel('Server status:' + self.status, self)
        self.statusLabel.move(25, 20)
        self.statusLabel.resize(200, 25)
        
        self.statusLabel2 = QtGui.QLabel('', self)
        self.statusLabel2.move(25, 45)
        self.statusLabel2.resize(200, 25)
        
        self.messageLine = QtGui.QLineEdit(self)
        self.messageLine.move(200, 20)
        
        self.messageButton = QtGui.QPushButton('Send Message', self)
        self.messageButton.setEnabled(False)
        self.messageButton.move(200, 45)
        
        self.ipLabel = QtGui.QLabel('IP Address', self)
        self.ipLabel.move(25, 110)
        
        self.connectionLabel = QtGui.QLabel('Connection', self)
        self.connectionLabel.move(115, 110)
        
        self.controlLabel = QtGui.QLabel('Control', self)
        self.controlLabel.move(205, 110)
        
        self.qListWidget = QtGui.QListWidget(self)
        self.qListWidget.move(25, 140)
        self.qListWidget.resize(256, 192)
        
        self.recordButton = QtGui.QPushButton('Start Recording', self)
        self.recordButton.move(300, 100)
        
        self.recordButton = QtGui.QPushButton('Pause Recording', self)
        self.recordButton.move(300, 150)
        
        self.recordButton = QtGui.QPushButton('Stop Recording', self)
        self.recordButton.move(300, 200)
        
        #Connections
        self.connect(self.server, QtCore.SIGNAL('newConnection()'), self.acceptConnection)  
        self.connect(self.startButton, QtCore.SIGNAL('pressed()'), self.startServer)
        self.connect(self.messageLine, QtCore.SIGNAL('textEdited(QString)'), self.enableMessageButton)
        self.connect(self.messageButton, QtCore.SIGNAL('pressed()'), self.sendCustomMessage)
        
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
    
    def startRead(self):
        #self.client.writeData('Hello Client!')
        message = self.client.read(self.client.bytesAvailable())   
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
    
    def acceptConnection(self):
        client = self.server.nextPendingConnection() 
        self.clients.append(client)
        self.connect(client, QtCore.SIGNAL("disconnected()"), self.clientDisconnected)
        self.updateList()
    
    def clientDisconnected(self):
        print 'Client Disconnected'
        client = QtCore.QObject.sender(self)
        logging.info("Client %s disconnected", client.localAddress().toString())
        self.clients.remove(client)
        self.updateList()
    
    def updateList(self):
        self.qListWidget.clear()
        for i in range(0, len(self.clients)):
            client = self.clients[i]
            listItem = QtGui.QListWidgetItem(client.localAddress().toString())
            self.qListWidget.addItem(listItem)
            self.qListWidget.setItemWidget(listItem, QtGui.QCheckBox())
            clientLabel = QtGui.QLabel('F1', self)
            clientLabel.move(5 + (i * 20), 150)
            
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
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = ServerG()
    main.show()
    sys.exit(app.exec_())


