# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_language.ui'
#
# Created: Sat Jan 22 15:07:13 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_languageMainWindow(object):
    def setupUi(self, languageMainWindow):
        languageMainWindow.setObjectName("languageMainWindow")
        languageMainWindow.resize(520, 162)
        languageMainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(languageMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.language_box = QtGui.QComboBox(self.centralwidget)
        self.language_box.setGeometry(QtCore.QRect(150, 20, 211, 31))
        self.language_box.setObjectName("language_box")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 30, 62, 17))
        self.label.setObjectName("label")
        self.country_box = QtGui.QComboBox(self.centralwidget)
        self.country_box.setGeometry(QtCore.QRect(150, 80, 211, 31))
        self.country_box.setObjectName("country_box")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 90, 62, 17))
        self.label_2.setObjectName("label_2")
        self.create_button = QtGui.QPushButton(self.centralwidget)
        self.create_button.setGeometry(QtCore.QRect(400, 50, 93, 27))
        self.create_button.setObjectName("create_button")
        languageMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(languageMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 520, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuUpdate = QtGui.QMenu(self.menubar)
        self.menuUpdate.setObjectName("menuUpdate")
        languageMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(languageMainWindow)
        self.statusbar.setObjectName("statusbar")
        languageMainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(languageMainWindow)
        self.actionExit.setIconText("Quit")
        self.actionExit.setToolTip("Quit")
        self.actionExit.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionExit.setObjectName("actionExit")
        self.translateAction = QtGui.QAction(languageMainWindow)
        self.translateAction.setObjectName("translateAction")
        self.menuFile.addAction(self.actionExit)
        self.menuUpdate.addAction(self.translateAction)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuUpdate.menuAction())

        self.retranslateUi(languageMainWindow)
        QtCore.QMetaObject.connectSlotsByName(languageMainWindow)

    def retranslateUi(self, languageMainWindow):
        languageMainWindow.setWindowTitle(QtGui.QApplication.translate("languageMainWindow", "Add Language", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("languageMainWindow", "Language", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("languageMainWindow", "Country", None, QtGui.QApplication.UnicodeUTF8))
        self.create_button.setText(QtGui.QApplication.translate("languageMainWindow", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("languageMainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuUpdate.setTitle(QtGui.QApplication.translate("languageMainWindow", "&Update", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("languageMainWindow", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("languageMainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.translateAction.setText(QtGui.QApplication.translate("languageMainWindow", "Update Translation Files", None, QtGui.QApplication.UnicodeUTF8))

