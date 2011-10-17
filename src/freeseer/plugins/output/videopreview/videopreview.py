'''
freeseer - vga/presentation capture software

Copyright (C) 2011  Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/fosslc/freeseer/

@author: Thanh Ha
'''

import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IOutput

class VideoPreview(IOutput):
    name = "Video Preview"
    type = "video"
    
    def get_output_bin(self, metadata=None):
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
