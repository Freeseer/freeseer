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


import pygst
import ConfigParser
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IOutput

class AudioFeedback(IOutput):
    name = "AudioFeedback"
    type = IOutput.AUDIO
    recordto = IOutput.OTHER
    
    # variables
    feedbacksink = "autoaudiosink"
    
    def get_output_bin(self, audio=True, video=False, metadata=None):
        bin = gst.Bin(self.name)
        
        audioqueue = gst.element_factory_make("queue", "audioqueue")
        bin.add(audioqueue)
        
        audiosink = gst.element_factory_make(self.feedbacksink, "audiosink")
        bin.add(audiosink)
        
        # Setup ghost pad
        pad = audioqueue.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        bin.add_pad(ghostpad)
        
        gst.element_link_many(audioqueue, audiosink)
        
        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        try:
            self.feedbacksink = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Audio Feedback Sink")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Audio Feedback Sink", self.feedbacksink)
        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            self.feedbackLabel = QtGui.QLabel(self.widget.tr("Feedback"))
            self.feedbackComboBox = QtGui.QComboBox()
            self.feedbackComboBox.addItem("autoaudiosink")
            self.feedbackComboBox.addItem("alsasink")
            
            layout.addRow(self.feedbackLabel, self.feedbackComboBox)
            
            self.widget.connect(self.feedbackComboBox, 
                                QtCore.SIGNAL('currentIndexChanged(const QString&)'), 
                                self.set_feedbacksink)
            
        return self.widget
    
    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        feedbackIndex = self.feedbackComboBox.findText(self.feedbacksink)
        self.feedbackComboBox.setCurrentIndex(feedbackIndex)
            
    def set_feedbacksink(self, feedbacksink):
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Audio Feedback Sink", feedbacksink)
        self.plugman.save()
        
    def get_properties(self):
        return ['FeedbackSink']
    
    def get_property_value(self, property):
        if property == "FeedbackSink":
            return self.feedbacksink
        else:
            return "There's no property with such name"
        
    def set_property_value(self, property, value):
        if(property == "FeedbackSink"):
            self.set_feedbacksink(value)          
        else:
            return "Error: There's no property with such name" 
