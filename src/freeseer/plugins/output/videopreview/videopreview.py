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

from freeseer.framework.plugin import IOutput

class VideoPreview(IOutput):
    name = "Video Preview"
    type = IOutput.VIDEO
    recordto = IOutput.OTHER
    
    # Video Preview variables
    previewsink = "autovideosink"
    
    def get_output_bin(self, audio=False, video=True, metadata=None):
        bin = gst.Bin(self.name)
        
        videoqueue = gst.element_factory_make("queue", "videoqueue")
        bin.add(videoqueue)
        
        videosink = gst.element_factory_make(self.previewsink, "videosink")
        bin.add(videosink)
        
        # Setup ghost pad
        pad = videoqueue.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        bin.add_pad(ghostpad)
        
        gst.element_link_many(videoqueue, videosink)
        
        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        try:
            self.previewsink = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Preview Sink")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Preview Sink", self.previewsink)

        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            self.previewLabel = QtGui.QLabel(self.widget.tr("Preview"))
            self.previewComboBox = QtGui.QComboBox()
            self.previewComboBox.addItem("autovideosink")
            self.previewComboBox.addItem("ximagesink")
            self.previewComboBox.addItem("xvimagesink")
            self.previewComboBox.addItem("gconfvideosink")
            
            layout.addRow(self.previewLabel, self.previewComboBox)
            
            self.widget.connect(self.previewComboBox, 
                                QtCore.SIGNAL('currentIndexChanged(const QString&)'), 
                                self.set_previewsink)
            
        return self.widget
    
    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        previewIndex = self.previewComboBox.findText(self.previewsink)
        self.previewComboBox.setCurrentIndex(previewIndex)
            
    def set_previewsink(self, previewsink):
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Preview Sink", previewsink)
        self.plugman.save()