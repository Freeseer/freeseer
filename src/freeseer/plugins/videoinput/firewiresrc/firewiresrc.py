import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IVideoInput

class FirewireSrc(IVideoInput):
    name = "Firewire Source"
    
    def get_videoinput_bin(self):
        bin = gst.Bin(self.name)

        videosrc = gst.element_factory_make("dv1394src", "videosrc")
        dv1394q1 =  gst.element_factory_make('queue', 'dv1394q1')
        dv1394dvdemux =  gst.element_factory_make('dvdemux', 'dv1394dvdemux')
        dv1394q2 =  gst.element_factory_make('queue', 'dv1394q2')
        dv1394dvdec =  gst.element_factory_make('dvdec', 'dv1394dvdec')
        
        bin.add(videosrc, dv1394q1, dv1394dvdemux, dv1394q2, dv1394dvdec)
        
        # Setup ghost pad
        pad = dv1394dvdec.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)
        
        return bin