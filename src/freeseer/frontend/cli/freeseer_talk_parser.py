#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/


import argparse

import sys,os
import re
import time

from freeseer.framework.core import FreeseerCore
from freeseer.framework.presentation import Presentation


class FreeseerTalkParser(argparse.ArgumentParser):
    def __init__(self, core):  
        argparse.ArgumentParser.__init__(self)
        
        self.core = core
        self.db_connector = self.core.db
        
      
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
