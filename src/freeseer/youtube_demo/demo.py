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
from freeseer.frontend.cli import freeseer_talk_parser


from PyQt4 import QtGui, QtCore

def upload():
	#------- Trying to default to the video directory
	config = ConfigParser.ConfigParser()


	configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
	      
	# Config location
	configfile = os.path.abspath("%s/freeseer.conf" % configdir)


	config.readfp(open(configfile))\
	#---Trying to get metadata

	vid = FreeSeerTalkParser(argparse.ArgumentParser)

	#vid.show_all_talks()



	email = raw_input("Email address: ")
	#vfile = browse_video_directory()
	vfile = raw_input("File: ")

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

	    

	vpath = config.get('Global', 'video_directory')


	

	os.system("python freeseer/youtube_demo/uploader.py --email="+email+" --title="+title+" --category="+category+" --description="+description+" --keywords="+keywords+" " + vpath + "/" + vfile)








# Basically a copy of freeseer_talk_parser.py with some added functions
class FreeSeerTalkParser(argparse.ArgumentParser):
    
    def __init__(self, core):
	configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        argparse.ArgumentParser.__init__(self)
        
        self.core = core
	#self.db_connector = self.core.db
        self.db_connector = QtDBConnector(configdir)
        
      
        self.add_argument('mode',nargs = '+', metavar='talk mode')
        
    def analyse_command(self, command):  
        '''
        Analyses the command typed by the user
        '''        
        try:
            namespace = self.parse_args(command.split())
        except:
            print "*** Syntax Error"
            return
        
        mode = self._get_mode(namespace.mode) 
        talk_mode = mode.split(" ")[0]
        
        if(talk_mode == "show"):  
            try:
                show_mode = mode.split(" ")[1]
            except:
                print "*** Please provide the show mode. To see all available modes type'talk help show'"
                return            
            if (show_mode == "events"):
                self.show_all_events()         
            elif(show_mode == "event"):
                self.show_talk_by_event(mode.split(" ")[2])
            elif(show_mode == "room" ):
                self.show_talk_by_room(mode.split(" ")[2])
            elif(show_mode == "id"):
                self.show_talk_by_id(mode.split(" ")[2]) 
            elif(show_mode == "all"):
                self.show_all_talks()
            else:
                print "*** Unavailable show mode, to see all available modes type'talk help show'"
            
                                   
        elif(talk_mode == "remove"):
            try:
                self.remove_talk(int(mode.split(" ")[1]))
            except ValueError:
                if (mode.split(" ")[1] == "all"):
                    self.remove_all_talks() 
                else:
                    print "*** Invalid Syntax"       
                                   
        elif(talk_mode == "add"):
            self.add_talk_by_prompt()

        elif(talk_mode == "update"):
            try:
                self.update_talk_by_prompt(int(mode.split(" ")[1]))    
            except:
                print "*** Invalid Syntax"          
                
        else:
            print "*** Unknown mode, please type one of the available modes or type 'help talk' to see all available modes"
            
            
    def show_all_events(self):
        print "---------------------------------- Events -----------------------------------"
        query = self.db_connector.get_events()
        count = 1
        while query.next():
            print "Event %d: %s" % (count,unicode(query.value(0).toString()))
            count += 1
        print "-----------------------------------------------------------------------------"
        
    def show_all_talks(self):
        print "---------------------------------- Talks ------------------------------------"
        count = 1
        query = self.db_connector.get_talks()
        
        while query.next():
            print "Talk Id: " + unicode(query.value(0).toString())
            print "Talk Title: " + unicode(query.value(1).toString())
            print "Talk Speaker: " + unicode(query.value(2).toString())
            print "Talk Event: " + unicode(query.value(5).toString())
            print "Talk Room: " + unicode(query.value(6).toString())
            print "#########################################################################"
            count+=1
        print "-----------------------------------------------------------------------------\n"


    #-----------Added this method to find a corresponding talk based on the file name -------------------
    def get_talk_by_file(self, filename):
	query = self.db_connector.get_talks()
	count = 1
	
	
	while query.next():
	    talk_id =  unicode(query.value(0).toString())
            title = unicode(query.value(1).toString())
            speaker = unicode(query.value(2).toString())
            event = unicode(query.value(5).toString())
            room = unicode(query.value(6).toString())

	    if title[:6].upper() in filename and speaker[:6].upper() in filename and event[:6].upper() in filename and room[:6].upper() in filename:
	    	return talk_id
	   
	    count+=1

	return -1 

    #-------Some getters----------------
    def get_title_by_id(self, id):
        presentation = self.db_connector.get_presentation(id)   
        if(presentation):
            return presentation.title
        else:
             print "--------------------------- Talk Not Found ----------------------------------"

    def get_speaker_by_id(self, id):
        presentation = self.db_connector.get_presentation(id)   
        if(presentation):
            return presentation.speaker
        else:
             print "--------------------------- Talk Not Found ----------------------------------"

    def get_room_by_id(self, id):
        presentation = self.db_connector.get_presentation(id)   
        if(presentation):
            return presentation.room
        else:
             print "--------------------------- Talk Not Found ----------------------------------"

    def get_event_by_id(self, id):
        presentation = self.db_connector.get_presentation(id)   
        if(presentation):
            return presentation.event
        else:
             print "--------------------------- Talk Not Found ----------------------------------"




        
    def show_talk_by_id(self, id):
        presentation = self.db_connector.get_presentation(id)   
        if(presentation):
            print "----------------------------- Talk Found ------------------------------------"
            print "Talk Title: " + presentation.title
            print "Talk Speaker: " + presentation.speaker
            print "Talk Room: " + presentation.room
            print "Talk Event: " + presentation.event
            print "-----------------------------------------------------------------------------\n"
        else:
             print "--------------------------- Talk Not Found ----------------------------------"

                
    def show_talk_by_event(self, event):
        count = 1
        query = self.db_connector.get_talks_by_event(event)
        while query.next():
            print "Talk Id: " + unicode(query.value(0).toString())
            print "Talk Title: " + unicode(query.value(1).toString())
            print "Talk Speaker: " + unicode(query.value(2).toString())
            print "Talk Event: " + unicode(query.value(5).toString())
            print "Talk Room: " + unicode(query.value(6).toString())
            print "#########################################################################"
            count+=1
                
    def show_talk_by_room(self, room):
        count = 1
        query = self.db_connector.get_talks_by_room(room)
        
        while query.next():
            print "Talk Id: " + unicode(query.value(0).toString())
            print "Talk Title: " + unicode(query.value(1).toString())
            print "Talk Speaker: " + unicode(query.value(2).toString())
            print "Talk Event: " + unicode(query.value(5).toString())
            print "Talk Room: " + unicode(query.value(6).toString())
            print "#########################################################################"
            count+=1      
                
    def remove_talk(self, id):
        presentation = self.db_connector.get_presentation(id)
        if presentation:
            self.show_talk_by_id(id)
            answer = raw_input("This will remove this presentation.Continue? (yes/no) ")
            
            while answer != "yes" and answer != "no":
                answer = raw_input("Please provide an available answer.Do you want to remove this presentation? (yes/no) ")
            else:
                if answer == "yes":
                    self.db_connector.delete_presentation(id)
                    print "Talk removed"
        else:
            print "There's no such presentation"
            
    def remove_all_talks(self):
        answer = raw_input("WARNING: This will remove ALL presentations.Continue? (yes/no) ")
        
        while answer != "yes" and answer != "no":
            answer = raw_input("Please provide an available answer. Do you want to remove ALL presentations? (yes/no) ")
        
        if answer == "yes":
                self.db_connector.clear_database()
           
    def add_talk_by_prompt(self):
        print "------------------------------ Adding a Talk -------------------------------\n"
        presentation = Presentation("")
        
        presentation.title = raw_input("Type the presentation title: ").strip()
        
        while(not len(presentation.title) > 0):
            presentation.title = raw_input("Please, type the presentation title: ").strip() 
        
        presentation.speaker = raw_input("Type the presentation speaker: ").strip()
        
        while(not len(presentation.speaker) > 0):
            presentation.speaker = raw_input("Please, type the presentation speaker: ").strip()
        
        presentation.description = raw_input("Type the presentation description or press <ENTER> to pass: ").strip()
        presentation.level = raw_input("Type the speaker level or press <ENTER> to pass: ").strip()
        presentation.event = raw_input("Type the event that held the presentation or press <ENTER> to pass: ").strip()
        presentation.room = raw_input("Type the room where the presentation will be performed or press <ENTER> to pass: ").strip()     
        presentation.time = raw_input("Type the presentation time (format: dd/MM/yyyy HH:mm) or press <ENTER> to pass: ").strip()
        
        while(not self._is_date_format(presentation.time)):
            if(len(presentation.time) > 0):
                presentation.time = raw_input("Wrong date format, please type the presentation time (format: dd/MM/yyyy HH:mm) or press <ENTER> to pass: ")
            else:
                break
             
        if not self.db_connector.presentation_exists(presentation):
            self.db_connector.insert_presentation(presentation)
            print "###################### Talk Added ############################"
        else:
            print "############### Error: Talk Already Exists ###################"

    def update_talk_by_prompt(self, id): 
        presentation = self.db_connector.get_presentation(id)
        if presentation:                  
            print "#### You have choosen to edit the following talk ###"
            
            self.show_talk_by_id(id)     
                                
            new_title = raw_input("Type the new presentation title (<ENTER> to keep old data): ")
            title = new_title if len(new_title) > 0 else presentation.title
                
            new_speaker = raw_input("Type the new presentation speaker (<ENTER> to keep old data): ")
            speaker = new_speaker if len(new_speaker) > 0 else presentation.speaker
                
            new_room = raw_input("Type the new room where the presentation will be performed (<ENTER> to keep old data): ")  
            room = new_room if len(new_room) > 0 else presentation.room
            
            new_event = raw_input("Type the new event that held the presentation (<ENTER> to keep old data): ")
            event = new_event if len(new_event) > 0 else presentation.event
                
            
            
            new_presentation = Presentation("")
            
            new_presentation.talk_id = id
            new_presentation.title = title
            new_presentation.speaker = speaker
            new_presentation.event = event
            new_presentation.room = room
            
            self.db_connector.update_presentation(id, new_presentation)
            
            print "### Talk Updated! ###"
            
        else:
            print "There's no such presentation"
            
        
    def _is_date_format(self, date):
        try:
            valid_date = time.strptime(date, '%d/%m/%Y %H:%M')
            return True
        except ValueError:
             return False

    
    def _get_mode(self, mode_list):
        mode = ""
        for item in mode_list:
            mode += item + " "
        return mode[0:len(mode)-1]
    
    def _get_number_of_args(self, namespace):
        count = 0
        if(namespace.event):
            count+=1
        if(namespace.presentation):
            count+=1
        if(namespace.room):
            count+=1
        
        return count


#----------------------------------

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



