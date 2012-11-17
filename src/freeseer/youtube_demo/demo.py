#!/usr/bin/python

# I realize there are imports that are unneeded but I was just playing around a bit

import ConfigParser
import logging
import argparse

#from freeseer.framework.QtDBConnector import QtDBConnector
import sys,os
import re
import time
#from freeseer.framework.core import FreeseerCore
#from freeseer.framework.presentation import Presentation
from freeseer.youtube_demo import uploader
import getpass
import shlex




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


	email = raw_input("Email address: ")
	password = getpass.getpass()
	#vfile = browse_video_directory()
	vfile = raw_input("File/Directory: ")

	
	# If the vfile is a directory then walk through the directory and upload all it's videos
	if os.path.isdir(vpath+"/"+vfile):
		for root, dirs, files in os.walk(vpath+"/"+vfile):
			i=0
			while i < len(files):
				#print str(root)+"/"+files[i-1]
				uploadToYouTube(str(root), files[i-1], email, password)
				i=i+1


	# Otherwise just upload the one video
	else:
		uploadToYouTube(vpath, vfile, email, password)



	#ogg_vfile = ""
	#mpg_vfile = vfile


	
	# This was for checking if the file video was an ogg or an mpg, checking if there existed a converted version already, and converting it
	"""
	if vfile[len(vfile)-3:] == "ogg":

		metadata = mutagen.oggvorbis.Open(vpath+"/"+vfile)
		ogg_vfile = vfile

		if vfile[:len(vfile)-4]+"_glued.mpg" not in os.listdir(vpath):
			print "NOT FOUND!"

			if raw_input("Convert video to mpg (ogg format is not accepted by YouTube) [Y/n]? ") == "Y":
				print os.system("../bin/post-process.sh " + vpath)

			else:
				print "YouTube will not accept ogg file. Goodbye."
				return

			
			mpg_vfile = vfile[:len(vfile)-4]+"_glued.mpg"
			
		print metadata.pprint()


	if vfile[len(vfile)-3:] == "mpg":
		
		if vfile[:len(vfile)-10] + ".ogg" in os.listdir(vpath):
			print "OGG FOR MPG!"
			mpg_vfile = vfile
			ogg_vfile = vfile[:len(vfile)-10] + ".ogg"

			metadata = mutagen.oggvorbis.Open(vpath+"/"+ogg_vfile)
			print metadata.pprint()

	"""




		

	#if ogg_vfile != "":

# Uploads an ogg or mpg to YouTube, using the metadata from an ogg
def uploadToYouTube(vpath, vfile, email, password):

	# Get the title and description if video is an ogg file
	if vfile.lower().endswith(('.ogg', '.mpg')):
		if vfile.lower().endswith('.ogg'):

			metadata = mutagen.oggvorbis.Open(vpath+"/"+vfile)
			#print metadata.pprint()

			try:
				title = metadata["title"][0]
				print title
			except KeyError:
				title = vfile


			try:
				description = metadata["description"][0]
				print description
			except KeyError:
				description = ""

		
	
		else:
			title = vfile
			description = ""
	else:
		print vpath+"/"+vfile +" is not an ogg or mpg"
		return

	# Default category to education for now
	category = "Education"


	uploader.main_upload(shlex.split("--email="+email+" --password="+password+" --title="+title+" --category="+category+" --description="+'"'+description+'" ' + vpath+"/"+vfile))





#----------------------------------


# Was maybe thinking of having a file browser to pick the file, but needs work
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







