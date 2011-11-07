'''
Created on Oct 15, 2011

@author: jord
'''

from PyQt4 import QtGui, QtCore

from UploaderWidget import UploaderMenuBar, UploaderWidget
from MinimalistCore import MinimalistCore

from freeseer.framework.core import FreeseerCore

class UploaderApp(QtGui.QMainWindow):
    '''
    Video Uploader Main window
    '''
    
#    def __init__(self, parent = None, flags = QtCore.Qt.WindowFlags()):
#        QtGui.QMainWindow.__init__(self, parent, flags)
    def __init__(self, core=None):
        # validate arguments #
        if core is None:
            core = MinimalistCore(self)
        assert isinstance(core, FreeseerCore) or isinstance(core, MinimalistCore)
        
        # superclass #
        QtGui.QMainWindow.__init__(self, None)
        
        # init gui #
        self.resize(560, 600)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/freeseer/freeseer_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        ## main window area ##       
        self.mainWidget = UploaderWidget(self)
        self.mainWidget.setObjectName("mainWidget")
        self.setCentralWidget(self.mainWidget)
        
        ## menubar ##
        self.menubar = UploaderMenuBar(self)
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        
        ## toolbar ##
        # it looks ugly, so it's left out.
#        self.toolbar = QtGui.QToolBar(self)
#        self.__initToolbar()
        
        self.retranslate()
        
        # Signals and slots' connections #
        self.__initConnections()
    
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
    
    def __initConnections(self):
        self.menubar.actionClose.triggered.connect(self.close)
        self.mainWidget.buttonbar.rejected.connect(self.close)
        self.menubar.actionUpload.triggered.connect(self.upload)
        self.mainWidget.buttonbar.accepted.connect(self.upload)
    
    @QtCore.pyqtSlot()
    def upload(self):
        QtGui.QMessageBox.critical(self, "", "Not yet implemented")
        success = False
        
        if success:
            self.close()
        
    # todo: custom slots; use the following template
#    @QtCore.pyqtSlot([type-list])
#    def customSlot(self, [var-list]):
#        assert isinstance([var], [type])

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