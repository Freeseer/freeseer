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

import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 600)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/freeseer/freeseer_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        
        ## todo: refactor class so that self is centralwidget
        
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_central = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_central.setObjectName("verticalLayout_central")
        
        ### top half ###
        
        self.horizontalLayout_serverdetails = QtGui.QHBoxLayout()
        self.horizontalLayout_serverdetails.setObjectName("horizontalLayout_serverdetails")
        self.groupBox_server = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_server.sizePolicy().hasHeightForWidth())
        self.groupBox_server.setSizePolicy(sizePolicy)
        self.groupBox_server.setObjectName("groupBox_server")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_server)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_serverdetails = QtGui.QFormLayout()
        self.formLayout_serverdetails.setObjectName("formLayout_serverdetails")
        self.label_username = QtGui.QLabel(self.groupBox_server)
        self.label_username.setObjectName("label_username")
        self.formLayout_serverdetails.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_username)
        self.label_password = QtGui.QLabel(self.groupBox_server)
        self.label_password.setObjectName("label_password")
        self.formLayout_serverdetails.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_password)
        self.label_Server = QtGui.QLabel(self.groupBox_server)
        self.label_Server.setObjectName("label_Server")
        self.formLayout_serverdetails.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_Server)
        self.horizontalLayout_serveraddress = QtGui.QHBoxLayout()
        self.horizontalLayout_serveraddress.setObjectName("horizontalLayout_serveraddress")
        self.lineEdit_Server = QtGui.QLineEdit(self.groupBox_server)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Server.sizePolicy().hasHeightForWidth())
        self.lineEdit_Server.setSizePolicy(sizePolicy)
        self.lineEdit_Server.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_Server.setObjectName("lineEdit_Server")
        self.horizontalLayout_serveraddress.addWidget(self.lineEdit_Server)
        self.label_port = QtGui.QLabel(self.groupBox_server)
        self.label_port.setObjectName("label_port")
        self.horizontalLayout_serveraddress.addWidget(self.label_port)
        self.lineEdit_port = QtGui.QLineEdit(self.groupBox_server)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_port.sizePolicy().hasHeightForWidth())
        self.lineEdit_port.setSizePolicy(sizePolicy)
        self.lineEdit_port.setMinimumSize(QtCore.QSize(50, 0))
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.horizontalLayout_serveraddress.addWidget(self.lineEdit_port)
        self.formLayout_serverdetails.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_serveraddress)
        self.lineEdit_password = QtGui.QLineEdit(self.groupBox_server)
        self.lineEdit_password.setText("")
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout_serverdetails.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_password)
        self.lineEdit_username = QtGui.QLineEdit(self.groupBox_server)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.formLayout_serverdetails.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_username)
        self.verticalLayout.addLayout(self.formLayout_serverdetails)
        self.horizontalLayout_servertype = QtGui.QHBoxLayout()
        self.horizontalLayout_servertype.setObjectName("horizontalLayout_servertype")
        self.radioButton_sftp = QtGui.QRadioButton(self.groupBox_server)
        self.radioButton_sftp.setObjectName("radioButton_sftp")
        self.horizontalLayout_servertype.addWidget(self.radioButton_sftp)
        self.radioButton_drupal = QtGui.QRadioButton(self.groupBox_server)
        self.radioButton_drupal.setObjectName("radioButton_drupal")
        self.horizontalLayout_servertype.addWidget(self.radioButton_drupal)
        self.verticalLayout.addLayout(self.horizontalLayout_servertype)
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
        
        self.groupBox_fileselect = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_fileselect.setObjectName("groupBox_fileselect")
        self.verticalLayout_fileselectgbox = QtGui.QVBoxLayout(self.groupBox_fileselect)
        self.verticalLayout_fileselectgbox.setObjectName("verticalLayout_fileselectgbox")
        self.horizontalLayout_filepathbuttons = QtGui.QHBoxLayout()
        self.horizontalLayout_filepathbuttons.setObjectName("horizontalLayout_filepathbuttons")
        self.toolButton_directorydropdown = QtGui.QToolButton(self.groupBox_fileselect)
        self.toolButton_directorydropdown.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolButton_directorydropdown.setArrowType(QtCore.Qt.DownArrow)
        self.toolButton_directorydropdown.setObjectName("toolButton_directorydropdown")
        self.horizontalLayout_filepathbuttons.addWidget(self.toolButton_directorydropdown)
        self.lineEdit_filepath = QtGui.QLineEdit(self.groupBox_fileselect)
        self.lineEdit_filepath.setObjectName("lineEdit_filepath")
        self.horizontalLayout_filepathbuttons.addWidget(self.lineEdit_filepath)
        self.toolButton_filepathgo = QtGui.QToolButton(self.groupBox_fileselect)
        self.toolButton_filepathgo.setObjectName("toolButton_filepathgo")
        self.horizontalLayout_filepathbuttons.addWidget(self.toolButton_filepathgo)
        self.line_filepathspacer = QtGui.QFrame(self.groupBox_fileselect)
        self.line_filepathspacer.setFrameShape(QtGui.QFrame.VLine)
        self.line_filepathspacer.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_filepathspacer.setObjectName("line_filepathspacer")
        self.horizontalLayout_filepathbuttons.addWidget(self.line_filepathspacer)
        self.pushButton_filepathbrowse = QtGui.QPushButton(self.groupBox_fileselect)
        self.pushButton_filepathbrowse.setObjectName("pushButton_filepathbrowse")
        self.horizontalLayout_filepathbuttons.addWidget(self.pushButton_filepathbrowse)
        self.verticalLayout_fileselectgbox.addLayout(self.horizontalLayout_filepathbuttons)
        self.listView_filelist = QtGui.QListView(self.groupBox_fileselect)
        self.listView_filelist.setObjectName("listView_filelist")
        self.verticalLayout_fileselectgbox.addWidget(self.listView_filelist)
        
        ## file selection modification buttons ##
        self.horizontalLayout_fileselectbuttons = QtGui.QHBoxLayout()
        self.horizontalLayout_fileselectbuttons.setObjectName("horizontalLayout_fileselectbuttons")
        
        # all #
        self.toolButton_selectall = QtGui.QToolButton(self.groupBox_fileselect)
        self.toolButton_selectall.setObjectName("toolButton_selectall")
        self.horizontalLayout_fileselectbuttons.addWidget(self.toolButton_selectall)
        
        # none #
        self.toolButton_selectnone = QtGui.QToolButton(self.groupBox_fileselect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_selectnone.sizePolicy().hasHeightForWidth())
