#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
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
"""
import glob
import os
import re
import shlex
import sys

import mutagen.oggvorbis
from PyQt4 import QtGui
from youtube_upload import uploadToYouTube

from freeseer.framework.core import FreeseerCore

class UploaderMainApp(QtGui.QWidget):
    def __init__(self, core=None):
        super(UploaderMainApp,self).__init__()
        self.core = FreeseerCore()
        self.config = self.core.get_config()
        #set label
        self.email = QtGui.QLabel('email address:')
        self.password = QtGui.QLabel('password:')
        self.path = QtGui.QLabel('video path:')        
        #self.title = QtGui.QLabel('title:')        
        self.category = QtGui.QLabel('category:')
        self.search_option = QtGui.QLabel('search option')
        self.search_title = QtGui.QLabel('title:') 
        self.search_artist = QtGui.QLabel('artist:')        
        self.search_performer = QtGui.QLabel('performer:')
        self.search_album = QtGui.QLabel('album:')        
        #self.search_location = QtGui.QLabel('location:')        
        self.search_date = QtGui.QLabel('date(y-m-d):')        
        #set button and edit box 
        self.email_edit = QtGui.QLineEdit(self)
        self.password_edit = QtGui.QLineEdit(self)
        self.path_edit = QtGui.QLineEdit(self)
        #self.title_edit = QtGui.QLineEdit(self)
        self.upbtn = QtGui.QPushButton('Upload',self)
        self.refbtn = QtGui.QPushButton('Select file',self)
        self.combo = QtGui.QComboBox(self)
        self.s_title_edit = QtGui.QLineEdit(self)
        self.s_artist_edit = QtGui.QLineEdit(self)
        self.s_performer_edit = QtGui.QLineEdit(self)
        self.s_album_edit = QtGui.QLineEdit(self)
        #self.s_location_edit = QtGui.QLineEdit(self)
        self.s_date_edit = QtGui.QLineEdit(self)
        #set category combo
        CATEGORY_VALUES = ('Education','Tech','Animals',
                'People','Travel','Entertainement','Howto',
                'Sports','Autos','Music','News','Games',
                'Nonprofit','Comedy','Film')
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
        #grid.addWidget(self.search_location,9,1)
        #grid.addWidget(self.s_location_edit,9,2,1,14)
        grid.addWidget(self.search_date,9,1)
        grid.addWidget(self.s_date_edit,9,2,1,14)
        #grid.addWidget(self.title,11,0)
        #grid.addWidget(self.title_edit,11,1,1,15)
        grid.addWidget(self.combo,10,1,1,15)
        grid.addWidget(self.category,10,0)
        grid.addWidget(self.upbtn,11,16)
        #connect function
        self.password_edit.setEchoMode(self.password_edit.Password)
        self.refbtn.clicked.connect(self.open_file_dialog) 
        self.setLayout(grid)
        self.setWindowTitle('Upload video to YouTube')
        self.upbtn.clicked.connect(self.upload)
    #open video folder
    def open_file_dialog(self):
        if (self.s_title_edit.text() or self.s_artist_edit.text()
        or self.s_performer_edit.text() or self.s_album_edit.text()
        or self.s_date_edit.text()):
            file_filter = self.search_video()
            filename = QtGui.QFileDialog.getOpenFileName(self,'Open File',self.config.videodir,file_filter)
        else:
            filename = QtGui.QFileDialog.getOpenFileName(self,'Open File',self.config.videodir,'*.ogg OR *.mpg OR *.mpeg')
        self.path_edit.setText(filename)
    
    def search_video(self):
        title = str(self.s_title_edit.text())
        artist = str(self.s_artist_edit.text())
        performer = str(self.s_performer_edit.text())
        album = str(self.s_album_edit.text())
        #location = self.s_location_edit.text()
        date = str(self.s_date_edit.text())
        video_list = glob.glob(self.config.videodir+'/*.ogg')
        meta = [[""]*5] * len(video_list)
        search_file_index = [True]*len(video_list)

        for i, videofile in enumerate(video_list):
            metadata = mutagen.oggvorbis.Open(videofile)
            try:
                meta[i][0]= metadata["title"][0]
            except KeyError:
                print "cannot extract title of " + videofile
            try:
                meta[i][1] = metadata["artist"][0]
            except KeyError:
                print "cannot extract artist of " + videofile
            try:
                meta[i][2] = metadata["performer"][0]
            except KeyError:
                print "cannot extract performer of " + videofile
            try:
                meta[i][3] = metadata["album"][0]
            except KeyError:
                print "cannot extract album of " + videofile
            try:
                meta[i][4] = metadata["date"][0]
            except KeyError:
                print "cannot extract date of " + videofile

        for i in xrange(len(video_list)):
            if not(re.search(title,meta[i][0])) and title:
                search_file_index[i] = False
            elif not(re.search(artist,meta[i][1])) and artist:
                search_file_index[i] = False
            elif not(re.search(performer,meta[i][2])) and performer:
                search_file_index[i] = False
            elif not(re.search(album,meta[i][3])) and album:
                search_file_index[i] = False
            elif not(re.search(date,meta[i][4])) and date:
                search_file_index[i] = False

        file_filter = ''
        for i in xrange(len(video_list)):
            if file_filter:
                file_filter += ' OR '
            if search_file_index[i]:
                search_file = video_list[i]
                file_filter += os.path.basename(search_file)
        return file_filter 
    
    def upload(self):
        email = str(self.email_edit.text())
        passwd = str(self.password_edit.text())
        path = str(self.path_edit.text())
        #title = str(self.title_edit.text())
        category = str(self.combo.currentText())
        vpath = os.path.dirname(path)
        vfile = os.path.basename(path)
        root, ext = os.path.splitext(vfile)
        if (ext == "ogg") or (ext == "mpg") or (ext == "mpeg"):
            uploadToYouTube(vpath, vfile, email, passwd, category)
        else:
            print vpath + vfile + " is not an ogg or mpg."
