# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'freeseer-ui-qt.ui'
#
# Created: Mon Feb  8 19:11:02 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FreeseerMainWindow(object):
    def setupUi(self, FreeseerMainWindow):
        FreeseerMainWindow.setObjectName("FreeseerMainWindow")
        FreeseerMainWindow.resize(499, 323)
        self.centralwidget = QtGui.QWidget(FreeseerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 481, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.recordButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.recordButton.setObjectName("recordButton")
        self.verticalLayout.addWidget(self.recordButton)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.deviceLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.deviceLabel.setMaximumSize(QtCore.QSize(40, 16777215))
        self.deviceLabel.setObjectName("deviceLabel")
        self.horizontalLayout_2.addWidget(self.deviceLabel)
        self.videoDeviceList = QtGui.QComboBox(self.verticalLayoutWidget)
        self.videoDeviceList.setObjectName("videoDeviceList")
        self.horizontalLayout_2.addWidget(self.videoDeviceList)
        self.videoSourceList = QtGui.QComboBox(self.verticalLayoutWidget)
        self.videoSourceList.setObjectName("videoSourceList")
        self.horizontalLayout_2.addWidget(self.videoSourceList)
        self.audioSourceList = QtGui.QComboBox(self.verticalLayoutWidget)
        self.audioSourceList.setObjectName("audioSourceList")
        self.horizontalLayout_2.addWidget(self.audioSourceList)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.talkLabel = QtGui.QLabel(self.verticalLayoutWidget)
        self.talkLabel.setMaximumSize(QtCore.QSize(40, 24))
        self.talkLabel.setObjectName("talkLabel")
        self.horizontalLayout_3.addWidget(self.talkLabel)
        self.talkList = QtGui.QComboBox(self.verticalLayoutWidget)
        self.talkList.setObjectName("talkList")
        self.horizontalLayout_3.addWidget(self.talkList)
        self.editTalksButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.editTalksButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.editTalksButton.setObjectName("editTalksButton")
        self.horizontalLayout_3.addWidget(self.editTalksButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.previewWidget = QtGui.QWidget(self.verticalLayoutWidget)
        self.previewWidget.setObjectName("previewWidget")
        self.horizontalLayout.addWidget(self.previewWidget)
        self.audioFeedbackSlider = QtGui.QSlider(self.verticalLayoutWidget)
        self.audioFeedbackSlider.setOrientation(QtCore.Qt.Vertical)
        self.audioFeedbackSlider.setObjectName("audioFeedbackSlider")
        self.horizontalLayout.addWidget(self.audioFeedbackSlider)
        self.verticalLayout.addLayout(self.horizontalLayout)
        FreeseerMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(FreeseerMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 499, 21))
        self.menubar.setObjectName("menubar")
        self.menuFreeseer = QtGui.QMenu(self.menubar)
        self.menuFreeseer.setObjectName("menuFreeseer")
        FreeseerMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(FreeseerMainWindow)
        self.statusbar.setObjectName("statusbar")
        FreeseerMainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFreeseer.menuAction())

        self.retranslateUi(FreeseerMainWindow)
        QtCore.QMetaObject.connectSlotsByName(FreeseerMainWindow)

    def retranslateUi(self, FreeseerMainWindow):
        FreeseerMainWindow.setWindowTitle(QtGui.QApplication.translate("FreeseerMainWindow", "freeseer - video studio in a backpack", None, QtGui.QApplication.UnicodeUTF8))
        self.recordButton.setText(QtGui.QApplication.translate("FreeseerMainWindow", "Record", None, QtGui.QApplication.UnicodeUTF8))
        self.deviceLabel.setText(QtGui.QApplication.translate("FreeseerMainWindow", "Device:", None, QtGui.QApplication.UnicodeUTF8))
        self.talkLabel.setText(QtGui.QApplication.translate("FreeseerMainWindow", "Talk:", None, QtGui.QApplication.UnicodeUTF8))
        self.editTalksButton.setText(QtGui.QApplication.translate("FreeseerMainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFreeseer.setTitle(QtGui.QApplication.translate("FreeseerMainWindow", "freeseer", None, QtGui.QApplication.UnicodeUTF8))

