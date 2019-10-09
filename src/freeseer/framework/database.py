#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2013  Free and Open Source Software Learning Centre
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

from PyQt4 import QtSql
from PyQt4.QtCore import QDate
from PyQt4.QtCore import QTime
from PyQt4.QtCore import QStringList

from freeseer import SCHEMA_VERSION
from freeseer.framework.presentation import Presentation
from freeseer.framework.failure import Failure, Report

log = logging.getLogger(__name__)


# Database Schema Versions
PRESENTATIONS_SCHEMA_300 = '''CREATE TABLE IF NOT EXISTS presentations
                                       (Id INTEGER PRIMARY KEY,
                                        Title varchar(255),
                                        Speaker varchar(100),
                                        Description text,
                                        Level varchar(25),
                                        Event varchar(100),
                                        Room varchar(25),
                                        Time timestamp,
                                        UNIQUE (Speaker, Title) ON CONFLICT IGNORE)'''

# The SQLITE timestamp field corresponds to the DateTime object. The Date column in the database can be created from
# a DateTime.date() call.
PRESENTATIONS_SCHEMA_310 = '''CREATE TABLE IF NOT EXISTS presentations
                                       (Id INTEGER PRIMARY KEY,
                                        Title varchar(255),
                                        Speaker varchar(100),
                                        Description text,
                                        Category varchar(25),
                                        Event varchar(100),
                                        Room varchar(25),
                                        Date timestamp,
                                        StartTime timestamp,
                                        EndTime timestamp,
                                        UNIQUE (Speaker, Title) ON CONFLICT IGNORE)'''

# TODO: Make PRESENTATIONS_SCHEMA_315 the default schema when the presentation table is created
# TODO: Make an upgrade method from PRESENTATIONS_SCHEMA_310 to PRESENTATIONS_SCHEMA_315
# TODO: Update the SCHEMA_VERSION to 315
# TODO: Integrate new database scheme with importers/exporter functions
# TODO: Force Presentation.Date to be a QDate
# TODO: Figure out what the types should be for Presentation.StartTime/EndTime e.g. QTime
# TODO: Enforce the default database values in the CSV/RSS importer
# TODO: Enforce the default database values in Presentation.__init__
# TODO: Enforce the default database values in db.insert_presentation()
# TODO: Check what format the csv and rss sample files are in. For instance, do the rss files use 'None' instead of ''
#       for missing fields?
# TODO: Update _helper_presentation_exists() and get_presentation_id() to use the new schema such that they no longer
#       check if the stored data values are NULL
PRESENTATIONS_SCHEMA_315 = '''CREATE TABLE IF NOT EXISTS presentations
                                       (Id INTEGER PRIMARY KEY,
                                        Title varchar(255) NOT NULL DEFAULT '',
                                        Speaker varchar(100) NOT NULL DEFAULT '',
                                        Description text NOT NULL DEFAULT '',
                                        Category varchar(25) NOT NULL DEFAULT '',
                                        Event varchar(100) NOT NULL DEFAULT '',
                                        Room varchar(25) NOT NULL DEFAULT '',
                                        Date timestamp NOT NULL DEFAULT '',
                                        StartTime timestamp NOT NULL DEFAULT '',
                                        EndTime timestamp NOT NULL DEFAULT '',
                                        UNIQUE (Speaker, Title, Event) ON CONFLICT IGNORE)'''

REPORTS_SCHEMA_300 = '''CREATE TABLE IF NOT EXISTS failures
                                        (Id INTERGER PRIMARY KEY,
                                        Comments TEXT,
                                        Indicator TEXT,
                                        Release INTEGER,
                                        UNIQUE (ID) ON CONFLICT REPLACE)'''

# TODO: Ensure that the CSV/RSS to presentation importers are done using the same conventions. For instance, convert a
#       room with value None to '' in both the csv and rss importer. Instead of the csv parser converting None to 'None'
#       and the rss importer doing something else etcetera.


