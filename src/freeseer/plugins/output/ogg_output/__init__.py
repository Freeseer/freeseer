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
# http://github.com/Freeseer/freeseer/

'''
Ogg Output
----------

An output plugin which records to Ogg format using Theora for encoding for
video and Vorbis encoding for Audio.

@author: Thanh Ha
'''

# python-libs
import ConfigParser


# GStreamer
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GstTag
from gi.repository import GLib

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeeseer
from freeseer.framework.plugin import IOutput

# .freeseer-plugin custom
import widget


class OggOutput(IOutput):
    name = "Ogg Output"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    type = IOutput.BOTH
    recordto = IOutput.FILE
    extension = "ogg"
    tags = None
    matterhorn = 0

    # Ogg Output variables
    audio_quality = 0.3
    video_bitrate = 2400

    def get_output_bin(self, audio=True, video=True, metadata=None):
        bin = Gst.Bin()

        if metadata is not None:
            self.set_metadata(metadata)
            if self.matterhorn == 2:  # checked
                self.generate_xml_metadata(metadata).write(self.location + ".xml")

        # Muxer
        muxer = Gst.ElementFactory.make("oggmux", None)
        bin.add(muxer)

        # File sink
        filesink = Gst.ElementFactory.make('filesink', None)
        filesink.set_property('location', self.location)
        bin.add(filesink)

        #
        # Setup Audio Pipeline if Audio Recording is Enabled
        #
        if audio:
            
            #Create audio elements
            q1 = Gst.ElementFactory.make('queue', None)
            enc = Gst.ElementFactory.make('vorbisenc', None)
            enc.set_property("quality", float(self.audio_quality))
            q2 = Gst.ElementFactory.make('queue', None)
            audioconvert = Gst.ElementFactory.make("audioconvert", None)
            audiolevel = Gst.ElementFactory.make('level', None)
            audiolevel.set_property('interval', 20000000)

            # # Setup metadata
            vorbistag = Gst.ElementFactory.make("vorbistag", None)
            #set tag merge mode to GST_TAG_MERGE_REPLACE
            merge_mode = Gst.TagMergeMode.__enum_values__[2]            

            if metadata is not None:
                # Only set tag if metadata is set
                vorbistag.merge_tags(self.tags, merge_mode)
            vorbistag.set_tag_merge_mode(merge_mode)
            
            #Add the audio elements to the bin
            bin.add(q1)
            bin.add(audiolevel)
            bin.add(audioconvert)
            bin.add(enc)
            bin.add(vorbistag)
            bin.add(q2)

            #link the audio elements
            q1.link(audiolevel)
            audiolevel.link(audioconvert)
            audioconvert.link(enc)
            enc.link(vorbistag)
            vorbistag.link(q2)
            q2.link(muxer)

            # Setup ghost pads
            audiopad = q1.get_static_pad("sink")
            audio_ghostpad = Gst.GhostPad.new("audiosink", audiopad)
            bin.add_pad(audio_ghostpad)

        #
        # Setup Video Pipeline
        #
        if video:
            videoqueue = Gst.ElementFactory.make("queue", None)
            bin.add(videoqueue)

            videocodec = Gst.ElementFactory.make("theoraenc", None)
            videocodec.set_property("bitrate", int(self.video_bitrate))
            bin.add(videocodec)

            # Setup ghost pads
            videopad = videoqueue.get_static_pad("sink")
            video_ghostpad = Gst.GhostPad.new("videosink", videopad)
            bin.add_pad(video_ghostpad)

            # Link Elements
            videoqueue.link(videocodec)
            videocodec.link(muxer)

        #
        # Link muxer to filesink
        #
        muxer.link(filesink)
        return bin

    def set_metadata(self, data):
        '''
        Populate global tag list variable with file metadata for
        vorbistag audio element
        '''
        self.tags = Gst.TagList.new_empty()
        merge_mode = Gst.TagMergeMode.__enum_values__[2]

        for tag in data.keys():
            if(Gst.tag_exists(tag)):
                if tag == "date":
                    s_date = data[tag].split("-")
                    Tag_date = GLib.Date() 
                    Tag_date.set_day(int(s_date[2]))
                    Tag_date.set_month(s_date[1])
                    Tag_date.set_year(int(s_date[0]))
                    self.tags.add_value(merge_mode, tag, Tag_date)
                else:
                    self.tags.add_value(merge_mode, tag, str(data[tag]))
            else:
                self.core.logger.log.debug("WARNING: Tag \"" + str(tag) + "\" is not registered with gstreamer.")
                pass

    def load_config(self, plugman):
        self.plugman = plugman

        try:
            self.audio_quality = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Quality")
            self.video_bitrate = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Video Bitrate")
            self.matterhorn = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Matterhorn"))
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Quality", self.audio_quality)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Bitrate", self.video_bitrate)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Matterhorn", self.matterhorn)
        except TypeError:
            # Temp fix for issue where reading audio_quality the 2nd time causes TypeError.
            pass

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.spinbox_audio_quality, SIGNAL('valueChanged(double)'), self.set_audio_quality)
        self.widget.connect(self.widget.spinbox_video_quality, SIGNAL('valueChanged(int)'), self.set_video_bitrate)
        self.widget.connect(self.widget.checkbox_matterhorn, SIGNAL('stateChanged(int)'), self.set_matterhorn)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        self.widget.spinbox_audio_quality.setValue(float(self.audio_quality))
        self.widget.spinbox_video_quality.setValue(int(self.video_bitrate))
        self.widget.checkbox_matterhorn.setCheckState(int(self.matterhorn))

        # Finally enable connections
        self.__enable_connections()

    def set_audio_quality(self):
        self.audio_quality = self.widget.spinbox_audio_quality.value()
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Quality", str(self.audio_quality))

    def set_video_bitrate(self):
        self.video_bitrate = self.widget.spinbox_video_quality.value()
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Bitrate", str(self.video_bitrate))

    def set_matterhorn(self, state):
        """
        Enables or Disables Matterhorn metadata generation.

        If enabled filename.xml will be created along side the video file
        containing matterhorn metadata in xml format.
        """
        self.matterhorn = state
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Matterhorn", str(self.matterhorn))

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.label_audio_quality.setText(self.gui.app.translate('plugin-ogg-output', 'Audio Quality'))
        self.widget.label_video_quality.setText(self.gui.app.translate('plugin-ogg-output', 'Video Quality (kb/s)'))
        self.widget.label_matterhorn.setText(self.gui.app.translate('plugin-ogg-output', 'Matterhorn Metadata'))
        self.widget.label_matterhorn.setToolTip(self.gui.app.translate('plugin-ogg-output', 'Generates Matterhorn Metadata in XML format'))
