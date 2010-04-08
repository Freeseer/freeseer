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

import os

import gobject
gobject.threads_init()
import pygst
pygst.require("0.10")
import gst

__version__=u'1.9.6'

class Freeseer:
    '''
    Freeseer backend class using gstreamer to record video and audio.
    '''
    def __init__(self, core):
        self.core = core
        self.window_id = None

        self.viddrv = 'v4lsrc'
        self.viddev = '/dev/video0'
        self.soundsrc = 'alsasrc'
        self.filename = 'default.ogg'
        self.video_codec = 'theoraenc'
        self.audio_codec = 'vorbisenc'

        self.player = gst.Pipeline('player')

        # GST Video
        self.vidsrc = gst.element_factory_make(self.viddrv, 'vidsrc')
        self.cspace = gst.element_factory_make('ffmpegcolorspace', "cspace")
        self.vidtee = gst.element_factory_make('tee', "vidtee")
        self.vidqueue1 = gst.element_factory_make('queue', 'vidqueue1')
        self.vidcodec = gst.element_factory_make(self.video_codec, 'vidcodec')
        self.vidcodec.set_property('bitrate', 2400)

        # GST Video Filtering
        self.fvidrate = gst.element_factory_make('videorate', 'fvidrate')
        self.fvidrate_cap = gst.element_factory_make('capsfilter', 'fvidrate_cap')
        self.fvidrate_cap.set_property('caps', gst.caps_from_string('video/x-raw-rgb, framerate=10/1, silent'))
        self.fvidscale = gst.element_factory_make('videoscale', 'fvidscale')
        self.fvidscale_cap = gst.element_factory_make('capsfilter', 'fvidscale_cap')
        self.fvidscale_cap.set_property('caps', gst.caps_from_string('video/x-raw-yuv, width=800, height=600'))
        self.fvidcspace = gst.element_factory_make('ffmpegcolorspace', 'fvidcspace')

        # GST Sound
        self.sndsrc = gst.element_factory_make(self.soundsrc, 'sndsrc')
