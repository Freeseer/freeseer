# freeseer - vga/presentation capture software
#
#  Copyright (C) 2010  Free and Open Source Software Learning Centre
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
# the #fosslc channel on IRC (freenode.net)

import gobject, pygst
pygst.require("0.10")
import gst

__version__=u'2.0'

class Freeseer:
    '''
    Freeseer backend class using gstreamer to record video and audio.
    '''
    def __init__(self):
        gobject.threads_init()
        self.window_id = None

        self.viddrv = 'v4lsrc'
        self.viddev = '/dev/video0'
        self.soundsrc = 'alsasrc'
        self.filename = 'default.ogg'
        self.video_codec = 'theoraenc'
        self.audio_codec = 'vorbisenc'

        self.player = gst.Pipeline("player")

        # GST Video
        self.vidsrc = gst.element_factory_make(self.viddrv, "vidsrc")
        self.cspace = gst.element_factory_make("ffmpegcolorspace", "cspace")
        self.vidtee = gst.element_factory_make("tee", "vidtee")
        self.vidqueue1 = gst.element_factory_make("queue", "vidqueue1")
        self.vidqueue2 = gst.element_factory_make("queue", "vidqueue2")
        self.vidcodec = gst.element_factory_make(self.video_codec, "vidcodec")
        self.vidcodec.set_property("quality", 48)
        self.vidcodec.set_property("sharpness", 2)
        self.vidcodec.set_property("bitrate", 300)
        self.vidsink = gst.element_factory_make("autovideosink", "vidsink")

        # GST Video Filtering
        self.fvidrate = gst.element_factory_make("videorate", "fvidrate")
        self.fvidrate_cap = gst.element_factory_make("capsfilter", "fvidrate_cap")
        self.fvidrate_cap.set_property('caps', gst.caps_from_string('video/x-raw-rgb, framerate=25/1, silent'))
        self.fvidscale = gst.element_factory_make("videoscale", "fvidscale")
        self.fvidscale_cap = gst.element_factory_make("capsfilter", "fvidscale_cap")
        self.fvidscale_cap.set_property('caps', gst.caps_from_string('video/x-raw-yuv, width=640, height=480'))
        self.fvidcspace = gst.element_factory_make("ffmpegcolorspace", "fvidcspace")


        # GST Sound
        self.sndsrc = gst.element_factory_make("alsasrc", "sndsrc")
