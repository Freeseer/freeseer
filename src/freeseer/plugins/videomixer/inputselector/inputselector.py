'''
freeseer - vga/presentation capture software

Copyright (C) 2011  Free and Open Source Software Learning Centre
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

from freeseer.framework.plugin import IVideoMixer

class InputSelector(IVideoMixer):
    name = "Input Selector"
    input1 = None
    widget = None
    
    def get_videomixer_bin(self):
        bin = gst.Bin(self.name)
        
        videomixer = gst.element_factory_make("input-selector", "videomixer")
        bin.add(videomixer)
        
        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)
        
        # Setup ghost pad
        sinkpad = videomixer.get_pad("sink%d")
        sink_ghostpad = gst.GhostPad("sink", sinkpad)
        bin.add_pad(sink_ghostpad)
        
        srcpad = colorspace.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)
        
        gst.element_link_many(videomixer, colorspace)
        
        return bin
    
    def set_input(self, input1):
        self.input1 = input1
        
    def get_inputs(self):
        inputs = [self.input1]
        return inputs
        
    def load_inputs(self, player, mixer, inputs):
        # Load inputs
        input = inputs[0]
        player.add(input)
        input.link(mixer)
   
    def load_config(self, plugman):
        self.plugman = plugman
        self.input1 = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "Input 1")
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Input 1")
            self.combobox = QtGui.QComboBox()
            layout.addRow(self.label, self.combobox)
            
            self.widget.connect(self.combobox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_input1)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.input1 = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "Input 1")
        except ConfigParser.NoSectionError:
            self.input1 = self.plugman.plugmanc.registerOptionFromPlugin("VideoMixer", self.name, "Input 1", None)
        
        sources = []
        plugins = self.plugman.plugmanc.getPluginsOfCategory("VideoInput")
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

    def set_input1(self, input):
        self.plugman.plugmanc.registerOptionFromPlugin("VideoMixer", self.name, "Input 1", input)
        self.plugman.save()
