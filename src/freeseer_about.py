# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'freeseer_about.ui'
#
# Created: Wed Feb 17 23:08:55 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FreeseerAbout(object):
    def setupUi(self, FreeseerAbout):
        FreeseerAbout.setObjectName("FreeseerAbout")
        FreeseerAbout.resize(519, 367)
        self.buttonBox = QtGui.QDialogButtonBox(FreeseerAbout)
        self.buttonBox.setGeometry(QtCore.QRect(170, 330, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(FreeseerAbout)
        self.label.setGeometry(QtCore.QRect(10, 10, 121, 121))
        self.label.setPixmap(QtGui.QPixmap("logo.png"))
        self.label.setObjectName("label")
        self.textBrowser = QtGui.QTextBrowser(FreeseerAbout)
        self.textBrowser.setGeometry(QtCore.QRect(140, 10, 371, 311))
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setOpenLinks(True)
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(FreeseerAbout)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), FreeseerAbout.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), FreeseerAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(FreeseerAbout)

    def retranslateUi(self, FreeseerAbout):
        FreeseerAbout.setWindowTitle(QtGui.QApplication.translate("FreeseerAbout", "About FreeSeeR", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setStyleSheet(QtGui.QApplication.translate("FreeseerAbout", "background-color: #e6ddd5;\n"
"border: none;\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("FreeseerAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">FreeSeeR</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Version 2.0b rev 2</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">FreeSeeR is a video capture utility capable of capturing presentations. It captures vga output and audio and mixes them together to produce a video.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Copyright (C) 2009-2010 <a href=\"http://www.fosslc.org\"><span style=\" text-decoration: underline; color:#0000ff;\">The Free and Open Source Software Learning Centre</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This software is provided \'as-is\', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software. </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

