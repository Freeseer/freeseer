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

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoMixer

class VideoPassthrough(IVideoMixer):
    name = "Video Passthrough"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    input1 = None
    widget = None
    
    # VideoPassthrough variables
    input_type = "video/x-raw-rgb"
    framerate = 30
    resolution = "NOSCALE"
    
    def get_videomixer_bin(self):
        bin = gst.Bin(self.name)
        
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
        
        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)
        
        gst.element_link_many(videorate, videorate_cap, videoscale, videoscale_cap, colorspace)
        
        # Setup ghost pad
        sinkpad = videorate.get_pad("sink")
        sink_ghostpad = gst.GhostPad("sink", sinkpad)
        bin.add_pad(sink_ghostpad)
        
        srcpad = colorspace.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)
        
        return bin
    
    def get_inputs(self):
        inputs = [self.input1]
        return inputs
        
    def load_inputs(self, player, mixer, inputs):
        # Load source
        input = inputs[0]
        player.add(input)
        input.link(mixer)
   
    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.input1 = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Video Input")
            self.input_type = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Input Type")
            self.framerate = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Framerate"))
            self.resolution = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Resolution")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Input", self.input1)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Input Type", self.input_type)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Framerate", self.framerate)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Resolution", self.resolution)
        except TypeError:
            # Temp fix for issue when reading framerate the 2nd time causes TypeError
            pass
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Video Input")
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
            self.widget.connect(self.combobox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_input)
            self.widget.connect(self.framerateSlider, QtCore.SIGNAL("valueChanged(int)"), self.framerateSpinBox.setValue)
            self.widget.connect(self.framerateSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.framerateSlider.setValue)
            self.widget.connect(self.videocolourComboBox, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.set_videocolour)
            self.widget.connect(self.framerateSlider, QtCore.SIGNAL("valueChanged(int)"), self.set_framerate)
            self.widget.connect(self.framerateSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.set_framerate)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        sources = []
        plugins = self.plugman.get_videoinput_plugins()
        for plugin in plugins:
            sources.append(plugin.plugin_object.get_name())
                
        # Load the combobox with inputs
        self.combobox.clear()
        n = 0
        for i in sources:
            self.combobox.addItem(i)
            if i == self.input1:
                self.combobox.setCurrentIndex(n)
            n = n + 1
            
        vcolour_index = self.videocolourComboBox.findText(self.input_type)
        self.videocolourComboBox.setCurrentIndex(vcolour_index)
        
        self.framerateSlider.setValue(self.framerate)

    def set_input(self, input):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Input", input)
        
    def set_videocolour(self, input_type):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Input Type", input_type)
        
    def set_framerate(self, framerate):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Framerate", str(framerate))
        
    def get_properties(self):
        return ['InputType', 'Input1', 'Framerate']
    
    def get_property_value(self, property):
        if property == "InputType":
            return self.input_type
        elif property == "Input1":
            return self.input1
        elif property == "Framerate":    
            return self.framerate
        elif property == "Resolution":
            return self.resolution  
        else:
            return "There's no property with such name"
        
    def set_property_value(self, property, value):
        if(property == "Framerate"):
            try:
                int_value = int(value)
                self.set_framerate(int_value)
            except:
                print "Failed"
        elif(property == "InputType"):
            try:
                self.set_videocolour(value)
            except:
                print "Failed"
        elif(property == "Input1"):
            if(value == "USB"):
                self.set_input("USB Source")
            elif(value == "Firewire"):
                self.set_input("Firewire Source")
            elif(value == "Desktop"):
                self.set_input("Desktop-Linux Source")
            elif(value == "VideoTest"):
                self.set_input("Video Test Source")
            else:
                print "Choose an available Input"
                #TODO List available options     
        else:
            return "Error: There's no property with such name"   
            
