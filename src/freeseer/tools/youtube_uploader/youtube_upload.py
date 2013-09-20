#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2012 Free and Open Source Software Learning Centre
# http://fosslc.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/


import ConfigParser
import os
import getpass
import shlex
import subprocess

import mutagen.oggvorbis

from lib.youtube_upload import youtube_upload
from lib.completer import completer


def upload():
    #------- Trying to default to the video directory
    config = ConfigParser.ConfigParser()
    configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
    # Config location
    configfile = os.path.abspath("%s/freeseer.conf" % configdir)
    config.readfp(open(configfile))
    vpath = config.get('Global', 'video_directory')

    email = raw_input("Email (user@example.com): ")
    password = getpass.getpass()
    #vfile = browse_video_directory()
    completer()
    vfile = raw_input("File: ")
    uploadTest(vfile, email, password)

    '''
	# Check whether the file exists, and ask again if not
	while os.path.exists(vpath+"/"+vfile) == False:
		print "Cannot find file or directory " + vpath+"/"+vfile
		vfile = raw_input("File or Directory: "+vpath+"/")
	
	# If the vfile is a directory then walk through the directory and upload all it's videos
	if os.path.isdir(vpath+"/"+vfile):
		for root, dirs, files in os.walk(vpath+"/"+vfile):
			i=0
			while i < len(files):
				print str(root)+"/"+files[i-1]
				uploadToYouTube(str(root), files[i-1], email, password)
				i=i+1
	# Otherwise just upload the one video
	else:
		uploadToYouTube(vpath, vfile, email, password)
	'''

    #ogg_vfile = ""
    #mpg_vfile = vfile
    # This was for checking if the file video was an ogg or an mpg, checking if there existed a converted version already,
    # and converting it. Leaving it for now since conversion may be done in
    # the future.
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
    # if ogg_vfile != "":

# Uploads an ogg or mpg to YouTube, using the metadata from an ogg


def uploadToYouTube(vpath, vfile, email, password):

    # Get the title and description if video is an ogg file
    if vfile.lower().endswith(('.ogg', '.mpg')):
        if vfile.lower().endswith('.ogg'):
            metadata = mutagen.oggvorbis.Open(vpath + "/" + vfile)
            # print metadata.pprint()
            try:
                title = metadata["title"][0]
            except KeyError:
                title = vfile

            try:
                description = metadata["description"][0]
            except KeyError:
                description = ""

        else:
            title = vfile
            description = ""
    else:
        print vpath + "/" + vfile + " is not an ogg or mpg"
        return

    # Default category to education for now
    category = "Education"

    p = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)(shlex.split("--email=" + email + " --password=" + password + " --title=" +
                                                               title + " --category=" + category + " --description=" + '"' + description + '" ' + vpath + "/" + vfile))


def uploadTest(vfile, email, password):
    # Get the title and description if video is an ogg file
    if vfile.lower().endswith(('.ogg', '.mpg')):
        if vfile.lower().endswith('.ogg'):
            metadata = mutagen.oggvorbis.Open(vfile)
            # print metadata.pprint()
            try:
                #title = metadata["title"][0]
                title = "test3"
            except KeyError:
                title = "test3"

            try:
                description = metadata["description"][0]
            except KeyError:
                description = ""

        else:
            title = "test3"
            description = ""
    else:
        print vfile + " is not an ogg or mpg"
        return

    # Default category to education for now
    category = "Education"
    #This is a hack, needs to be fixed
    command = "/home/alex/git/freeseer/src/lib/youtube_upload/youtube_upload.py -m" + email + " -p" + \
        password + " -t" + title + " -c" + category + " " + vfile
    os.system(command)

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
