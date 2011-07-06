import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IAudioInput

class USBSrc(IAudioInput):
    name = "ALSA Source"
    
    def get_videoinput_bin(self):
        bin = gst.Bin(self.name)
        
        audiosrc = gst.element_factory_make("alsasrc", "audiosrc")
        bin.add(audiosrc)
        
        # Setup ghost pad
        pad = audiosrc.get_pad("src")
        ghostpad = gst.GhostPad("audiosrc", pad)
        bin.add_pad(ghostpad)
        
        return bin
