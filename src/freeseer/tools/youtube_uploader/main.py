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

@author: Takayuki Higuchi
'''
import sys
sys.path.append('../../tools/youtube_uploader/')
import youtube_upload as youtube
from PyQt4 import QtGui
import os
import commands
#from freeseer import project_info
#from freeseer.framework.core import *
#from freeseer.framework.freeseer_about import *

class UploaderMainApp(QtGui.QWidget):
    def __init__(self, core=None):
        super(UploaderMainApp,self).__init__()

        self.email = QtGui.QLabel('email address:')
        self.password = QtGui.QLabel('password:')
        self.path = QtGui.QLabel('video path:')        
        self.title = QtGui.QLabel('title:')        
        self.category = QtGui.QLabel('category:')        
        
        self.email_edit = QtGui.QLineEdit(self)
        self.password_edit = QtGui.QLineEdit(self)
        self.path_edit = QtGui.QLineEdit(self)
        self.title_edit = QtGui.QLineEdit(self)
        self.upbtn = QtGui.QPushButton('Upload',self)
        self.refbtn = QtGui.QPushButton('reference',self)
        self.combo = QtGui.QComboBox(self)
        self.combo.addItem('Tech')
        self.combo.addItem('Education')
        self.combo.addItem('Animals')
        self.combo.addItem('People')
        self.combo.addItem('Travel')
        self.combo.addItem('Entertainment')
        self.combo.addItem('Howto')
        self.combo.addItem('Sports')
        self.combo.addItem('Autos')
        self.combo.addItem('Music')
        self.combo.addItem('News')
        self.combo.addItem('Games')
        self.combo.addItem('Nonprofit')
        self.combo.addItem('Comedy')
        self.combo.addItem('Film')

        grid = QtGui.QGridLayout()  
        grid.setSpacing(10)
	grid.addWidget(self.email,1,0)
        grid.addWidget(self.password,2,0)
        grid.addWidget(self.path,3,0)
        grid.addWidget(self.email_edit,1,1,1,15)
        grid.addWidget(self.password_edit,2,1,1,15)
        grid.addWidget(self.path_edit,3,1,1,15)
        grid.addWidget(self.title_edit,4,1,1,15)
        grid.addWidget(self.combo,5,1,1,15)
        grid.addWidget(self.refbtn,3,16)
        grid.addWidget(self.title,4,0)
        grid.addWidget(self.category,5,0)
        grid.addWidget(self.upbtn,6,16)
       
        self.password_edit.setEchoMode(self.password_edit.Password)
        self.refbtn.clicked.connect(self.reffile) 
        self.setLayout(grid)
        self.setWindowTitle('Upload video to YouTube')
        self.upbtn.clicked.connect(self.upload)

    def reffile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,'Open File','/home')
        self.path_edit.setText(fname)
    def upload(self):
        email = self.email_edit.text()
        passwd = self.password_edit.text()
        path = str(self.path_edit.text())
        title = self.title_edit.text()
        category = self.combo.currentText()
        cmd = 'youtube-upload --email='+str(email)+' --password='+str(passwd)+' --title='+str(title)+' --category='+str(category)+' '+path
        print cmd
        out = commands.getoutput(cmd)
        print out
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = UploaderMainApp()
    main.show();
    sys.exit(app.exec_())
