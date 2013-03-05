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

import datetime
import logging
import os
import unicodedata

import gobject
gobject.threads_init()
import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IOutput

class Gstreamer:
    NULL = 0
    RECORD = 1
    PAUSE = 2
    STOP = 3
    
    def __init__(self, config, plugman, window_id=None, audio_feedback=None):
        self.config = config
        self.plugman = plugman
        self.window_id = window_id
        self.audio_feedback_event = audio_feedback
        
        self.record_audio = False
        self.record_video = False
        
        self.current_state = Gstreamer.NULL
        
        # Initialize Player
        self.player = gst.Pipeline('player')
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('message', self.on_message)
        bus.connect('sync-message::element', self.on_sync_message)
        
        # Initialize Entry Points
        self.audio_tee = gst.element_factory_make('tee', 'audio_tee')
        self.video_tee = gst.element_factory_make('tee', 'video_tee')
        self.player.add(self.audio_tee)
        self.player.add(self.video_tee)
        
        logging.debug("Gstreamer initialized.")

    ##
    ## GST Player Functions
    ##
    def on_message(self, bus, message):
        t = message.type

        if t == gst.MESSAGE_EOS:
            self.stop()

        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            #self.core.logger.log.debug('Error: ' + str(err) + str(debug))
            #self.player.set_state(gst.STATE_NULL)
            #self.stop()

        elif message.structure is not None:
            s = message.structure.get_name()

            if s == 'level':
                msg = message.structure.to_string()
                rms_dB = float(msg.split(',')[6].split('{')[1].rstrip('}'))
                
                # This is an inaccurate representation of decibels into percent
                # conversion, this code should be revisited.
                try:
                    percent = (int(round(rms_dB)) + 50) * 2
                except OverflowError:
                    percent = 0
                self.audio_feedback_event(percent)
            
    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == 'prepare-xwindow-id':
            imagesink = message.src
            imagesink.set_property('force-aspect-ratio', True)
            imagesink.set_xwindow_id(int(self.window_id))
            logging.debug("Preview loaded into window.")
            
    def keyboard_event(self, key):
        """
        Keyboard event handler.
        """
        pass
            
    ##
    ## Recording functions
    ##
    def record(self):
        """
        Start recording.
        """
        self.player.set_state(gst.STATE_PLAYING)
        self.current_state = Gstreamer.RECORD
        logging.debug("Recording started.")
        
    def pause(self):
        """
        Pause recording.
        """
        self.player.set_state(gst.STATE_PAUSED)
        self.current_state = Gstreamer.PAUSE
        logging.debug("Gstreamer paused.")
    
    def stop(self):
        """
        Stop recording.
        """
        if self.current_state != Gstreamer.NULL and self.current_state != Gstreamer.STOP:
            self.player.set_state(gst.STATE_NULL)
            
            self.unload_audiomixer()
            self.unload_videomixer()    
            self.unload_output_plugins()
            
            self.current_state = Gstreamer.STOP
            logging.debug("Gstreamer stopped.")
            
            
    ##
    ## Record Filename Functions
    ##
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
        
    ##
    ## Plugin Loading
    ##

    def load_backend(self, presentation):
        logging.debug("Loading Output plugins...")
        
        load_plugins = []
        
        if self.config.record_to_file:
            p = self.plugman.get_plugin_by_name(self.config.record_to_file_plugin, "Output")
            load_plugins.append(p)
            
        if self.config.record_to_stream:
            p = self.plugman.get_plugin_by_name(self.config.record_to_stream_plugin, "Output")
            load_plugins.append(p)
            
        if self.config.audio_feedback:
            p = self.plugman.get_plugin_by_name("Audio Feedback", "Output")
            load_plugins.append(p)
            
        if self.config.video_preview:
            p = self.plugman.get_plugin_by_name("Video Preview", "Output")
            load_plugins.append(p)
                
        plugins = []
        for plugin in load_plugins:
            logging.debug("Loading Output: %s", plugin.plugin_object.get_name())
            
            extension = plugin.plugin_object.get_extension()

            # Create a filename to record to.
            record_name = self.get_record_name(presentation, extension)
    
            # Prepare metadata.
            metadata = self.prepare_metadata(presentation)
            #self.populate_metadata(data)
    
            record_location = os.path.abspath(self.config.videodir + '/' + record_name)                
            plugin.plugin_object.set_recording_location(record_location)
            
            plugin.plugin_object.load_config(self.plugman)
            plugins.append(plugin.plugin_object)

        self.load_output_plugins(plugins,
                                         self.config.enable_audio_recording,
                                         self.config.enable_video_recording,
                                         metadata)
        
        if self.config.enable_audio_recording:
            logging.debug("Loading Audio Recording plugins...")
            audiomixer = self.plugman.get_plugin_by_name(self.config.audiomixer, "AudioMixer").plugin_object
            if audiomixer is not None:
                audiomixer.load_config(self.plugman)
                
                # Get audio mixer inputs bins.
                audiomixer_inputs = []
                
                audioinputs = audiomixer.get_inputs()
                for i in audioinputs:
                    logging.debug("Loading Audio Mixer Input: %s", i)
                    audio_input = self.plugman.get_plugin_by_name(i, "AudioInput").plugin_object
                    audio_input.load_config(self.plugman)
                    audiomixer_inputs.append(audio_input.get_audioinput_bin())
                
                self.load_audiomixer(audiomixer, audiomixer_inputs)
        
        if self.config.enable_video_recording:
            logging.debug("Loading Video Recording plugins...")
            videomixer = self.plugman.get_plugin_by_name(self.config.videomixer, "VideoMixer").plugin_object
            if videomixer is not None:
                videomixer.load_config(self.plugman)
                
                # Get video mixer inputs bins.
                videomixer_inputs = []
                
                videoinputs = videomixer.get_inputs()
                for i in videoinputs:
                    logging.debug("Loading Video Mixer Input: %s", i)
                    video_input = self.plugman.get_plugin_by_name(i, "VideoInput").plugin_object
                    video_input.load_config(self.plugman)
                    videomixer_inputs.append(video_input.get_videoinput_bin())
                
                self.load_videomixer(videomixer, videomixer_inputs)
                
        self.pause()
    
    def load_output_plugins(self, plugins, record_audio, record_video, metadata):
        self.output_plugins = []
        for plugin in plugins:
            type = plugin.get_type()
            bin = plugin.get_output_bin(record_audio, record_video, metadata)
            
            if type == IOutput.AUDIO:
                if record_audio:
                    self.player.add(bin)
                    self.audio_tee.link(bin)
                    self.output_plugins.append(bin)
            elif type == IOutput.VIDEO:
                if record_video:
                    self.player.add(bin)
                    self.video_tee.link(bin)
                    self.output_plugins.append(bin)
            elif type == IOutput.BOTH:
                self.player.add(bin)
                if record_audio: self.audio_tee.link_pads("src%d", bin, "audiosink")                
                if record_video: self.video_tee.link_pads("src%d", bin, "videosink")
                self.output_plugins.append(bin)
                
    def unload_output_plugins(self):
        for plugin in self.output_plugins:
            self.video_tee.unlink(plugin)
            self.audio_tee.unlink(plugin)
            self.player.remove(plugin)
    
    def load_audiomixer(self, mixer, inputs):
        self.record_audio = True
        self.audio_input_plugins = inputs
        
        self.audiomixer = mixer.get_audiomixer_bin()
        self.player.add(self.audiomixer)
        self.audiomixer.link(self.audio_tee)
        
        mixer.load_inputs(self.player, self.audiomixer, inputs)
        
    def unload_audiomixer(self):
        if self.record_audio is True:
            for plugin in self.audio_input_plugins:
                self.audio_tee.unlink(plugin)
                self.player.remove(plugin)
        
            self.audiomixer.unlink(self.audio_tee)
            self.player.remove(self.audiomixer)

    def load_videomixer(self, mixer, inputs):
        self.record_video = True
        self.video_input_plugins = inputs
        
        self.videomixer = mixer.get_videomixer_bin()
        self.player.add(self.videomixer)
        self.videomixer.link(self.video_tee)
        
        mixer.load_inputs(self.player, self.videomixer, inputs)
        
    def unload_videomixer(self):
        if self.record_video is True:
            for plugin in self.video_input_plugins:
                self.video_tee.unlink(plugin)
                self.player.remove(plugin)
            
            self.videomixer.unlink(self.video_tee)
            self.player.remove(self.videomixer)
