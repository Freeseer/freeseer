import ConfigParser

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IAudioMixer

class Adder(IAudioMixer):
    name = "Adder"
    input1 = None
    widget = None
    
    def get_audiomixer_bin(self):
        bin = gst.Bin(self.name)
        
        audiomixer = gst.element_factory_make("adder", "audiomixer")
        bin.add(audiomixer)
        
        # Setup ghost pad
        sinkpad = audiomixer.get_pad("sink%d")
        sink_ghostpad = gst.GhostPad("sink", sinkpad)
        bin.add_pad(sink_ghostpad)
        
        srcpad = audiomixer.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)
        
        return bin
        
    def load_inputs(self, player, mixer, inputs):
        loaded = []
        for plugin in inputs:
            if plugin.is_activated and plugin.plugin_object.get_name() == self.input1:
                input = plugin.plugin_object.get_audioinput_bin()
                player.add(input)
                input.link(mixer)
                loaded.append(input)
                break
            
        return loaded


    def load_config(self, plugman):
        self.plugman = plugman
        self.input1 = self.plugman.plugmanc.readOptionFromPlugin("AudioMixer", self.name, "Audio Input 1")
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Audio Input 1")
            self.combobox = QtGui.QComboBox()
            layout.addRow(self.label, self.combobox)
            
            self.widget.connect(self.combobox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_input)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.input1 = self.plugman.plugmanc.readOptionFromPlugin("AudioMixer", self.name, "Audio Input 1")
        except ConfigParser.NoSectionError:
            self.input1 = self.plugman.plugmanc.registerOptionFromPlugin("AudioMixer", self.name, "Audio Input 1", None)
        
        sources = []
        plugins = self.plugman.plugmanc.getPluginsOfCategory("AudioInput")
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
        self.plugman.plugmanc.registerOptionFromPlugin("AudioMixer", self.name, "Audio Input 1", input)
        self.plugman.save()
