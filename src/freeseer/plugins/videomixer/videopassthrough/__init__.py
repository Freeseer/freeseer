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
Video Passthrough
-----------------

A simple video mixer plugin that takes 1 input and passes it on to the
output plugin. This plugin is capable of configuring the video framerate
as well.

@author: Thanh Ha
'''

# GStreamer modules
import pygst
pygst.require("0.10")
import gst

# PyQt modules
from PyQt4.QtCore import SIGNAL

# Freeseer modules
from freeseer.framework.plugin import IVideoMixer
from freeseer.framework.config import Config, options

# .freeseer-plugin custom modules
import widget


class VideoPassthroughConfig(Config):
    """Configuration class for VideoPassthrough plugin."""
    input = options.StringOption("Video Test Source")
    input_type = options.StringOption("video/x-raw-rgb")
    framerate = options.IntegerOption(30)
    resolution = options.StringOption("NOSCALE")


class VideoPassthrough(IVideoMixer):
    name = "Video Passthrough"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    widget = None
    CONFIG_CLASS = VideoPassthroughConfig

    def get_videomixer_bin(self):
        bin = gst.Bin()

        # Video Rate
        videorate = gst.element_factory_make("videorate", "videorate")
        bin.add(videorate)
        videorate_cap = gst.element_factory_make("capsfilter",
                                                 "video_rate_cap")
        videorate_cap.set_property("caps",
                        gst.caps_from_string("%s, framerate=%d/1" % (self.config.input_type, self.config.framerate)))
        bin.add(videorate_cap)
        # --- End Video Rate

        # Video Scaler (Resolution)
        videoscale = gst.element_factory_make("videoscale", "videoscale")
        bin.add(videoscale)
        videoscale_cap = gst.element_factory_make("capsfilter",
                                                  "videoscale_cap")
        if self.config.resolution != "NOSCALE":
            videoscale_cap.set_property('caps',
                                        gst.caps_from_string('%s, width=640, height=480' % (self.config.input_type)))
        bin.add(videoscale_cap)
        # --- End Video Scaler

        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)

        # Link Elements
        videorate.link(videorate_cap)
        videorate_cap.link(videoscale)
        videoscale.link(videoscale_cap)
        videoscale_cap.link(colorspace)

        # Setup ghost pad
        sinkpad = videorate.get_pad("sink")
        sink_ghostpad = gst.GhostPad("sink", sinkpad)
        bin.add_pad(sink_ghostpad)

        srcpad = colorspace.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)

        return bin

    def get_inputs(self):
        inputs = [(self.config.input, 0)]
        return inputs

    def load_inputs(self, player, mixer, inputs):
        # Load source
        input = inputs[0]
        player.add(input)
        input.link(mixer)

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()
        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.inputCombobox, SIGNAL('currentIndexChanged(const QString&)'), self.set_input)
        self.widget.connect(self.widget.framerateSlider, SIGNAL("valueChanged(int)"), self.widget.framerateSpinBox.setValue)
        self.widget.connect(self.widget.framerateSpinBox, SIGNAL("valueChanged(int)"), self.widget.framerateSlider.setValue)
        self.widget.connect(self.widget.videocolourComboBox, SIGNAL("currentIndexChanged(const QString&)"), self.set_input_type)
        self.widget.connect(self.widget.framerateSlider, SIGNAL("valueChanged(int)"), self.set_framerate)
        self.widget.connect(self.widget.framerateSpinBox, SIGNAL("valueChanged(int)"), self.set_framerate)
        self.widget.connect(self.widget.inputSettingsToolButton, SIGNAL('clicked()'), self.source1_setup)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        sources = []
        plugins = self.plugman.get_videoinput_plugins()
        for plugin in plugins:
            sources.append(plugin.plugin_object.get_name())

        # Load the combobox with inputs
        self.widget.inputCombobox.clear()
        n = 0
        for i in sources:
            self.widget.inputCombobox.addItem(i)
            if i == self.config.input:
                self.widget.inputCombobox.setCurrentIndex(n)
                self.__enable_source_setup(self.config.input)
            n = n + 1

        vcolour_index = self.widget.videocolourComboBox.findText(self.config.input_type)
        self.widget.videocolourComboBox.setCurrentIndex(vcolour_index)

        # Need to set both the Slider and Spingbox since connections
        # are not yet loaded at this point
        self.widget.framerateSlider.setValue(self.config.framerate)
        self.widget.framerateSpinBox.setValue(self.config.framerate)

        # Finally enable connections
        self.__enable_connections()

    def source1_setup(self):
        plugin = self.plugman.get_plugin_by_name(self.config.input, "VideoInput")
        plugin.plugin_object.get_dialog()

    def set_input(self, input):
        self.config.input = input
        self.config.save()
        self.__enable_source_setup(self.config.input)

    def __enable_source_setup(self, source):
        '''Activates the source setup button if it has configurable settings'''
        plugin = self.plugman.get_plugin_by_name(source, "VideoInput")
        if plugin.plugin_object.get_widget() is not None:
            self.widget.inputSettingsStack.setCurrentIndex(1)
        else:
            self.widget.inputSettingsStack.setCurrentIndex(0)

    def set_input_type(self, input_type):
        self.config.input_type = input_type
        self.config.save()

    def set_framerate(self, framerate):
        self.config.framerate = framerate
        self.config.save()

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.inputLabel.setText(self.gui.app.translate('plugin-video-passthrough', 'Video Input'))
        self.widget.videocolourLabel.setText(self.gui.app.translate('plugin-video-passthrough', 'Colour Format'))
        self.widget.framerateLabel.setText(self.gui.app.translate('plugin-video-passthrough', 'Framerate'))
        self.widget.videoscaleLabel.setText(self.gui.app.translate('plugin-video-passthrough', 'Video Scale'))
