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
Picture-In-Picture
------------------

A video mixer plugin which takes 2 video sources and creates a
Picture-In-Picture mode.

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


class PictureInPictureConfig(Config):
    """Configuration class for PIP plugin."""
    main = options.StringOption("Video Test Source")
    pip = options.StringOption("Video Test Source")


class PictureInPicture(IVideoMixer):
    name = "Picture-In-Picture"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    widget = None
    CONFIG_CLASS = PictureInPictureConfig

    def get_videomixer_bin(self):
        bin = gst.Bin()

        videomixer = gst.element_factory_make("videomixer", "videomixer")
        bin.add(videomixer)

        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)
        videomixer.link(colorspace)

        # Picture-In-Picture
        videobox = gst.element_factory_make("videobox", "videobox")
        bin.add(videobox)

        videobox.link(videomixer)

        videobox2 = gst.element_factory_make("videobox", "videobox2")
        bin.add(videobox2)

        videobox2.set_property("alpha", 0.6)
        videobox2.set_property("border-alpha", 0)
        videobox2.set_property("top", -20)
        videobox2.set_property("left", -25)

        videobox2.link(videomixer)

        # Setup ghost pad
        sinkpad = videobox.get_pad("sink")
        sink_ghostpad = gst.GhostPad("sink_main", sinkpad)
        bin.add_pad(sink_ghostpad)

        pip_sinkpad = videobox2.get_pad("sink")
        pip_ghostpad = gst.GhostPad("sink_pip", pip_sinkpad)
        bin.add_pad(pip_ghostpad)

        srcpad = colorspace.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)

        return bin

    def get_inputs(self):
        inputs = [(self.config.main, 0), (self.config.pip, 1)]
        return inputs

    def load_inputs(self, player, mixer, inputs):
        # Load main source
        input1 = inputs[0]

        # Create videoscale element in order to scale to dimensions not supported by camera
        mainsrc_scale = gst.element_factory_make("videoscale", "mainsrc_scale")

        # Create ffmpegcolorspace element to convert from what camera supports to rgb
        mainsrc_colorspace = gst.element_factory_make("ffmpegcolorspace", "mainsrc_colorspace")

        # Create capsfilter for limiting to x-raw-rgb pixel video format and setting dimensions
        mainsrc_capsfilter = gst.element_factory_make("capsfilter", "mainsrc_capsfilter")
        mainsrc_capsfilter.set_property('caps',
                        gst.caps_from_string('video/x-raw-rgb, width=640, height=480'))

        mainsrc_elements = [input1, mainsrc_scale, mainsrc_capsfilter, mainsrc_colorspace]

        # Add elements to player in list order
        map(lambda element: player.add(element), mainsrc_elements)

        # Link elements in a specific order
        input1.link(mainsrc_scale)
        mainsrc_scale.link(mainsrc_capsfilter)
        mainsrc_capsfilter.link(mainsrc_colorspace)

        # Link colorspace element to sink pad for pixel format conversion
        srcpad = mainsrc_colorspace.get_pad("src")
        sinkpad = mixer.get_pad("sink_main")
        srcpad.link(sinkpad)

        # Load the secondary source
        input2 = inputs[1]

        # Create gst elements as above, but set smaller dimensions
        pipsrc_scale = gst.element_factory_make("videoscale", "pipsrc_scale")
        pipsrc_colorspace = gst.element_factory_make("ffmpegcolorspace", "pipsrc_colorspace")
        pipsrc_capsfilter = gst.element_factory_make("capsfilter", "pipsrc_capsfilter")
        pipsrc_capsfilter.set_property('caps',
                        gst.caps_from_string('video/x-raw-rgb, width=200, height=150'))

        pipsrc_elements = [input2, pipsrc_scale, pipsrc_capsfilter, pipsrc_colorspace]

        #Add elements to player in list order
        map(lambda element: player.add(element), pipsrc_elements)

        # Link elements in specific order
        input2.link(pipsrc_scale)
        pipsrc_scale.link(pipsrc_capsfilter)
        pipsrc_capsfilter.link(pipsrc_colorspace)

        # Link colorspace element to sink pad for pixel format conversion
        srcpad = pipsrc_colorspace.get_pad("src")
        sinkpad = mixer.get_pad("sink_pip")
        srcpad.link(sinkpad)

    def get_widget(self):

        if self.widget is None:
            self.widget = widget.ConfigWidget()

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.mainInputComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.set_maininput)
        self.widget.connect(self.widget.mainInputSetupButton, SIGNAL('clicked()'), self.open_mainInputSetup)
        self.widget.connect(self.widget.pipInputComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.set_pipinput)
        self.widget.connect(self.widget.pipInputSetupButton, SIGNAL('clicked()'), self.open_pipInputSetup)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        sources = []
        plugins = self.plugman.get_videoinput_plugins()
        for plugin in plugins:
            sources.append(plugin.plugin_object.get_name())

        box_config_pairs = [
            (self.widget.mainInputComboBox, self.config.main, self.__enable_maininput_setup),
            (self.widget.pipInputComboBox, self.config.pip, self.__enable_pipinput_setup),
        ]

        # Load combo boxes with inputs:
        for combo_box, config, setup in box_config_pairs:
            combo_box.clear()
            for i, source in enumerate(sources):
                combo_box.addItem(source)
                if source == config:  # Find the current input source and set it
                    combo_box.setCurrentIndex(i)
                    setup(config)

        # Finally enable connections
        self.__enable_connections()

    ###
    ### Main Input Functions
    ###

    def set_maininput(self, input):
        self.config.main = input
        self.config.save()
        self.__enable_maininput_setup(self.config.main)

    def open_mainInputSetup(self):
        plugin_name = str(self.widget.mainInputComboBox.currentText())
        plugin = self.plugman.get_plugin_by_name(plugin_name, "VideoInput")
        plugin.plugin_object.set_instance(0)
        plugin.plugin_object.get_dialog()

    def __enable_maininput_setup(self, source):
        '''Activates the source setup button if it has configurable settings'''
        plugin = self.plugman.get_plugin_by_name(source, "VideoInput")
        if plugin.plugin_object.get_widget() is not None:
            self.widget.mainInputSetupStack.setCurrentIndex(1)
        else:
            self.widget.mainInputSetupStack.setCurrentIndex(0)

    ###
    ### PIP Functions
    ###

    def set_pipinput(self, input):
        self.config.pip = input
        self.config.save()
        self.__enable_pipinput_setup(self.config.pip)

    def open_pipInputSetup(self):
        plugin_name = str(self.widget.pipInputComboBox.currentText())
        plugin = self.plugman.get_plugin_by_name(plugin_name, "VideoInput")
        plugin.plugin_object.set_instance(1)
        plugin.plugin_object.get_dialog()

    def __enable_pipinput_setup(self, source):
        '''Activates the source setup button if it has configurable settings'''
        plugin = self.plugman.get_plugin_by_name(source, "VideoInput")
        if plugin.plugin_object.get_widget() is not None:
            self.widget.pipInputSetupStack.setCurrentIndex(1)
        else:
            self.widget.pipInputSetupStack.setCurrentIndex(0)

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.mainInputLabel.setText(self.gui.app.translate('plugin-pip', 'Main Source'))
        self.widget.pipInputLabel.setText(self.gui.app.translate('plugin-pip', 'PIP Source'))
