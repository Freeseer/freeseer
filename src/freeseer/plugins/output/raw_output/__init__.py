# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://github.com/Freeseer/freeseer/

'''
Raw Output
----------

An output plugin which records to raw audio/video format and stores it to an AVI container.

@author: Thanh Ha
'''

# GStreamer
import pygst
pygst.require("0.10")
import gst

# Freeeseer
from freeseer.framework.plugin import IOutput


class RawOutput(IOutput):
    name = "Raw Output"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    type = IOutput.BOTH
    recordto = IOutput.FILE
    extension = "avi"

    def get_output_bin(self, audio=True, video=True, metadata=None):
        """Returns a bin that muxes audio and video inputs into a raw AVI file

        Pipeline:
            audio_input > queue > audioconvert > audiolevel > avimux
            video_input > queue > avimux
            avimux > filesink
        """
        bin = gst.Bin()

        # Muxer
        muxer = gst.element_factory_make("avimux", "muxer")
        bin.add(muxer)

        # File sink
        filesink = gst.element_factory_make('filesink', 'filesink')
        filesink.set_property('location', self.location)
        bin.add(filesink)

        #
        # Setup Audio Pipeline if Audio Recording is Enabled
        #
        if audio:
            audioqueue = gst.element_factory_make("queue", "audioqueue")
            bin.add(audioqueue)

            audioconvert = gst.element_factory_make("audioconvert", "audioconvert")
            bin.add(audioconvert)

            audiolevel = gst.element_factory_make('level', 'audiolevel')
            audiolevel.set_property('interval', 20000000)
            bin.add(audiolevel)

            # Setup ghost pads
            audiopad = audioqueue.get_pad("sink")
            audio_ghostpad = gst.GhostPad("audiosink", audiopad)
            bin.add_pad(audio_ghostpad)

            # Link Elements
            audioqueue.link(audioconvert)
            audioconvert.link(audiolevel)
            audiolevel.link(muxer)

        #
        # Setup Video Pipeline
        #
        if video:
            videoqueue = gst.element_factory_make("queue", "videoqueue")
            bin.add(videoqueue)

            videorate = gst.element_factory_make("videorate", "videorate")
            bin.add(videorate)

            # Setup ghost pads
            videopad = videoqueue.get_pad("sink")
            video_ghostpad = gst.GhostPad("videosink", videopad)
            bin.add_pad(video_ghostpad)

            # Link Elements
            videoqueue.link(videorate)
            videorate.link(muxer)

        #
        # Link muxer to filesink
        #
        muxer.link(filesink)

        return bin
