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

from config import Config
from db_connector import DB_Connector
import os


class Presentation():	
    '''
    This class is responsible for encapsulate data about presentations
    and its database related operations
    '''

    def __init__(self,title,speaker="",description="",level="",event="",time="",room=""):
        
        '''
        Initialize a presentation instance
        '''
        self.speaker = speaker
        self.title = title
        self.description = description
        self.level = level
        self.event = event
        self.time = time
        self.room = room
    
        self.db_connection = DB_Connector(None)
  
    def save_to_db(self):
        '''
	    Write current presentation data on database
	    '''      
        self.db_connection.run_query('''insert into presentations values (?,?,?,?,?,?,?,NULL)''',[self.speaker,self.title,self.description,self.level,
                                            self.event,self.time,self.room])            



