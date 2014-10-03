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
Multiple Audio Plugin
---------------------

An audio mixer plugin that combines 2 audio sources into a single output.

@author: Aaron Brubacher
'''

# python-libs
try:  # Import using Python3 module name
    import configparser
except ImportError:
    import ConfigParser as configparser

# GStreamer
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin import IAudioMixer

# .freeseer-plugin custom
import widget


class MultiAudio(IAudioMixer):
    name = 'Multiple Audio Inputs'
    os = ['linux', 'linux2', 'win32', 'cygwin', 'darwin']
    input1 = None
    input2 = None
    widget = None

    def get_audiomixer_bin(self):
        mixerbin = Gst.Bin()

        audiomixer = Gst.ElementFactory.make('adder', 'audiomixer')
        mixerbin.add(audiomixer)

        # ghost pads
        sinkpad1 = audiomixer.get_static_pad('sink%d')
        sink_ghostpad1 = Gst.GhostPad.new('sink1', sinkpad1)
        mixerbin.add_pad(sink_ghostpad1)

        sinkpad2 = audiomixer.get_static_pad('sink%d')
        sink_ghostpad2 = Gst.GhostPad.new('sink2', sinkpad2)
        mixerbin.add_pad(sink_ghostpad2)

        srcpad = audiomixer.get_static_pad('src')
        src_ghostpad = Gst.GhostPad.new('src', srcpad)
        mixerbin.add_pad(src_ghostpad)

        return mixerbin

    def get_inputs(self):
        inputs = [(self.input1, 0), (self.input2, 1)]
        return inputs

    def load_inputs(self, player, mixer, inputs):
        input1 = inputs[0]
        player.add(input1)
        input1.link(mixer)

        input2 = inputs[1]
        player.add(input2)
        input2.link(mixer)

    def load_config(self, plugman):
        self.plugman = plugman

        try:
            self.input1 = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 1')
            self.input2 = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 2')
        except configparser.NoSectionError, configparser.NoOptionError:
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 1', self.input1)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 2', self.input2)

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.source1_combobox, SIGNAL('currentIndexChanged(const QString&)'), self.set_input1)
        self.widget.connect(self.widget.source1_button, SIGNAL('clicked()'), self.source1_setup)
        self.widget.connect(self.widget.source2_combobox, SIGNAL('currentIndexChanged(const QString&)'), self.set_input2)
        self.widget.connect(self.widget.source2_button, SIGNAL('clicked()'), self.source2_setup)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        plugins = self.plugman.get_audioinput_plugins()
        self.widget.source1_combobox.clear()
        self.widget.source2_combobox.clear()
        for i, source in enumerate(plugins):
            name = source.plugin_object.get_name()
            self.widget.source1_combobox.addItem(name)
            if self.input1 == name:
                self.widget.source1_combobox.setCurrentIndex(i)
                self.__enable_source1_setup(self.input1)
            self.widget.source2_combobox.addItem(name)
            if self.input2 == name:
                self.widget.source2_combobox.setCurrentIndex(i)
                self.__enable_source2_setup(self.input2)

        # Finally enable connections
        self.__enable_connections()

    ###
    ### Source 1
    ###

    def source1_setup(self):
        plugin_name = str(self.widget.source1_combobox.currentText())
        plugin = self.plugman.get_plugin_by_name(plugin_name, "AudioInput")
        plugin.plugin_object.set_instance(0)
        plugin.plugin_object.get_dialog()

    def set_input1(self, input1):
        self.input1 = input1
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Input 1", input1)
        self.__enable_source1_setup(self.input1)

    def __enable_source1_setup(self, source):
        '''Activates the source setup button if it has configurable settings'''
        plugin = self.plugman.get_plugin_by_name(source, "AudioInput")
        if plugin.plugin_object.get_widget() is not None:
            self.widget.source1_stack.setCurrentIndex(1)
        else:
            self.widget.source1_stack.setCurrentIndex(0)

    ###
    ### Source 2
    ###

    def source2_setup(self):
        plugin_name = str(self.widget.source2_combobox.currentText())
        plugin = self.plugman.get_plugin_by_name(plugin_name, "AudioInput")
        plugin.plugin_object.set_instance(1)
        plugin.plugin_object.get_dialog()

    def set_input2(self, input2):
        self.input2 = input2
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Input 2", input2)
        self.__enable_source2_setup(self.input2)

    def __enable_source2_setup(self, source):
        '''Activates the source setup button if it has configurable settings'''
        plugin = self.plugman.get_plugin_by_name(source, "AudioInput")
        if plugin.plugin_object.get_widget() is not None:
            self.widget.source2_stack.setCurrentIndex(1)
        else:
            self.widget.source2_stack.setCurrentIndex(0)

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.source1_label.setText(self.gui.app.translate('plugin-multiaudio', 'Source 1'))
        self.widget.source2_label.setText(self.gui.app.translate('plugin-multiaudio', 'Source 2'))
