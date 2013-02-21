#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
freeseer - vga/presentation capture software

Copyright (C) 2013  Free and Open Source Software Learning Centre
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
import glob
from os.path import expanduser
import youtube_upload as youtube
from PyQt4 import QtGui
import os
from scrapemark import scrape

class UploaderMainApp(QtGui.QWidget):
    def __init__(self, core=None):
        super(UploaderMainApp,self).__init__()
        #set label
        self.email = QtGui.QLabel('email address:')
        self.password = QtGui.QLabel('password:')
        self.path = QtGui.QLabel('video path:')        
        self.title = QtGui.QLabel('title:')        
        self.category = QtGui.QLabel('category:')
        self.search_option = QtGui.QLabel('search option')
        self.search_title = QtGui.QLabel('title:') 
        self.search_artist = QtGui.QLabel('artist:')        
        self.search_performer = QtGui.QLabel('performer:')
        self.search_album = QtGui.QLabel('album:')        
        self.search_location = QtGui.QLabel('location:')        
        self.search_date = QtGui.QLabel('date(y-m-d):')        
        #set button and edit box 
        self.email_edit = QtGui.QLineEdit(self)
        self.password_edit = QtGui.QLineEdit(self)
        self.path_edit = QtGui.QLineEdit(self)
        self.title_edit = QtGui.QLineEdit(self)
        self.upbtn = QtGui.QPushButton('Upload',self)
        self.refbtn = QtGui.QPushButton('reference',self)
        self.combo = QtGui.QComboBox(self)
        self.s_title_edit = QtGui.QLineEdit(self)
        self.s_artist_edit = QtGui.QLineEdit(self)
        self.s_performer_edit = QtGui.QLineEdit(self)
        self.s_album_edit = QtGui.QLineEdit(self)
        self.s_location_edit = QtGui.QLineEdit(self)
        self.s_date_edit = QtGui.QLineEdit(self)
        #set category combo
	CATEGORY_VALUES = ['Tech','Education','Animals',
			'People','Travel','Entertainement','Howto',
			'Sports','Autos','Music','News','Games'
			'Nonprofit','Comedy','Film']
        for category in CATEGORY_VALUES:
            self.combo.addItem(category)
	#arrange items
        grid = QtGui.QGridLayout()  
        grid.setSpacing(10)
	grid.addWidget(self.email,1,0)
        grid.addWidget(self.email_edit,1,1,1,15)
        grid.addWidget(self.password,2,0)
        grid.addWidget(self.password_edit,2,1,1,15)
        grid.addWidget(self.path,3,0)
        grid.addWidget(self.path_edit,3,1,1,15)
        grid.addWidget(self.refbtn,3,16)
        grid.addWidget(self.search_option,4,1,1,15)
        grid.addWidget(self.search_title,5,1)
        grid.addWidget(self.s_title_edit,5,2,1,14)
        grid.addWidget(self.search_artist,6,1)
        grid.addWidget(self.s_artist_edit,6,2,1,14)
        grid.addWidget(self.search_performer,7,1)
        grid.addWidget(self.s_performer_edit,7,2,1,14)
        grid.addWidget(self.search_album,8,1)
        grid.addWidget(self.s_album_edit,8,2,1,14)
        grid.addWidget(self.search_location,9,1)
        grid.addWidget(self.s_location_edit,9,2,1,14)
        grid.addWidget(self.search_date,10,1)
        grid.addWidget(self.s_date_edit,10,2,1,14)
        grid.addWidget(self.title,11,0)
        grid.addWidget(self.title_edit,11,1,1,15)
        grid.addWidget(self.combo,12,1,1,15)
        grid.addWidget(self.category,12,0)
        grid.addWidget(self.upbtn,13,16)
        #connect function
        self.password_edit.setEchoMode(self.password_edit.Password)
        self.refbtn.clicked.connect(self.reffile) 
        self.setLayout(grid)
        self.setWindowTitle('Upload video to YouTube')
        self.upbtn.clicked.connect(self.upload)
    #open video folder
    def reffile(self):
	if not((self.s_title_edit.text()=='') and (self.s_artist_edit.text()=='') \
	and (self.s_performer_edit.text()=='') and (self.s_album_edit.text()=='') \
	and (self.s_location_edit.text()=='') and (self.s_date_edit.text()=='')):
	    filt = self.search_video()
            fname = QtGui.QFileDialog.getOpenFileName(self,'Open File',expanduser("~/Videos/"),filt)
	else:
            fname = QtGui.QFileDialog.getOpenFileName(self,'Open File',expanduser("~/Videos/"),'*.ogg OR *.mpg OR *.mpeg')
        self.path_edit.setText(fname)
        

    #upload video
    def search_video(self):
        title = self.s_title_edit.text()
        artist = self.s_artist_edit.text()
        performer = self.s_performer_edit.text()
        album = self.s_album_edit.text()
        location = self.s_location_edit.text()
        date = self.s_date_edit.text()
	xml_list = glob.glob(expanduser("~/Videos/")+'*.xml')
	meta = [[0 for j in range(6)] for i in range(len(xml_list))]
	upload_file_index = [True for i in range(len(xml_list))]
	i = 0
	for xml in xml_list:
	    f = open(xml)
            meta_text = f.read()
            meta[i][0] = scrape("""<title>{{ }}</title>""",meta_text)
            meta[i][1] = scrape("""<artist>{{ }}</artist>""",meta_text)
            meta[i][2] = scrape("""<performer>{{ }}</performer>""",meta_text)
            meta[i][3] = scrape("""<album>{{ }}</album>""",meta_text)
            meta[i][4] = scrape("""<location>{{ }}</location>""",meta_text)
            meta[i][5] = scrape("""<date>{{ }}</date>""",meta_text)
            f.close()
            i = i+1
        for i in range(len(xml_list)):
            if not((meta[i][0]==title) or (title=='')):
                upload_file_index[i]=False
                continue
            elif not((meta[i][1]==artist) or (artist=='')):
                upload_file_index[i]=False
                continue
            elif not((meta[i][2]==performer) or (performer=='')):
                upload_file_index[i]=False
                continue
            elif not((meta[i][3]==album) or (album=='')):
                upload_file_index[i]=False
                continue
            elif not((meta[i][4]==location) or (location=='')):
                upload_file_index[i]=False
                continue
            elif not((meta[i][5]==date) or (date=='')):
                upload_file_index[i]=False
                continue
        filt = ''
        for i in range(len(xml_list)):
            if not(filt==''):
                filt = filt + ' OR '
            if upload_file_index[i]==True:
                xml_file = xml_list[i]
                filt = filt + os.path.basename(xml_file.replace('.xml',''))

        return filt 
    def upload(self):
        email = self.email_edit.text()
        passwd = self.password_edit.text()
        path = str(self.path_edit.text())
        title = self.title_edit.text()
        category = self.combo.currentText()
	#replace existing cli
        cmd = 'youtube-upload --email='+str(email)+' --password='+str(passwd)+' --title='+str(title)+' --category='+str(category)+' '+path
        print cmd
        out = commands.getoutput(cmd)
        print out
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = UploaderMainApp()
    main.show();
    sys.exit(app.exec_())
