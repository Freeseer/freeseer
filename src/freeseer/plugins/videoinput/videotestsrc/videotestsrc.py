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

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoInput

class VideoTestSrc(IVideoInput):
    name = "Video Test Source"
    os = ["linux2", "win32", "cygwin", "darwin"]
    
    # variables
    live = False
    pattern = "smpte"
    
    # Patterns
    PATTERNS = ["smpte", "snow", "black", "white", "red", "green", "blue",
                "circular", "blink", "smpte75", "zone-plate", "gamut",
                "chroma-zone-plate", "ball", "smpte100", "bar"]
    
    def get_videoinput_bin(self):
        bin = gst.Bin() # Do not pass a name so that we can load this input more than once.
        
        videosrc = gst.element_factory_make("videotestsrc", "videosrc")
        videosrc.set_property("pattern", self.pattern)
        videosrc.set_property("is-live", self.live)
        bin.add(videosrc)
        
        # Setup ghost pad
        pad = videosrc.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)
        
        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            live = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Live")
            if live == "True": self.live = True
            self.pattern = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Pattern")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Live", self.live)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Pattern", self.pattern)
        except TypeError:
            # Temp fix for issue where reading checkbox the 2nd time causes TypeError.
            pass
        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QVBoxLayout()
            self.widget.setLayout(layout)
            
            #
            # Settings
            #
            
            self.liveCheckBox = QtGui.QCheckBox("Live Source")
            layout.addWidget(self.liveCheckBox)
            
            formWidget = QtGui.QWidget()
            formLayout = QtGui.QFormLayout()
            formWidget.setLayout(formLayout)
            layout.addWidget(formWidget)
            
            self.patternLabel = QtGui.QLabel("Pattern")
            self.patternComboBox = QtGui.QComboBox()
            for i in self.PATTERNS:
                self.patternComboBox.addItem(i)
            
            formLayout.addRow(self.patternLabel, self.patternComboBox)
            
            self.widget.connect(self.liveCheckBox, QtCore.SIGNAL('toggled(bool)'), self.set_live)
            self.widget.connect(self.patternComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_pattern)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        self.liveCheckBox.setChecked(bool(self.live))
        patternIndex = self.patternComboBox.findText(self.pattern)
        self.patternComboBox.setCurrentIndex(patternIndex)

    def set_live(self, checked):
        self.live = checked
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Live", self.live)
        self.plugman.save()
        
    def set_pattern(self, pattern):
        self.pattern = pattern
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Pattern", self.pattern)
        self.plugman.save()
        
    def get_properties(self):
        return ['Live','Pattern']
    
    def get_property_value(self, property):
        if property == 'Live':
            return self.live
        elif property == 'Pattern':
            return self.pattern
        else:
            return "There's no property with such name"
        
    def set_property_value(self, property, value):
        if property == 'Live':
            if(value == "ON"):                
                self.set_live(True)
            elif(value == "OFF"):
                self.set_live(False)
            else:
                return "Please choose one of the acceptable variable values: ON or OFF"
        elif property == "Pattern":
            self.set_pattern(value)            
        else:
            return "Error: There's no property with such name" 
