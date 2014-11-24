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


class Presentation(object):
    '''
    This class is responsible for encapsulate data about presentations
    and its database related operations
    '''
    def __init__(self, title, speaker="", description="", category="", event="Default", room="Default", date="", startTime="", endTime=""):
        '''
        Initialize a presentation instance
        '''
        self.title = title
        self.speaker = speaker
        self.description = description
        self.category = category
        self.event = event
        self.room = room
        self.date = date  # QDateTime.currentDateTime().toString(1) # eg date='2010-05-14T10:45'
        self.startTime = startTime  # QDateTime.currentDateTime().toString(1) # eg startTime='2010-05-14T10:45'
        self.endTime = endTime

    def __eq__(self, obj):
        if (
            self.title == obj.title and
            self.speaker == obj.speaker and
            self.description == obj.description and
            self.category == obj.category and
            self.event == obj.event and
            self.room == obj.room and
            self.date == obj.date and
            self.startTime == obj.startTime and
            self.endTime == obj.endTime
        ):
            return True
        else:
            return False

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
