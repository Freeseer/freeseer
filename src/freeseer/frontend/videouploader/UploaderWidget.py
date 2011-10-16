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
# Form implementation generated from reading ui file 'VideoUploader.ui'
#
# Created: Sat Oct 15 09:20:29 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.7
#

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
from ServerDetailsGroupBox import ServerDetailsGroupBox
from FileSelectGroupBox import FileSelectGroupBox
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 600)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/freeseer/freeseer_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        
        ## todo: refactor class so that self is centralwidget
        ## or that self is the MainWindow
        
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_central = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_central.setObjectName("verticalLayout_central")
        
        ### top half ###
        self.horizontalLayout_serverdetails = QtGui.QHBoxLayout()
        self.horizontalLayout_serverdetails.setObjectName("horizontalLayout_serverdetails")
        
        self.groupBox_server = ServerDetailsGroupBox(MainWindow)
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
#        sizePolicy.setVerticalStretch(0)
#        sizePolicy.setHeightForWidth(self.groupBox_server.sizePolicy().hasHeightForWidth())
        self.groupBox_server.setSizePolicy(sizePolicy)
        
        self.horizontalLayout_serverdetails.addWidget(self.groupBox_server)
        
        self.verticalLayout_uploadbutton = QtGui.QVBoxLayout()
        self.verticalLayout_uploadbutton.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout_uploadbutton.setContentsMargins(4, 4, 4, 20)
        self.verticalLayout_uploadbutton.setObjectName("verticalLayout_uploadbutton")
        self.pushButton_upload = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_upload.sizePolicy().hasHeightForWidth())
        
        self.pushButton_upload.setSizePolicy(sizePolicy)
        self.pushButton_upload.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_upload.setBaseSize(QtCore.QSize(0, 100))
        self.pushButton_upload.setAutoDefault(True)
        self.pushButton_upload.setDefault(True)
        self.pushButton_upload.setObjectName("pushButton_upload")
        self.verticalLayout_uploadbutton.addWidget(self.pushButton_upload)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_uploadbutton.addItem(spacerItem)
        self.horizontalLayout_serverdetails.addLayout(self.verticalLayout_uploadbutton)
        
        self.verticalLayout_central.addLayout(self.horizontalLayout_serverdetails)
        
        ### bottom half ###
        
        self.groupBox_fileselect = FileSelectGroupBox(self.centralwidget)
        self.verticalLayout_central.addWidget(self.groupBox_fileselect)
        
        ## closebutton ##
        self.buttonBox_windowactions = QtGui.QDialogButtonBox(self.groupBox_fileselect)
        self.buttonBox_windowactions.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox_windowactions.setObjectName("buttonBox_windowactions")
        self.verticalLayout_central.addWidget(self.buttonBox_windowactions)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        ### menubar ###
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 557, 29))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_Directory = QtGui.QAction(MainWindow)
        self.actionOpen_Directory.setObjectName("actionOpen_Directory")
        self.actionUpload = QtGui.QAction(MainWindow)
        self.actionUpload.setObjectName("actionUpload")
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionSelect_None = QtGui.QAction(MainWindow)
        self.actionSelect_None.setObjectName("actionSelect_None")
        self.actionInvert_Selection = QtGui.QAction(MainWindow)
        self.actionInvert_Selection.setObjectName("actionInvert_Selection")
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionFilter = QtGui.QAction(MainWindow)
        self.actionFilter.setObjectName("actionFilter")
        self.actionFile_Name = QtGui.QAction(MainWindow)
        self.actionFile_Name.setCheckable(True)
        self.actionFile_Name.setChecked(True)
        self.actionFile_Name.setObjectName("actionFile_Name")
        self.actionTitle = QtGui.QAction(MainWindow)
        self.actionTitle.setCheckable(True)
        self.actionTitle.setChecked(True)
        self.actionTitle.setObjectName("actionTitle")
        self.actionArtist = QtGui.QAction(MainWindow)
        self.actionArtist.setCheckable(True)
        self.actionArtist.setChecked(True)
        self.actionArtist.setObjectName("actionArtist")
        self.actionAlbum = QtGui.QAction(MainWindow)
        self.actionAlbum.setObjectName("actionAlbum")
        self.actionLocation = QtGui.QAction(MainWindow)
        self.actionLocation.setCheckable(True)
        self.actionLocation.setChecked(True)
        self.actionLocation.setObjectName("actionLocation")
        self.actionTrack_Number = QtGui.QAction(MainWindow)
        self.actionTrack_Number.setObjectName("actionTrack_Number")
        self.actionDate = QtGui.QAction(MainWindow)
        self.actionDate.setCheckable(True)
        self.actionDate.setChecked(True)
        self.actionDate.setObjectName("actionDate")
        self.actionComment = QtGui.QAction(MainWindow)
        self.actionComment.setObjectName("actionComment")
        self.actionDuration = QtGui.QAction(MainWindow)
        self.actionDuration.setCheckable(True)
        self.actionDuration.setChecked(True)
        self.actionDuration.setObjectName("actionDuration")
        self.actionMetadata_Launch_Ex_Falso = QtGui.QAction(MainWindow)
        self.actionMetadata_Launch_Ex_Falso.setObjectName("actionMetadata_Launch_Ex_Falso")
        
        self.menuFile.addAction(self.actionOpen_Directory)
        self.menuFile.addAction(self.actionUpload)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionSelect_None)
        self.menuEdit.addAction(self.actionInvert_Selection)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionMetadata_Launch_Ex_Falso)
        self.menuEdit.addAction(self.actionPreferences)
        self.menuView.addAction(self.actionFilter)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionFile_Name)
        self.menuView.addAction(self.actionTrack_Number)
        self.menuView.addAction(self.actionTitle)
        self.menuView.addAction(self.actionArtist)
        self.menuView.addAction(self.actionAlbum)
        self.menuView.addAction(self.actionLocation)
        self.menuView.addAction(self.actionDate)
        self.menuView.addAction(self.actionComment)
        self.menuView.addAction(self.actionDuration)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        
        
        
        # Signals and slots connections
