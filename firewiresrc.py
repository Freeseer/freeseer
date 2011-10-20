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

import os

import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IVideoInput

class FirewireSrc(IVideoInput):
    name = "Firewire Source"
    
    def __init__(self):
        IVideoInput.__init__(self)
        
        #
        # Detect available devices
        #
        i = 1
        path = "/dev/fw"
        devpath = path + str(i)
        
        while os.path.exists(devpath):
            self.device_list.append(devpath)
            i=i+1
            devpath=path + str(i)
    
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