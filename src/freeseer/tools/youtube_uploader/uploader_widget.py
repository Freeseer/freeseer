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

class UploaderGuiApp(QtGui.QWidget):
    """
    Class documentation
    GUI for Youtube uploader
    """
    def __init__(self, core=None):
        """
        initial setting of gui for youube uploader
        """
        super(UploaderGuiApp,self).__init__()
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
        self.search_description = QtGui.QLabel('description:')        
        self.search_speaker = QtGui.QLabel('speaker:')
        self.search_event = QtGui.QLabel('event:')        
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
        self.s_description_edit = QtGui.QLineEdit(self)
        self.s_speaker_edit = QtGui.QLineEdit(self)
        self.s_event_edit = QtGui.QLineEdit(self)
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
        grid.addWidget(self.search_description,6,1)
        grid.addWidget(self.s_description_edit,6,2,1,14)
        grid.addWidget(self.search_speaker,7,1)
        grid.addWidget(self.s_speaker_edit,7,2,1,14)
        grid.addWidget(self.search_event,8,1)
        grid.addWidget(self.s_event_edit,8,2,1,14)
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

    def open_file_dialog(self):
        """
        open dialog box for easy video selecting.
        """
        file_filter = "*.ogg OR *.mpg OR *.mpeg"
        if (self.s_title_edit.text() or self.s_description_edit.text()
           or self.s_speaker_edit.text() or self.s_event_edit.text()
           or self.s_date_edit.text()):
            file_filter = self.get_video_filter()
        filename = QtGui.QFileDialog.getOpenFileName(self,'Open File',self.config.videodir,file_filter)
        self.path_edit.setText(filename)
    
    def get_video_filter(self):
        """
        make video filter for easy video search
        """
        title = str(self.s_title_edit.text())
        description = str(self.s_description_edit.text())
        speaker = str(self.s_speaker_edit.text())
        event = str(self.s_event_edit.text())
        #location = self.s_location_edit.text()
        date = str(self.s_date_edit.text())
        video_list = glob.glob(self.config.videodir+'/*.ogg')
        meta = [["" for j in range(5)] for i in range(len(video_list))]
        search_file_index = [True]*len(video_list)

        for i, videofile in enumerate(video_list):
            metadata = mutagen.oggvorbis.Open(videofile)
            print metadata
            if 'title' in metadata:
                meta[i][0]= metadata['title'][0]
            if 'comment' in metadata:
                meta[i][1] = metadata['comment'][0]
            if 'performer' in metadata:
                meta[i][2] = metadata['performer'][0]
            if 'album' in metadata:
                meta[i][3] = metadata['album'][0]
            if 'date' in metadata:
                meta[i][4] = metadata['date'][0]

        for i in xrange(len(video_list)):
            if not(re.search(title.lower(),meta[i][0].lower())) and title:
                search_file_index[i] = False
            elif not(re.search(description.lower(),meta[i][1].lower())) and description:
                search_file_index[i] = False
            elif not(re.search(speaker.lower(),meta[i][2].lower())) and speaker:
                search_file_index[i] = False
            elif not(re.search(event.lower(),meta[i][3].lower())) and event:
                search_file_index[i] = False
            elif not(re.search(date.lower(),meta[i][4].lower())) and date:
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
        """
        execute CLI of youtube uploader
        """
        email = str(self.email_edit.text())
        passwd = str(self.password_edit.text())
        path = str(self.path_edit.text())
        #title = str(self.title_edit.text())
        category = str(self.combo.currentText())
        vpath = os.path.dirname(path)
        vfile = os.path.basename(path)
        ext = os.path.splitext(vfile)[1]
        accepted_formats = ('.ogg', '.mpg', '.mpeg')
        if ext in accepted_formats:
            uploadToYouTube(vpath, vfile, email, passwd, category)
        else:
            print vpath + '/' + vfile + 'is not an ogg or mpg.'
            self.upload_error(vpath + '/' + vfile)
    def upload_error(self,path):
        """
        show error for invalid file uploading
        """
        msgBox = QtGui.QMessageBox(self, windowTitle='upload error', text=path+' is not an ogg or mpg')
        msgBox.exec_()

            
            
