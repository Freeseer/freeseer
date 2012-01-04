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

@author: Jordan Klassen
'''


import functools
import pygst
pygst.require('0.10')
import gst
from PyQt4 import QtGui, QtCore
# i don't know if this works with translate's scanner, 
#  may need some hand coding of translation files
tr = functools.partial(QtCore.QCoreApplication.translate, "metadata_gstreamerdiscoverer")

from freeseer.framework import uploader
from freeseer.framework.plugin import IMetadataReader

class GStreamerDiscoverer(IMetadataReader):
    name = "GstDiscoverer Parser"
    
    fields_provided = {
        'album':            IMetadataReader.header(tr("Album"), str, 202), 
        'comment':          IMetadataReader.header(tr("Description"), str, 203), 
#        'performer':        IMetadataReader.header(tr("Performer"), str),
#        'encoder-version':  IMetadataReader.header(tr("Encoder Version"), int), 
        'title':            IMetadataReader.header(tr("Title"), str, 200), 
#        'audio-codec':      IMetadataReader.header(tr("Audio Codec"), str), 
        'artist':           IMetadataReader.header(tr("Artist"), str, 201), 
#        'encoder':          IMetadataReader.header(tr("Encoder"), str), 
#        'nominal-bitrate':  IMetadataReader.header(tr("Nominal Bitrate"), int), 
#        'date':             IMetadataReader.header(tr("Recording Date"), gst.Date),
#        'video-codec':      IMetadataReader.header(tr("Video Codec"), str), 
#        'bitrate':          IMetadataReader.header(tr("Bitrate"), int), 
#        'container-format': IMetadataReader.header(tr("Format"), str),
        'duration':         IMetadataReader.header(tr("Duration"), long, 204),
        'videowidth':       IMetadataReader.header(tr("Width"), int, 205),
        'videoheight':      IMetadataReader.header(tr("Height"), int, 206),
        }
    
    def retrieve_metadata_internal(self, filepath):
        # TODO: implement batch begin/end for this class so that the 
        #  gobject main loop isn't constantly being started and stopped
        # TODO: call discoverer directly instead of through uploader.VideoData
        
        d = uploader.VideoData(filepath)
        d.run()
        
        return {
        'album':            d.album, 
        'comment':          d.comment, 
        'title':            d.title, 
        'artist':           d.artist, 
#        'date':             ,
        'duration':         humantime(d.raw_duration),
        'videowidth':       d.videowidth,
        'videoheight':      d.videoheight,
        }

# adapted from gst.extend.discoverer._time_to_string
def humantime(value):
    """
    transform a value in nanoseconds into a human-readable string
    """
    ms = value / gst.MSECOND
    sec = ms / 1000
    ms = ms % 1000
    mn = sec / 60
    sec = sec % 60
#    return "%2dm %2ds %3d" % (mn, sec, ms)
    return "{0:0>2}m {1:0>2}s".format(mn, sec)

#    return QtCore.QTime().addMSecs(ms)