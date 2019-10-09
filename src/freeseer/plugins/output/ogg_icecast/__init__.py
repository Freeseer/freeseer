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
Ogg Icecast
-----------

A streaming plugin which records sends an Ogg stream to an icecast server.

@author: Thanh Ha
'''

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.multimedia import Quality
from freeseer.framework.plugin import IOutput
from freeseer.framework.config import Config, options

# .freeseer-plugin custom
from . import widget


class OggIcecastConfig(Config):
    """Configuration class for OggIcecast Plugin."""
    ip = options.StringOption("127.0.0.1")
    port = options.IntegerOption(8000)
    password = options.StringOption("hackme")
    mount = options.StringOption("stream.ogg")
    audio_quality = options.FloatOption(0.3)
    video_bitrate = options.IntegerOption(2400)


class OggIcecast(IOutput):
    name = "Ogg Icecast"
    os = ["linux", "linux2"]
    type = IOutput.BOTH
    recordto = IOutput.STREAM
    extension = "ogg"
    tags = None
    CONFIG_CLASS = OggIcecastConfig
    configurable = True
    AUDIO_MIN = -0.1
    AUDIO_RANGE = 1.1

    def get_output_bin(self, audio=True, video=True, metadata=None):
        bin = gst.Bin()

        if metadata is not None:
            self.set_metadata(metadata)

        # Muxer
        muxer = gst.element_factory_make("oggmux", "muxer")
        bin.add(muxer)

        icecast = gst.element_factory_make("shout2send", "icecast")
        icecast.set_property("ip", self.config.ip)
        icecast.set_property("port", self.config.port)
        icecast.set_property("password", self.config.password)
        icecast.set_property("mount", self.config.mount)
        bin.add(icecast)

        #
        # Setup Audio Pipeline
        #
        if audio:
            audioqueue = gst.element_factory_make("queue", "audioqueue")
            bin.add(audioqueue)

            audioconvert = gst.element_factory_make("audioconvert", "audioconvert")
            bin.add(audioconvert)

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

            # Link elements
            audioqueue.link(audioconvert)
            audioconvert.link(audiocodec)
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

            videopad = videoqueue.get_pad("sink")
            video_ghostpad = gst.GhostPad("videosink", videopad)
            bin.add_pad(video_ghostpad)

            videoqueue.link(videocodec)
            videocodec.link(muxer)

        #
        # Link muxer to icecast
        #
        muxer.link(icecast)

        return bin

    def set_metadata(self, data):
        '''
        Populate global tag list variable with file metadata for
        vorbistag audio element
        '''
        self.tags = gst.TagList()

        for tag in list(data.keys()):
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
        self.widget.connect(self.widget.lineedit_ip, SIGNAL('editingFinished()'), self.set_ip)
        self.widget.connect(self.widget.spinbox_port, SIGNAL('valueChanged(int)'), self.set_port)
        self.widget.connect(self.widget.lineedit_password, SIGNAL('editingFinished()'), self.set_password)
        self.widget.connect(self.widget.lineedit_mount, SIGNAL('editingFinished()'), self.set_mount)
        self.widget.connect(self.widget.spinbox_audio_quality, SIGNAL('valueChanged(double)'), self.audio_quality_changed)
        self.widget.connect(self.widget.spinbox_video_quality, SIGNAL('valueChanged(int)'), self.video_bitrate_changed)

    def widget_load_config(self, plugman):
        self.get_config()

        self.widget.lineedit_ip.setText(self.config.ip)
        self.widget.spinbox_port.setValue(self.config.port)
        self.widget.lineedit_password.setText(self.config.password)
        self.widget.lineedit_mount.setText(self.config.mount)

        # Finally enable connections
        self.__enable_connections()

    def set_ip(self):
        self.config.ip = str(self.widget.lineedit_ip.text())
        self.config.save()

    def set_port(self, port):
        self.config.port = port
        self.config.save()

    def set_password(self):
        self.config.password = str(self.widget.lineedit_password.text())
        self.config.save()

    def set_mount(self):
        self.config.mount = str(self.widget.lineedit_mount.text())
        self.config.save()

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

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.label_ip.setText(self.gui.app.translate('plugin-icecast', 'IP'))
        self.widget.label_port.setText(self.gui.app.translate('plugin-icecast', 'Port'))
        self.widget.label_password.setText(self.gui.app.translate('plugin-icecast', 'Password'))
        self.widget.label_mount.setText(self.gui.app.translate('plugin-icecast', 'Mount'))
