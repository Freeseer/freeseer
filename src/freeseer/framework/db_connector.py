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

from sqlite3 import connect
from presentation import *
import os


class DB_Connector():
    '''
    Freeseer database connection.
    '''    
    def __init__(self, configdir):
        
        self._CREATE_QUERY = '''CREATE TABLE presentations
                                (Speaker varchar(100),
                                Title varchar(255) UNIQUE,
                                Description text,
                                Level varchar(25),
                                Event varchar(100),
                                Time timestamp,
                                Room varchar(25),
                                Id INTEGER PRIMARY KEY,
                                FileNameId INTEGER)'''
                                
        self._DEFAULT_TALK = '''INSERT INTO presentations VALUES
                                ("Thanh Ha",
                                 "Intro to Freeseer",
                                 "",
                                 "",
                                 "",
                                 "",
                                 "T105",
                                 NULL,
                                 0)'''

        self.configdir = configdir
        self.presentations_file = os.path.abspath("%s/presentations.db" % self.configdir)
        self.cursor = None
        
        if not os.path.isfile(self.presentations_file):
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
        self.db_connection.commit()
        self.cursor.close()
        
    def get_talk_titles(self):
        '''
        Returns the talk titles as listed in presentations.db
        '''
        talk_titles = []
        
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''SELECT Speaker, Title, Room, Event, Time, Id FROM presentations''')

        for row in self.cursor:
            speaker = row[0]
            title = row[1]
            room = row[2]
            event = row[3]
            time = row[4]
            talk_id = row[5]
            talk_titles.append([speaker, title, room, event, time, talk_id])
            
        self.cursor.close()
            
        return talk_titles
    
    def get_talk_events(self):
        talk_events = []
 
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''SELECT DISTINCT Event FROM presentations''')
        
        for row in self.cursor:
            talk_events.append(row[0])
            
        self.cursor.close()
        
        return talk_events
    
    def get_talk_rooms(self):
        talk_rooms = []
 
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''SELECT DISTINCT Room FROM presentations''')
        
        for row in self.cursor:
            talk_rooms.append(row[0])
        
        self.cursor.close()
        
        return talk_rooms
    
    def db_contains(self, presentation):
        '''
        Check if database already contains such presentation. Two presentations
        are considered the same if they have same title, same event and same speaker.
        '''
        self.cursor = self.db_connection.cursor()
        talk_titles = self.cursor.execute('''select distinct Title from presentations''')
        talk_events = self.cursor.execute('''select distinct Event from presentations''')
        talk_speakers = self.cursor.execute('''select distinct Speaker from presentations''')

        self.cursor.close()
        
        if (presentation.title in talk_titles and presentation.event in talk_events and presentation.speaker in talk_speakers):
            return True
        return False

    def filter_talks_by_event_room(self, event, room):
        talks_matched = []

        self.cursor = self.db_connection.cursor()
        if (event == "All"):
            if (room == "All"):
                self.cursor.execute('''SELECT Speaker, Title, Room FROM presentations ORDER BY Id ASC''')
            else:
                self.cursor.execute('''SELECT DISTINCT Speaker, Title, Room FROM presentations \
                                       WHERE Room=? ORDER BY Time''', [unicode(room)])
            
        else:
            if (room == "All"):
                self.cursor.execute('''SELECT DISTINCT Speaker, Title, Room FROM presentations \
                                       WHERE Event=? ORDER BY Time''', [unicode(event)])
            else:
                self.cursor.execute('''SELECT DISTINCT Speaker, Title, Room FROM presentations \
                                       WHERE Event=? and Room=? ORDER BY Time''', [unicode(event), unicode(room)])

        # Prepare list to be returned
        for row in self.cursor:
            speaker = row[0]
            title = row[1]
            room = row[2]

            if (room == 'None'):
                text = "%s - %s" % (speaker, title)	
            else:
                text = "%s - %s - %s" % (room, speaker, title)
                
            talks_matched.append(text)

        self.cursor.close()
        return talks_matched
    
    
    def filter_rooms_by_event(self,event):
        rooms_matched = []
        
        self.cursor = self.db_connection.cursor()
        if(event == "All"):
            self.cursor.execute('''SELECT DISTINCT Room FROM presentations ORDER BY Id ASC''')
        
        else:
            self.cursor.execute('''SELECT DISTINCT Room FROM presentations WHERE Event=?''', [unicode(event)])
            
        rooms_matched.append("All")
        
        for row in self.cursor:
            rooms_matched.append(row[0])
        
        self.cursor.close()
        
        return rooms_matched
        

    def get_presentation(self, talk_id):
        
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''SELECT Speaker, 
                            Title,
                            Description,
                            Level,
                            Event,
                            Time,
                            Room,
                            Id,
                            FileNameId
                            FROM presentations WHERE Id=?''',
                            [unicode(talk_id)])
        for row in self.cursor:
            speaker 	 = row[0]
            title 	 = row[1]
            description  = row[2]
            level 	 = row[3]
            event 	 = row[4]
            time	 = row[5]
            room	 = row[6]
            talk_id 	 = row[7]
            filename_id  = row[8]
    
            self.cursor.close()                
            return Presentation(title, speaker, description, level, event, time, room, talk_id, filename_id)	 
 
    def make_filename_id(self, event_name):
        
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''SELECT COUNT(*) FROM presentations WHERE Event=?''',
                                                            [unicode(event_name)])

        for row in self.cursor:
            id = row[0]
            self.cursor.close()
            return id
   
    def get_filename_id(self, talk_id):
        
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''SELECT FileNameId FROM presentations WHERE Id=?''',
                                        [unicode(talk_id)])
        for row in self.cursor:
            id = row[0]
            self.cursor.close()
            return id
 
    def add_talk(self, presentation):
        '''
        Write current presentation data on database
        '''		
        #create filename id (id's for each talk at an event)
        filename_id = unicode(self.make_filename_id(presentation.event))

        self.run_query('''INSERT INTO presentations VALUES (?,?,?,?,?,?,?,NULL,?)''',
                    [presentation.speaker,
                     presentation.title,
                     presentation.description,
                     presentation.level,
                     presentation.event,
                     presentation.time,
                     presentation.room,
                     filename_id])

    def delete_talk(self, talk_id):
        
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''DELETE FROM presentations WHERE Id=?''',
                               [unicode(talk_id)])
        self.db_connection.commit()
  
        self.cursor.close()
    
    def clear_database(self):
        
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''DELETE FROM presentations''')
        self.db_connection.commit()
        self.cursor.close()
        
    def update_talk(self, talk_id, new_speaker, new_title, new_room, new_event, new_time):
        
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''UPDATE presentations SET Speaker=?, Title=?, Room=?, Event=?, Time=?  WHERE Id=?''',
                            [unicode(new_speaker),
                             unicode(new_title),
                             unicode(new_room),
                             unicode(new_event),
                             unicode(new_time),
                             unicode(talk_id)])
        self.db_connection.commit()
        self.cursor.close()
        
    def get_presentation_id(self, presentation):
        
        self.cursor = self.db_connection.cursor()
        self.cursor.execute('''SELECT Id FROM presentations WHERE Speaker=? AND Title=? AND Event=?''',
                            [unicode(presentation.speaker),
                             unicode(presentation.title),
                             unicode(presentation.event)])
        
        for row in self.cursor:
            id = row[0]
            self.cursor.close()
            return id
