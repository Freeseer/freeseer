# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms/freeseer_about.ui'
#
# Created: Fri Apr  2 20:10:35 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FreeseerAbout(object):
    def setupUi(self, FreeseerAbout):
        FreeseerAbout.setObjectName("FreeseerAbout")
        FreeseerAbout.resize(519, 367)
        self.gridLayout_2 = QtGui.QGridLayout(FreeseerAbout)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtGui.QLabel(FreeseerAbout)
        self.label.setPixmap(QtGui.QPixmap("freeseer_logo.png"))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.aboutInfo = QtGui.QLabel(FreeseerAbout)
        self.aboutInfo.setTextFormat(QtCore.Qt.RichText)
        self.aboutInfo.setWordWrap(True)
        self.aboutInfo.setOpenExternalLinks(True)
        self.aboutInfo.setObjectName("aboutInfo")
        self.gridLayout_2.addWidget(self.aboutInfo, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(FreeseerAbout)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(FreeseerAbout)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), FreeseerAbout.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), FreeseerAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(FreeseerAbout)

    def retranslateUi(self, FreeseerAbout):
        FreeseerAbout.setWindowTitle(QtGui.QApplication.translate("FreeseerAbout", "About Freeseer", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutInfo.setText(QtGui.QApplication.translate("FreeseerAbout", "Freeseer", None, QtGui.QApplication.UnicodeUTF8))

