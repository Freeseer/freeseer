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

# python-lib
import ConfigParser
import logging
import sys

# GStreamer modules
import pygst
pygst.require("0.10")
import gst

# PyQt4 modules
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDesktopWidget

# Freeseer modules
from freeseer.framework.plugin import IVideoInput
from freeseer.framework.area_selector import AreaSelector

# .freeseer-plugin custom modules
import widget

log = logging.getLogger(__name__)

class DesktopLinuxSrc(IVideoInput):
    name = "Desktop Source"
    os = ["linux", "linux2", "win32", "cygwin"]
    
    # ximagesrc
    desktop = "Full"
    screen = 0
    window = ""
    
    # Area Select
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    
    def get_videoinput_bin(self):
        """
        Return the video input object in gstreamer bin format.
        """
        bin = gst.Bin() # Do not pass a name so that we can load this input more than once.
        
        videosrc = None
        if sys.platform.startswith("linux"):
            videosrc = gst.element_factory_make("ximagesrc", "videosrc")
            
            # Configure coordinates if we're not recording full desktop
            if self.desktop == "Area":
                videosrc.set_property("startx", self.start_x)
                videosrc.set_property("starty", self.start_y)
                videosrc.set_property("endx", self.end_x)
                videosrc.set_property("endy", self.end_y)
                log.debug('Recording Area start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
                
            if self.desktop == "Window":
                videosrc.set_property("xname", self.window)
            
        elif sys.platform in ["win32", "cygwin"]:
            videosrc = gst.element_factory_make("dx9screencapsrc", "videosrc")
            
            # Configure coordinates if we're not recording full desktop
            if self.desktop == "Area":
                videosrc.set_property("x", self.start_x)
                videosrc.set_property("y", self.start_y)
                videosrc.set_property("width", self.start_x + self.end_x)
                videosrc.set_property("height", self.start_y + self.end_y)
                log.debug('Recording Area start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
                
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
            self.desktop = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Desktop")
            self.screen = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Screen")
            self.window = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Window")
            self.start_x = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "start_x"))
            self.start_y = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "start_y"))
            self.end_x = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "end_x"))
            self.end_y = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "end_y"))
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Desktop", self.desktop)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Screen", self.screen)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Window", self.window)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "start_x", self.start_x)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "start_x", self.start_y)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "end_x", self.end_x)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "end_x", self.end_y)
        except TypeError:
            # Temp fix for issue where reading audio_quality the 2nd time causes TypeError.
            pass
        
    def area_select(self):
        self.area_selector = AreaSelector(self)
        self.area_selector.show()
        self.gui.hide()
        self.widget.window().hide()

    def areaSelectEvent(self, start_x, start_y, end_x, end_y):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "start_x", start_x)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "start_y", start_y)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "end_x", end_x)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "end_y", end_y)
        log.debug('Area selector start: %sx%s end: %sx%s' % (start_x, start_y, end_x, end_y))
        self.gui.show()        
        self.widget.window().show()
        
    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()
            
        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.desktopButton, SIGNAL('clicked()'), self.set_desktop_full)
        self.widget.connect(self.widget.areaButton, SIGNAL('clicked()'), self.set_desktop_area)
        self.widget.connect(self.widget.setAreaButton, SIGNAL('clicked()'), self.area_select)
        self.widget.connect(self.widget.screenSpinBox, SIGNAL('valueChanged(int)'), self.set_screen)

    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        if self.desktop == "Full":
            self.widget.desktopButton.setChecked(True)
        elif self.desktop == "Area":
            self.widget.areaButton.setChecked(True)
        
        # Try to detect how many screens the user has
        # minus 1 since we like to start count at 0
        max_screens = QDesktopWidget().screenCount()
        self.widget.screenSpinBox.setMaximum(max_screens - 1)

        # Finally enable connections
        self.__enable_connections()
            
    def set_screen(self, screen):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Screen", screen)
        
    def set_desktop_full(self):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Desktop", "Full")
        
    def set_desktop_area(self):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Desktop", "Area")
