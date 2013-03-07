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
import os

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoInput

class FirewireSrc(IVideoInput):
    name = "Firewire Source"
    os = ["linux", "linux2"]
    device = "/dev/fw1"
    device_list = []
    
    def __init__(self):
        IVideoInput.__init__(self)
        
        #
        # Detect available devices
        #
        i = 1
        path = "/dev/fw"
        devpath = path + str(i)
        
        while os.path.exists(devpath):
            self.device_list.append(devpath)
            i=i+1
            devpath=path + str(i)
    
    def get_videoinput_bin(self):
        bin = gst.Bin() # Do not pass a name so that we can load this input more than once.

        videosrc = gst.element_factory_make("dv1394src", "videosrc")
        dv1394q1 =  gst.element_factory_make('queue', 'dv1394q1')
        dv1394dvdemux =  gst.element_factory_make('dvdemux', 'dv1394dvdemux')
        dv1394q2 =  gst.element_factory_make('queue', 'dv1394q2')
        dv1394dvdec =  gst.element_factory_make('dvdec', 'dv1394dvdec')
        
        # Add Elements
        bin.add(videosrc)
        bin.add(dv1394q1)
        bin.add(dv1394dvdemux)
        bin.add(dv1394q2)
        bin.add(dv1394dvdec)
        
        # Link Elements
        videosrc.link(dv1394q1)
        dv1394q1.link(dv1394dvdemux)
        dv1394dvdemux.link(dv1394q2)
        dv1394q2.link(dv1394dvdec)
        
        # Setup ghost pad
        pad = dv1394dvdec.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)
        
        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.device = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Video Device")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Device", self.device)
        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Video Device")
            self.combobox = QtGui.QComboBox()
            layout.addRow(self.label, self.combobox)
            
            # Connections
            self.widget.connect(self.combobox, 
                                QtCore.SIGNAL('currentIndexChanged(const QString&)'), 
                                self.set_device)
                        
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
                
        # Load the combobox with inputs
        self.combobox.clear()
        n = 0
        for i in self.device_list:
            self.combobox.addItem(i)
            if i == self.device:
                self.combobox.setCurrentIndex(n)
            n = n +1
            
    def set_device(self, device):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Device", device)
