import ConfigParser

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoMixer

class InputSelector(IVideoMixer):
    name = "Input Selector"
    input1 = None
    widget = None
    
    def get_videomixer_bin(self):
        bin = gst.Bin(self.name)
        
        videomixer = gst.element_factory_make("input-selector", "videomixer")
        bin.add(videomixer)
        
        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)
        
        # Setup ghost pad
        sinkpad = videomixer.get_pad("sink%d")
        sink_ghostpad = gst.GhostPad("sink", sinkpad)
        bin.add_pad(sink_ghostpad)
        
        srcpad = colorspace.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)
        
        gst.element_link_many(videomixer, colorspace)
        
        return bin
    
    def set_input(self, input1):
        self.input1 = input1
        
    def load_inputs(self, player, mixer, inputs):
        loaded = []
        for plugin in inputs:
            print self.input1, plugin.plugin_object.get_name()
            if plugin.is_activated and plugin.plugin_object.get_name() == self.input1:
                input = plugin.plugin_object.get_videoinput_bin()
                player.add(input)
                input.link(mixer)
                loaded.append(input)
                break
            
        return loaded
   
    def load_config(self, plugman):
        self.plugman = plugman
        self.input1 = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "Input 1")
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Input 1")
            self.combobox = QtGui.QComboBox()
            layout.addRow(self.label, self.combobox)
            
            self.widget.connect(self.combobox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_input1)
            
        return self.widget

    def widget_load_sources(self, plugman):
        self.plugman = plugman
        
        try:
            self.input1 = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "Input 1")
        except ConfigParser.NoSectionError:
            self.input1 = self.plugman.plugmanc.registerOptionFromPlugin("VideoMixer", self.name, "Input 1", None)
        
        sources = []
        plugins = self.plugman.plugmanc.getPluginsOfCategory("VideoInput")
        for plugin in plugins:
            if plugin.is_activated:
                sources.append(plugin.plugin_object.get_name())
                
        # Load the combobox with inputs
        self.combobox.clear()
        n = 0
        for i in sources:
            self.combobox.addItem(i)
            if i == self.input1:
                self.combobox.setCurrentIndex(n)
            n = n +1

    def set_input1(self, input):
        self.plugman.plugmanc.registerOptionFromPlugin("VideoMixer", self.name, "Input 1", input)
        self.plugman.save()
