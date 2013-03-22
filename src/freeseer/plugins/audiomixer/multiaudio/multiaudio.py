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

class multiaudio(IAudioMixer):
    name = 'Multiple Audio Inputs'
    os = ['linux', 'linux2', 'win32', 'cygwin', 'darwin']
    input1 = None
    input2 = None
    widget = None
    
    def get_audiomixer_bin(self):
        bin = gst.Bin()
        
        audiomixer = gst.element_factory_make('adder', 'audiomixer')
        bin.add(audiomixer)
        
        # ghost pads
        sinkpad = audiomixer.get_pad('sink%d')
        sink_ghostpad = gst.GhostPad('sink', sinkpad)
        bin.add_padd(sink_ghostpad)
        
        srcpad = audiomixer.get_ad('src')
        src_ghostpad = gst.GhostPad('src', srcpad)
        bin.add_pad(src_ghostpad)
        
        return bin

    def get_inputs(self):
        inputs = [self.input1, self.input2]
        return inputs
    
    def load_inputs(self, player, mixer, inputs):
        input1 = inputs[0]
        player.add(input1)
        input1.link(mixer)
        
        input2 = inputs[2]
        player.add(input2)
        input2.link(mixer)
        
    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.input1 = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 1')
            self.input2 = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), 'Audio Input 2')
        except ConfigParser.NoSectionError:
            
            
    
    