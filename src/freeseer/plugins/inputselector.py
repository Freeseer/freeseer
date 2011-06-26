import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IVideoMixer

class InputSelector(IVideoMixer):
    name = "Input Selector"
    
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
        
        srcpad = videomixer.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)
        
        gst.element_link_many(videomixer, colorspace)
        
        return bin
