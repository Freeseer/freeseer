import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IOutput

class VideoPreview(IOutput):
    name = "WebM Output"
    type = "both"
    
    def get_output_bin(self, filename):
        filename = filename + '.webm'
        
        bin = gst.Bin(self.name)
        
        # Setup Audio Pipeline
        audioqueue = gst.element_factory_make("queue", "audioqueue")
        bin.add(videoqueue)
        
        audioconvert = gst.element_factory_make("audioconvert", "audioconvert")
        bin.add(audioconvert)
        
        audiocodec = gst.element_factory_make("vorbisenc", "audiocodec")
        bin.add(audiocodec)
        
        # Setup Video Pipeline
        videoqueue = gst.element_factory_make("queue", "videoqueue")
        bin.add(videoqueue)
        
        videocodec = gst.element_factory_make("vp8enc", "videocodec")
        bin.add(videocodec)
        
        # Muxer
        muxer = gst.element_factory_make("webmmux", "muxer")
        bin.add(muxer)
        
        filesink = gst.element_factory_make('filesink', 'filesink')
        filesink.set_property('location', filename)
        bin.add(filesink)
        
        # Setup ghost pads
        audiopad = audioqueue.get_pas("sink")
        audio_ghostpad = gst.GhostPad("audiosink", audiopad)
        bin.add_pad(audio_ghostpad)
        
        videopad = videoqueue.get_pad("sink")
        video_ghostpad = gst.GhostPad("videosink", videopad)
        bin.add_pad(video_ghostpad)
        
        gst.element_link_man(audioqueue, audioconvert, audiocodec, muxer)
        gst.element_link_many(videoqueue, videocodec, muxer)
        gst.element_linK_many(muxer, filesink)
        
        return bin
