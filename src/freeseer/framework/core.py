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
# http://wiki.github.com/fosslc/freeseer/


import codecs
import datetime
import time
import logging
import logging.config
import unicodedata

from freeseer import project_info
import gstreamer

from config import Config
from logger import Logger
from QtDBConnector import *
from rss_parser import *
from presentation import *
from plugin import PluginManager

__version__= project_info.VERSION

class FreeseerCore:
    '''
    Freeseer core logic code.  Used to link a GUI frontend with a recording
    backend such as backend.gstreamer
    '''
    def __init__(self, window_id=None):
        
        # Read in config information
        configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        self.config = Config(configdir)
        self.logger = Logger(configdir)
        self.db = QtDBConnector(configdir)
        self.plugman = PluginManager(configdir)

        # Start Freeseer Recording Backend
        self.backend = gstreamer.Gstreamer(window_id)

        self.feedback = False
        self.spaces = False
      
        logging.info(u"Core initialized")   

    def get_config(self):
        return self.config

    def get_plugin_manager(self):
        return self.plugman

    def duplicate_exists(self, recordname):
        '''
        Checks to see if a record name already exists in the directory.
        '''
        filename = self.config.videodir + '/' + recordname
        try:
            result = open(filename, 'r')
        except IOError:
            return False
        return True


    def get_record_name(self, presentation, extension):
        '''
        Returns the filename to use when recording.
        '''
        recordname = self.make_record_name(presentation)
                
        count = 0
        tempname = recordname
        
        # check if this record name already exists in this directory and add "-NN" ending if so.
        while(self.duplicate_exists("%s.%s" % (tempname, extension))):
            tempname = recordname + "-" + self.make_id_from_string(count, "0123456789")
            count+=1

        recordname = "%s.%s" % (tempname, extension)
                     
        logging.debug('Set record name to ' + recordname)        
        
        return recordname


    def make_record_name(self, presentation):
        '''
        Create an 'EVENT-ROOM-SPEAKER-TITLE' record name
        If any information is missing, we blank it out intelligently
        And if we have nothing for some reason, we use "default"
        '''	
        event = self.make_shortname(presentation.event)
        title = self.make_shortname(presentation.title)
        room = self.make_shortname(presentation.room)
        speaker = self.make_shortname(presentation.speaker)

        recordname=""
            
        if(event!=""):
            if(recordname!=""):
                recordname=recordname+"-"+event
            else:
                recordname=event
        
        if(room!=""):
            if(recordname!=""):
                recordname=recordname+"-"+room
            else:
                recordname=room
        
        if(speaker!=""):
            if(recordname!=""):
                recordname=recordname+"-"+speaker
            else:
                recordname=speaker
                
        if(title!=""):
            if(recordname!=""):
                recordname=recordname+"-"+title
            else:
                recordname=title
           
        # Convert unicode filenames to their equivalent ascii so that
        # we don't run into issues with gstreamer or filesystems
        recordname=unicodedata.normalize('NFKD', recordname).encode('ascii','ignore')
                
        if(recordname!=""):
            return recordname
                    
        return "default"

    def make_id_from_string(self, position, string='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        '''
        Returns an "NN" id given an integer and a string of valid characters for the id
        ('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' are the valid characters for UNIQUE in a record name)
        '''
        index1 = position % string.__len__()
        index0 = int( position / string.__len__() )

        if(index0 >= string.__len__() ):
            logging.debug('WARNING: Unable to generate unique filename.')
            # Return a unique 2 character string which will not overwrite previous files.
            # There is a possibility of infinite looping on testing duplicates once
            # all possible UNIQUE's and NN's are exhausted if all the files are kept 
            # in the same directory.
            # (36 * 36 * 100 filenames before this occurs, assuming EVENT is unique inside the directory.)
            return "##" 

        return string[index0]+string[index1]


    def make_shortname(self, providedString):
        '''
        Returns the first 6 characters of a string.
        Strip out non alpha-numeric characters, spaces, and most punctuation
        '''
                
        bad_chars = set("!@#$%^&*()+=|:;{}[]',? <>~`/\\")
        providedString="".join(ch for ch in providedString if ch not in bad_chars)
        return providedString[0:6].upper()

    ##
    ## Database Functions
    ##
    
    def add_talks_from_rss(self, rss):
        entry = str(rss)
        feedparser = FeedParser(entry)

        if len(feedparser.build_data_dictionary()) == 0:
            logging.info("RSS: No data found.")

        else:
            for presentation in feedparser.build_data_dictionary():
                talk = Presentation(presentation["Title"],
                                    presentation["Speaker"],
                                    presentation["Abstract"],  # Description
                                    presentation["Level"],
                                    presentation["Event"],
                                    presentation["Room"],
                                    presentation["Time"])
                self.db.insert_presentation(talk)

    ##
    ## Backend Functions
    ##

    def set_recording_area(self, x1, y1, x2, y2):
        # gstreamer backend needs to have the lower x/y coordinates
        # sent first.
        if (x2 < x1):
            if (y2 < y1):
                self.backend.set_recording_area(x2, y2, x1, y1)
            else:
                self.backend.set_recording_area(x2, y1, x1, y2)
        else:
            if (y2 < y1):
                self.backend.set_recording_area(x1, y2, x2, y1)
            else:
                self.backend.set_recording_area(x1, y1, x2, y2)

    def prepare_metadata(self, presentation):
        '''
        Returns a dictionary of tags and tag values to be used
        to populate the current recording's file metadata.
        '''
        return { "title" : presentation.title,
                 "artist" : presentation.speaker,
                 "performer" : presentation.speaker,
                 "album" : presentation.event,
                 "location" : presentation.room,
                 "date" : str(datetime.date.today()),
                 "comment" : presentation.description}


    def record(self, presentation):
        '''
        Informs backend to begin recording presentation.
        '''

        logging.debug("Loading Output plugins...")
        plugins = []
        for plugin in self.plugman.plugmanc.getPluginsOfCategory("Output"):
            if plugin.is_activated:
                logging.debug("Loading Output: %s" % plugin.plugin_object.get_name())
                
                extension = plugin.plugin_object.get_extension()

                #create a filename to record to
                record_name = self.get_record_name(presentation, extension)
        
                #prepare metadata
                metadata = self.prepare_metadata(presentation)
                #self.backend.populate_metadata(data)
        
                record_location = os.path.abspath(self.config.videodir + '/' + record_name)                
                plugin.plugin_object.set_recording_location(record_location)
                
                plugin.plugin_object.load_config(self.plugman)
                plugins.append(plugin.plugin_object)

        self.backend.load_output_plugins(plugins, metadata)
        
        if self.config.enable_audio_recoding:
            logging.debug("Loading Audio recording plugins...")
            audiomixer = self.plugman.plugmanc.getPluginByName(self.config.audiomixer, "AudioMixer").plugin_object
            if audiomixer is not None:
                audioinputs = self.plugman.plugmanc.getPluginsOfCategory("AudioInput")
                audiomixer.load_config(self.plugman)
                self.backend.load_audiomixer(audiomixer, audioinputs)
        
        if self.config.enable_video_recoding:
            logging.debug("Loading Video recording plugins...")
            videomixer = self.plugman.plugmanc.getPluginByName(self.config.videomixer, "VideoMixer").plugin_object
            if videomixer is not None:
                videoinputs = self.plugman.plugmanc.getPluginsOfCategory("VideoInput")
                videomixer.load_config(self.plugman)
                self.backend.load_videomixer(videomixer, videoinputs)
        
        self.backend.record()

    def stop(self):
        '''
        Informs backend to stop recording.
        '''
        self.backend.stop()
