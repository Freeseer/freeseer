import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoMixer

class PictureInPicture(IVideoMixer):
    name = "Picture-In-Picture"
    input1 = None
    input2 = None
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
        
        videobox_capsfilter = gst.element_factory_make("capsfilter", "videobox_capsfilter")
        videobox_capsfilter.set_property('caps',
                        gst.caps_from_string('alpha=0.6 top=-20 left=-25'))
        bin.add(videobox_capsfilter)
        
        gst.element_link_many(videobox, videobox_capsfilter, videomixer)
        
        # Setup ghost pad
        sinkpad = videomixer.get_pad("sink_%d")
        sink_ghostpad = gst.GhostPad("sink", sinkpad)
        bin.add_pad(sink_ghostpad)
        
        pip_sinkpad = videobox.get_pad("sink")
        pip_ghostpad = gst.GhostPad("sink_pip", pip_sinkpad)
        bin.add_pad(pip_ghostpad)
        
        srcpad = colorspace.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)
        
        return bin
    
    def set_input_main(self, input1):
        self.input1 = input1
        
    def set_input_pip(self, input2):
        self.input2 = input2
        
    def load_inputs(self, player, mixer, inputs):
        loaded = []
        
        # Load main source
        for plugin in inputs:
            if plugin.is_activated and plugin.plugin_object.get_name() == self.input1:
                input1 = plugin.plugin_object.get_videoinput_bin()
                player.add(input1)
                
                gst.element_link_many(input1, mixer)
                loaded.append(input1)
                break
            
        # Load pip source
        for plugin in inputs:
            if plugin.is_activated and plugin.plugin_object.get_name() == self.input2:
                input2 = plugin.plugin_object.get_videoinput_bin()
                player.add(input2)
                
                pipsrc_capsfilter = gst.element_factory_make("capsfilter", "pipsrc_capsfilter")
                pipsrc_capsfilter.set_property('caps',
                                gst.caps_from_string('video/x-raw-rgb, framerate=10/1, width=200, height=150'))
                player.add(pipsrc_capsfilter)
                
                gst.element_link_many(input2, pipsrc_capsfilter, mixer)
                loaded.append(input2)
                loaded.append(pipsrc_capsfilter)
                break
            
        return loaded
    
    def load_config(self, plugman):
        self.plugman = plugman
        self.input1 = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "Main Source")
        self.input2 = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "PIP Source")
    
    def get_widget(self):
        
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label_maininput = QtGui.QLabel("Main Source")
            self.combobox_maininput = QtGui.QComboBox()
            layout.addRow(self.label_maininput, self.combobox_maininput)
            
            self.label_pipinput = QtGui.QLabel("PIP Source")
            self.combobox_pipinput = QtGui.QComboBox()
            layout.addRow(self.label_pipinput, self.combobox_pipinput)
            
            self.widget.connect(self.combobox_maininput, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_maininput)
            self.widget.connect(self.combobox_pipinput, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_pipinput)
            
        return self.widget
    
    def widget_load_sources(self, plugman):
        self.plugman = plugman
        
        mainsrc = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "Main Source")
        pipsrc = self.plugman.plugmanc.readOptionFromPlugin("VideoMixer", self.name, "PIP Source")
        
        sources = []
        plugins = self.plugman.plugmanc.getPluginsOfCategory("VideoInput")
        for plugin in plugins:
            if plugin.is_activated:
                sources.append(plugin.plugin_object.get_name())
        
        n = 0
        for i in sources:
            self.combobox_maininput.addItem(i)
            if i == mainsrc:
                self.combobox_maininput.setCurrentIndex(n)
            n = n +1
        n = 0
        for i in sources:
            self.combobox_pipinput.addItem(i)
            if i == pipsrc:
                self.combobox_pipinput.setCurrentIndex(n)
            n = n +1
        
            
    def set_maininput(self, input):
        self.plugman.plugmanc.registerOptionFromPlugin("VideoMixer", self.name, "Main Source", input)
        self.plugman.save()
        
    def set_pipinput(self, input):
        self.plugman.plugmanc.registerOptionFromPlugin("VideoMixer", self.name, "PIP Source", input)
        self.plugman.save()    
