#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011-2012  Free and Open Source Software Learning Centre
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

import datetime
import logging
import os
import unicodedata
import csv

from freeseer import project_info
import gstreamer

from config import Config
from logger import Logger
from QtDBConnector import QtDBConnector
from rss_parser import FeedParser
from presentation import Presentation
from plugin import PluginManager

__version__= project_info.VERSION

class FreeseerCore:
    """Freeseer's core logic code.
    
    Used to link a GUI frontend with a recording backend, such as
    backend.gstreamer.
    """
    def __init__(self, window_id=None, audio_feedback=None):
        
        # Read in config information
        configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        self.config = Config(configdir)
        self.logger = Logger(configdir)
        self.db = QtDBConnector(configdir)
        self.plugman = PluginManager(configdir)

        # Start Freeseer Recording Backend
        self.backend = gstreamer.Gstreamer(window_id, audio_feedback)
        
        logging.info("Core initialized")   

    def get_config(self):
        return self.config

    def get_plugin_manager(self):
        return self.plugman

    def duplicate_exists(self, recordname):
        """Checks to see if a record name already exists in the directory."""
        filename = self.config.videodir + '/' + recordname
        try:
            result = open(filename, 'r')
        except IOError:
            return False
        return True


    def get_record_name(self, presentation, extension):
        """Returns the filename to use when recording.
        
        If a record name with a .None extension is returned, the record name
        will just be ignored by the output plugin (e.g. Video Preview plugin).
        """
        
        if presentation:
            recordname = self.make_record_name(presentation)
                    
            count = 0
            tempname = recordname
            
            # Add "-NN" to the end of a duplicate record name to make it unique.
            while(self.duplicate_exists("%s.%s" % (tempname, extension))):
                tempname = "{0}-{1}".format(recordname, self.make_id_from_string(count, "0123456789"))
                count+=1

        recordname = "%s.%s" % (tempname, extension)
                     
        if extension is not None:
            logging.debug('Set record name to %s', recordname)        
        
        return recordname


    def make_record_name(self, presentation):
        """Create an 'EVENT-ROOM-SPEAKER-TITLE' record name.

        If any information is missing, we blank it out intelligently
        And if we have nothing for some reason, we use "default"
        """	
        event = self.make_shortname(presentation.event)
        title = self.make_shortname(presentation.title)
        room = self.make_shortname(presentation.room)
        speaker = self.make_shortname(presentation.speaker)

        recordname = ""  # TODO: add substrings to a list then ''.join(list) -- better practice
            
        if event != "": # TODO: empty strings are falsy, use 'if not string:'
            if recordname != "":
                recordname = recordname + "-" + event
            else:
                recordname = event
        
        if room != "":
            if recordname != "":
                recordname = recordname + "-" + room
            else:
                recordname = room
        
        if speaker != "":
            if recordname != "":
                recordname = recordname + "-" + speaker
            else:
                recordname = speaker
                
        if title != "":
            if recordname != "":
                recordname = recordname + "-" + title
            else:
                recordname = title
           
        # Convert unicode filenames to their equivalent ascii so that
        # we don't run into issues with gstreamer or filesystems.
        recordname = unicodedata.normalize('NFKD', recordname).encode('ascii','ignore')
                
        if recordname != "":
            return recordname
                    
        return "default"

    def make_id_from_string(self, position, string='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        """Returns a 2-character id from a string of valid characters.
        
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' are the valid characters for
        UNIQUE in a record name.
        """
        index1 = position % string.__len__()
        index0 = int( position / string.__len__() )

        if index0 >= string.__len__():
            logging.debug('WARNING: Unable to generate unique filename.')
            # Return a unique 2 character string which will not overwrite previous files.
            # There is a possibility of infinite looping on testing duplicates once
            # all possible UNIQUE's and NN's are exhausted if all the files are kept 
            # in the same directory.
            # (36 * 36 * 100 filenames before this occurs, assuming EVENT is unique inside the directory.)
            return "##" 

        return string[index0] + string[index1]


    def make_shortname(self, string):
        """Returns the first 6 characters of a string in uppercase.

        Strip out non alpha-numeric characters, spaces, and most punctuation.
        """
                
        bad_chars = set("!@#$%^&*()+=|:;{}[]',? <>~`/\\")
        string = "".join(ch for ch in string if ch not in bad_chars)
        return string[0:6].upper()

    ##
    ## Database Functions
    ##
    def add_talks_from_rss(self, rss):
        """Adds talks from an rss feed."""
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
    
    def add_talks_from_csv(self, fname):
        """Adds talks from a csv file.
        
        Title and speaker must be present.
        """
        file = open(fname,'r')
        try:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    title = row['Title']
                    speaker = row['Speaker']
                except KeyError:
                    logging.error("Missing Key in Row: %s", row)
                    return
                    
                try:
                    abstract = row['Abstract'] # Description
                except KeyError:
                    abstract = ''
                
                try:
                    level = row['Level']
                except KeyError:
                    level = ''
                
                try:
                    event = row['Event']
                except KeyError:
                    event = ''
                
                try:
                    room = row['Room']
                except KeyError:
                    room = ''
                
                try:
                    time = row['Time']
                except KeyError:
                    time = ''
                
                talk = Presentation(title,
                                    speaker,
                                    abstract,
                                    level,
                                    event,
                                    room,
                                    time)
                self.db.insert_presentation(talk)
            
        except IOError:
            logging.error("CSV: File %s not found", file)
        
        finally:
            file.close()
                 
    def export_talks_to_csv(self, fname):
        #fname = '/home/parallels/Documents/git/freeseer/src/test/export.csv'

        fieldNames = ('Title',
                      'Speaker',
                      'Abstract',
                      'Level',
                      'Event',
                      'Room',
                      'Time')
        
        try:
            file = open(fname, 'w')
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            headers = dict( (n,n) for n in fieldNames )
            writer.writerow(headers)
            
            result = self.db.get_talks()
            while result.next():
                #print unicode(result.value(1).toString())
                writer.writerow({'Title':unicode(result.value(1).toString()),
                                 'Speaker':unicode(result.value(2).toString()),
                                 'Abstract':unicode(result.value(3).toString()),
                                 'Level':unicode(result.value(4).toString()),
                                 'Event':unicode(result.value(5).toString()),
                                 'Room':unicode(result.value(6).toString()),
                                 'Time':unicode(result.value(7).toString())})   
        finally:
            file.close()
    
    def export_reports_to_csv(self, fname):
        fieldNames = ('Title',
                      'Speaker',
                      'Abstract',
                      'Level',
                      'Event',
                      'Room',
                      'Time',
                      'Problem',
                      'Error')
        try:
            file = open(fname, 'w')
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            headers = dict( (n,n) for n in fieldNames)
            writer.writerow(headers)
            
            result = self.db.get_reports()
            for report in result:
                writer.writerow({'Title':report.presentation.title,
                                 'Speaker':report.presentation.speaker,
                                 'Abstract':report.presentation.description,
                                 'Level':report.presentation.level,
                                 'Event':report.presentation.event,
                                 'Room':report.presentation.room,
                                 'Time':report.presentation.time,
                                 'Problem':report.failure.indicator,
                                 'Error':report.failure.comment})
        finally:
            file.close()
            
    ##
    ## Backend Functions
    ##
    
    def set_recording_area(self, x1, y1, x2, y2):
        # gstreamer backend needs to have the lower x/y coordinates
        # sent first.
        if x2 < x1:
            if y2 < y1:
                self.backend.set_recording_area(x2, y2, x1, y1)
            else:
                self.backend.set_recording_area(x2, y1, x1, y2)
        else:
            if y2 < y1:
                self.backend.set_recording_area(x1, y2, x2, y1)
            else:
                self.backend.set_recording_area(x1, y1, x2, y2)

    def prepare_metadata(self, presentation):
        """Returns a dictionary of tags and tag values.
        
        To be used for populating the current recording's file metadata.
        """
        return { "title" : presentation.title,
                 "artist" : presentation.speaker,
                 "performer" : presentation.speaker,
                 "album" : presentation.event,
                 "location" : presentation.room,
                 "date" : str(datetime.date.today()),
                 "comment" : presentation.description }


    def load_backend(self, presentation):
        logging.debug("Loading Output plugins...")
        
        load_plugins = []
        
        if self.config.record_to_file:
            p = self.plugman.plugmanc.getPluginByName(self.config.record_to_file_plugin, "Output")
            load_plugins.append(p)
            
        if self.config.record_to_stream:
            p = self.plugman.plugmanc.getPluginByName(self.config.record_to_stream_plugin, "Output")
            load_plugins.append(p)
            
        if self.config.audio_feedback:
            p = self.plugman.plugmanc.getPluginByName("Audio Feedback", "Output")
            load_plugins.append(p)
            
        if self.config.video_preview:
            p = self.plugman.plugmanc.getPluginByName("Video Preview", "Output")
            load_plugins.append(p)
                
        plugins = []
        for plugin in load_plugins:
            logging.debug("Loading Output: %s", plugin.plugin_object.get_name())
            
            extension = plugin.plugin_object.get_extension()

            # Create a filename to record to.
            record_name = self.get_record_name(presentation, extension)
    
            # Prepare metadata.
            metadata = self.prepare_metadata(presentation)
            #self.backend.populate_metadata(data)
    
            record_location = os.path.abspath(self.config.videodir + '/' + record_name)                
            plugin.plugin_object.set_recording_location(record_location)
            
            plugin.plugin_object.load_config(self.plugman)
            plugins.append(plugin.plugin_object)

        self.backend.load_output_plugins(plugins,
                                         self.config.enable_audio_recording,
                                         self.config.enable_video_recording,
                                         metadata)
        
        if self.config.enable_audio_recording:
            logging.debug("Loading Audio Recording plugins...")
            audiomixer = self.plugman.plugmanc.getPluginByName(self.config.audiomixer, "AudioMixer").plugin_object
            if audiomixer is not None:
                audiomixer.load_config(self.plugman)
                
                # Get audio mixer inputs bins.
                audiomixer_inputs = []
                
                audioinputs = audiomixer.get_inputs()
                for i in audioinputs:
                    logging.debug("Loading Audio Mixer Input: %s", i)
                    audio_input = self.plugman.plugmanc.getPluginByName(i, "AudioInput").plugin_object
                    audio_input.load_config(self.plugman)
                    audiomixer_inputs.append(audio_input.get_audioinput_bin())
                
                self.backend.load_audiomixer(audiomixer, audiomixer_inputs)
        
        if self.config.enable_video_recording:
            logging.debug("Loading Video Recording plugins...")
            videomixer = self.plugman.plugmanc.getPluginByName(self.config.videomixer, "VideoMixer").plugin_object
            if videomixer is not None:
                videomixer.load_config(self.plugman)
                
                # Get video mixer inputs bins.
                videomixer_inputs = []
                
                videoinputs = videomixer.get_inputs()
                for i in videoinputs:
                    logging.debug("Loading Video Mixer Input: %s", i)
                    video_input = self.plugman.plugmanc.getPluginByName(i, "VideoInput").plugin_object
                    video_input.load_config(self.plugman)
                    videomixer_inputs.append(video_input.get_videoinput_bin())
                
                self.backend.load_videomixer(videomixer, videomixer_inputs)
                
        self.pause()

    def record(self):
        """Informs backend to begin recording presentation."""
        self.backend.record()

    def pause(self):
        """Sets the pipeline up in paused state."""
        self.backend.pause()

    def stop(self):
        """Informs backend to stop recording."""
        self.backend.stop()
