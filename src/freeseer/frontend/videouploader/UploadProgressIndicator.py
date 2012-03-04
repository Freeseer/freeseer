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
http://wiki.github.com/Freeseer/freeseer/

@author: Jordan Klassen
'''

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
class UploadProgressIndicator(QtGui.QWidget):
    def __init__(self, parent=None):
        super(UploadProgressIndicator, self).__init__(parent)
        self.ui = Ui_UploadProgressIndicator(self)
        self.ui.buttonBox.rejected.connect(self.onCancel)
        
        self._fileList = []
        self._destination = ''
        self._current = 0
        
        self.cancelPrompt = None
        self.completeReviewer = None
        
    fileList = property(lambda self:self._fileList)
    @fileList.setter
    def fileList(self, files):
        self.ui.progressBar.setMaximum(len(files))
        self._fileList = files
    
    destination = property(lambda self:self._destination)
    @destination.setter
    def destination(self, server):
        self._destination = server
        self.ui.label_destination.setText(server)
    
    current = property(lambda self:self._current)
    @current.setter
    def current(self, index):
        self._current = index
        self.ui.label_current.setText(self.fileList[index])
        self.ui.progressBar.setValue(index+1)
        
    @QtCore.pyqtSlot(int)
    def setCurrent(self, index):
        self.current = index
        
    def onCancel(self):
        self.cancelPrompt = UploadCancelPrompt(self)
        self.cancelPrompt.accepted.connect(self.forceCancel)
        self.cancelPrompt.delayedAndAccepted.connect(self.cancel)
        self.cancelPrompt.show()
        
    def cancel(self):
        self.cancelRequested.emit()
        
    def forceCancel(self):
        self.forceCancelRequested.emit()
        self.close()
    
    @QtCore.pyqtSlot(int)
    def onComplete(self, num=-1):
        if num == -1:
            num = len(self.fileList)
        self.close()
        self.completeReviewer = UploadCompleteReviewer()
        self.completeReviewer.setFileList(self.fileList[:num])
        self.completeReviewer.show()
        
#    def resizeEvent(self, event):
#        return QtGui.QWidget.resizeEvent(self, event)
    
    cancelRequested = QtCore.pyqtSignal()
    forceCancelRequested = QtCore.pyqtSignal()
        
    retranslate = lambda self:self.ui.retranslateUi()

class Ui_UploadProgressIndicator(object):
    def __init__(self, target):
        assert isinstance(target, UploadProgressIndicator)
        self.target = target
        target.setWindowFlags(target.windowFlags() & ~Qt.WindowCloseButtonHint & ~Qt.WindowMaximizeButtonHint)
        
        target.resize(400, 140)
        target.setMaximumHeight(100)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(target.sizePolicy().hasHeightForWidth())
        target.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(target)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_current_head = QtGui.QLabel(target)
        self.label_current_head.setObjectName("label_current_head")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_current_head)
        self.label_destination_head = QtGui.QLabel(target)
        self.label_destination_head.setObjectName("label_destination_head")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_destination_head)
        self.label_current = QtGui.QLabel(target)
        self.label_current.setText("")
        self.label_current.setObjectName("label_current")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_current)
        self.label_destination = QtGui.QLabel(target)
        self.label_destination.setText("")
        self.label_destination.setObjectName("label_destination")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_destination)
        self.verticalLayout.addLayout(self.formLayout)
        
        self.progressBar = QtGui.QProgressBar(target)
        self.progressBar.setMaximum(3)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(target)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(target)
    
    def retranslateUi(self):
        self.target.setWindowTitle(QtGui.QApplication.translate(
                "UploadProgressIndicator", "Uploading Videos", 
                None, QtGui.QApplication.UnicodeUTF8))
        self.label_current_head.setText(QtGui.QApplication.translate(
                "UploadProgressIndicator", "Current File", 
                None, QtGui.QApplication.UnicodeUTF8))
        self.label_destination_head.setText(QtGui.QApplication.translate(
                "UploadProgressIndicator", "Destination", 
                None, QtGui.QApplication.UnicodeUTF8))
        self.progressBar.setFormat(QtGui.QApplication.translate(
                "UploadProgressIndicator", "Transferring file %v of %m (%p%)", 
                None, QtGui.QApplication.UnicodeUTF8))

class UploadCancelPrompt(QtGui.QMessageBox):
    def __init__(self, parent=None):
        super(UploadCancelPrompt, self).__init__(QtGui.QMessageBox.Question,
            QtGui.QApplication.translate(
                "UploadCancelPrompt", "Cancel Upload", 
                None, QtGui.QApplication.UnicodeUTF8), 
                QtGui.QApplication.translate(
                "UploadCancelPrompt", "Are you sure you want to cancel the current upload?", 
                None, QtGui.QApplication.UnicodeUTF8),
            buttons=QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, 
            parent=parent)
        self.thirdoption = QtGui.QPushButton(
                QtGui.QApplication.translate(
                "UploadCancelPrompt", "Yes, but &finish the current file",
                None, QtGui.QApplication.UnicodeUTF8))
        self.addButton(self.thirdoption, QtGui.QMessageBox.YesRole)
        
        self.setDefaultButton(self.Yes)
        self.setEscapeButton(self.No)
        
        self.button(self.Yes).clicked.connect(self.accept)
        self.button(self.No).clicked.connect(self.reject)
        self.thirdoption.clicked.connect(self.delayAndAccept)
        
    @QtCore.pyqtSlot()
    def delayAndAccept(self):
        self.delayedAndAccepted.emit()    
    
    delayedAndAccepted = QtCore.pyqtSignal()

class UploadCompleteReviewer(QtGui.QDialog):
    def __init__(self, parent=None):
        super(UploadCompleteReviewer, self).__init__(parent)
        self.ui = Ui_UploadCompleteReviewer(self)
        self.ui.buttonBox.accepted.connect(self.accept)
    
    def setFileList(self, files):
        self.ui.textEdit_completeStatus.setText("\n".join(files))

class Ui_UploadCompleteReviewer(object):
    def __init__(self, target):
        self.target = target
        
        self.verticalLayout = QtGui.QVBoxLayout(target)
        self.label_completeStatus = QtGui.QLabel(target)
#        font = self.label_completeStatus.font()
#        font.setItalic(True)
#        self.label_completeStatus.setFont(font)
        self.verticalLayout.addWidget(self.label_completeStatus)
        self.textEdit_completeStatus = QtGui.QTextEdit(target)
        self.textEdit_completeStatus.setReadOnly(True)
        self.verticalLayout.addWidget(self.textEdit_completeStatus)
        self.buttonBox = QtGui.QDialogButtonBox(target)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)
        
        self.buttonBox.accepted.connect(target.close)
        self.retranslateUi()
        
    def retranslateUi(self):
        self.target.setWindowTitle(QtGui.QApplication.translate(
                "UploadCompleteReviewer", 
                "File Transfer Complete", 
                None, QtGui.QApplication.UnicodeUTF8))
        self.label_completeStatus.setText(QtGui.QApplication.translate(
                "UploadCompleteReviewer", 
                "<em>The following files were successfully uploaded:</em>", 
                None, QtGui.QApplication.UnicodeUTF8))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = UploadProgressIndicator()
    main.show()
    secondary = UploadCompleteReviewer()
    secondary.show()
#    msgbox = UploadCancelPrompt(main)
#    msgbox.show()
    sys.exit(app.exec_())