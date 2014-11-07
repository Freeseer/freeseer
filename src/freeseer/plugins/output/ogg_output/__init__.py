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

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeeseer
from freeseer.framework.multimedia import Quality
from freeseer.framework.plugin import IOutput
from freeseer.framework.config import Config, options

# .freeseer-plugin custom
import widget


class OggOutputConfig(Config):
    """Configuration class for OggOutput plugin."""
    matterhorn = options.IntegerOption(0)
    audio_quality = options.FloatOption(0.3)
    video_bitrate = options.IntegerOption(2400)


class OggOutput(IOutput):
    name = "Ogg Output"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    type = IOutput.BOTH
    recordto = IOutput.FILE
    extension = "ogg"
    tags = None
    CONFIG_CLASS = OggOutputConfig
    configurable = True
    AUDIO_MIN = -0.1
    AUDIO_RANGE = 1.1

    def get_output_bin(self, audio=True, video=True, metadata=None):
        bin = gst.Bin()

        if metadata is not None:
            self.set_metadata(metadata)
            if self.config.matterhorn == 2:  # checked
                self.generate_xml_metadata(metadata).write(self.location + ".xml")

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
            audiocodec.set_property("quality", self.config.audio_quality)
            bin.add(audiocodec)

            # Setup metadata
            vorbistag = gst.element_factory_make("vorbistag", "vorbistag")
            # set tag merge mode to GST_TAG_MERGE_REPLACE
            merge_mode = gst.TagMergeMode.__enum_values__[2]

            if metadata is not None:
                # Only set tag if metadata is set
                vorbistag.merge_tags(self.tags, merge_mode)
            vorbistag.set_tag_merge_mode(merge_mode)
            bin.add(vorbistag)

            # Setup ghost pads
            audiopad = audioqueue.get_pad("sink")
            audio_ghostpad = gst.GhostPad("audiosink", audiopad)
            bin.add_pad(audio_ghostpad)

            # Link Elements
            audioqueue.link(audioconvert)
            audioconvert.link(audiolevel)
            audiolevel.link(audiocodec)
            audiocodec.link(vorbistag)
            vorbistag.link(muxer)

        #
        # Setup Video Pipeline
        #
        if video:
            videoqueue = gst.element_factory_make("queue", "videoqueue")
            bin.add(videoqueue)

            videocodec = gst.element_factory_make("theoraenc", "videocodec")
            videocodec.set_property("bitrate", self.config.video_bitrate)
            bin.add(videocodec)

            # Setup ghost pads
            videopad = videoqueue.get_pad("sink")
            video_ghostpad = gst.GhostPad("videosink", videopad)
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
        self.tags = gst.TagList()

        for tag in data.keys():
            if(gst.tag_exists(tag)):
                self.tags[tag] = data[tag]
            else:
                #self.core.logger.log.debug("WARNING: Tag \"" + str(tag) + "\" is not registered with gstreamer.")
                pass

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

        return self.widget

    def get_video_quality_layout(self):
        """Returns a layout with the video quality config widgets for configtool to use."""
        return self.get_widget().get_video_quality_layout()

    def get_audio_quality_layout(self):
        """Returns a layout with the audio quality config widgets for configtool to use."""
        return self.get_widget().get_audio_quality_layout()

    def __enable_connections(self):
        self.widget.connect(self.widget.spinbox_audio_quality, SIGNAL('valueChanged(double)'), self.audio_quality_changed)
        self.widget.connect(self.widget.spinbox_video_quality, SIGNAL('valueChanged(int)'), self.video_bitrate_changed)
        self.widget.connect(self.widget.checkbox_matterhorn, SIGNAL('stateChanged(int)'), self.set_matterhorn)

    def widget_load_config(self, plugman):
        self.get_config()

        self.widget.spinbox_audio_quality.setValue(self.config.audio_quality)
        self.widget.spinbox_video_quality.setValue(self.config.video_bitrate)
        self.widget.checkbox_matterhorn.setCheckState(self.config.matterhorn)

        # Finally enable connections
        self.__enable_connections()

    def audio_quality_changed(self):
        """Called when a change to the SpinBox for audio quality is made"""
        self.config.audio_quality = self.widget.spinbox_audio_quality.value()
        self.config.save()

    def set_audio_quality(self, quality):
        self.get_config()

        if quality == Quality.LOW:
            self.config.audio_quality = self.AUDIO_MIN + (self.AUDIO_RANGE * Quality.LOW_AUDIO_FACTOR)
        elif quality == Quality.MEDIUM:
            self.config.audio_quality = self.AUDIO_MIN + (self.AUDIO_RANGE * Quality.MEDIUM_AUDIO_FACTOR)
        elif quality == Quality.HIGH:
            self.config.audio_quality = self.AUDIO_MIN + (self.AUDIO_RANGE * Quality.HIGH_AUDIO_FACTOR)

        if self.widget_config_loaded:
            self.widget.spinbox_audio_quality.setValue(self.config.audio_quality)

        self.config.save()

    def video_bitrate_changed(self):
        """Called when a change to the SpinBox for video bitrate is made"""
        self.config.video_bitrate = self.widget.spinbox_video_quality.value()
        self.config.save()

    def set_video_bitrate(self, bitrate):
        self.get_config()

        if self.widget_config_loaded:
            self.widget.spinbox_video_quality.setValue(bitrate)

        self.config.video_bitrate = bitrate
        self.config.save()

    def set_matterhorn(self, state):
        """
        Enables or Disables Matterhorn metadata generation.

        If enabled filename.xml will be created along side the video file
        containing matterhorn metadata in xml format.
        """
        self.config.matterhorn = state
        self.config.save()

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.label_audio_quality.setText(self.gui.app.translate('plugin-ogg-output', 'Audio Quality'))
        self.widget.label_video_quality.setText(self.gui.app.translate('plugin-ogg-output', 'Video Quality (kb/s)'))
        self.widget.label_matterhorn.setText(self.gui.app.translate('plugin-ogg-output', 'Matterhorn Metadata'))
        self.widget.label_matterhorn.setToolTip(self.gui.app.translate('plugin-ogg-output', 'Generates Matterhorn Metadata in XML format'))
