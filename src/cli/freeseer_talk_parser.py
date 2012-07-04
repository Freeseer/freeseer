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
# http://wiki.github.com/fosslc/freeseer/


import argparse

import sys,os
import re

from freeseer.framework.core import FreeseerCore
from freeseer.framework.presentation import Presentation


class FreeSeerTalkParser(argparse.ArgumentParser):
    def __init__(self, core):  
        argparse.ArgumentParser.__init__(self)
        
        self.core = core
        self.db_connector = self.core.db
        
      
        self.add_argument('mode',nargs = '+', metavar='talk mode')
        
        self.add_argument('--all', dest='remove_all', action='store_const',const=True, default=False)    
        self.add_argument('-e', dest='event',nargs = '+',type=str)
        self.add_argument('-p', dest='presentation',type=str)
        self.add_argument('-r', dest='room',nargs = '+',type=str)
        
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
        
        if(mode == "show events"):
            self.show_all_events()
            
        elif(mode == "show talks"):
            if(namespace.presentation == None and namespace.event == None and namespace.room == None):
                self.show_all_talks()
            elif(namespace.event):
                self.show_talk_by_event(self._get_mode(namespace.event))
            elif(namespace.room):
                self.show_talk_by_room(self._get_mode(namespace.room))
            
        elif(mode == "show talk"):
            #TODO Search how to get arguments with space
            if(namespace.presentation == None):
                print "*** Error: Please specify the talk id"
            else:
                self.show_talk_by_id(namespace.presentation)  
            
                                   
        elif(mode == "remove talk"):            
            if(namespace.presentation == None and namespace.remove_all == None):
                print "*** Error: Please specify the talk id or the -all argument"
            else:  
                if(namespace.presentation != None and namespace.remove_all):
                    print "*** Error: Please specify only one option"
                else:
                    print namespace.remove_all
                    if(namespace.presentation):
                        self.remove_talk(namespace.presentation)
                    elif namespace.remove_all:
                        self.remove_all_talks()   
                                             
        elif(mode == "add talk"):
            self.add_talk_by_prompt()


        elif(mode == "update"):
            self.update_talk_by_prompt(namespace.presentation)               
                
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
            print "Talk #" + str(count)
            print "Talk Id: " + unicode(query.value(0).toString())
            print "Talk Title: " + unicode(query.value(1).toString())
            print "Talk Speaker: " + unicode(query.value(2).toString())
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
            print "Talk #" + str(count)
            print "Talk Id: " + unicode(query.value(0).toString())
            print "Talk Title: " + unicode(query.value(1).toString())
            print "Talk Speaker: " + unicode(query.value(2).toString())
            print "#########################################################################"
            count+=1
                
    def show_talk_by_room(self, room):
        count = 1
        query = self.db_connector.get_talks_by_room(room)
        
        while query.next():
            print "Talk #" + str(count)
            print "Talk Id: " + unicode(query.value(0).toString())
            print "Talk Title: " + unicode(query.value(1).toString())
            print "Talk Speaker: " + unicode(query.value(2).toString())
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
        
        presentation.title = raw_input("Type the presentation title: ")
        
        while(not len(presentation.title) > 0):
            presentation.title = raw_input("Please, type the presentation title: ")            
        
        presentation.speaker = raw_input("Type the presentation speaker: ")
        
        while(not len(presentation.speaker) > 0):
            presentation.speaker = raw_input("Please, type the presentation speaker: ")
        
        presentation.description = raw_input("Type the presentation description or press <ENTER> to pass: ")
        presentation.level = raw_input("Type the speaker level or press <ENTER> to pass: ")
        presentation.event = raw_input("Type the event that held the presentation or press <ENTER> to pass: ")
        presentation.room = raw_input("Type the room where the presentation will be performed or press <ENTER> to pass: ")        
        data = raw_input("Type the presentation time (format: dd/MM/yyyy HH:mm) or press <ENTER> to pass: ")
        
        while(not self._is_date_format(data)):
            if(len(data) > 0):
                data = raw_input("Wrong date format, please type the presentation time (format: dd/MM/yyyy HH:mm) or press <ENTER> to pass: ")
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
                
            new_event = raw_input("Type the new event that held the presentation (<ENTER> to keep old data): ")
            event = new_event if len(new_event) > 0 else presentation.event
                
            new_room = raw_input("Type the new room where the presentation will be performed (<ENTER> to keep old data): ")  
            room = new_room if len(new_room) > 0 else presentation.room
            
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
            
        
    def _is_date_format(self, value):
        if(re.match("[0-3][0-9]/[0-1][0-9]/[0-9][0-9][0-9][0-9] [0-2][0-9]:[0-5][0-9]", value)):
            return True
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