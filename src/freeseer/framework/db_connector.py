#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2010  Free and Open Source Software Learning Centre
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

import os
import presentation

from logger import Logger
from config import Config
from sqlite3 import connect



class DB_Connector():
    '''
    Freeseer database connection. Used to link database code with
    Freeseer GUI
    '''    
    def __init__(self,gui):
        
        self._CREATE_QUERY = '''create table presentations
                    (Speaker varchar(100), Title varchar(255) UNIQUE, Description text, Level varchar(25), Event varchar(100),
                    Time timestamp, Room varchar(25), Id INTEGER PRIMARY KEY)'''
        self._DEFAULT_TALK = '''insert into presentations values ("Thanh Ha","Intro to Freeseer","","","","","T105",NULL)'''
                    
        configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        self.config = Config(configdir)
        self.presentations_file = self.config.presentations_file
        self.cursor = None
        self.logger = Logger(configdir)
        self.ui = gui
        
        if not os.path.isfile(self.config.presentations_file):
            self.db_connection = connect(self.presentations_file)            
            self.create_table() 
            self.cursor = self.db_connection.cursor() 
            return
        
        self.db_connection = connect(self.presentations_file)
        self.cursor = self.db_connection.cursor()

        
    def run_query(self,querie,args=None):
        self.cursor = self.db_connection.cursor()
        try:
            self.cursor.execute(querie,args)
        except:
            return            
        self.db_connection.commit()
        return self.cursor
       
    def create_table(self):
        self.cursor = self.db_connection.cursor()
        self.cursor.execute(self._CREATE_QUERY)
        self.cursor.execute(self._DEFAULT_TALK)        
        self.end_query()
        self.db_connection.commit()
        
    def aux(self):
        self.cursor.execute('''select * from presentations''')

    def end_query(self):
        self.cursor.close()
        
    def get_talk_titles(self):
        '''
        Returns the talk titles as listed in presentations.db
        '''
        talk_titles = []
 
        self.cursor.execute('''select * from presentations''')

        for row in self.cursor:
            talk_titles.append([row[0],row[1],row[6],row[7]])            

        #self.logger.log.debug('Available talk titles:')
        
        #for talk in talk_titles:
            #self.logger.log.debug('  ' + talk.encode('utf-8'))
            
        self.end_query()
            
        return talk_titles
    
    def get_talk_events(self):
        talk_events = []
 
        self.cursor.execute('''select distinct Event from presentations''')
        
        for row in self.cursor:
            talk_events.append(row[0])
            
        self.end_query()
        
        return talk_events
    
    def get_talk_rooms(self):
        talk_rooms = []
 
        self.cursor.execute('''select distinct Room from presentations''')
        
        for row in self.cursor:
            talk_rooms.append(row[0])
        
        return talk_rooms
    
    def db_contains(self,presentation):
        '''
        Check if database already contains such presentation
        Two presentations are considered the same if they have same title, same event and same speaker
        '''
        talk_titles = self.cursor.execute('''select distinct Title from presentations''')
        talk_events = self.cursor.execute('''select distinct Event from presentations''')
        talk_speakers = self.cursor.execute('''select distinct Speaker from presentations''')
        
        if (presentation.title in talk_titles and presentation.event in talk_events and presentation.speaker in talk_speakers):
            return True
        return False
    
    def filter_by_room(self,roomName):
        talks_matched = []
        
        self.ui.talkList.clear()
        if roomName != "All":            
            if(self.ui.eventList.currentText()!="All"):
                self.cursor.execute('''select distinct Speaker,Title,Room from presentations \
                                        where Event=? and Room=? ''', [str(self.ui.eventList.currentText()),str(roomName)])
            else:
                self.cursor.execute('''select distinct Speaker,Title,Room from presentations \
                                        where Room=? ''', [str(roomName)])           
            for row in self.cursor:
                text = "%s - %s - %s" % (row[0],row[1],row[2])
                talks_matched.append(text)
            for entry in talks_matched:
                self.ui.talkList.addItem(entry)
        else:
            if(self.ui.eventList.currentText()=="All"):
                return False
            else:
                self.cursor.execute('''select distinct Speaker,Title,Room from presentations \
                                        where Event=? ''', [str(self.ui.eventList.currentText())])
                for row in self.cursor:
                    text = "%s - %s - %s" % (row[0],row[1],row[2])
                    talks_matched.append(text)
                for entry in talks_matched:
                    self.ui.talkList.addItem(entry)
    
        return True
    
    def filter_by_event(self,eventName):
        talks_matched = []

        self.ui.talkList.clear()
        if eventName != "All":       
            if(self.ui.roomList.currentText()!="All"):
                self.cursor.execute('''select distinct Speaker,Title,Room from presentations \
                                        where Event=? and Room=? ''', [str(eventName),str(self.ui.roomList.currentText())])
            else:
                self.cursor.execute('''select distinct Speaker,Title,Room from presentations \
                                        where Event=? ''', [str(eventName)])  
            for row in self.cursor:
                text = "%s - %s - %s" % (row[0],row[1],row[2])
                talks_matched.append(text)
            for entry in talks_matched:
                self.ui.talkList.addItem(entry)
        else:
            if(self.ui.roomList.currentText()=="All"):
                return False
            else:
                self.cursor.execute('''select distinct Speaker,Title,Room from presentations \
                                        where Room=? ''', [str(self.ui.roomList.currentText())])
                for row in self.cursor:
                    text = "%s - %s - %s" % (row[0],row[1],row[2])
                    talks_matched.append(text)
                for entry in talks_matched:
                    self.ui.talkList.addItem(entry)
        return True
    
    def delete_talk(self,id):
        self.cursor.execute('''delete from presentations 
                                    where Id=?''',
                                        [str(id)])
        self.cursor.execute('''select * from presentations''')        
        self.db_connection.commit()
  
        self.cursor.close()
    
    def clear_database(self):
        self.cursor.execute('''delete from presentations''')
        self.db_connection.commit()
        self.cursor.close()


        
        
            
    
    
    
    
    
    
    
    
    
    
    
    
    