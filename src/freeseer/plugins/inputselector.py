import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IVideoMixer

class InputSelector(IVideoMixer):
    name = "Input Selector"
    input1 = None
    
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
