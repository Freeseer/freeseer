#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

Copyright (C) 2011  Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/Freeseer/freeseer/

@author: Jordan Klassen
'''
import logging
import os

#from PyQt4 import QtGui, QtCore
#from freeseer.framework.core import FreeseerCore
from freeseer.framework.config import Config
from freeseer.framework.logger import Logger
from freeseer.framework.plugin import PluginManager

# mainly for testing, to reduce startup time. I'm only using config and logger.
class MinimalistCore(object):
    def __init__(self, window=None, audio_feedback=None):
        # Read in config information
        configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        self.config = Config(configdir)
        self.logger = Logger(configdir)
        self.plugman = PluginManager(configdir)
        logging.info("Mock Core initialized")   
