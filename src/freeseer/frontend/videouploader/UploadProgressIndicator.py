

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
class UploadProgressIndicator(QtGui.QWidget):
    def __init__(self, parent=None):
        super(UploadProgressIndicator, self).__init__(parent)
        self.ui = Ui_UploadProgressIndicator(self)
        
        self.ui.buttonBox.rejected.connect(self.onCancel)
        
    def setFileList(self, files):
        pass
    
    def setDestination(self, server):
        pass
    
    def setCurrent(self, index):
        pass
    
    def onCancel(self):
        self.close()
        
#    def onComplete(self):
#        self.ui.displayComplete(True)
        
    def resizeEvent(self, event):
        print event
        return QtGui.QWidget.resizeEvent(self, event)
    
    cancelRequested = QtCore.pyqtSignal()
        
    retranslate = lambda self:self.ui.retranslateUi()

class Ui_UploadProgressIndicator(object):
    def __init__(self, target):
        assert isinstance(target, UploadProgressIndicator)
        self.target = target
        self.iscomplete = False
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
    
    def displayComplete(self, iscomplete):
        self.iscomplete = iscomplete
        (self.statusWidget if iscomplete else self.completeWidget).setVisible(False)
        (self.completeWidget if iscomplete else self.statusWidget).setVisible(True)
        self.retranslateUi()
    
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

class UploadCancelPrompt(QtGui.QDialog):
    def __init__(self):
        super(UploadCancelPrompt, self).__init__()
#        self.ui = Ui_UploadCancelPrompt(self)
        
#        QtGui.QDialog.

class UploadCompleteReviewer(QtGui.QDialog):
    def __init__(self, parent=None):
        super(UploadCompleteReviewer, self).__init__(parent)
        self.ui = Ui_UploadCompleteReviewer(self)
    
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
    msgbox = QtGui.QMessageBox(QtGui.QMessageBox.Question,
            "Cancel Upload", "Are you sure you want to cancel the current upload?", 
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
    msgbtn_tertiary = QtGui.QPushButton("Finish the current upload and cancel the rest")
    msgbox.addButton(msgbtn_tertiary, QtGui.QMessageBox.ActionRole)
    msgbox.show()
    sys.exit(app.exec_())