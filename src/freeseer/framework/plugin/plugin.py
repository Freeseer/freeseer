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

import abc
#import ConfigParser
import logging
#import os
#import sys
#import xml.etree.ElementTree as ET

#from PyQt4 import QtCore

log = logging.getLogger(__name__)


class Plugin(object):

    __metaclass__ = abc.ABCMeta

    # I know we want to ensure that they have NAME and CATEGORY attributes.
    # I was looking for how to ensure that and this is what I saw.
    # Is this how one would do it?
    @abc.abstractproperty
    def NAME(self):
        pass    # What should I do here?

    @NAME.setter
    def NAME(self, name):
        pass    # Echo


class AudioInput(Plugin):

    __metaclass__ = abc.ABCMeta
