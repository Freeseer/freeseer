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
pygst.require('0.10')
import gst
from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IAudioMixer

class MultiAudio(IAudioMixer):
    name = 'Multiple Audio Inputs'
    os = ['linux', 'linux2', 'win32', 'cygwin', 'darwin']
    input1 = "Pulse Audio Source" #None
    input2 = "ALSA Source" #None
    widget = None
    
    def get_audiomixer_bin(self):
        mixerbin = gst.Bin()
        
        audiomixer = gst.element_factory_make('adder', 'audiomixer')
        mixerbin.add(audiomixer)
        
        # ghost pads
        sinkpad1 = audiomixer.get_pad('sink%d')
        sink_ghostpad1 = gst.GhostPad('sink1', sinkpad1)
        mixerbin.add_pad(sink_ghostpad1)
        
        sinkpad2 = audiomixer.get_pad('sink%d')
        sink_ghostpad2 = gst.GhostPad('sink2', sinkpad2)
        mixerbin.add_pad(sink_ghostpad2)
        
        srcpad = audiomixer.get_pad('src')
        src_ghostpad = gst.GhostPad('src', srcpad)
        mixerbin.add_pad(src_ghostpad)
        
        return mixerbin

    def get_inputs(self):
        inputs = [self.input1, self.input2]
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
        except ConfigParser.NoSectionError:
            self.input1 = self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 1', self.input1)
            self.input2 = self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 2', self.input2)
    
    def get_widget(self):
        if self.widget is None:
            #TODO
            pass
        
        return self.widget
    
    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        #TODO widget
        
    def __set_input1(self, input1):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 1', self.input1)
        
    def __set_input2(self, input2):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 2', self.input2)
        
    def get_properties(self):
        return ['Input1', 'Input2']
    
    def get_property_value(self, p):
        if p == 'Input1':
            return self.input1
        elif p == 'Input2':
            return self.input2
        else:
            return "There's no property with such name"
        
    def set_property_value(self, p, value):
        if value not in self.plugman.get_audioinput_plugins():
            print "Choose an available Input"
            #TODO List available options
            return
            
        if p == 'Input1':
            self.__set_input1(value)
        elif p == 'Input2':
            self.__set_input2(value)
        else:
            return "Error: There's no property with such name"
        
            
            
    
    