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

import ConfigParser
import os
import logging

log = logging.getLogger(__name__)

class Config:
    '''
    This class is responsible for reading/writing settings to/from a config file.
    '''

    def __init__(self, configdir):
        '''
        Initialize settings from a configfile
        '''
        # Get the user's home directory
        self.userhome = os.path.expanduser('~')
        
        # Config location
        self.configdir = configdir
        self.configfile = os.path.abspath("%s/freeseer.conf" % self.configdir)
        self.presentations_file = os.path.abspath('%s/presentations.db' % self.configdir)
        
        #
        # Set default settings
        #
        
        # Global
        self.videodir = os.path.abspath('%s/Videos/' % self.userhome)
        self.auto_hide = False
        self.resolution = '0x0' # no scaling for video
        self.enable_video_recording = True
        self.enable_audio_recording = True
        self.videomixer = 'Video Passthrough'
        self.audiomixer = 'Audio Passthrough'
        self.record_to_file = True
        self.record_to_file_plugin = 'Ogg Output'
        self.record_to_stream = False
        self.record_to_stream_plugin = 'RTMP Streaming'
        self.audio_feedback = False
        self.video_preview = True
        self.default_language = "tr_en_US.qm" # Set default language to English if user did not define

        # Lastrun
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        
        self.delay_recording = 0

        # Map of resolution names to the actual resolution (both stream and record)
        # Names should include all options available in the GUI

        self.resmap = { '240p':'320x240', 
                        '360p':'480x360', 
                        '480p':'640x480', 
                        '720p':'1280x720', 
                        '1080p':'1920x1080' }

        # Read in the config file
        self.readConfig()
        
        # Make the recording directory
        try:
            os.makedirs(self.videodir)
        except OSError:
            log.info(u'Video directory exists.')
            
    def readConfig(self):
        '''
        Read in settings from config file if exists.
        If the config file does not exist create one and set some defaults.
        '''
        config = ConfigParser.ConfigParser()
        
        try:
            config.readfp(open(self.configfile))
        # Config file does not exist, create a default
        except IOError:
            self.writeConfig()
            return
                
        # Config file exists, read in the settings
        try:
            # Global Section
            self.videodir = config.get('Global', 'video_directory')
            self.resolution = config.get('Global', 'resolution')
            self.auto_hide = config.getboolean('Global', 'auto_hide')
            self.enable_video_recording = config.getboolean('Global','enable_video_recording')
            self.enable_audio_recording = config.getboolean('Global','enable_audio_recording')
            self.videomixer = config.get('Global', 'videomixer')
            self.audiomixer = config.get('Global', 'audiomixer')
            self.record_to_file = config.getboolean('Global', 'record_to_file')
            self.record_to_file_plugin = config.get('Global', 'record_to_file_plugin')
            self.record_to_stream = config.getboolean('Global', 'record_to_stream')
            self.record_to_stream_plugin = config.get('Global', 'record_to_stream_plugin')
            self.default_language = config.get('Global', 'Default Language')
            
            # LastRun Section
            self.start_x = config.get('lastrun', 'area_start_x')
            self.start_y = config.get('lastrun', 'area_start_y')
            self.end_x = config.get('lastrun', 'area_end_x')
            self.end_y = config.get('lastrun', 'area_end_y')
            self.delay_recording = config.get('lastrun', 'delay_recording')

        except:
            print('Corrupt config found, creating a new one.')
            self.writeConfig()
        
    def writeConfig(self):
        '''
        Write settings to a config file.
        '''
        config = ConfigParser.ConfigParser()
        
        # Set config settings
        config.add_section('Global')
        config.set('Global', 'video_directory', self.videodir)
        config.set('Global', 'resolution', self.resolution)
        config.set('Global', 'auto_hide', self.auto_hide)
        config.set('Global','enable_video_recording',self.enable_video_recording)
        config.set('Global','enable_audio_recording',self.enable_audio_recording)
        config.set('Global','videomixer',self.videomixer)
        config.set('Global','audiomixer',self.audiomixer)
        config.set('Global','record_to_file', self.record_to_file)
        config.set('Global','record_to_file_plugin', self.record_to_file_plugin)
        config.set('Global','record_to_stream', self.record_to_stream)
        config.set('Global','record_to_stream_plugin', self.record_to_stream_plugin)
        config.set('Global', 'Default Language', self.default_language)
        
        config.add_section('lastrun')
        config.set('lastrun', 'area_start_x', self.start_x)
        config.set('lastrun', 'area_start_y', self.start_y)
        config.set('lastrun', 'area_end_x', self.end_x)
        config.set('lastrun', 'area_end_y', self.end_y)
        config.set('lastrun', 'delay_recording', self.delay_recording)
        # Make sure the config directory exists before writing to the configfile 
        try:
            os.makedirs(self.configdir)
        except OSError:
            pass # directory exists.
        
        # Save default settings to new config file
        with open(self.configfile, 'w') as configfile:
            config.write(configfile)
