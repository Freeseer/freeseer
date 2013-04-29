'''
freeseer - vga/presentation capture software

Copyright (C) 2011-2013  Free and Open Source Software Learning Centre
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

from freeseer.framework.plugin import IAudioMixer

class AudioPassthrough(IAudioMixer):
    name = "Audio Passthrough"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    input1 = None
    widget = None
    
    def get_audiomixer_bin(self):
        bin = gst.Bin()
        
        audiomixer = gst.element_factory_make("adder", "audiomixer")
        bin.add(audiomixer)
        
        # Setup ghost pad
        sinkpad = audiomixer.get_pad("sink%d")
        sink_ghostpad = gst.GhostPad("sink", sinkpad)
        bin.add_pad(sink_ghostpad)
        
        srcpad = audiomixer.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)
        
        return bin
        
    def get_inputs(self):
        inputs = [(self.input1, 0)]
        return inputs
        
    def load_inputs(self, player, mixer, inputs):
        # Load inputs
        input = inputs[0]
        player.add(input)
        input.link(mixer)


    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.input1 = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Input")
        except ConfigParser.NoSectionError:
            self.input1 = self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Input", self.input1)
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Audio Input")
            self.combobox = QtGui.QComboBox()
            self.combobox.setMinimumWidth(150)
            layout.addRow(self.label, self.combobox)
            
            self.widget.connect(self.combobox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_input)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        sources = []
        plugins = self.plugman.get_audioinput_plugins()
        for plugin in plugins:
            sources.append(plugin.plugin_object.get_name())
                
        # Load the combobox with inputs
        self.combobox.clear()
        n = 0
        for i in sources:
            self.combobox.addItem(i)
            if i == self.input1:
                self.combobox.setCurrentIndex(n)
            n = n +1

    def set_input(self, input):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Input", input)