#        self.toolButton_selectnone.setSizePolicy(sizePolicy)
        self.toolButton_selectnone.setObjectName("toolButton_selectnone")
        self.horizontalLayout_fileselectbuttons.addWidget(self.toolButton_selectnone)
        
        # invert #
        self.toolButton_selectinvert = QtGui.QToolButton(self.groupBox_fileselect)
        self.toolButton_selectinvert.setObjectName("toolButton_selectinvert")
        self.horizontalLayout_fileselectbuttons.addWidget(self.toolButton_selectinvert)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_fileselectbuttons.addItem(spacerItem1)
        self.toolButton_selectfilter = QtGui.QToolButton(self.groupBox_fileselect)
        self.toolButton_selectfilter.setObjectName("toolButton_selectfilter")
        self.horizontalLayout_fileselectbuttons.addWidget(self.toolButton_selectfilter)
        self.verticalLayout_fileselectgbox.addLayout(self.horizontalLayout_fileselectbuttons)
        
        ## closebutton ##
        self.buttonBox_windowactions = QtGui.QDialogButtonBox(self.groupBox_fileselect)
        self.buttonBox_windowactions.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox_windowactions.setObjectName("buttonBox_windowactions")
        self.verticalLayout_fileselectgbox.addWidget(self.buttonBox_windowactions)
        self.verticalLayout_central.addWidget(self.groupBox_fileselect)
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
        QtCore.QObject.connect(self.buttonBox_windowactions, QtCore.SIGNAL("clicked(QAbstractButton*)"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication
            .translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_server.setTitle(QtGui.QApplication
            .translate("MainWindow", "Server Details", None, QtGui.QApplication.UnicodeUTF8))
        self.label_username.setText(QtGui.QApplication
            .translate("MainWindow", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_password.setText(QtGui.QApplication
            .translate("MainWindow", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_Server.setText(QtGui.QApplication
            .translate("MainWindow", "Server", None, QtGui.QApplication.UnicodeUTF8))
        self.label_port.setText(QtGui.QApplication
            .translate("MainWindow", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_sftp.setText(QtGui.QApplication
            .translate("MainWindow", "SFTP/SCP", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_drupal.setText(QtGui.QApplication
            .translate("MainWindow", "Drupal", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_upload.setText(QtGui.QApplication
            .translate("MainWindow", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_fileselect.setTitle(QtGui.QApplication
            .translate("MainWindow", "File Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_directorydropdown.setText(QtGui.QApplication
            .translate("MainWindow", "Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_filepath.setText(QtGui.QApplication
            .translate("MainWindow", "~/Videos", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_filepathgo.setText(QtGui.QApplication
            .translate("MainWindow", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_filepathbrowse.setText(QtGui.QApplication
            .translate("MainWindow", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_selectall.setText(QtGui.QApplication
            .translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_selectnone.setText(QtGui.QApplication
            .translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_selectinvert.setText(QtGui.QApplication
            .translate("MainWindow", "Invert", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_selectfilter.setText(QtGui.QApplication
            .translate("MainWindow", "Filter...", None, QtGui.QApplication.UnicodeUTF8))
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
    
