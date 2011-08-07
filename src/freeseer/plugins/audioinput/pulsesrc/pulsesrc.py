import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IAudioInput

class PulseSrc(IAudioInput):
    name = "Pulse Audio Source"
    
    def get_audioinput_bin(self):
        bin = gst.Bin(self.name)
        
        audiosrc = gst.element_factory_make("pulsesrc", "audiosrc")
        bin.add(audiosrc)
        
        # Setup ghost pad
        pad = audiosrc.get_pad("src")
        ghostpad = gst.GhostPad("audiosrc", pad)
        bin.add_pad(ghostpad)
        
        return bin