#        QtCore.QObject.connect(self.buttonBox_windowactions, QtCore.SIGNAL("clicked(QAbstractButton*)"), MainWindow.close)
        QtCore.QObject.connect(self.buttonBox_windowactions, QtCore.SIGNAL("clicked(QAbstractButton*)"), self.customButtonBoxSlot)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#        self.buttonBox_windowactions.connect(QObject, SIGNAL()
#        self.buttonBox_windowactions.clicked.connect(self.customButtonBoxSlot)
#        self.buttonBox_windowactions.clicked.emit(self.toolButton_selectall)
#        self.connect(self.addTalkWidget.addButton, QtCore.SIGNAL('clicked()'), self.add_talk)
#        self.actionClose.triggered.
        
    @QtCore.pyqtSlot(QtGui.QAbstractButton)
    def customButtonBoxSlot(self, button):
        print "clicked"
        print button
#    
#    def testslot(self, button):
#        print "clicked"
#        print button

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication
            .translate("MainWindow", "Freeseer Video Uploader", None, QtGui.QApplication.UnicodeUTF8))
        
        self.pushButton_upload.setText(QtGui.QApplication
            .translate("MainWindow", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        
        self.menuFile.setTitle(QtGui.QApplication
            .translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication
            .translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication
            .translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Directory.setText(QtGui.QApplication
            .translate("MainWindow", "Open Directory...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpload.setText(QtGui.QApplication
            .translate("MainWindow", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication
            .translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication
            .translate("MainWindow", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelect_None.setText(QtGui.QApplication
            .translate("MainWindow", "Select None", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInvert_Selection.setText(QtGui.QApplication
            .translate("MainWindow", "Invert Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication
            .translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFilter.setText(QtGui.QApplication
            .translate("MainWindow", "Filter...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFile_Name.setText(QtGui.QApplication
            .translate("MainWindow", "Filename", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTitle.setText(QtGui.QApplication
            .translate("MainWindow", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.actionArtist.setText(QtGui.QApplication
            .translate("MainWindow", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAlbum.setText(QtGui.QApplication
            .translate("MainWindow", "Album", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLocation.setText(QtGui.QApplication
            .translate("MainWindow", "Location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTrack_Number.setText(QtGui.QApplication
            .translate("MainWindow", "Track Number", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDate.setText(QtGui.QApplication
            .translate("MainWindow", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.actionComment.setText(QtGui.QApplication
            .translate("MainWindow", "Comment", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDuration.setText(QtGui.QApplication
            .translate("MainWindow", "Duration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMetadata_Launch_Ex_Falso.setText(QtGui.QApplication
            .translate("MainWindow", "Metadata (Launch Ex Falso)", None, QtGui.QApplication.UnicodeUTF8))
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = QtGui.QMainWindow()
    Ui_MainWindow().setupUi(main)
    main.show()
    sys.exit(app.exec_())
    
