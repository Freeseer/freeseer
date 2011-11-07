'''
Created on Oct 15, 2011

@author: jord
'''
from PyQt4 import QtGui, QtCore
from UploaderWidget import UploaderMenuBar, UploaderWidget

class UploaderApp(QtGui.QMainWindow):
    '''
    Video Uploader Main window
    '''
    
#    def __init__(self, parent = None, flags = QtCore.Qt.WindowFlags()):
#        QtGui.QMainWindow.__init__(self, parent, flags)
    def __init__(self, core=None):
        flags = QtCore.Qt.WindowFlags()
#        if core != Qt.Popup:
#            flags |= QtCore.Qt.SplashScreen
        QtGui.QMainWindow.__init__(self, None, flags)
        self.setObjectName("UploaderApp")
        
        self.resize(560, 600)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/freeseer/freeseer_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        ### main window area ###       
        self.mainWidget = UploaderWidget(self)
        self.mainWidget.setObjectName("mainWidget")
        self.setCentralWidget(self.mainWidget)
        
        ### menubar ###
        self.menubar = UploaderMenuBar(self)
        self.setMenuBar(self.menubar)
        
        ### toolbar ###
        # it looks ugly, so it's left out.
#        self.toolbar = QtGui.QToolBar(self)
#        self.__initToolbar()
        
        self.retranslate()
        
        # Signals and slots connections
        self.__initConnect()
    
    def __initToolbar(self):
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.menubar.actionUpload)
        toolbarspacer = QtGui.QWidget(self)
        spacerpolicy = QtGui.QSizePolicy()
        spacerpolicy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
        toolbarspacer.setSizePolicy(spacerpolicy)
        self.toolbar.addWidget(toolbarspacer)
        self.toolbar.addAction(self.menubar.actionClose)
        
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
    
    def __initConnect(self):
        self.menubar.actionClose.triggered.connect(self.close)
        self.mainWidget.buttonBox_windowactions.
        self.mainWidget.buttonBox_windowactions.clicked.connect(
                                                    self.windowActionSlot)
    
    @QtCore.pyqtSlot(QtGui.QAbstractButton)
    def windowActionSlot(self, button):
        assert isinstance(button, QtGui.QAbstractButton)
        
        # the following is like a case statement. Figure it out, 
        #  and you will have taken one more step to being a python ninja!
        
        # to add more "cases", add a function below, 
        #  with the actions you want to do
        # then add an entry to the dict
        
        # all this does is chain its call to the menubar.actionClose QAction
        def close():
            self.menubar.actionClose.trigger()
#            self.close()
        
        {QtGui.QDialogButtonBox.Close: close
         }[self.mainWidget.buttonBox_windowactions.standardButton(button)]()

    def retranslate(self):
        self.setWindowTitle(self.tr("Freeseer Video Uploader"))
    
    def changeEvent(self, event):
        QtGui.QMainWindow.changeEvent(self, event)
        assert isinstance(event, QtCore.QEvent)
        
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslate()
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = UploaderApp()
    main.show()
    sys.exit(app.exec_())