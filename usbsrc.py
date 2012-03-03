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

class USBSrc(IVideoInput):
    name = "USB Source"
    device = "/dev/video0"
    device_list = []
    input_type = "video/x-raw-rgb"
    framerate = 10
    resolution = "NOSCALE"
    
    def __init__(self):
        IVideoInput.__init__(self)
        
        #
        # Detect available devices
        #
        i = 0
        path = "/dev/video"
        devpath = path + str(i)
        
        while os.path.exists(devpath):
            self.device_list.append(devpath)
            i=i+1
            devpath=path + str(i)
    
    def get_videoinput_bin(self):
        """
        Return the video input object in gstreamer bin format.
        """
        bin = gst.Bin() # Do not pass a name so that we can load this input more than once.
        
        videosrc = gst.element_factory_make("v4l2src", "videosrc")
        videosrc.set_property("device", self.device)
        bin.add(videosrc)
        
        
        # Video Rate
        videorate = gst.element_factory_make("videorate", "videorate")
        bin.add(videorate)
        videorate_cap = gst.element_factory_make("capsfilter",
                                                    "video_rate_cap")
        videorate_cap.set_property("caps",
                        gst.caps_from_string("%s, framerate=%d/1" % (self.input_type, self.framerate)))
        bin.add(videorate_cap)
        # --- End Video Rate
        
        
        # Video Scaler (Resolution)
        videoscale = gst.element_factory_make("videoscale", "videoscale")
        bin.add(videoscale)
        videoscale_cap = gst.element_factory_make("capsfilter",
                                                    "videoscale_cap")
        if self.resolution != "NOSCALE":
            videoscale_cap.set_property('caps',
                                        gst.caps_from_string('%s, width=640, height=480' % (self.input_type)))
        bin.add(videoscale_cap)
        # --- End Video Scaler
        
        
        # Setup ghost pad
        pad = videoscale_cap.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)
        
        gst.element_link_many(videosrc, videorate, videorate_cap, videoscale, videoscale_cap)
        
        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        self.device = self.plugman.plugmanc.readOptionFromPlugin("VideoInput", self.name, "Video Device")
        self.input_type = self.plugman.plugmanc.readOptionFromPlugin("VideoInput", self.name, "Input Type")
        self.framerate = self.plugman.plugmanc.readOptionFromPlugin("VideoInput", self.name, "Framerate")
        self.resolution = self.plugman.plugmanc.readOptionFromPlugin("VideoInput", self.name, "Resolution")
        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Video Device")
            self.combobox = QtGui.QComboBox()
            layout.addRow(self.label, self.combobox)
            
            self.videocolourLabel = QtGui.QLabel(self.widget.tr("Colour Format"))
            self.videocolourComboBox = QtGui.QComboBox()
            self.videocolourComboBox.addItem("video/x-raw-rgb")
            self.videocolourComboBox.addItem("video/x-raw-yuv")
            self.videocolourComboBox.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
            layout.addRow(self.videocolourLabel, self.videocolourComboBox)
            
            self.framerateLabel = QtGui.QLabel("Framerate")
            self.framerateLayout = QtGui.QHBoxLayout()
            self.framerateSlider = QtGui.QSlider()
            self.framerateSlider.setOrientation(QtCore.Qt.Horizontal)
            self.framerateSlider.setMinimum(0)
            self.framerateSlider.setMaximum(60)
            self.framerateSpinBox = QtGui.QSpinBox()
            self.framerateSpinBox.setMinimum(0)
            self.framerateSpinBox.setMaximum(60)
            self.framerateLayout.addWidget(self.framerateSlider)
            self.framerateLayout.addWidget(self.framerateSpinBox)
            layout.addRow(self.framerateLabel, self.framerateLayout)
            
            self.videoscaleLabel = QtGui.QLabel("Video Scale")
            self.videoscaleComboBox = QtGui.QComboBox()
            self.videoscaleComboBox.addItem("NOSCALE")
            self.videoscaleComboBox.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
            layout.addRow(self.videoscaleLabel, self.videoscaleComboBox)
            
            # Connections
            self.widget.connect(self.combobox, 
                                QtCore.SIGNAL('currentIndexChanged(const QString&)'), 
                                self.set_device)
            self.widget.connect(self.framerateSlider,
                                QtCore.SIGNAL("valueChanged(int)"),
                                self.framerateSpinBox.setValue)
            self.widget.connect(self.framerateSpinBox,
                                QtCore.SIGNAL("valueChanged(int)"),
                                self.framerateSlider.setValue)
            self.widget.connect(self.videocolourComboBox,
                                QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                                self.set_videocolour)
            self.widget.connect(self.framerateSlider,
                                QtCore.SIGNAL("valueChanged(int)"),
                                self.set_framerate)
            self.widget.connect(self.framerateSpinBox,
                                QtCore.SIGNAL("valueChanged(int)"),
                                self.set_framerate)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.device = self.plugman.plugmanc.readOptionFromPlugin("VideoInput", self.name, "Video Device")
            self.input_type = self.plugman.plugmanc.readOptionFromPlugin("VideoInput", self.name, "Input Type")
            self.framerate = int(self.plugman.plugmanc.readOptionFromPlugin("VideoInput", self.name, "Framerate"))
            self.resolution = self.plugman.plugmanc.readOptionFromPlugin("VideoInput", self.name, "Resolution")
        except ConfigParser.NoSectionError:
            self.plugman.plugmanc.registerOptionFromPlugin("VideoInput", self.name, "Video Device", self.device)
            self.plugman.plugmanc.registerOptionFromPlugin("VideoInput", self.name, "Input Type", self.input_type)
            self.plugman.plugmanc.registerOptionFromPlugin("VideoInput", self.name, "Framerate", self.framerate)
            self.plugman.plugmanc.registerOptionFromPlugin("VideoInput", self.name, "Resolution", self.resolution)
                
        # Load the combobox with inputs
        self.combobox.clear()
        n = 0
        for i in self.device_list:
            self.combobox.addItem(i)
            if i == self.device:
                self.combobox.setCurrentIndex(n)
            n = n +1
            
        vcolour_index = self.videocolourComboBox.findText(self.input_type)
        self.videocolourComboBox.setCurrentIndex(vcolour_index)
        
        self.framerateSlider.setValue(self.framerate)
            
    def set_device(self, device):
        self.plugman.plugmanc.registerOptionFromPlugin("VideoInput", self.name, "Video Device", device)
        self.plugman.save()

    def set_videocolour(self, input_type):
        self.plugman.plugmanc.registerOptionFromPlugin("VideoInput", self.name, "Input Type", input_type)
        self.plugman.save()
        
    def set_framerate(self, framerate):
        self.plugman.plugmanc.registerOptionFromPlugin("VideoInput", self.name, "Framerate", framerate)
        self.plugman.save()