class QtDBConnector(object):
    def __init__(self, db_filepath, plugman):
        """
        Initialize the QtDBConnector
        """
        self.talkdb_file = db_filepath
        self.plugman = plugman

        self.presentationsModel = None
        self.failuresModel = None
        self.recentconnModel = None
        self.__open_table()

    def __open_table(self):
        """Opens a connection to the database. Uses by the init function."""
        self.talkdb = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.talkdb.setDatabaseName(self.talkdb_file)

        if self.talkdb.open():

            # check if presentations table exists and if not create it.
            if not self.talkdb.tables().contains("presentations"):
                self.__create_presentations_table()
                self.__insert_default_talk()

                # If presentations table did not exist, it is safe to say that the reports table needs to be reset
                # or initialized.
                self.clear_report_db()
                self.__create_failures_table()

                # Set the database version (so the updater does not update)
                QtSql.QSqlQuery('PRAGMA user_version = %i' % SCHEMA_VERSION)

            # check if recentConnections table exists and if not create it.
            if not self.talkdb.tables().contains("recentconn"):
                self.__create_recentconn_table()

            # verify that correct version of database exists
            self.__update_version()
        else:
            log.error("Unable to create talkdb file.")

    def __close_table(self):
        """Closes the connection the the database."""
        self.talkdb.close()

    def __get_db_version_int(self):
        """Gets the database's current version. Default is 0 if unset (for 2x and older)"""
        query = QtSql.QSqlQuery('PRAGMA user_version')
        query.first()
        return query.value(0).toInt()[0]

    def __update_version(self):
        """Upgrade database to the latest SCHEMA_VERSION"""

        db_version = self.__get_db_version_int()
        if db_version == SCHEMA_VERSION:
            return

        #
        # Define functions for upgrading between schema versions
        #
        def update_2xto30():
            """Incremental update of database from Freeseer 2.x and older to 3.0

            SCHEMA_VERSION is 300
            """
            if db_version > 300:
                log.debug('Database newer than schema version 300.')
                return  # No update needed

            log.debug('Updating to schema 300.')
            QtSql.QSqlQuery('ALTER TABLE presentations RENAME TO presentations_old')  # temporary table
            self.__create_presentations_table(PRESENTATIONS_SCHEMA_300)
            QtSql.QSqlQuery("""INSERT INTO presentations
                            SELECT Id, Title, Speaker, Description, Level, Event, Room, Time FROM presentations_old""")
            QtSql.QSqlQuery('DROP TABLE presentations_old')

        def update_30to31():
            """Performs incremental update of database from 3.0 and older to 3.1."""
            QtSql.QSqlQuery('ALTER TABLE presentations RENAME TO presentations_old')
            self.__create_presentations_table(PRESENTATIONS_SCHEMA_310)
            QtSql.QSqlQuery("""INSERT INTO presentations
                            SELECT Id, Title, Speaker, Description, Level, Event, Room, Time, Time, Time
                            FROM presentations_old""")
            QtSql.QSqlQuery('DROP TABLE presentations_old')

        #
        # Perform the upgrade
        #
        updaters = [update_2xto30, update_30to31]
        for updater in updaters:
            updater()

        QtSql.QSqlQuery('PRAGMA user_version = %i' % SCHEMA_VERSION)
        log.info('Upgraded presentations database from version {} to {}'.format(db_version, SCHEMA_VERSION))

    def __create_presentations_table(self, schema=PRESENTATIONS_SCHEMA_310):
        """Creates the presentations table in the database. Should be used to initialize a new table."""
        log.info("table created")
        QtSql.QSqlQuery(schema)

    def __insert_default_talk(self):
        """Inserts the required placeholder talk into the database.At least one talk must exist"""
        self.insert_presentation(Presentation("", "", "", "", "", "", "", "", ""))

    def get_talks(self):
        """Gets all the talks from the database including all columns"""
        return QtSql.QSqlQuery('''SELECT * FROM presentations''')

    def get_events(self):
        """Gets all the talk events from the database"""
        return QtSql.QSqlQuery('''SELECT DISTINCT Event FROM presentations''')

    def get_talk_ids(self):
        """Gets all the talk events from the database"""
        return QtSql.QSqlQuery('''SELECT Id FROM presentations''')

    def get_talks_by_event(self, event):
        """Gets the talks signed in a specific event from the database"""
        return QtSql.QSqlQuery('''SELECT * FROM presentations WHERE Event=%s''' % event)

    def get_talks_by_room(self, room):
        """Gets the talks hosted in a specific room from the database"""
        return QtSql.QSqlQuery('''SELECT * FROM presentations WHERE Room=%s''' % room)

    def get_talks_by_room_and_time(self, room):
        """Returns the talks hosted in a specified room, starting from the current date and time"""
        current_date = QDate.currentDate().toString(1)  # yyyy-mm-dd
        current_time = QTime.currentTime().toString()  # hh:mm:ss
        return QtSql.QSqlQuery('''SELECT * FROM presentations
                                  WHERE Room='{}' AND Date='{}'
                                  AND StartTime >= '{}' ORDER BY StartTime ASC'''.format(room, current_date, current_time))

    def get_presentation(self, talk_id):
        """Returns a Presentation object associated to a talk_id"""
        result = QtSql.QSqlQuery('''SELECT * FROM presentations WHERE Id="%s"''' % talk_id)
        if next(result):
            return Presentation(title=str(result.value(1).toString()),
                             speaker=str(result.value(2).toString()),
                             description=str(result.value(3).toString()),
                             category=str(result.value(4).toString()),
                             event=str(result.value(5).toString()),
                             room=str(result.value(6).toString()),
                             date=str(result.value(7).toString()),
                             startTime=str(result.value(8).toString()),
                             endTime=str(result.value(9).toString()))
        else:
            return None

    def get_string_list(self, column):
        """Returns a column as a QStringList"""
        tempList = QStringList()
        result = QtSql.QSqlQuery('''SELECT DISTINCT %s FROM presentations''' % column)
        while next(result):
            tempList.append(result.value(0).toString())
        return tempList

    def presentation_exists(self, presentation):
        """Checks if there's a presentation with the same Speaker and Title already stored"""
        result = QtSql.QSqlQuery('''SELECT * FROM presentations''')
        while next(result):
            if (str(presentation.title) == str(result.value(1).toString())
            and str(presentation.speaker) == str(result.value(2).toString())):
                return True
        return False

    #
    # Presentation Create, Update, Delete
    #
    def insert_presentation(self, presentation):
        """Inserts a passed Presentation into the database."""
        # Duplicate time to date field for older RSS / CSV formats
        # If date is empty, and time has a full DateTime, split the DateTime to
        # both Date and Time

        if not presentation.date and presentation.startTime and len(presentation.startTime) == 16:
            presentation.date, presentation.startTime = presentation.startTime[:-6], presentation.startTime[11:]

        QtSql.QSqlQuery(
            '''INSERT INTO presentations VALUES (NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' %
            (presentation.title,
             presentation.speaker,
             presentation.description,
             presentation.category,
             presentation.event,
             presentation.room,
             presentation.date,
             presentation.startTime,
             presentation.endTime))
        log.info("Talk added: %s - %s, Time: %s - %s" % (presentation.speaker, presentation.title, presentation.startTime, presentation.endTime))

    def update_presentation(self, talk_id, presentation):
        """Updates an existing Presentation in the database."""
        QtSql.QSqlQuery(
            '''UPDATE presentations SET Title="%s", Speaker="%s", Description="%s", Category="%s",
                Event="%s", Room="%s", Date="%s", StartTime="%s", EndTime="%s"
                WHERE Id="%s"''' %
            (presentation.title,
             presentation.speaker,
             presentation.description,
             presentation.category,
             presentation.event,
             presentation.room,
             presentation.date,
             presentation.startTime,
             presentation.endTime,
             talk_id))
        log.info("Talk %s updated: %s - %s" % (talk_id, presentation.speaker, presentation.title))

    def delete_presentation(self, talk_id):
        """Removes a Presentation from the database"""
        QtSql.QSqlQuery('''DELETE FROM presentations WHERE Id="%s"''' % talk_id)
        log.info("Talk %s deleted." % talk_id)

    def clear_database(self):
        """Clears the presentations table"""
        QtSql.QSqlQuery('''DELETE FROM presentations''')
        log.info("Database cleared.")

    #
    # Data Model Retrieval
    #
    def get_presentations_model(self):
        """Gets the Presentation Table Model. Useful for Qt GUI based Frontends to load the Model in Table Views"""
        if self.presentationsModel is None:
            self.presentationsModel = QtSql.QSqlTableModel()
            self.presentationsModel.setTable("presentations")
            self.presentationsModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            self.presentationsModel.select()
        return self.presentationsModel

    def get_events_model(self):
        """Gets the Events Model. Useful for Qt GUI based Frontends to load the Model into Views"""
        self.eventsModel = QtSql.QSqlQueryModel()
        self.eventsModel.setQuery("SELECT DISTINCT Event FROM presentations ORDER BY Event ASC")
        return self.eventsModel

    def get_dates_from_event_room_model(self, event, room):
        """Gets the Dates Model. Useful for Qt GUI based Frontends to load the Model into Views."""
        self.datesModel = QtSql.QSqlQueryModel()
        self.datesModel.setQuery(
            "SELECT DISTINCT date FROM presentations WHERE Event='%s' and Room='%s' ORDER BY Date ASC"
            % (event, room))
        return self.datesModel

    def get_rooms_model(self, event):
        """Gets the Rooms Model. Useful for Qt GUI based Frontends to load the Model into Views"""
        self.roomsModel = QtSql.QSqlQueryModel()
        self.roomsModel.setQuery("SELECT DISTINCT Room FROM presentations WHERE Event='%s' ORDER BY Room ASC" % event)
        return self.roomsModel

    def get_talks_model(self, event, room, date=None):
        """Gets the Talks Model. A talk is defined as "<presenter> - <talk_title>"
        Useful for Qt GUI based Frontends to load the Model into Views"""
        self.talksModel = QtSql.QSqlQueryModel()
        if date == "":
            self.talksModel.setQuery("SELECT (Speaker || ' - ' || Title), Id FROM presentations \
                                   WHERE Event='%s' and Room='%s' ORDER BY Date ASC" % (event, room))
        else:
            self.talksModel.setQuery("SELECT (Speaker || ' - ' || Title), Id FROM presentations \
                                   WHERE Event='%s' and Room='%s' and date(Date) LIKE '%s' ORDER BY Date ASC"
                                   % (event, room, date))
        return self.talksModel

    def get_talk_between_time(self, event, room, startTime, endTime):
        """Returns the talkID of the first talk found between a startTime, and endTime for a specified event/room.
        Else return None"""
        query = QtSql.QSqlQuery("SELECT Id, Date FROM presentations \
                                 WHERE Event='%s' AND Room='%s' \
                                 AND Date BETWEEN '%s' \
                                              AND '%s' ORDER BY Date ASC" % (event, room, startTime, endTime))
        next(query)
        if query.isValid():
            return query.value(0)
        else:
            return None

    #
    # Import / Export Functions
    #
    # Needs to be updated for category field, separate date and time fields
    def add_talks_from_rss(self, feed_url):
        """Adds talks from an rss feed."""
        plugin = self.plugman.get_plugin_by_name("Rss FeedParser", "Importer")
        feedparser = plugin.plugin_object
        presentations = feedparser.get_presentations(feed_url)

        if presentations:
            for presentation in presentations:
                talk = Presentation(presentation["Title"],
                                    presentation["Speaker"],
                                    presentation["Abstract"],  # Description
                                    presentation["Level"],
                                    presentation["Event"],
                                    presentation["Room"],
                                    presentation["Time"],
                                    presentation["Time"])
                self.insert_presentation(talk)

        else:
            log.info("RSS: No data found.")

    def add_talks_from_csv(self, fname):
        """Adds talks from a csv file.

        Title and speaker must be present.
        """
        plugin = self.plugman.get_plugin_by_name("CSV Importer", "Importer")
        importer = plugin.plugin_object
        presentations = importer.get_presentations(fname)

        if presentations:
            for presentation in presentations:
                if presentation['Time']:
                    talk = Presentation(presentation["Title"],
                                        presentation["Speaker"],
                                        presentation["Abstract"],  # Description
                                        presentation["Level"],
                                        presentation["Event"],
                                        presentation["Room"],
                                        presentation["Time"],
                                        presentation["Time"])  # Presentation using legacy time field
                else:
                    talk = Presentation(presentation["Title"],
                                        presentation["Speaker"],
                                        presentation["Abstract"],  # Description
                                        presentation["Level"],
                                        presentation["Event"],
                                        presentation["Room"],
                                        presentation["Date"],
                                        presentation["StartTime"],
                                        presentation["EndTime"])
                self.insert_presentation(talk)

        else:
            log.info("CSV: No data found.")

    def export_talks_to_csv(self, fname):
        fieldNames = ('Title',
                      'Speaker',
                      'Abstract',
                      'Category',
                      'Event',
                      'Room',
                      'Date',
                      'StartTime',
                      'EndTime')

        try:
            file = open(fname, 'w')
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            headers = dict((n, n) for n in fieldNames)
            writer.writerow(headers)

            result = self.get_talks()
            while next(result):
                log.debug(str(result.value(1).toString()))
                writer.writerow({'Title': str(result.value(1).toString()),
                                 'Speaker': str(result.value(2).toString()),
                                 'Abstract': str(result.value(3).toString()),
                                 'Category': str(result.value(4).toString()),
                                 'Event': str(result.value(5).toString()),
                                 'Room': str(result.value(6).toString()),
                                 'Date': str(result.value(7).toString()),
                                 'StartTime': str(result.value(8).toString()),
                                 'EndTime': str(result.value(9).toString())})
        finally:
            file.close()

    def export_reports_to_csv(self, fname):
        fieldNames = ('Title',
                      'Speaker',
                      'Abstract',
                      'Category',
                      'Event',
                      'Room',
                      'Date',
                      'StartTime',
                      'EndTime',
                      'Problem',
                      'Error')
        try:
            file = open(fname, 'w')
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            headers = dict((n, n) for n in fieldNames)
            writer.writerow(headers)

            result = self.get_reports()
            for report in result:
                writer.writerow({'Title': report.presentation.title,
                                 'Speaker': report.presentation.speaker,
                                 'Abstract': report.presentation.description,
                                 'Category': report.presentation.category,
                                 'Event': report.presentation.event,
                                 'Room': report.presentation.room,
                                 'Date': report.presentation.date,
                                 'StartTime': report.presentation.startTime,
                                 'EndTime': report.presentation.endTime,
                                 'Problem': report.failure.indicator,
                                 'Error': report.failure.comment})
        finally:
            file.close()

    #
    # Reporting Feature
    #
    def __create_failures_table(self, schema=REPORTS_SCHEMA_300):
        """Creates the failures table in the database. Should be used to initialize a new table"""
        QtSql.QSqlQuery(schema)

    def clear_report_db(self):
        """Drops the failures (reports) table from the database"""
        QtSql.QSqlQuery('''DROP TABLE IF EXISTS failures''')

    def get_report(self, talkid):
        """Returns a failure from a given talkid. Returned value is a Failure object"""
        result = QtSql.QSqlQuery('''SELECT * FROM failures WHERE Id = "%s"''' % talkid)
        if next(result):
            failure = Failure(str(result.value(0).toString()),  # id
                              str(result.value(1).toString()),  # comment
                              str(result.value(2).toString()),  # indicator
                              result.value(3).toBool())             # release
        else:
            failure = None
        return failure

    def get_reports(self):
        """Returns a list of failures in Report format"""
        result = QtSql.QSqlQuery('''Select * FROM failures''')
        list = []
        while next(result):
            failure = Failure(str(result.value(0).toString()),    # id
                              str(result.value(1).toString()),    # comment
                              str(result.value(2).toString()),    # indicator
                              bool(result.value(3)))                  # release
            p = self.get_presentation(failure.talkId)
            r = Report(p, failure)
            list.append(r)
        return list

    def insert_failure(self, failure):
        """Inserts a failure into the database"""
        QtSql.QSqlQuery(
            '''INSERT INTO failures VALUES ("%d", "%s", "%s", %d)''' %
            (int(failure.talkId), failure.comment, failure.indicator, failure.release))
        log.info("Failure added: %s - %s" % (failure.talkId, failure.comment))

    def update_failure(self, talk_id, failure):
        """Updates an existing Failure in the database"""
        QtSql.QtSqlQuery('''UPDATE failures SET Comments="%s", Indicator="%s", Release="%d" WHERE Id="%s"''' %
            (failure.comment,
             failure.indicator,
             failure.release,
             failure.talkId))
        log.info("Failure updated: %s %s" % (failure.talkId, failure.comment))

    def delete_failure(self, talk_id):
        """Removes a Presentation from the database"""
        QtSql.QSqlQuery('''DELETE FROM failures WHERE Id="%s"''' % talk_id)
        log.info("Failure %s deleted." % talk_id)

    def get_failures_model(self):
        """Gets the Failure reports table Model. Useful for QT GUI based Frontends to load the Model in Table Views"""
        if self.failuresModel is None:
            self.failuresModel = QtSql.QSqlTableModel()
            self.failuresModel.setTable("failures")
            self.failuresModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            self.failuresModel.select()

        return self.failuresModel

    #
    # Controller Feature
    #
    def __create_recentconn_table(self):
        """Creates the recentconn table in the database. Should be used to initialize a new table"""
        QtSql.QSqlQuery('''CREATE TABLE IF NOT EXISTS recentconn
                                        (host varchar(255),
                                         port int,
                                         passphrase varchar(255),
                                         UNIQUE (host, port) ON CONFLICT REPLACE)''')

    def clear_recentconn_table(self):
        """Drops the recentconn (Controller) table from the database"""
        QtSql.QSqlQuery('''DROP TABLE IF EXISTS recentconn''')

    def insert_recentconn(self, chost, cport, cpass):
        """Insert a failure into the database"""
        QtSql.QSqlQuery('''INSERT INTO recentconn VALUES("%s", "%d", "%s")''' % (chost, cport, cpass))
        log.info("Recent connection added: %s:%d" % (chost, cport))

    def get_recentconn_model(self):
        """Gets the Recent Connections table Model
        Useful for QT GUI based Frontends to load the Model in Table Views"""
        self.recentconnModel = QtSql.QSqlTableModel()
        self.recentconnModel.setTable("recentconn")
        self.recentconnModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.recentconnModel.select()

        return self.recentconnModel
