import ConfigParser

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoMixer

class VideoPassthrough(IVideoMixer):
    name = "Video Passthrough"
    input1 = None
    widget = None
    
    def get_videomixer_bin(self):
        bin = gst.Bin(self.name)
        
        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)
        
        # Setup ghost pad
        sinkpad = colorspace.get_pad("sink")
        sink_ghostpad = gst.GhostPad("sink", sinkpad)
        bin.add_pad(sink_ghostpad)
        
        srcpad = colorspace.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)
        
        return bin
        
    def load_inputs(self, player, mixer, inputs):
        loaded = []
        for plugin in inputs:
            if plugin.is_activated and plugin.plugin_object.get_name() == self.input1:
                input = plugin.plugin_object.get_videoinput_bin()
                player.add(input)
                input.link(mixer)
                loaded.append(input)
                break
            
        return loaded
   
    def load_config(self, plugman):
        self.plugman = plugman
        self.input1 = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "Video Input")
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Video Input")
            self.combobox = QtGui.QComboBox()
            layout.addRow(self.label, self.combobox)
            
            self.widget.connect(self.combobox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_input)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.input1 = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "Video Input")
        except ConfigParser.NoSectionError:
            self.input1 = self.plugman.plugmanc.registerOptionFromPlugin("VideoMixer", self.name, "Video Input", None)
        
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

    def set_input(self, input):
        self.plugman.plugmanc.registerOptionFromPlugin("VideoMixer", self.name, "Video Input", input)
        self.plugman.save()
