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
# http://wiki.github.com/Freeseer/freeseer/

from PyQt4 import QtCore, QtGui

class Failure():    
    '''
    This class is responsible for encapsulate data about failures
    and its database related operations
    '''

    def __init__(self, talkID, comment, indicator):
        
        '''
        Initialize a failure report instance
        '''
        self.talkId = talkID
        self.comment = comment
        self.indicator = indicator

class Report():
    def __init__(self, presentation, failure):    
        '''
        Initialize a report instance
        '''
        self.presentation = presentation
        self.failure = failure