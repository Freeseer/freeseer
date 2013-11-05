#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011-2013  Free and Open Source Software Learning Centre
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

import csv
import logging
import os

from PyQt4 import QtSql
from PyQt4.QtCore import QDate

from freeseer import __version__
from freeseer.framework.presentation import Presentation
from freeseer.framework.failure import Failure, Report
from freeseer.framework.rss_parser import FeedParser

log = logging.getLogger(__name__)

class QtDBConnector():
    presentationsModel = None
    failuresModel = None
    recentconnModel = None
    
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
                
            # check if recentConnections table exists and if not create it.
            if not self.talkdb.tables().contains("recentconn"):
                self.__create_recentconn_table()
                
            #verify that correct version of database exists
            self.__update_version()
        else:
            log.error("Unable to create talkdb file.")
            
    def __close_table(self):
        """
        This function is used to close the connection the the database.    
        """
        self.talkdb.close()

    def get_program_version_int(self):
        """
        Get Freeseer's current version as an integer.
        """
        result = []
        for c in __version__:
            if c.isdigit():
                result.append(c)
        return int(''.join(result))
    
    def __get_db_version_int(self):
        """
        Get the database's current version. Default is 0 if unset (for 2x and older)
        """
        query = QtSql.QSqlQuery('PRAGMA user_version')
        query.first()
        return query.value(0).toInt()[0]

    def __update_version(self):
        """
        Upgrade database to the latest version.
        updaterVersion[i] version number of the incremental update function located at updaters[i]
        updaters[] functions are then called in order starting at the old version to the end.
        Version # of 2.x and older is 0
        """
        
        db_version = self.__get_db_version_int()
        program_version = self.get_program_version_int()
        if program_version == db_version:
            return
        
        def update_2xto30():
            """
            Incremental update of database from 2.x and older to 3.0.
            """
            QtSql.QSqlQuery('ALTER TABLE presentations RENAME TO presentations_old') #temporary table
            self.__create_presentations_table()
            QtSql.QSqlQuery("""INSERT INTO presentations 
                            SELECT Id, Title, Speaker, Description, Category, Event, Room, Time from presentations_old""")
            QtSql.QSqlQuery('DROP TABLE presentations_old')
        
        def update_30to31():
            """
            Incremental update of database from 3.0 and older to 3.1.

            """
            QtSql.QSqlQuery('ALTER TABLE presentations RENAME TO presentations_old') #temporary table
            self.__create_presentations_table()
            QtSql.QSqlQuery("""INSERT INTO presentations 
                            SELECT Id, Title, Speaker, Description, Category, Event, Room, Time from presentations_old""")
            QtSql.QSqlQuery('ALTER TABLE presentations RENAME COLUMN Category to Category')
            QtSql.QSqlQuery('ALTER TABLE presentations RENAME COLUMN Time to Date')
            QtSql.QSqlQuery('ALTER TABLE presentations ADD COLUMN Time timestamp')
            QtSql.QSqlQuery('UPDATE table SET Date = Time')
            QtSql.QSqlQuery('DROP TABLE presentations_old')


        updaters = [update_30to31]
        updaterVersion = [0] #next entry is 300
        if len(updaters) != len(updaterVersion) or db_version not in updaterVersion: #not setup properly
            log.info('Database upgrade failed.')
            return
        for updater in updaters[updaterVersion.index(db_version):]:
            updater()
        QtSql.QSqlQuery('PRAGMA user_version = %i' % program_version)
        log.info('Upgraded presentations database from version %i', db_version)
    
    def __create_presentations_table(self):
        """
        Creates the presentations table in the database. Should be used to
        initialize a new table.
        """
        print "table created"
        query = QtSql.QSqlQuery('''CREATE TABLE IF NOT EXISTS presentations
                                       (Id INTEGER PRIMARY KEY,
                                        Title varchar(255),
                                        Speaker varchar(100),
                                        Description text,
                                        Category varchar(25),
                                        Event varchar(100),
                                        Room varchar(25),
                                        Date timestamp,
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
                                    "",
                                    ""
                                    )
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
                             unicode(result.value(4).toString()),    # category
                             unicode(result.value(5).toString()),    # event
                             unicode(result.value(6).toString()),    # room
                             unicode(result.value(7).toString()),    # date
                             unicode(result.value(8).toString()))    # time
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
        #Handle old field names
        #Level to Category
        if hasattr(presentation, 'level'):
            print "has level" 
            print presentation.level
            if (presentation.level == '' and presentation.category != ''):
                presentation.level = presentation.category

        #Duplicate time to date field for older RSS / CSV formats
        if (presentation.date == '' and presentation.time != ''):
            presentation.date = presentation.time
            presentation.date = presentation.date[:-6]
            presentation.time = presentation.time[11:]


        query = QtSql.QSqlQuery('''INSERT INTO presentations VALUES (NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' %
                                    (presentation.title,
                                     presentation.speaker,
                                     presentation.description,
                                     presentation.category,
                                     presentation.event,
                                     presentation.room,
                                     presentation.date,
                                     presentation.time))
        log.info("Talk added: %s - %s" % (presentation.speaker, presentation.title))
        
    def update_presentation(self, talk_id, presentation):
        """
        Update an existing Presentation in the database.
        """
        query = QtSql.QSqlQuery('''UPDATE presentations SET Title="%s", Speaker="%s", Event="%s", Room="%s", Date="%s", Time="%s"  WHERE Id="%s"''' %
                            (presentation.title,
                             presentation.speaker,
                             presentation.event,
                             presentation.room,
                             presentation.date,
                             presentation.time,
                             talk_id))
        log.info("Talk %s updated: %s - %s" % (talk_id, presentation.speaker, presentation.title))
        
    def delete_presentation(self, talk_id):
        """
        Removes a Presentation from the database
        """
        query = QtSql.QSqlQuery('''DELETE FROM presentations WHERE Id="%s"''' % talk_id)
        log.info("Talk %s deleted." % talk_id)
        
    def clear_database(self):
        """
        Clears the presentations table
        """
        query = QtSql.QSqlQuery('''DELETE FROM presentations''')
        log.info("Database cleared.")
    
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
        self.datesModel.setQuery("SELECT DISTINCT date(Time) FROM presentations WHERE Event='%s' and Room='%s' ORDER BY Date ASC" % (event, room))
        
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
                                   WHERE Event='%s' and Room='%s' ORDER BY Date ASC" % (event, room))
        else:
            self.talksModel.setQuery("SELECT (Speaker || ' - ' || Title), Id FROM presentations \
                                   WHERE Event='%s' and Room='%s' and date(Date) LIKE '%s' ORDER BY Date ASC" % (event, room, date))
            
        return self.talksModel
    
    def get_talk_between_time(self, event, room, starttime, endtime):
        """
        Returns the talkID of the first talk found between a starttime, and endtime for a specified event/room.
        Else return None
        """
        query = QtSql.QSqlQuery("SELECT Id, Date FROM presentations \
                                 WHERE Event='%s' AND Room='%s' \
                                 AND Date BETWEEN '%s' \
                                              AND '%s' ORDER BY Date ASC" % (event, room, starttime, endtime))
        query.next()
        if query.isValid():
            return query.value(0)
        else:
            return None
        
        
    ##
    ## Import / Export Functions
    ##
    # Needs to be updated for category field, separate date and time fields
    def add_talks_from_rss(self, rss):
        """Adds talks from an rss feed."""
        entry = str(rss)
        feedparser = FeedParser(entry)

        if len(feedparser.build_data_dictionary()) == 0:
            log.info("RSS: No data found.")

        else:
            for presentation in feedparser.build_data_dictionary():
                talk = Presentation(presentation["Title"],
                                    presentation["Speaker"],
                                    presentation["Abstract"],  # Description
                                    presentation["Category"],
                                    presentation["Level"],  
                                    presentation["Event"],
                                    presentation["Room"],
                                    presentation["Date"],
                                    presentation["Time"])
                self.insert_presentation(talk)
    
    def add_talks_from_csv(self, fname):
        """Adds talks from a csv file.
        
        Title and speaker must be present.
        """
        file = open(fname,'r')
        try:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    title = row['Title']
                    speaker = row['Speaker']
                except KeyError:
                    log.error("Missing Key in Row: %s", row)
                    return
                    
                try:
                    abstract = row['Abstract'] # Description
                except KeyError:
                    abstract = ''
                
                try:
                    category = row['Category']
                except KeyError:
                    category = ''

                try:
                    level = row['Level']
                except KeyError:
                    level = ''

                if (category == '' and level != ''): #Check for old csv namings
                    category = level
                
                try:
                    event = row['Event']
                except KeyError:
                    event = ''
                
                try:
                    room = row['Room']
                except KeyError:
                    room = ''
                
                try:
                    date = row['Date']
                except KeyError:
                    date = ''
                
                try:
                    time = row['Time']
                except KeyError:
                    time = ''

                talk = Presentation(title,
                                    speaker,
                                    abstract,
                                    category,
                                    event,
                                    room,
                                    date,
                                    time)
                self.insert_presentation(talk)
            
        except IOError:
            log.error("CSV: File %s not found", file)
        
        finally:
            file.close()
    
    # Needs to be updated to accept csv files with updated fields (category, time, date)         
    def export_talks_to_csv(self, fname):
        #fname = '/home/parallels/Documents/git/freeseer/src/test/export.csv'

        fieldNames = ('Title',
                      'Speaker',
                      'Abstract',
                      'Category',
                      'Event',
                      'Room',
                      'Date',
                      'Time')
        
        try:
            file = open(fname, 'w')
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            headers = dict( (n,n) for n in fieldNames )
            writer.writerow(headers)
            
            result = self.get_talks()
            while result.next():
                log.debug(unicode(result.value(1).toString()))
                writer.writerow({'Title':unicode(result.value(1).toString()),
                                 'Speaker':unicode(result.value(2).toString()),
                                 'Abstract':unicode(result.value(3).toString()),
                                 'Category':unicode(result.value(4).toString()),
                                 'Event':unicode(result.value(5).toString()),
                                 'Room':unicode(result.value(6).toString()),
                                 'Date':unicode(result.value(7).toString()),
                                 'Time':unicode(result.value(8).toString())})   
        finally:
            file.close()
    
    # Needs to be updated to accept csv files with updated fields (category, time, date)
    def export_reports_to_csv(self, fname):
        fieldNames = ('Title',
                      'Speaker',
                      'Abstract',
                      'Category',
                      'Event',
                      'Room',
                      'Date',
                      'Time',
                      'Problem',
                      'Error')
        try:
            file = open(fname, 'w')
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            headers = dict( (n,n) for n in fieldNames)
            writer.writerow(headers)
            
            result = self.get_reports()
            for report in result:
                writer.writerow({'Title':report.presentation.title,
                                 'Speaker':report.presentation.speaker,
                                 'Abstract':report.presentation.description,
                                 'Category':report.presentation.category,
                                 'Event':report.presentation.event,
                                 'Room':report.presentation.room,
                                 'Date':report.presentation.date,
                                 'Time':report.presentation.time,
                                 'Problem':report.failure.indicator,
                                 'Error':report.failure.comment})
        finally:
            file.close()
            
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
                              bool(result.value(3)))                  # release
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
        log.info("Failure added: %s - %s" % (failure.talkId, failure.comment))
    
    def update_failure(self, talk_id, failure):
        """
        Update an existing Failure in the database.
        """
        
        query = QtSqlQuery('''UPDATE failures SET Comments="%s", Indicator="%s", Release="%d" WHERE Id="%s"''' %
                           (failure.comment,
                            failure.indicator,
                            failure.release,
                            failure.talkId))
        log.info("Failure updated: %s %s" % (failure.talkId, failure.comment))
    
    def delete_failure(self, talk_id):
        """
        Removes a Presentation from the database
        """
        query = QtSql.QSqlQuery('''DELETE FROM failures WHERE Id="%s"''' % talk_id)
        log.info("Failure %s deleted." % talk_id)
        
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
        
    ##
    ## Controller Feature
    ##
    
    def __create_recentconn_table(self):
        """
        Create the recentconn table in the database 
        Should be used to initialize a new table.
        """
        query = QtSql.QSqlQuery('''CREATE TABLE IF NOT EXISTS recentconn
                                        (host varchar(255),
                                         port int,
                                         passphrase varchar(255),
                                         UNIQUE (host, port) ON CONFLICT REPLACE)''')
                                     
    def clear_recentconn_table(self):
        """
        Drops the recentconn (Controller) table from the database
        """
        query = QtSql.QSqlQuery('''DROP TABLE IF EXISTS recentconn''')
        
    def insert_recentconn(self, chost, cport, cpass):
        """
        Insert a failure into the database.
        """
        
        query = QtSql.QSqlQuery('''INSERT INTO recentconn VALUES("%s", "%d", "%s")''' %
                                   (chost, cport, cpass))
        log.info("Recent connection added: %s:%d" % (chost, cport))
        
    def get_recentconn_model(self):
        """
        Gets the Recent Connections table Model
        Useful for QT GUI based Frontends to load the Model in Table Views.
        """
        self.recentconnModel = QtSql.QSqlTableModel()
        self.recentconnModel.setTable("recentconn")
        self.recentconnModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.recentconnModel.select()
        
        return self.recentconnModel