#        self.sndsrc.set_property("device", "alsa_output.pci-0000_00_1b.0.analog-stereo")
        self.sndtee = gst.element_factory_make('tee', 'sndtee')
        self.sndqueue1 = gst.element_factory_make('queue', 'sndqueue1')        
        self.audioconvert = gst.element_factory_make('audioconvert', 'audioconvert')
        self.sndcodec = gst.element_factory_make(self.audio_codec, 'sndcodec')

        # GST Muxer
        self.mux = gst.element_factory_make('oggmux', 'mux')
        self.filesink = gst.element_factory_make('filesink', 'filesink')
        self.filesink.set_property('location', self.filename)

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
        bus.connect('message', self.on_message)
        bus.connect('sync-message::element', self.on_sync_message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            self.core.logger.debug('Error: ' + str(err) + str(debug))
            self.player.set_state(gst.STATE_NULL)

            if (err.startswith('Could not get/set settings from/on resource.')):
                # if v4l2src driver does not work, fallback to the older v4lsrc
                if (debug.startswith('v4l2_calls.c')):
                    self.core.logger.debug('v4l2src failed, falling back to v4lsrc')
                    self.change_videosrc('v4lsrc', self.viddev)
                    self.player.set_state(gst.STATE_PLAYING)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == 'prepare-xwindow-id':
            imagesink = message.src
            imagesink.set_property('force-aspect-ratio', True)
            imagesink.set_xwindow_id(self.window_id)

    def get_video_sources(self, stype):
        vid_source = None
        if stype == 'usb':
            vid_source = ['v4l2src', 'v4lsrc']
        elif stype == 'firewire':
            vid_source = ['dv1394src']
        elif stype == 'local':
            vid_source = ['ximagesrc']
        # return all types
        else:
            vid_source = ['v4l2src', 'v4lsrc', 'dv1394src', 'ximagesrc']
        return vid_source

    def get_video_devices(self, videosrc):
        vid_devices = None
        if videosrc == 'v4l2src':
            vid_devices = self._get_devices('/dev/video', 0)
        elif videosrc == 'v4lsrc':
            vid_devices = self._get_devices('/dev/video', 0)
        elif videosrc == 'dv1394src':
            vid_devices = self._get_devices('/dev/fw', 1)
        # return all types
        else:
            vid_devices = self._get_devices('/dev/video', 0)
            vid_devices += self._get_devices('/dev/fw', 1)

        return vid_devices

    def get_audio_sources(self):
        snd_sources_list = ['pulsesrc', 'alsasrc']

        snd_sources = []
        for src in snd_sources_list:
            try:
                gst.element_factory_make(src, 'testsrc')
                snd_sources.append(src)
                self.core.logger.debug(src + ' is available.')
            except:
                self.core.logger.debug(src + ' is not available')

        return snd_sources

    def get_video_codecs(self):
        video_codec_list = ['theoraenc', 'ffenc_msmpeg4']
        
        video_codecs = []
        for codec in video_codec_list:
            try:
                gst.element_factory_make(codec, 'testcodec')
                video_codecs.append(src)
                self.core.logger.debug(codec + ' is available.')
            except:
                self.core.logger.debug(codec + ' is not available')
        return video_codecs

    def _get_devices(self, path, index):
        i = index
        devices = []
        devpath=path + str(i)
        while os.path.exists(devpath):
            i=i+1
            devices.append(devpath)
            devpath=path + str(i)
        return devices

    def _dvdemux_padded(self, dbin, pad):
        self.core.logger.debug("dvdemux got pad %s" % pad.get_name())
        if pad.get_name() == 'video':
            self.core.logger.debug('Linking dvdemux to queue1')
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
        self.vidsrc = gst.element_factory_make(self.viddrv, 'vidsrc')
        self.player.add(self.vidsrc)

        if (self.viddrv == 'v4lsrc'):
            self.vidsrc.set_property('device', self.viddev)
        elif (self.viddrv == 'v4l2src'):
            self.vidsrc.set_property('device', self.viddev)
        elif (self.viddrv == 'dv1394src'):
            self.dv1394q1 =  gst.element_factory_make('queue', 'dv1394q1')
            self.dv1394q2 =  gst.element_factory_make('queue', 'dv1394q2')
            self.dv1394dvdemux =  gst.element_factory_make('dvdemux', 'dv1394dvdemux')
            self.dv1394dvdec =  gst.element_factory_make('dvdec', 'dv1394dvdec')
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
        old_sndsrc = self.sndsrc

        try:
            self.core.logger.debug('loading ' + self.soundsrc)
            self.sndsrc = gst.element_factory_make(self.soundsrc, 'sndsrc')
        except:
            self.core.logger.debug('Failed to load ' + self.soundsrc + '.')
            return False

        self.player.remove(old_sndsrc)
        self.player.add(self.sndsrc)
        self.sndsrc.link(self.sndtee)
        self.core.logger.debug(self.soundsrc + ' loaded.')
        return True

    def record(self, filename):
        '''
        Start recording to a file.

        filename: filename to record to
        '''
        self.filename = filename
        self.filesink.set_property('location', self.filename)
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
        
        # check if the new video codec is valid
        # if not return False
        try:
            self.core.logger.debug('checking availability of ' + self.video_codec)
            self.vidcodec = gst.element_factory_make(self.video_codec, 'vidcodec')
        except:
            self.core.logger.debug('Failed to load ' + self.soundsrc + '.')
            return False

        # codec is available for use, now set pipeline to use it
        self.player.remove(self.vidcodec)
        self.vidcodec = gst.element_factory_make(self.video_codec, 'vidcodec')
        self.player.add(self.vidcodec)
        gst.element_link_many(self.vidqueue1, self.vidcodec, self.mux)

    def change_audio_codec(self, new_acodec):
        '''
        Change the audio codec
        '''
        self.audio_codec = new_acodec
        self.player.remove(self.sndcodec)
        self.sndcodec = gst.element_factory_make(self.audio_codec, 'sndcodec')
        self.player.add(self.sndcodec)
        gst.element_link_many(self.audioconvert, self.sndcodec, self.mux)

    def change_muxer(self, new_mux):
        '''
        Change the muxer
        '''
        self.muxer = new_mux
        self.player.remove(self.mux)
        self.mux = gst.element_factory_make(self.muxer, 'mux')
        self.player.add(self.mux)
        gst.element_link_many(self.sndcodec, self.mux)
        gst.element_link_many(self.vidcodec, self.mux)
        gst.element_link_many(self.mux, self.filesink)

    def enable_preview(self, window_id):
        '''
        Activate video feedback. Will send video to a preview window.
        '''
        self.window_id = window_id

        vpqueue = gst.element_factory_make('queue', 'vpqueue')
        vpsink = gst.element_factory_make('autovideosink', 'vpsink')
        
        self.player.add(vpqueue, vpsink)
        gst.element_link_many(self.vidtee, vpqueue, vpsink)

    def disable_preview(self):
        '''
        Disable the video preview
        '''
        vpqueue = self.player.get_by_name('vpqueue')
        vpsink = self.player.get_by_name('vpsink')
        self.player.remove(vpqueue, vpsink)

    def enable_audio_feedback(self):
        '''
        Activate audio feedback.  Will send the recorded audio back out the speakers.
        '''
        afqueue = gst.element_factory_make('queue', 'afqueue')
        afsink = gst.element_factory_make('autoaudiosink', 'afsink')
        self.player.add(afqueue, afsink)
        gst.element_link_many(self.sndtee, afqueue, afsink)

    def disable_audio_feedback(self):
        '''
        Disable the audio feedback.
        '''
        afqueue = self.player.get_by_name('afqueue')
        afsink = self.player.get_by_name('afsink')
        self.player.remove(afqueue, afsink)
