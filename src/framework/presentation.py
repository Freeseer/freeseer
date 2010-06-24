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

from sqlite3 import *
from config import Config
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
	self.database = None

	configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
	self.config = Config(configdir)
	self.presentationsfile = os.path.abspath('%s/presentations.db' % self.config.configdir)

	self.initializeDB()

	
    def initializeDB(self):
    	'''
    	Create a connection with a database file,
    	if it doesnt exists, we create them
    	'''
	if os.path.isfile(self.presentationsfile):	
            self.database = connect(self.presentationsfile)
	else:	
            connection = connect(self.presentationsfile)
	    cursor = connection.cursor()
	    cursor.execute('''create table presentations
			    (Speaker varchar(100), Title varchar(255), Description text, Level varchar(25), Event varchar(100),
			    Time timestamp, Room varchar(25) )''')
	    cursor.close()
	    self.database = connection    
  
    def saveToDB(self):
	'''
	Write current presentation data on database
	'''
	cursor = self.database.cursor()
	try:
	    cursor.execute('''insert into presentations values (?,?,?,?,?,?,?)''',[self.speaker,self.title,self.description,self.level,
										self.event,self.time,self.room])	
	    self.database.commit()
	    cursor.close()
	except:
	    return
  
    #This method is only for depuration, it's not necessary
    def showBd(self):
	cursor = self.database.cursor()
	cursor.execute('''select * from presentations''')
	for row in cursor:
		print row


if __name__ == "__main__":
	myPresentation = Presentation("Felipe","Felipe's Presentation 2","That's my presentation")
	myPresentation.saveToDB()
	myPresentation.showBd()


