#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011-2012  Free and Open Source Software Learning Centre
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

import logging
import os

from PyQt4 import QtSql

from freeseer.framework.presentation import *
from freeseer.framework.failure import *

class QtDBConnector():
    presentationsModel = None
    failuresModel = None
    def __init__(self, configdir, talkdb_file="presentations.db"):
        """
        Initialize the QtDBConnector
        """
        self.configdir = configdir
        self.talkdb_file = os.path.abspath("%s/%s" % (self.configdir, talkdb_file))
        
        if not os.path.isfile(self.talkdb_file):
            file = open(self.talkdb_file, 'w')
            file.write('')
            file.close()
        
        self.__open_table()
    
    def __open_table(self):
        """
        This function options a connection to the database. Used by the init function.
        """
        self.talkdb = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.talkdb.setDatabaseName(self.talkdb_file)
        
        if (self.talkdb.open()):
            
            # check if presentations table exists and if not create it.
            if not self.talkdb.tables().contains("presentations"):
                self.__create_presentations_table()
                self.__insert_default_talk()
            
            # check if failures table exists and if not create it.
            if not self.talkdb.tables().contains("failures"):
                self.__create_failures_table()
        else:
            print "Unable to create talkdb file."
            
    def __close_table(self):
        """
        This function is used to close the connection the the database.    
        """
        self.talkdb.close()
            
    def __create_presentations_table(self):
        """
        Creates the presentations table in the database. Should be used to
        initialize a new table.
        """
        query = QtSql.QSqlQuery('''CREATE TABLE IF NOT EXISTS presentations
                                       (Id INTEGER PRIMARY KEY,
                                        Title varchar(255),
                                        Speaker varchar(100),
                                        Description text,
                                        Level varchar(25),
                                        Event varchar(100),
                                        Room varchar(25),
                                        Time timestamp,
                                        UNIQUE (Speaker, Title) ON CONFLICT IGNORE)''')
        
    def __insert_default_talk(self):
        """
        Insert the default talk data into the database.
        """
        presentation = Presentation("Intro to Freeseer",
                                    "Thanh Ha",
                                    "",
                                    "",
                                    "SC2011",
                                    "T105",
                                    "")
        self.insert_presentation(presentation)
        
    def get_talks(self):
        """
        Gets all the talks from the database including all columns.
        """
        result = QtSql.QSqlQuery('''SELECT * FROM presentations''')
        return result
    
    def get_events(self):
        """
        Gets all the talk events from the database.
        """
        result = QtSql.QSqlQuery('''SELECT DISTINCT Event FROM presentations''')
        return result
    
    def get_talk_ids(self):
        """
        Gets all the talk events from the database.
        """
        result = QtSql.QSqlQuery('''SELECT Id FROM presentations''')
        return result
    
    def get_talks_by_event(self, event):
        """
        Gets the talks signed in a specific event from the database.
        """
        result = QtSql.QSqlQuery('''SELECT * FROM presentations WHERE Event=%s''' % event)
        return result
    
    def get_talks_by_room(self, room):
        """
        Gets the talks hosted in a specific room from the database.
        """
        result = QtSql.QSqlQuery('''SELECT * FROM presentations WHERE Room=%s''' % room)
        return result
    
    def get_presentation(self, talk_id):
        """
        Return a Presentation object associated to a talk_id.
        """
        result = QtSql.QSqlQuery('''SELECT * FROM presentations WHERE Id="%s"''' % talk_id)
        if result.next():
            p = Presentation(unicode(result.value(1).toString()),    # title
                             unicode(result.value(2).toString()),    # speaker
                             unicode(result.value(3).toString()),    # description
                             unicode(result.value(4).toString()),    # level
                             unicode(result.value(5).toString()),    # event
                             unicode(result.value(6).toString()),    # room
                             unicode(result.value(7).toString()))    # time
        else:
            p = None
            
        return p
    
    def presentation_exists(self, presentation):
        """
        Check if there's a presentation with the same Speaker and Title already stored
        """
        result = QtSql.QSqlQuery('''SELECT * FROM presentations''')
        while(result.next()):                    
            if(unicode(presentation.title) == unicode(result.value(1).toString()) and unicode(presentation.speaker) == unicode(result.value(2).toString())):
                return True            
        return False
        
    #
    # Presentation Create, Update, Delete
    #
    def insert_presentation(self, presentation):
        """
        Insert a Presentation into the database.
        """
        query = QtSql.QSqlQuery('''INSERT INTO presentations VALUES (NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' %
                                    (presentation.title,
                                     presentation.speaker,
                                     presentation.description,
                                     presentation.level,
                                     presentation.event,
                                     presentation.room,
                                     presentation.time))
        logging.info("Talk added: %s - %s" % (presentation.speaker, presentation.title))
        
    def update_presentation(self, talk_id, presentation):
        """
        Update an existing Presentation in the database.
        """
        query = QtSql.QSqlQuery('''UPDATE presentations SET Title="%s", Speaker="%s", Event="%s", Room="%s", Time="%s"  WHERE Id="%s"''' %
                            (presentation.title,
                             presentation.speaker,
                             presentation.event,
                             presentation.room,
                             presentation.time,
                             talk_id))
        logging.info("Talk %s updated: %s - %s" % (talk_id, presentation.speaker, presentation.title))
        
    def delete_presentation(self, talk_id):
        """
        Removes a Presentation from the database
        """
        query = QtSql.QSqlQuery('''DELETE FROM presentations WHERE Id="%s"''' % talk_id)
        logging.info("Talk %s deleted." % talk_id)
        
    def clear_database(self):
        """
        Clears the presentations table
        """
        query = QtSql.QSqlQuery('''DELETE FROM presentations''')
        logging.info("Database cleared.")
    
    #
    # Data Model Retrieval 
    #
    def get_presentations_model(self):
        """
        Gets the Presentation Table Model.
        Useful for Qt GUI based Frontends to load the Model in Table Views.
        """
        if self.presentationsModel is None:
            self.presentationsModel = QtSql.QSqlTableModel()
            self.presentationsModel.setTable("presentations")
            self.presentationsModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            self.presentationsModel.select()
        
        return self.presentationsModel

    def get_failures_model(self):
        """
        Gets the Failure reports table Model
        Useful for QT GUI based Frontends to load the Model in Table Views.
        """
        if self.failuresModel is None:
            self.failuresModel = QtSql.QSqlTableModel()
            self.failuresModel.setTable("failures")
            self.failuresModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            self.failuresModel.select()

        return self.failuresModel

    def get_events_model(self):
        """
        Gets the Events Model.
        Useful for Qt GUI based Frontends to load the Model into Views.
        """
        self.eventsModel = QtSql.QSqlQueryModel()
        self.eventsModel.setQuery("SELECT DISTINCT Event FROM presentations ORDER BY Event ASC")
            
        return self.eventsModel
    
    def get_dates_from_event_room_model(self, event, room):
        """
        Gets the Rooms Model.
        Useful for Qt GUI based Frontends to load the Model into Views.
        """
        self.datesModel = QtSql.QSqlQueryModel()
        self.datesModel.setQuery("SELECT DISTINCT date(Time) FROM presentations WHERE Event='%s' and Room='%s' ORDER BY Time ASC" % (event, room))
        
        return self.datesModel
    
    def get_rooms_model(self, event):
        """
        Gets the Rooms Model.
        Useful for Qt GUI based Frontends to load the Model into Views.
        """
        self.roomsModel = QtSql.QSqlQueryModel()
        self.roomsModel.setQuery("SELECT DISTINCT Room FROM presentations WHERE Event='%s' ORDER BY Room ASC" % event)
            
        return self.roomsModel
    
    def get_talks_model(self, event, room, date=None):
        """
        Gets the Talks Model. A talk is defined as "<presenter> - <talk_title>"
        Useful for Qt GUI based Frontends to load the Model into Views.
        """
        
        self.talksModel = QtSql.QSqlQueryModel()
        if date == "":
            self.talksModel.setQuery("SELECT (Speaker || ' - ' || Title), Id FROM presentations \
                                   WHERE Event='%s' and Room='%s' ORDER BY Time ASC" % (event, room))
        else:
            self.talksModel.setQuery("SELECT (Speaker || ' - ' || Title), Id FROM presentations \
                                   WHERE Event='%s' and Room='%s' and date(Time) LIKE '%s' ORDER BY Time ASC" % (event, room, date))
            
        return self.talksModel
    
    def get_talk_between_time(self, event, room, starttime, endtime):
        """
        Returns the talkID of the first talk found between a starttime, and endtime for a specified event/room.
        Else return None
        """
        query = QtSql.QSqlQuery("SELECT Id, Time FROM presentations \
                                 WHERE Event='%s' AND Room='%s' \
                                 AND Time BETWEEN '%s' \
                                              AND '%s' ORDER BY Time ASC" % (event, room, starttime, endtime))
        query.next()
        if query.isValid():
            return query.value(0)
        else:
            return None
        
        
    #
    # Reporting Feature
    #
    
    def __create_failures_table(self):
        """
        Create the failures table in the database 
        Should be used to initialize a new table.
        """
        query = QtSql.QSqlQuery('''CREATE TABLE IF NOT EXISTS failures
                                        (Id INTERGER PRIMARY KEY,
                                        Comments TEXT,
                                        Indicator TEXT,
                                        Release INTEGER,
                                        UNIQUE (ID) ON CONFLICT REPLACE)''')
    def clear_report_db(self):
        """
        Drops the failures (reports) table from the database
        """
        query = QtSql.QSqlQuery('''DROP TABLE IF EXISTS failures''')
        
    def get_report(self, talkid):
        """
        Return a failure from a given talkid
        
        Returned value is a Failure object
        """
        result = QtSql.QSqlQuery('''SELECT * FROM failures WHERE Id = "%s"''' % talkid)
        if result.next():
            failure = Failure(unicode(result.value(0).toString()),  # id
                              unicode(result.value(1).toString()),  # comment
                              unicode(result.value(2).toString()),  # indicator
                              result.value(3).toBool())             # release
        else:
            failure = None
        return failure
        
    def get_reports(self):
        """
        Return a list of failures in Report format.
        """
        result = QtSql.QSqlQuery('''Select * FROM failures''')
        #return result
        list = []
        while(result.next()):
            failure = Failure(unicode(result.value(0).toString()),    # id
                              unicode(result.value(1).toString()),    # comment
                              unicode(result.value(2).toString()),    # indicator
                              bool(result.value(3))),                 # release
            p = self.get_presentation(failure.talkId)
            r = Report(p, failure)
            list.append(r)
        return list
    
    def insert_failure(self, failure):
        """
        Insert a failure into the database.
        """
        
        query = QtSql.QSqlQuery('''INSERT INTO failures VALUES ("%d", "%s", "%s", %d)''' %
                           (int(failure.talkId), failure.comment, failure.indicator, failure.release))
        logging.info("Failure added: %s - %s" % (failure.talkId, failure.comment))
    
    def update_failure(self, talk_id, failure):
        """
        Update an existing Failure in the database.
        """
        
        query = QtSqlQuery('''UPDATE failures SET Comments="%s", Indicator="%s", Release="%d" WHERE Id="%s"''' %
                           (failure.comment,
                            failure.indicator,
                            failure.release,
                            failure.talkId))
        logging.info("Failure updated: %s %s" % (failure.talkId, failure.comment))
    
    def delete_failure(self, talk_id):
        """
        Removes a Presentation from the database
        """
        query = QtSql.QSqlQuery('''DELETE FROM failures WHERE Id="%s"''' % talk_id)
        logging.info("Failure %s deleted." % talk_id)
        
    def get_failures_model(self):
        """
        Gets the Failure reports table Model
        Useful for QT GUI based Frontends to load the Model in Table Views.
        """
        if self.failuresModel is None:
            self.failuresModel = QtSql.QSqlTableModel()
            self.failuresModel.setTable("failures")
            self.failuresModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            self.failuresModel.select()
        
        return self.failuresModel 
    
"""
Test code to independently test the methods in the QtDBConnector() class.    
"""    
if __name__ == "__main__":
    
    # Imports
    import sys
    import tempfile
    
    from PyQt4 import QtCore
    
    # Main
    app = QtCore.QCoreApplication(sys.argv)
    
    tmpdir = tempfile.gettempdir()
    print "Temp Directory: %s" % tmpdir # prints the current temporary directory
    
    testdbcon = QtDBConnector(os.path.abspath(tmpdir))
    
    print "Talks: "
    result = testdbcon.get_talks()
    
    while(result.next()):
        id = result.value(0).toString()
        presenter = result.value(1).toString()
        talk = result.value(2).toString()
        print "%s - %s - %s" % (id, presenter, talk)
        
    # Get the presentation table model
    testdbcon.get_presentations_model()
    testdbcon.get_presentations_model()
    
    # Get the events model
    testdbcon.get_events_model()
    testdbcon.get_events_model()
    
    # Get the rooms model
    testdbcon.get_rooms_model("SC2011")
    testdbcon.get_rooms_model("SC2011")
    
    # Get the talks model
    testdbcon.get_talks_model("SC2011", "T105")
    testdbcon.get_talks_model("SC2011", "T105")
