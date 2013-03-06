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
import logging
import sys

import pygst
pygst.require("0.10")
import gst

if sys.platform.startswith("linux"):
    import Xlib.display

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoInput
from freeseer.framework.qt_area_selector import QtAreaSelector

class DesktopLinuxSrc(IVideoInput):
    name = "Desktop Source"
    os = ["linux", "linux2", "win32", "cygwin"]
    
    # ximagesrc
    desktop = "Full"
    screen = 0
    
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
                logging.debug('Recording Area start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
            
        elif sys.platform in ["win32", "cygwin"]:
            videosrc = gst.element_factory_make("dx9screencapsrc", "videosrc")
            
            # Configure coordinates if we're not recording full desktop
            if self.desktop == "Area":
                videosrc.set_property("x", self.start_x)
                videosrc.set_property("y", self.start_y)
                videosrc.set_property("width", self.start_x + self.end_x)
                videosrc.set_property("height", self.start_y + self.end_y)
                logging.debug('Recording Area start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
                
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
            self.start_x = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "start_x"))
            self.start_y = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "start_y"))
            self.end_x = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "end_x"))
            self.end_y = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "end_y"))
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Desktop", self.desktop)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Screen", self.screen)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "start_x", self.start_x)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "start_x", self.start_y)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "end_x", self.end_x)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "end_x", self.end_y)
        except TypeError:
            # Temp fix for issue where reading audio_quality the 2nd time causes TypeError.
            pass
        
    def area_select(self):
        self.area_selector = QtAreaSelector(self)
        self.area_selector.show()
        self.gui.hide()
        self.widget.window().hide()

    def desktopAreaEvent(self, start_x, start_y, end_x, end_y):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "start_x", start_x)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "start_y", start_y)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "end_x", end_x)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "end_y", end_y)
        logging.debug('Area selector start: %sx%s end: %sx%s' % (start_x, start_y, end_x, end_y))
        self.gui.show()        
        self.widget.window().show()
        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.desktopLabel = QtGui.QLabel("Record Desktop")
            self.areaLabel = QtGui.QLabel("Record Region")
            self.desktopButton = QtGui.QRadioButton()
            areaGroup = QtGui.QHBoxLayout()
            self.areaButton = QtGui.QRadioButton()
            self.setAreaButton = QtGui.QPushButton("Set")
            areaGroup.addWidget(self.areaButton)
            areaGroup.addWidget(self.setAreaButton)
            layout.addRow(self.desktopLabel, self.desktopButton)
            layout.addRow(self.areaLabel, areaGroup)
            
            self.screenLabel = QtGui.QLabel("Screen")
            self.screenSpinBox = QtGui.QSpinBox()
            layout.addRow(self.screenLabel, self.screenSpinBox)
            
            # Connections
            self.widget.connect(self.desktopButton, QtCore.SIGNAL('clicked()'), self.set_desktop_full)
            self.widget.connect(self.areaButton, QtCore.SIGNAL('clicked()'), self.set_desktop_area)
            self.widget.connect(self.setAreaButton, QtCore.SIGNAL('clicked()'), self.area_select)
            self.widget.connect(self.screenSpinBox, QtCore.SIGNAL('valueChanged(int)'), self.set_screen)
            self.widget.connect(self.setAreaButton, QtCore.SIGNAL('clicked()'), self.area_select)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        if self.desktop == "Full":
            self.desktopButton.setChecked(True)
        elif self.desktop == "Area":
            self.areaButton.setChecked(True)
        
        # Xlib is only available on linux
        if sys.platform.startswith("linux"):
            display = Xlib.display.Display()
            self.screenSpinBox.setMaximum(display.screen_count() - 1) # minus 1 since we like to start count at 0
            
    def set_screen(self, screen):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Screen", screen)
        
    def set_desktop_full(self):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Desktop", "Full")
        
    def set_desktop_area(self):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Desktop", "Area")
