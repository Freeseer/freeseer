'''
freeseer - vga/presentation capture software

Copyright (C) 2011-2012  Free and Open Source Software Learning Centre
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
import os

import pygst
pygst.require("0.10")
import gst

import Xlib.display

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoInput

class DesktopLinuxSrc(IVideoInput):
    name = "Desktop-Linux Source"
    os = ["linux2"]
    
    # ximagesrc
    screen = 0
    
    def get_videoinput_bin(self):
        """
        Return the video input object in gstreamer bin format.
        """
        bin = gst.Bin() # Do not pass a name so that we can load this input more than once.
        
        videosrc = gst.element_factory_make("ximagesrc", "videosrc")
        bin.add(videosrc)
        
        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)
        videosrc.link(colorspace)
        
        # Setup ghost pad
        pad = colorspace.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)
        
        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.screen = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Screen")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Screen", self.screen)
        except TypeError:
            # Temp fix for issue where reading audio_quality the 2nd time causes TypeError.
            pass
        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.screenLabel = QtGui.QLabel("Screen")
            self.screenSpinBox = QtGui.QSpinBox()
            layout.addRow(self.screenLabel, self.screenSpinBox)
            
            # Connections
            self.widget.connect(self.screenSpinBox, QtCore.SIGNAL('valueChanged(int)'), self.set_screen)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
                
        display = Xlib.display.Display()
        self.screenSpinBox.setMaximum(display.screen_count() - 1) # minus 1 since we like to start count at 0
            
    def set_screen(self, screen):
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Screen", screen)
        self.plugman.save()
