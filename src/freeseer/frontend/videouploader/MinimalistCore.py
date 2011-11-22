'''
Created on Nov 6, 2011

@author: jord
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
        logging.info(u"Mock Core initialized")   