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

import ConfigParser
import os

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
        
        # Set default settings
        self.videodir = os.path.abspath('%s/Videos/' % self.userhome)
        self.talksfile = os.path.abspath('%s/talks.txt' % self.configdir)
        self.resolution = '800x600'
        
        # Read in the config file
        self.readConfig()
        
        # Make the recording directory
        try:
            os.makedirs(self.videodir)
        except OSError:
            print('Video directory exists.')
            
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
            self.videodir = config.get('Global', 'video_directory')
            self.talksfile = config.get('Global', 'talks_file')
            self.resolution = config.get('Global', 'resolution')
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
        config.set('Global', 'talks_file', self.talksfile)
        config.set('Global', 'resolution', self.resolution)
        
        # Make sure the config directory exists before writing to the configfile 
        try:
            os.makedirs(self.configdir)
        except OSError:
            print('freeseer directory exists.')
        
        # Save default settings to new config file
        with open(self.configfile, 'w') as configfile:
            config.write(configfile)
            
# Config class test code
if __name__ == "__main__":
    config = Config(os.path.abspath(os.path.expanduser('~/.freeseer/')))
    print('\nTesting freeseer config file')
    print('Video Directory at %s' % config.videodir)
    print('Talks file at %s' % config.talksfile)
    print('Test complete!')
