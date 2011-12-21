#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

Copyright (C) 2011  Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/fosslc/freeseer/

@author: Jordan Klassen
'''

from PyQt4 import QtGui, QtCore

from os import path

from UploaderWidget import UploaderMenuBar, UploaderWidget
from MinimalistCore import MinimalistCore

from freeseer.framework.core import FreeseerCore
from freeseer.framework.metadata import FreeseerMetadataLoader
from freeseer.frontend.videouploader import exfalsolauncher
from freeseer.frontend.videouploader.ServerDetailsGroupBox import ServerDetailsGroupBox
from freeseer.framework import const
from freeseer.frontend.videouploader.UploadProgressIndicator import UploadProgressIndicator
import time
import functools
import logging

def retranslateOnLanguageChange(klass):
    def changeEvent(self, event):
        super(klass, self).changeEvent(event)
        assert isinstance(event, QtCore.QEvent)
        
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslate()
    
    klass.changeEvent = changeEvent
    return klass

@retranslateOnLanguageChange
class UploaderApp(QtGui.QMainWindow):
    '''
    Video Uploader Main window
    '''
    USE_NATIVE_DIALOG = True
    
#    def __init__(self, parent = None, flags = QtCore.Qt.WindowFlags()):
#        QtGui.QMainWindow.__init__(self, parent, flags)
    def __init__(self, core=None):
        # validate arguments #
        if core is None:
            core = MinimalistCore(self)
        assert isinstance(core, FreeseerCore) or isinstance(core, MinimalistCore)
        
        # superclass #
        QtGui.QMainWindow.__init__(self, None)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        # define members #
        self.core = core
        self.mainWidget = None
        self.menubar = None
        self.backend = None
        
        metadataloader = FreeseerMetadataLoader(core.plugman)
        
        self.__initGui()
        self.mainWidget.fileselect.filemodel.setMetadataLoader(metadataloader)
        self.menubar.setMetadataLoader(metadataloader)
        self.__loadDefaults()
        self.__loadSettings()
        self.__initConnections()
        self.__doInitialActions()
    
    def __initGui(self):
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
    def __loadDefaults(self):
        abspath = path.expanduser("~/Videos")
        self.mainWidget.fileselect.lineEdit_filepath.setText(abspath)
    def __loadSettings(self):
        self.mainWidget.fileselect.lineEdit_filepath.setText(
                self.core.config.videodir)
        self.mainWidget.serverdetails.serverAddress = (
                self.core.config.uploader.serverhistory.server)
        servertype = self.core.config.uploader.serverhistory.servertype
        if servertype != const.NotSelected:
            self.mainWidget.serverdetails.serverType = servertype
        if servertype == const.Sftp:
            self.mainWidget.serverdetails.serverPort = (
                    self.core.config.uploader.serverhistory.port)
        self.mainWidget.serverdetails.username = (
                self.core.config.uploader.serverhistory.username)
    def __initConnections(self):
        self.menubar.actionClose.triggered.connect(self.close)
        self.mainWidget.buttonbar.rejected.connect(self.close)
        self.menubar.actionUpload.triggered.connect(self.upload)
        self.mainWidget.buttonbar.accepted.connect(self.upload)
        
        self.menubar.actionOpen_Directory.triggered.connect(self.browse)
        self.mainWidget.fileselect.browse.connect(self.browse)
        self.mainWidget.fileselect.goDirectory.connect(self.directoryChanged)
        
        self.mainWidget.fileselect._initConnections()
        self.menubar.actionSelect_All.triggered.connect(
                                self.mainWidget.fileselect.filemodel.checkAll)
        self.menubar.actionSelect_None.triggered.connect(
                                self.mainWidget.fileselect.filemodel.checkNone)
        self.menubar.actionInvert_Selection.triggered.connect(
                                self.mainWidget.fileselect.filemodel.checkInvert)
        
        self.menubar.actionMetadata_Launch_Ex_Falso.triggered.connect(
                                self.launchExFalso)
    
    def _validateArguments(self):
        validation_messages = []
        
        # verify arguments
        username = self.mainWidget.serverdetails.username
        state, _ = self.mainWidget.serverdetails.text_validator.validate(
                                                                username, 0)
        if state != QtGui.QValidator.Acceptable:
            validation_messages.append("Please enter a username.")
            
        password = self.mainWidget.serverdetails.password
        state, _ = self.mainWidget.serverdetails.text_validator.validate(
                                                                password, 0)
        if state != QtGui.QValidator.Acceptable:
            validation_messages.append("Please enter your password.")
        serveraddress = self.mainWidget.serverdetails.serverAddress
        state, _ = self.mainWidget.serverdetails.text_validator.validate(
                                                                serveraddress, 0)
        if state != QtGui.QValidator.Acceptable:
            validation_messages.append("Please enter the server address.")
        
        servertype = self.mainWidget.serverdetails.serverType
        if servertype == const.NotSelected:
            validation_messages.append("Server type not selected.")
            
        serverport = None
        if servertype == const.Sftp:
            serverport = self.mainWidget.serverdetails.serverPort
            state, _ = self.mainWidget.serverdetails.port_validator.validate(
                                                                serverport, 0)
            if state != QtGui.QValidator.Acceptable:
                validation_messages.append("Invalid port number.")
            else:
                serverport = int(serverport)
        
        files = self.mainWidget.fileselect.filemodel.getSelectedFiles()
        
        if len(files) <= 0:
            validation_messages.append("Please select one or more files.")
        
        if len(validation_messages) > 0:
            QtGui.QMessageBox.critical(self, "", "\n".join(validation_messages))
            return None
            
        drupal = servertype == const.Drupal
        
        return username, password, serveraddress, serverport, drupal, files
    def _saveHistory(self, args):
        username, password, serveraddress, serverport, drupal, files = args
        history = self.core.config.uploader.serverhistory
        history.port = serverport
        history.username = username
        history.server = serveraddress
        history.servertype = const.Drupal if drupal else const.Sftp
        self.core.config.uploader.write()
    
    @QtCore.pyqtSlot()
    def upload(self):
        args = self._validateArguments()
        if args == None:
            return
        self._saveHistory(args)
        _,_,serveraddress,_,_,files = args
        progressIndicator = UploadProgressIndicator()
        self.backend = UploaderBackend(args, progressIndicator)
        progressIndicator.fileList = files
        progressIndicator.destination = serveraddress
        
        # connect signals/slots between backend and frontend
        progressIndicator.cancelRequested.connect(self.backend.cancel)
        progressIndicator.forceCancelRequested.connect(self.backend.forceCancel)
        self.backend.uploadStarted.connect(progressIndicator.setCurrent)
        self.backend.uploadsComplete.connect(progressIndicator.onComplete)
        progressIndicator.show()
        
        self.backend.uploadAll()
        self.close()
    
    def browse(self):
        oldpath = self.mainWidget.fileselect.directory
        def setPath(newpath):
            if newpath:
                self.mainWidget.fileselect.directory = newpath
                if oldpath != newpath:
                    self.directoryChanged()
        
        if UploaderApp.USE_NATIVE_DIALOG:
            newpath = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Open Directory"), 
                                                             oldpath,
                                                             QtGui.QFileDialog.ShowDirsOnly)
            setPath(newpath)
            
        else:
            dialog = QtGui.QFileDialog(self, self.tr("Open Directory"), oldpath)
            dialog.setModal(True)
            dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
            dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
            dialog.setFileMode(QtGui.QFileDialog.Directory)
            # TODO: set these to favourites.
            sideurls = dialog.sidebarUrls()
            sideurls.append(QtCore.QUrl("file://" + path.expanduser(self.core.config.videodir)))
            dialog.setSidebarUrls(sideurls)
            dialog.directoryEntered.connect(setPath)
            dialog.show()
    
    def directoryChanged(self):
        self.mainWidget.fileselect.filemodel.setDirectory(self.mainWidget.fileselect.directory)

    def __doInitialActions(self):
        self.directoryChanged()

    def retranslate(self):
        self.setWindowTitle(self.tr("Freeseer Video Uploader"))
        
    def launchExFalso(self):
        #exfalsolauncher.run_in_new_process(self.mainWidget.fileselect.directory)
        exfalsolauncher.run(str(self.mainWidget.fileselect.directory))
        
class UploaderBackend(QtCore.QObject):
    '''
    This class starts a single thread that uploads individual files
    '''
    def __init__(self, args, parent=None):
        super(UploaderBackend, self).__init__(parent)
        self.currentindex = -1
        self.numfiles = len(args[5])
        self.cancelRequested = False
        self.cancelForced = False
        
        # we use a different thread so that the ui isn't blocked
        self.uploadThread = UploaderBackendThread(args, self)
        self.uploadThread.finished.connect(self._uploadNext)
#        
#        self.current = QtCore.QTimer()
    
    # called when a single upload is started
    uploadStarted = QtCore.pyqtSignal(int)
    
    # called when all uploads are complete
    uploadsComplete = QtCore.pyqtSignal(int)
    
#    _startUpload = QtCore.pyqtSignal()
    
    def uploadAll(self):
        self.currentindex = -1
        self._uploadNext()
        
    def _uploadNext(self):
        index = self.currentindex
        if self.cancelRequested:
            self.uploadsComplete.emit(index+1)
            return
        if self.cancelForced:
#            self.uploadsComplete.emit(index)
            return
        
        if index+1 >= self.numfiles:
            self.uploadsComplete.emit(index+1)
        else:
            self.currentindex = index+1
            self.upload(self.currentindex)
    
    def upload(self, index):
        self.uploadThread.current = index
        self.uploadStarted.emit(index)
        self.uploadThread.start()
#        self._uploadNext(index)
    
    def cancel(self):
        self.cancelRequested=True
    
    def forceCancel(self):
        self.cancelForced=True
        # todo: find a better way to terminate upload
        self.uploadThread.terminate()
        self.uploadsComplete.emit(self.currentindex)

class UploaderBackendThread(QtCore.QThread):
    def __init__(self, args, parent=None):
        super(UploaderBackendThread, self).__init__(parent)
        (self.username, 
         self.password, 
         self.serveraddress, 
         self.serverport, 
         self.drupal, 
         self.files) = args
        self.current = -1
    
    def __del__(self):
        self.wait()
    
    def run(self):
        current_file = self.files[self.current]
        logging.info("Uploading {0}".format(current_file))
        
#        from freeseer.framework import uploader
        # TODO: set global variables (uuuggghh) in uploader and run.
        # or write a better alternative to uploader
        
        # following is code from the uploader's main that we will have to emulate
#        if drupal:
#            video = VideoData(VIDEO)
#            video.run()
#            node = DrupalNode (video.title, video.body, USER, PASS, HOST, VIDEO)
#            node.save()
#        else:
#            protocol.ClientCreator(reactor, Transport).connectTCP(HOST, 22)
#            reactor.run() #@UndefinedVariable
        
        # placeholder for basic ui testing
        time.sleep(12)
         
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = UploaderApp()
    main.show()
    sys.exit(app.exec_())