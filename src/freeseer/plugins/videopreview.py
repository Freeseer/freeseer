import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IOutput

class VideoPreview(IOutput):
    name = "Video Preview"
    type = "video"
    
    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type
    
    def get_output_bin(self):
        bin = gst.Bin(self.name)
        
        videoqueue = gst.element_factory_make("queue", "videoqueue")
        bin.add(videoqueue)
        
        videosink = gst.element_factory_make("autovideosink", "videosink")
        bin.add(videosink)
        
        # Setup ghost pad
        pad = videoqueue.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        bin.add_pad(ghostpad)
        
        gst.element_link_many(videoqueue, videosink)
        
        return bin
