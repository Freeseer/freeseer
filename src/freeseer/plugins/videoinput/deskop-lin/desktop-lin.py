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
http://wiki.github.com/fosslc/freeseer/

@author: Thanh Ha
'''

import ConfigParser
import os

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoInput

class DesktopLinuxSrc(IVideoInput):
    name = "Desktop-Linux Source"
    
    def get_videoinput_bin(self):
        """
        Return the video input object in gstreamer bin format.
        """
        bin = gst.Bin(self.name)
        
        videosrc = gst.element_factory_make("ximagesrc", "videosrc")
        bin.add(videosrc)
        
        videorate = gst.element_factory_make("videorate", "videorate")
        bin.add(videorate)
        videorate_cap = gst.element_factory_make("capsfilter",
                                                    "video_rate_cap")
        videorate_cap.set_property("caps",
                        gst.caps_from_string("video/x-raw-rgb, framerate=30/1"))
        bin.add(videorate_cap)
        
        videoscale = gst.element_factory_make("videoscale", "videoscale")
        bin.add(videoscale)
        videoscale_cap = gst.element_factory_make("capsfilter",
                                                    "videoscale_cap")
        videoscale_cap.set_property('caps',
                gst.caps_from_string('video/x-raw-rgb, width=640, height=480'))
        bin.add(videoscale_cap)
        
        # Setup ghost pad
        pad = videoscale_cap.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)
        
        gst.element_link_many(videosrc, videorate, videorate_cap, videoscale, videoscale_cap)
        
        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
        return self.widget

    def widget_load_config(self, plugman):
        self.plugman = plugman
        
        try:
            pass
        except ConfigParser.NoSectionError:
            pass
