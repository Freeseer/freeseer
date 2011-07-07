import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IVideoInput

class USBSrc(IVideoInput):
    name = "USB Source"
    
    def get_videoinput_bin(self):
        bin = gst.Bin(self.name)
        
        videosrc = gst.element_factory_make("v4l2src", "videosrc")
        bin.add(videosrc)
        
        # Setup ghost pad
        pad = videosrc.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)
        
        return bin