#        self.sndsrc.set_property("device", "alsa_output.pci-0000_00_1b.0.analog-stereo")
        self.sndtee = gst.element_factory_make("tee", "sndtee")
        self.sndqueue1 = gst.element_factory_make("queue", "sndqueue1")
        self.sndqueue2 = gst.element_factory_make("queue", "sndqueue2")
        self.audioconvert = gst.element_factory_make("audioconvert", "audioconvert")
        self.sndcodec = gst.element_factory_make(self.audio_codec, "sndcodec")
        self.sndsink = gst.element_factory_make("autoaudiosink", "sndsink")

        # GST Muxer
        self.mux = gst.element_factory_make("oggmux", "mux")
        self.filesink = gst.element_factory_make("filesink", "filesink")
        self.filesink.set_property("location", self.filename)

        # GST Add Components
        self.player.add(self.vidsrc, self.cspace, self.vidtee, self.vidqueue1, self.vidcodec)
        self.player.add(self.fvidrate, self.fvidrate_cap, self.fvidscale, self.fvidscale_cap, self.fvidcspace)
        self.player.add(self.sndsrc, self.sndtee, self.sndqueue1, self.audioconvert, self.sndcodec)
        self.player.add(self.mux, self.filesink)

        # GST Link Components
        gst.element_link_many(self.vidsrc, self.cspace, self.fvidrate, self.fvidrate_cap, self.fvidscale, self.fvidscale_cap, self.fvidcspace, self.vidtee)
        gst.element_link_many(self.vidtee, self.vidqueue1, self.vidcodec, self.mux)
        gst.element_link_many(self.sndsrc, self.sndtee)
        gst.element_link_many(self.sndtee, self.sndqueue1, self.audioconvert, self.sndcodec, self.mux)
        gst.element_link_many(self.mux, self.filesink)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(self.window_id)

    def _dvdemux_padded(self, dbin, pad):
        print "dvdemux got pad %s" % pad.get_name()
        if pad.get_name() == 'video':
            print "Linking dvdemux to queue1"
            self.dv1394dvdemux.link(self.dv1394q1)

    def change_videosrc(self, new_source, new_device):
        '''
        Changes the video source
        '''
        if (self.viddrv == 'dv1394src'):
            self.player.remove(self.dv1394q1)
            self.player.remove(self.dv1394q2)
            self.player.remove(self.dv1394dvdemux)
            self.player.remove(self.dv1394dvdec)
            self.dv1394q1 = None
            self.dv1394q2 = None
            self.dv1394dvdemux = None
            self.dv1394dvdec = None

        self.viddrv = new_source
        self.viddev = new_device
        self.player.remove(self.vidsrc)
        self.vidsrc = gst.element_factory_make(self.viddrv, "vidsrc")
        self.player.add(self.vidsrc)

        if (self.viddrv == 'v4lsrc'):
            self.vidsrc.set_property("device", self.viddev)
        elif (self.viddrv == 'v4l2src'):
            self.vidsrc.set_property("device", self.viddev)
        elif (self.viddrv == 'dv1394src'):
            self.dv1394q1 =  gst.element_factory_make("queue", "dv1394q1")
            self.dv1394q2 =  gst.element_factory_make("queue", "dv1394q2")
            self.dv1394dvdemux =  gst.element_factory_make("dvdemux", "dv1394dvdemux")
            self.dv1394dvdec =  gst.element_factory_make("dvdec", "dv1394dvdec")
            self.player.add(self.dv1394q1, self.dv1394q2, self.dv1394dvdemux, self.dv1394dvdec)
            self.vidsrc.link(self.dv1394dvdemux)
            self.dv1394dvdemux.connect('pad-added', self._dvdemux_padded)
            gst.element_link_many( self.dv1394q1, self.dv1394dvdec, self.cspace)
            return

        gst.element_link_many(self.vidsrc, self.cspace)

    def change_soundsrc(self, new_source):
        '''
        Changes the sound source
        '''
        self.soundsrc = new_source
        self.player.remove(self.sndsrc)
        self.sndsrc = gst.element_factory_make(self.soundsrc, "sndsrc")
        self.player.add(self.sndsrc)
        self.sndsrc.link(self.sndtee)

    def record(self, filename):
        '''
        Start recording to a file.

        filename: filename to record to
        '''
        self.filename = filename
        self.filesink.set_property("location", self.filename)
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        '''
        Stop recording.
        '''
        self.player.set_state(gst.STATE_NULL)

    def change_video_codec(self, new_vcodec):
        '''
        Change the video codec
        '''
        self.video_codec = new_vcodec
        self.player.remove(self.vidcodec)
        self.vidcodec = gst.element_factory_make(self.video_codec, "vidcodec")
        self.player.add(self.vidcodec)
        gst.element_link_many(self.vidqueue1, self.vidcodec, self.mux)

    def change_audio_codec(self, new_acodec):
        '''
        Change the audio codec
        '''
        self.audio_codec = new_acodec
        self.player.remove(self.sndcodec)
        self.sndcodec = gst.element_factory_make(self.audio_codec, "sndcodec")
        self.player.add(self.sndcodec)
        gst.element_link_many(self.audioconvert, self.sndcodec, self.mux)

    def change_muxer(self, new_mux):
        '''
        Change the muxer
        '''
        self.muxer = new_mux
        self.player.remove(self.mux)
        self.mux = gst.element_factory_make(self.muxer, "mux")
        self.player.add(self.mux)
        gst.element_link_many(self.sndcodec, self.mux)
        gst.element_link_many(self.vidcodec, self.mux)
        gst.element_link_many(self.mux, self.filesink)

    def enable_preview(self, window_id):
        '''
        Activate video feedback. Will send video to a preview window.
        '''
        self.window_id = window_id
        self.player.add(self.vidqueue2, self.vidsink)
        gst.element_link_many(self.vidtee, self.vidqueue2, self.vidsink)

    def disable_preview(self):
        '''
        Disable the video preview
        '''
        self.player.remove(self.vidqueue2, self.vidsink)

    def enable_audio_feedback(self):
        '''
        Activate audio feedback.  Will send the recorded audio back out the speakers.
        '''
        self.player.add(self.sndqueue2, self.sndsink)
        gst.element_link_many(self.sndtee, self.sndqueue2, self.sndsink)

    def disable_audio_feedback(self):
        '''
        Disable the audio feedback.
        '''
        self.player.remove(self.sndqueue2, self.sndsink)
