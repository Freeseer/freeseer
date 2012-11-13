#!/usr/bin/python

# I realize there are things in here that are unneeded but I was just playing around a bit

import ConfigParser
import logging
import argparse

from freeseer.framework.QtDBConnector import QtDBConnector

import sys,os
import re
import time

from freeseer.framework import metadata_2
from freeseer.framework import plugin as pluginpkg
#from freeseer.framework.plugin import IBackendPlugin
#from freeseer.framework import plugin
import functools


from freeseer.framework.core import FreeseerCore
from freeseer.framework.presentation import Presentation

#from ..framework import metadata
#from freeseer.framework import uploader
from freeseer.frontend.cli import freeseer_talk_parser


from PyQt4 import QtGui, QtCore

def upload():
	#------- Trying to default to the video directory
	config = ConfigParser.ConfigParser()


	configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
	      
	# Config location
	configfile = os.path.abspath("%s/freeseer.conf" % configdir)


	config.readfp(open(configfile))
	#---Trying to get metadata

	vid = FreeSeerTalkParser(argparse.ArgumentParser)

	#vid.show_all_talks()



	#email = raw_input("Email address: ")
	email = "hououo@gmail.com"
	
	#vfile = browse_video_directory()
	#vfile = raw_input("File: ")
	vfile = "TESERT-JOE-TEST.ogg"

	vpath = config.get('Global', 'video_directory')

	#IMetadataReaderB = IMetadataReaderBase()
	base = metadata_2.IMetadataReaderBase()
	meta = metadata_2.FreeseerMetadataLoader(base)
	#meta2 = metadata_2.IMetadataReader(IMetadataReaderBase())
	print meta2.retrieve_metadata(vpath+"/"+vfile)
	

	# Check to see if the filename has a talk in the db
	vid_id = vid.get_talk_by_file(vfile)	
	print vid_id
	

	if vid_id == -1:
    	    title = raw_input("Video title: ")
	    
	    description = raw_input("Description (optional): ")
	    

	else:
	    title = vid.get_title_by_id(vid_id)
	    description = "Event: " + vid.get_event_by_id(vid_id) +"\nSpeaker: " + vid.get_speaker_by_id(vid_id) + "\nRoom: " + vid.get_room_by_id(vid_id)

	category = raw_input("Category (eg Education): ")
	keywords = raw_input("Keywords (optional): ")

	    

	


	

	os.system("python freeseer/youtube_demo/uploader.py --email="+email+" --title="+title+" --category="+category+" --description="+description+" --keywords="+keywords+" " + vpath + "/" + vfile)









#def browse_video_directory():
#    configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
#
#    fileDialog = QtGui.QFileDialog()
#    fileDialog.setFileMode(QtGui.QFileDialog.ShowDirsOnly)
#    filename = fileDialog.getOpenFileName(self, 'Select USB Drive Location')    
#
#    
#    newDir = QtGui.QFileDialog.getExistingDirectory( "Select Video Directory", configdir)
#    if newDir == "": newDir = directory
#       
#    videodir = os.path.abspath(str(newDir))
#
#    return videodir

    #self.generalWidget.recordDirLineEdit.setText(videodir)
    #self.generalWidget.recordDirLineEdit.emit(QtCore.SIGNAL("editingFinished()"))



