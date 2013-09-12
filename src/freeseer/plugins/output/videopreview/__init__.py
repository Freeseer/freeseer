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

# python-libs
import ConfigParser

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQT
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin import IOutput

# .freeseer-plugin custom
import widget


class VideoPreview(IOutput):
    name = "Video Preview"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    type = IOutput.VIDEO
    recordto = IOutput.OTHER

    # Video Preview variables
    previewsink = "autovideosink"
    leakyqueue = "no"

    # Leaky Queue
    LEAKY_VALUES = ["no", "upstream", "downstream"]

    def get_output_bin(self, audio=False, video=True, metadata=None):
        bin = gst.Bin()

        # Leaky queue necessary to work with rtmp streaming
        videoqueue = gst.element_factory_make("queue", "videoqueue")
        videoqueue.set_property("leaky", self.leakyqueue)
        bin.add(videoqueue)

        cspace = gst.element_factory_make("ffmpegcolorspace", "cspace")
        bin.add(cspace)

        videosink = gst.element_factory_make(self.previewsink, "videosink")
        bin.add(videosink)

        # Setup ghost pad
        pad = videoqueue.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        bin.add_pad(ghostpad)

        # Link Elements
        videoqueue.link(cspace)
        cspace.link(videosink)

        return bin

    def load_config(self, plugman):
        self.plugman = plugman
        try:
            self.previewsink = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Preview Sink")
            self.leakyqueue = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Leaky Queue")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Preview Sink", self.previewsink)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Leaky Queue", self.leakyqueue)

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()
            self.widget.leakyQueueComboBox.addItems(self.LEAKY_VALUES)

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.previewComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.set_previewsink)
        self.widget.connect(self.widget.leakyQueueComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.set_leakyqueue)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        previewIndex = self.widget.previewComboBox.findText(self.previewsink)
        self.widget.previewComboBox.setCurrentIndex(previewIndex)

        leakyQueueIndex = self.widget.leakyQueueComboBox.findText(self.leakyqueue)
        self.widget.leakyQueueComboBox.setCurrentIndex(leakyQueueIndex)

        # Finally enable connections
        self.__enable_connections()

    def set_previewsink(self, previewsink):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Preview Sink", previewsink)

    def set_leakyqueue(self, value):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Leaky Queue", value)

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.previewLabel.setText(self.gui.app.translate('plugin-videopreview', 'Preview'))
        self.widget.leakyQueueLabel.setText(self.gui.app.translate('plugin-videopreview', 'Leaky Queue'))
