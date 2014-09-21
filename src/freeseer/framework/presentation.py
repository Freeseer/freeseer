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

from os import path

from PyQt4.QtCore import QDate
from PyQt4.QtCore import QDateTime


# TODO: Add a print presentation method? print self.__dict__
# TODO: Write a database record to Presentation method
class Presentation(object):
    '''
    This class is responsible for encapsulate data about presentations
    and its database related operations
    '''

    # TODO: Are Default variable necessary if they are all empty-string values?
    DEFAULT_ROOM = ''
    DEFAULT_DATE = ''
    DEFAULT_TIME = ''

    # TODO: Confirm Presentation.date is or is not a QDate object.
    # TODO: Confirm Presentation.startTime should store a QDateTime object or a QTime object.
    # TODO: Confirm Presentation.endTime should store a QDateTime object or a QTime object.
    def __init__(self, title, speaker='', description='', category='', event='', room='',
                 date='', startTime='', endTime=''):
        '''
        Initialize a presentation instance
        '''
        self.title = title
        self.speaker = speaker
        self.description = description
        self.category = category
        self.event = event
        self.room = room
        self.date = date
        self.startTime = startTime
        self.endTime = endTime

        if not self.room:
            self.room = self.DEFAULT_ROOM

        # Set the date, startTime, or endTime if they are null timestamp values
        if self.date == QDate():
            self.date = self.DEFAULT_DATE
        if self.startTime == QDateTime():
            self.startTime = self.DEFAULT_TIME
        if self.endTime == QDateTime():
            self.endTime = self.DEFAULT_TIME

    def __eq__(self, obj):
        return self.__dict__ == obj.__dict__

    def __ne__(self, obj):
        return not self == obj


class PresentationFile(Presentation):

    '''
    This class represents a presentation that has been already been written
    to a file and the metadata that has been loaded from it
    '''

    def __init__(self, title, speaker="", description="", category="", event="Default", room="Default", date="", startTime="", endTime=""):
        Presentation.__init__(
            self, title, speaker, description, category, event, room, date, startTime, endTime)

        self.filename = ""
        self.album = ""
        self.tracknumber = None
        self.filedate = None
        self.duration = None
        self.filesize = None

    artist = property(lambda self: self.speaker,
                      lambda self, value: self.__setattr__('speaker', value))

    filebase = property(lambda self: path.basename(self.filename))
    filepath = property(lambda self: path.dirname(self.filename))
