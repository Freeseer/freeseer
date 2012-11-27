'''
freeseer - vga/presentation capture software

Copyright (C) 2011-2012  Free and Open Source Software Learning Centre
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

@author: Thanh Ha
'''

import ConfigParser

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IOutput

class OggOutput(IOutput):
    name = "Ogg Output"
    type = IOutput.BOTH
    recordto = IOutput.FILE
    extension = "ogg"
    tags = None
    
    # Ogg Output variables
    audio_quality = 0.3
    video_bitrate = 2400
    
    def get_output_bin(self, audio=True, video=True, metadata=None):
        bin = gst.Bin(self.name)
        
        if metadata is not None:
            self.set_metadata(metadata)
            
        # Muxer
        muxer = gst.element_factory_make("oggmux", "muxer")
        bin.add(muxer)
        
        # File sink
        filesink = gst.element_factory_make('filesink', 'filesink')
        filesink.set_property('location', self.location)
        bin.add(filesink)
        
        #
        # Setup Audio Pipeline if Audio Recording is Enabled
        #
        if audio:
            audioqueue = gst.element_factory_make("queue", "audioqueue")
            bin.add(audioqueue)
            
            audioconvert = gst.element_factory_make("audioconvert", "audioconvert")
            bin.add(audioconvert)
            
            audiolevel = gst.element_factory_make('level', 'audiolevel')
            audiolevel.set_property('interval', 20000000)
            bin.add(audiolevel)
            
            audiocodec = gst.element_factory_make("vorbisenc", "audiocodec")
            audiocodec.set_property("quality", float(self.audio_quality))
            bin.add(audiocodec)
            
            # Setup metadata
            vorbistag = gst.element_factory_make("vorbistag", "vorbistag")
            # set tag merge mode to GST_TAG_MERGE_REPLACE
            merge_mode = gst.TagMergeMode.__enum_values__[2]
    
            vorbistag.merge_tags(self.tags, merge_mode)
            vorbistag.set_tag_merge_mode(merge_mode)
            bin.add(vorbistag)
            
            # Setup ghost pads
            audiopad = audioqueue.get_pad("sink")
            audio_ghostpad = gst.GhostPad("audiosink", audiopad)
            bin.add_pad(audio_ghostpad)
            
            gst.element_link_many(audioqueue, audioconvert, audiolevel, audiocodec, vorbistag, muxer)
        
        
        #
        # Setup Video Pipeline
        #
        if video:
            videoqueue = gst.element_factory_make("queue", "videoqueue")
            bin.add(videoqueue)
            
            videocodec = gst.element_factory_make("theoraenc", "videocodec")
            videocodec.set_property("bitrate", int(self.video_bitrate))
            bin.add(videocodec)
            
            # Setup ghost pads
            videopad = videoqueue.get_pad("sink")
            video_ghostpad = gst.GhostPad("videosink", videopad)
            bin.add_pad(video_ghostpad)
            
            gst.element_link_many(videoqueue, videocodec, muxer)
        
        #
        # Link muxer to filesink
        #
        gst.element_link_many(muxer, filesink)
        
        return bin
    
    def set_metadata(self, data):
        '''
        Populate global tag list variable with file metadata for
        vorbistag audio element
        '''
        self.tags = gst.TagList()

        for tag in data.keys():
            if(gst.tag_exists(tag)):
                self.tags[tag] = data[tag]
            else:
                #self.core.logger.log.debug("WARNING: Tag \"" + str(tag) + "\" is not registered with gstreamer.")
                pass
            
    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.audio_quality = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Audio Quality")
            self.video_bitrate = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Video Bitrate")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Audio Quality", self.audio_quality)
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Video Bitrate", self.video_bitrate)
        except TypeError:
            # Temp fix for issue where reading audio_quality the 2nd time causes TypeError.
            pass
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            #
            # Audio Quality
            #
            
            self.label_audio_quality = QtGui.QLabel("Audio Quality")
            self.spinbox_audio_quality = QtGui.QDoubleSpinBox()
            self.spinbox_audio_quality.setMinimum(0.0)
            self.spinbox_audio_quality.setMaximum(1.0)
            self.spinbox_audio_quality.setSingleStep(0.1)
            self.spinbox_audio_quality.setDecimals(1)
            self.spinbox_audio_quality.setValue(0.3)            # Default value 0.3
            layout.addRow(self.label_audio_quality, self.spinbox_audio_quality)
            
            self.widget.connect(self.spinbox_audio_quality, QtCore.SIGNAL('valueChanged(double)'), self.set_audio_quality)
            
            #
            # Video Quality
            #
            
            self.label_video_quality = QtGui.QLabel("Video Quality (kb/s)")
            self.spinbox_video_quality = QtGui.QSpinBox()
            self.spinbox_video_quality.setMinimum(0)
            self.spinbox_video_quality.setMaximum(16777215)
            self.spinbox_video_quality.setValue(2400)           # Default value 2400
            layout.addRow(self.label_video_quality, self.spinbox_video_quality)
            
            self.widget.connect(self.spinbox_video_quality, QtCore.SIGNAL('valueChanged(int)'), self.set_video_bitrate)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        self.spinbox_audio_quality.setValue(float(self.audio_quality))
        self.spinbox_video_quality.setValue(int(self.video_bitrate))

    def set_audio_quality(self):
        self.audio_quality = self.spinbox_audio_quality.value()
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Audio Quality", str(self.audio_quality))
        self.plugman.save()
        
    def set_video_bitrate(self):
        self.video_bitrate = self.spinbox_video_quality.value()
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Video Bitrate", str(self.video_bitrate))
        self.plugman.save()
        
    def get_properties(self):
        return ['AudioQuality', 'VideoBitrate']
    
    def get_property_value(self, property):
        if property == "audioquality":
            return self.audio_quality
        elif property == "videobitrate":
            return self.video_bitrate
        else:
            return "There's no property with such name"
        
    def set_property_value(self, property, value):
        if property == "audioquality":
            return self.set_audio_quality(value)
        elif property == "videobitrate":
            return self.set_video_bitrate(value)
        else:
            return "Error: There's no property with such name" 

