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


import codecs
import datetime
import time
import logging
import logging.config
import os

from freeseer.backend.gstreamer import *

from configtool_configloader import Config
from freeseer.framework.logger import Logger
from freeseer.framework.presentation import *

class ConfigCore:
    '''
    Freeseer core logic code.  Used to link a GUI frontend with a recording
    backend such as backend.gstreamer
    '''
    def __init__(self, ui):
        self.ui = ui
        
        # Read in config information
        configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        self.config = Config(configdir)
        self.logger = Logger(configdir)

        # Start Freeseer Recording Backend
        self.backend = Freeseer_gstreamer(self)       
        self.logger.log.info(u"Config Core initialized")   
	
   
    ##
    ## Backend Functions
    ##
    def get_video_sources(self):
        '''
        Returns supported video sources.
        '''
        vidsrcs = self.backend.get_video_sources()
        self.logger.log.debug('Available video sources: ' + str(vidsrcs))
        return vidsrcs
        
    def get_video_devices(self, device_type):
        '''
        Returns available video devices.
        '''
        viddevs = self.backend.get_video_devices(device_type)
        self.logger.log.debug('Available video devices for ' + device_type + ': ' + str(viddevs))
        return viddevs
    

    def get_audio_sources(self):
        '''
        Returns supported audio sources.
        '''
        sndsrcs = self.backend.get_audio_sources()
        self.logger.log.debug('Available audio sources: ' + str(sndsrcs))
        return sndsrcs     
        
    def preview(self, enable=False, window_id=None):
        '''
        Enable/Disable the video preview window.
        '''
        if enable == True:
            self.backend.enable_video_feedback(window_id)
            self.logger.log.info('Video Preview Activated')
        else:
            self.backend.disable_video_feedback()
            self.logger.log.info('Video Preview Deactivated')
