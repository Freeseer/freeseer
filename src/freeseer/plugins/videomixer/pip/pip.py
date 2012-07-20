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

from freeseer.framework.plugin import IVideoMixer

class PictureInPicture(IVideoMixer):
    name = "Picture-In-Picture"
    input1 = None # Main Source
    input2 = None # PIP Source
    widget = None
    
    def get_videomixer_bin(self):
        bin = gst.Bin(self.name)
        
        videomixer = gst.element_factory_make("videomixer", "videomixer")
        bin.add(videomixer)
        
        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)
        videomixer.link(colorspace)
        
        # Picture-In-Picture
        videobox = gst.element_factory_make("videobox", "videobox")
        bin.add(videobox)
        
        videobox.link(videomixer)
        
        
        videobox2 = gst.element_factory_make("videobox", "videobox2")
        bin.add(videobox2)
        
        videobox2.set_property("alpha", 0.6)
        videobox2.set_property("border-alpha", 0)
        videobox2.set_property("top", -20)
        videobox2.set_property("left", -25)
        
        videobox2.link(videomixer) 
        
        
        # Setup ghost pad
        sinkpad = videobox.get_pad("sink")
        sink_ghostpad = gst.GhostPad("sink_main", sinkpad)
        bin.add_pad(sink_ghostpad)
        
        pip_sinkpad = videobox2.get_pad("sink")
        pip_ghostpad = gst.GhostPad("sink_pip", pip_sinkpad)
        bin.add_pad(pip_ghostpad)
        
        srcpad = colorspace.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)
        
        return bin
    
    def get_inputs(self):
        inputs = [self.input1, self.input2]
        return inputs
        
    def load_inputs(self, player, mixer, inputs):
        # Load main source
        input1 = inputs[0]
        player.add(input1)
        
        mainsrc_capsfilter = gst.element_factory_make("capsfilter", "mainsrc_capsfilter")
        mainsrc_capsfilter.set_property('caps',
                        gst.caps_from_string('video/x-raw-rgb, width=640, height=480'))
        player.add(mainsrc_capsfilter)
        
        input1.link(mainsrc_capsfilter)
        srcpad = mainsrc_capsfilter.get_pad("src")
        sinkpad = mixer.get_pad("sink_main")
        srcpad.link(sinkpad)
    
        # Load the secondary source
        input2 = inputs[1]
        player.add(input2)
        
        pipsrc_capsfilter = gst.element_factory_make("capsfilter", "pipsrc_capsfilter")
        pipsrc_capsfilter.set_property('caps',
                        gst.caps_from_string('video/x-raw-rgb, width=200, height=150'))
        player.add(pipsrc_capsfilter)
        
        input2.link(pipsrc_capsfilter)
        srcpad = pipsrc_capsfilter.get_pad("src")
        sinkpad = mixer.get_pad("sink_pip")
        srcpad.link(sinkpad)
    
    def load_config(self, plugman):
        self.plugman = plugman
        try:
            self.input1 = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Main Source")
            self.input2 = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "PIP Source")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Main Source", self.input1)
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "PIP Source", self.input2)
    
    def get_widget(self):
        
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QGridLayout()
            self.widget.setLayout(layout)
            
            self.mainInputLabel = QtGui.QLabel("Main Source")
            self.mainInputComboBox = QtGui.QComboBox()
            self.mainInputSetupButton = QtGui.QPushButton("Setup")
            layout.addWidget(self.mainInputLabel, 0, 0)
            layout.addWidget(self.mainInputComboBox, 0, 1)
            layout.addWidget(self.mainInputSetupButton, 0, 2)
            
            self.pipInputLabel = QtGui.QLabel("PIP Source")
            self.pipInputComboBox = QtGui.QComboBox()
            self.pipInputSetupButton = QtGui.QPushButton("Setup")
            layout.addWidget(self.pipInputLabel, 1, 0)
            layout.addWidget(self.pipInputComboBox, 1, 1)
            layout.addWidget(self.pipInputSetupButton, 1, 2)
            
            self.widget.connect(self.mainInputComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_maininput)
            self.widget.connect(self.mainInputSetupButton, QtCore.SIGNAL('clicked()'), self.open_mainInputSetup)
            self.widget.connect(self.pipInputComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_pipinput)
            self.widget.connect(self.pipInputSetupButton, QtCore.SIGNAL('clicked()'), self.open_pipInputSetup)
            
        return self.widget
    
    def widget_load_config(self, plugman):
        self.load_config(plugman)
        
        sources = []
        plugins = self.plugman.plugmanc.getPluginsOfCategory("VideoInput")
        for plugin in plugins:
            sources.append(plugin.plugin_object.get_name())
        
        # Load the main combobox with inputs
        self.mainInputComboBox.clear()
        n = 0
        for i in sources:
            self.mainInputComboBox.addItem(i)
            if i == self.input1: # Find the current main input source and set it
                self.mainInputComboBox.setCurrentIndex(n)
            n = n +1
        
        # Load the pip combobox with inputs
        self.pipInputComboBox.clear()
        n = 0
        for i in sources:
            self.pipInputComboBox.addItem(i)
            if i == self.input2: # Find the current pip input source and set it
                self.pipInputComboBox.setCurrentIndex(n)
            n = n +1
        
            
    def set_maininput(self, input):
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Main Source", input)
        self.plugman.save()
        
    def open_mainInputSetup(self):
        plugin_name = str(self.mainInputComboBox.currentText())
        plugin = self.plugman.plugmanc.getPluginByName(plugin_name, "VideoInput")
        plugin.plugin_object.set_instance(0)
        plugin.plugin_object.get_dialog()
        
    def set_pipinput(self, input):
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "PIP Source", input)
        self.plugman.save()
        
    def open_pipInputSetup(self):
        plugin_name = str(self.pipInputComboBox.currentText())
        plugin = self.plugman.plugmanc.getPluginByName(plugin_name, "VideoInput")
        plugin.plugin_object.set_instance(1)
        plugin.plugin_object.get_dialog()
        
    def get_properties(self):
        return ['MainInput', "PIPInput"]
    
    def get_property_value(self, property):
        if property == "MainInput":
            return self.input1
        elif property == "PIPInput":
            return self.input2
        else:
            return "There's no property with such name"
        
    def set_property_value(self, property, value):
        if(property == "MainInput"):
            if(value == "USB"):
                self.set_maininput("USB Source")
            elif(value == "Firewire"):
                self.set_maininput("Firewire Source")
            elif(value == "Desktop"):
                self.set_maininput("Desktop-Linux Source")
            elif(value == "VideoTest"):
                self.set_maininput("Video Test Source")
            else:
                print "Choose an available Input"
                #TODO List available options   
        if(property == "PIPInput"):
            if(value == "USB"):
                self.set_pipinput("USB Source")
            elif(value == "Firewire"):
                self.set_pipinput("Firewire Source")
            elif(value == "Desktop"):
                self.set_pipinput("Desktop-Linux Source")
            elif(value == "VideoTest"):
                self.set_pipinput("Video Test Source")
            else:
                print "Choose an available Input"
                #TODO List available options               
        else:
            return "Error: There's no property with such name" 
