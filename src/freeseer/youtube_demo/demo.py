#!/usr/bin/python

# I realize there are things in here that are unneeded but I was just playing around a bit

import ConfigParser
import logging
import argparse

from freeseer.framework.QtDBConnector import QtDBConnector

import sys,os
import re
import time

from freeseer.framework.core import FreeseerCore
from freeseer.framework.presentation import Presentation

#from ..framework import metadata
#from freeseer.framework import uploader
#from freeseer.frontend.cli import freeseer_talk_parser

#from mutagen.oggtheora import OggTheora
#import mutagen.ogg
import mutagen.oggtheora
import mutagen.oggvorbis


from PyQt4 import QtGui, QtCore

def upload():
	#------- Trying to default to the video directory
	config = ConfigParser.ConfigParser()


	configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
	      
	# Config location
	configfile = os.path.abspath("%s/freeseer.conf" % configdir)

	config.readfp(open(configfile))

	


	vpath = config.get('Global', 'video_directory')

	#email = raw_input("Email address: ")
	email = "hououo@gmail.com"
	#vfile = browse_video_directory()
	#vfile = raw_input("File: ")
	vfile1 = "SUPER-THEROO-JACK-TEST2.ogg"
	vfile2 = "T12345-01.ogg"
	vfile = "SUPER-THEROO-JACK-TEST2_glued.mpg"


	#---Trying to get metadata
	
	#vid = mutagen.ogg.OggFileType(vpath+"/"+vfile)
	#video = OggTheora(vpath+"/"+vfile)
	#metadata = mutagen.oggtheora.Open(vpath+"/"+vfile)
	if vfile[len(vfile)-3:] == "ogg":
		metadata = mutagen.oggvorbis.Open(vpath+"/"+vfile)
	#metadata.load(vpath+"/"+vfile)
	#metadata["title"] = "An example"
		print metadata.pprint()
	#print metadata._Tags
	#print metadata["title"]

        #video["title"] = "An example"
        #video.pprint()
  
	
	#title1 = str(metadata["artist"])[3:len(str(metadata["title"]))-2]
	#print title1
    	#title = raw_input("Video title: ")
		try:
			meta_title = str(metadata["title"])[3:len(str(metadata["title"]))-2]
			title = raw_default("Video title: ", meta_title)
		except KeyError:
			title = raw_input("Video title: ")


		category = raw_input("Category (eg Education): ")


		try:
			artist = str(metadata["artist"])[3:len(str(metadata["artist"]))-2]
			artist2 = "Speaker: " + artist
		except KeyError:
			artist = ""
			artist2 = ""

		try:
			album = str(metadata["album"])[3:len(str(metadata["album"]))-2]
			album2 = "Event: " + album
		except KeyError:
			album = ""
			album2 = ""

		try:
			comment = str(metadata["comment"])[3:len(str(metadata["comment"]))-2]
		except KeyError:
			comment = ""

		try:
			date = str(metadata["date"])[3:len(str(metadata["date"]))-2]
		except KeyError:
			date = ""


		    
		description = raw_default("Description (optional): ",artist2 + " " + album2 + " " + comment + " " + date)
		keywords = raw_default("Keywords (optional): ", artist + "," + album)
	
	else:
		title = raw_input("Video title: ")
		category = raw_input("Category (eg Education): ")
		description = raw_input("Description (optional): ")
		keywords = raw_input("Keywords (optional): ")
	



	

	os.system("python freeseer/youtube_demo/uploader.py --email="+email+" --title="+title+" --category="+category+" --description="+description+" --keywords="+keywords+" " + vpath + "/" + vfile)

	#os.system("python freeseer/youtube_demo/uploader.py --email="+email+" --title="+title+" --category="+category+" --description="+description+" --keywords="+keywords+" " + vpath + "/T12345-01_glued.mpg")





#----------------------------------

"""
def browse_video_directory():
    configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))

    fileDialog = QtGui.QFileDialog()
    fileDialog.setFileMode(QtGui.QFileDialog.ShowDirsOnly)
    filename = fileDialog.getOpenFileName(self, 'Select USB Drive Location')    

    
    newDir = QtGui.QFileDialog.getExistingDirectory( "Select Video Directory", configdir)
    if newDir == "": newDir = directory
       
    videodir = os.path.abspath(str(newDir))

    return videodir

    #self.generalWidget.recordDirLineEdit.setText(videodir)
    #self.generalWidget.recordDirLineEdit.emit(QtCore.SIGNAL("editingFinished()"))
"""




def raw_default(prompt, dflt=None):
	if dflt:
		prompt = "%s [%s]: " % (prompt, dflt)
		res = raw_input(prompt)
	if not res and dflt:
		return dflt
	return res
