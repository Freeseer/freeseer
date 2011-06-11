import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IOutput

class VideoPreview(IOutput):
    name = "video_preview"
    type = "video"
    
    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type
    
    def get_output_bin(self):
        bin = gst.Bin(self.name)
        
        videocspace = gst.element_factory_make("ffmpegcolorspace", "videocspace")
        bin.add(videocspace) 
           
        pad = videocspace.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        bin.add_pad(ghostpad)
        
        videoqueue = gst.element_factory_make("queue", "videoqueue")
        bin.add(videoqueue) 
        
        videosink = gst.element_factory_make("autovideosink", "videosink")
        bin.add(videosink)
        
        gst.element_link_many(videocspace, videoqueue, videosink)
        
        return bin