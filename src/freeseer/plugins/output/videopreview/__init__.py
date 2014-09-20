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
Video Preview
-------------

An output plugin which provides a video window to preview the video that
is being recorded in real time.

@author: Thanh Ha
'''

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQT
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin import IOutput
from freeseer.framework.config import Config, options

# .freeseer-plugin custom
import widget

# Leaky Queue
LEAKY_VALUES = ["no", "upstream", "downstream"]


class VideoPreviewConfig(Config):
    """Configuration class for VideoPreview plugin."""
    # Video Preview variables
    previewsink = options.StringOption("autovideosink")
    leakyqueue = options.ChoiceOption(LEAKY_VALUES, "no")


class VideoPreview(IOutput):
    name = "Video Preview"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    type = IOutput.VIDEO
    recordto = IOutput.OTHER
    CONFIG_CLASS = VideoPreviewConfig

    def get_output_bin(self, audio=False, video=True, metadata=None):
        bin = gst.Bin()

        # Leaky queue necessary to work with rtmp streaming
        videoqueue = gst.element_factory_make("queue", "videoqueue")
        videoqueue.set_property("leaky", self.config.leakyqueue)
        bin.add(videoqueue)

        cspace = gst.element_factory_make("ffmpegcolorspace", "cspace")
        bin.add(cspace)

        videosink = gst.element_factory_make(self.config.previewsink, "videosink")
        bin.add(videosink)

        # Setup ghost pad
        pad = videoqueue.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        bin.add_pad(ghostpad)

        # Link Elements
        videoqueue.link(cspace)
        cspace.link(videosink)

        return bin

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()
            self.widget.leakyQueueComboBox.addItems(LEAKY_VALUES)
        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.previewComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.set_previewsink)
        self.widget.connect(self.widget.leakyQueueComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.set_leakyqueue)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        previewIndex = self.widget.previewComboBox.findText(self.config.previewsink)
        self.widget.previewComboBox.setCurrentIndex(previewIndex)

        leakyQueueIndex = self.widget.leakyQueueComboBox.findText(self.config.leakyqueue)
        self.widget.leakyQueueComboBox.setCurrentIndex(leakyQueueIndex)

        # Finally enable connections
        self.__enable_connections()

    def set_previewsink(self, previewsink):
        self.config.previewsink = previewsink
        self.config.save()

    def set_leakyqueue(self, value):
        self.config.leakyqueue = value
        self.config.save()

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.previewLabel.setText(self.gui.app.translate('plugin-videopreview', 'Preview'))
        self.widget.leakyQueueLabel.setText(self.gui.app.translate('plugin-videopreview', 'Leaky Queue'))
