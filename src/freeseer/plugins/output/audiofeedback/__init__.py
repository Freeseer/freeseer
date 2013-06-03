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

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin import IOutput

# .freeseer-plugin
import widget

class AudioFeedback(IOutput):
    name = "Audio Feedback"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    type = IOutput.AUDIO
    recordto = IOutput.OTHER
    
    # variables
    feedbacksink = "autoaudiosink"
    
    def get_output_bin(self, audio=True, video=False, metadata=None):
        bin = gst.Bin()
        
        audioqueue = gst.element_factory_make("queue", "audioqueue")
        bin.add(audioqueue)
        
        audiosink = gst.element_factory_make(self.feedbacksink, "audiosink")
        bin.add(audiosink)
        
        # Setup ghost pad
        pad = audioqueue.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        bin.add_pad(ghostpad)
        
        audioqueue.link(audiosink)
        
        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        try:
            self.feedbacksink = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Feedback Sink")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Feedback Sink", self.feedbacksink)
        
    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()
            
            self.widget.connect(self.widget.feedbackComboBox, 
                                SIGNAL('currentIndexChanged(const QString&)'), 
                                self.set_feedbacksink)
            
        return self.widget
    
    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        feedbackIndex = self.widget.feedbackComboBox.findText(self.feedbacksink)
        self.widget.feedbackComboBox.setCurrentIndex(feedbackIndex)
            
    def set_feedbacksink(self, feedbacksink):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Feedback Sink", feedbacksink)
