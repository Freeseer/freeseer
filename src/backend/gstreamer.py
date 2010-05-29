#!/usr/bin/python
# -*- coding: utf-8 -*-

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

from framework.backend_interface import *

__version__=u'1.9.7'

class Freeseer_gstreamer(BackendInterface):
    '''
    Freeseer backend class using gstreamer to record video and audio.
    '''
    def __init__(self, core):
        self.core = core
        self.window_id = None

        ##
        ## Global State Variables
        ##
        self.record_video = True
        self.record_audio = True

        # Video Related
        self.recording_video_bitrate = 2400
        self.recording_video_codec = 'theoraenc'
        self.recording_video_feedback = False
        self.recording_width = 0
        self.recording_height = 0

        # Audio Related
        self.recording_audio_codec = 'vorbisenc'
        self.recording_audio_feedback = False
        
        # Initialize Player
        self.player = gst.Pipeline('player')
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('message', self.on_message)
        bus.connect('sync-message::element', self.on_sync_message)

    def on_message(self, bus, message):
        t = message.type
      
        if t == gst.MESSAGE_EOS:
            #self.player.set_state(gst.STATE_NULL)
            self.stop()
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            self.core.logger.log.debug('Error: ' + str(err) + str(debug))
            #self.player.set_state(gst.STATE_NULL)
            self.stop()

            if (str(err).startswith('Could not get/set settings from/on resource.')):
                # if v4l2src driver does not work, fallback to the older v4lsrc
                if (str(debug).startswith('v4l2_calls.c')):
                    self.core.logger.log.debug('v4l2src failed, falling back to v4lsrc')
                    self.change_videosrc('usb_fallback', self.viddev)
                    self.record()
                    
        elif message.structure is not None:
            s = message.structure.get_name()

            # Check the mic audio levels and pass it up as a percent value to core
            if s == 'level':
                msg = message.structure.to_string()
                rms_dB = float(msg.split(',')[6].split('{')[1].rstrip('}'))
                
                # This is an inaccurate representation of decibels into percent
                # conversion, this code should be revisited.
                try:
                    percent = (int(round(rms_dB)) + 50) * 2
                except OverflowError:
                    percent = 0
                self.core.audioFeedbackEvent(percent)
            
    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == 'prepare-xwindow-id':
            imagesink = message.src
            imagesink.set_property('force-aspect-ratio', True)
            imagesink.set_xwindow_id(self.window_id)

    def get_video_sources(self):
        return ['desktop', 'usb', 'firewire']

    def get_video_devices(self, videosrc):
        vid_devices = None
        if videosrc == 'usb':
            vid_devices = self._get_devices('/dev/video', 0)
        elif videosrc == 'firewire':
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
                self.core.logger.log.debug(src + ' is available.')
            except:
                self.core.logger.log.debug(src + ' is not available')

        return snd_sources

    def get_video_codecs(self):
        video_codec_list = ['theoraenc', 'ffenc_msmpeg4']
        
        video_codecs = []
        for codec in video_codec_list:
            try:
                gst.element_factory_make(codec, 'testcodec')
                video_codecs.append(codec)
                self.core.logger.log.debug(codec + ' is available.')
            except:
                self.core.logger.log.debug(codec + ' is not available')
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

    def change_videosrc(self, source_type, source_device):
        '''
        Changes the video source
        '''
        self.video_source_type = source_type
        self.video_device = source_device

        if (source_type == 'desktop'):
            self.video_source = 'ximagesrc'
        elif (source_type == 'usb'):
            self.video_source = 'v4l2src'
        elif (source_type == 'usb_fallback'):
            self.video_source = 'v4lsrc'
        elif (source_type == 'firewire'):
            self.video_source = 'dv1394src'

    def set_recording_area(self, start_x, start_y, end_x, end_y):
        self.vidsrc.set_property('startx', start_x)
        self.vidsrc.set_property('starty', start_y)
        self.vidsrc.set_property('endx', end_x)
        self.vidsrc.set_property('endy', end_y)

    def change_output_resolution(self, width, height):
        self.recording_width = width
        self.recording_height = height

    ###
    ### Muxer Functions
    ###
    def _set_muxer(self, filename):
        self.mux = gst.element_factory_make('oggmux', 'mux')
        filesink = gst.element_factory_make('filesink', 'filesink')
        filesink.set_property('location', filename)

        self.player.add(self.mux, filesink)
        gst.element_link_many(self.mux, filesink)

    def _clear_muxer(self):
        filesink = self.player.get_by_name('filesink')
        self.player.remove(self.mux, filesink)

    ###
    ### Video Functions
    ###
    def _set_video_source(self):
        video_src = gst.element_factory_make(self.video_source, 'video_src')
        if (self.video_source_type == 'usb'):
            video_src.set_property('device', self.video_device)
        video_rate = gst.element_factory_make('videorate', 'video_rate')
        video_rate_cap = gst.element_factory_make('capsfilter',
                                                    'video_rate_cap')
        video_rate_cap.set_property('caps',
                        gst.caps_from_string('framerate=10/1'))
        video_scale = gst.element_factory_make('videoscale', 'video_scale')
        video_scale_cap = gst.element_factory_make('capsfilter',
                                                    'video_scale_cap')
        video_cspace = gst.element_factory_make('ffmpegcolorspace',
                                                    'video_cspace')
        self.video_tee = gst.element_factory_make('tee', 'video_tee')

        if self.recording_width != 0:
            video_scale_cap.set_property('caps',
                gst.caps_from_string('width=%s, height=%s'
                % (self.recording_width, self.recording_height)))

        self.player.add(video_src,
                        video_rate,
                        video_rate_cap,
                        video_scale,
                        video_scale_cap,
                        video_cspace,
                        self.video_tee)

        if (self.video_source_type == 'firewire'):
            self.dv1394q1 =  gst.element_factory_make('queue', 'dv1394q1')
            self.dv1394q2 =  gst.element_factory_make('queue', 'dv1394q2')
            self.dv1394dvdemux =  gst.element_factory_make('dvdemux',
                                                           'dv1394dvdemux')
            self.dv1394dvdec =  gst.element_factory_make('dvdec', 'dv1394dvdec')
            
            self.player.add(self.dv1394q1,
                            self.dv1394q2,
                            self.dv1394dvdemux,
                            self.dv1394dvdec)
                            
            video_src.link(self.dv1394dvdemux)
            
            self.dv1394dvdemux.connect('pad-added', self._dvdemux_padded)
            gst.element_link_many(self.dv1394q1, self.dv1394dvdec, video_rate)
        else:
            video_src.link(video_rate)

        gst.element_link_many(video_rate,
                              video_rate_cap,
                              video_scale,
                              video_scale_cap,
                              video_cspace,
                              self.video_tee)

    def _clear_video_source(self):
        video_src = self.player.get_by_name('video_src')
        video_rate = self.player.get_by_name('video_rate')
        video_rate_cap = self.player.get_by_name('video_rate_cap')
        video_scale = self.player.get_by_name('video_scale')
        video_scale_cap = self.player.get_by_name('video_scale_cap')
        video_cspace = self.player.get_by_name('video_cspace')

        self.player.remove(video_src,
                           video_rate,
                           video_rate_cap,
                           video_scale,
                           video_scale_cap,
                           video_cspace,
                           self.video_tee)

        if (self.video_source_type == 'firewire'):
            self.player.remove(self.dv1394q1,
                               self.dv1394q2,
                               self.dv1394dvdemux,
                               self.dv1394dvdec)

    def _set_video_encoder(self):
        videoenc_queue = gst.element_factory_make('queue', 'videoenc_queue')
        videoenc_codec = gst.element_factory_make(self.recording_video_codec,
                                                    'videoenc_codec')
        videoenc_codec.set_property('bitrate', self.recording_video_bitrate)

        self.player.add(videoenc_queue, videoenc_codec)
        gst.element_link_many(self.video_tee,
                              videoenc_queue,
                              videoenc_codec,
                              self.mux)

    def _clear_video_encoder(self):
        videoenc_queue = self.player.get_by_name('videoenc_queue')
        videoenc_codec = self.player.get_by_name('videoenc_codec')
        self.player.remove(videoenc_queue, videoenc_codec)

    def _set_video_feedback(self):
        vpqueue = gst.element_factory_make('queue', 'vpqueue')
        vpsink = gst.element_factory_make('autovideosink', 'vpsink')

        self.player.add(vpqueue, vpsink)
        gst.element_link_many(self.video_tee, vpqueue, vpsink)
    
    def _clear_video_feedback(self):
        vpqueue = self.player.get_by_name('vpqueue')
        vpsink = self.player.get_by_name('vpsink')
        self.player.remove(vpqueue, vpsink)

    def _dvdemux_padded(self, dbin, pad):
        self.core.logger.log.debug("dvdemux got pad %s" % pad.get_name())
        if pad.get_name() == 'video':
            self.core.logger.log.debug('Linking dvdemux to queue1')
            self.dv1394dvdemux.link(self.dv1394q1)

    ###
    ### Audio Functions
    ###

    def _set_audio_source(self):
        audio_src = gst.element_factory_make(self.audio_source, 'audio_src')
        self.audio_tee = gst.element_factory_make('tee', 'audio_tee')
        self.player.add(audio_src, self.audio_tee)
        audio_src.link(self.audio_tee)

    def _clear_audio_source(self):
        audio_src = self.player.get_by_name('audio_src')
        self.player.remove(audio_src, self.audio_tee)

    def _set_audio_encoder(self):
        '''
        Sets the audio encoder pipeline
        '''
        
        audioenc_queue = gst.element_factory_make('queue',
                                                        'audioenc_queue')
        audioenc_convert = gst.element_factory_make('audioconvert',
                                                        'audioenc_convert')
        audioenc_level = gst.element_factory_make('level', 'audioenc_level')
        audioenc_level.set_property('interval', 20000000)
        audioenc_codec = gst.element_factory_make(self.recording_audio_codec,
                                                        'audioenc_codec')

        self.player.add(audioenc_queue,
                        audioenc_convert,
                        audioenc_level,
                        audioenc_codec)

        gst.element_link_many(self.audio_tee,
                              audioenc_queue,
                              audioenc_convert,
                              audioenc_level,
                              audioenc_codec,
                              self.mux)
                              
    def _clear_audio_encoder(self):
        '''
        Clears the audio encoder pipeline
        '''
        audioenc_queue = self.player.get_by_name('audioenc_queue')
        audioenc_convert = self.player.get_by_name('audioenc_convert')
        audioenc_level = self.player.get_by_name('audioenc_level')
        audioenc_codec = self.player.get_by_name('audioenc_codec')

        self.player.remove(audioenc_queue,
                           audioenc_convert,
                           audioenc_level,
                           audioenc_codec)

    def _set_audio_feedback(self):
        afqueue = gst.element_factory_make('queue', 'afqueue')
        afsink = gst.element_factory_make('autoaudiosink', 'afsink')
        self.player.add(afqueue, afsink)
        gst.element_link_many(self.audio_tee, afqueue, afsink)

    def _clear_audio_feedback(self):
        afqueue = self.player.get_by_name('afqueue')
        afsink = self.player.get_by_name('afsink')
        self.player.remove(afqueue, afsink)

    ###
    ### Framework Required Functions
    ###

    def change_soundsrc(self, new_source):
        '''
        Changes the sound source
        '''

        # Ensure the new sound source is valid
        try:
            self.core.logger.log.debug('loading ' + new_source)
            src = gst.element_factory_make(new_source, 'sndsrc')
        except:
            self.core.logger.log.debug('Failed to load ' + new_source + '.')
            return False

        self.audio_source = new_source
        self.core.logger.log.debug(self.audio_source + ' loaded.')
        
        return True

    def record(self, filename):
        '''
        Start recording to a file.

        filename: filename to record to
        '''
        self._set_muxer(filename)

        if self.record_video == True:
            self._set_video_source()
            self._set_video_encoder()

            if self.recording_video_feedback == True:
                self._set_video_feedback()

        if self.record_audio == True:
            self._set_audio_source()
            self._set_audio_encoder()
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        '''
        Stop recording.
        '''
        self.player.set_state(gst.STATE_NULL)
        self._clear_muxer()

        if self.record_video == True:
            self._clear_video_source()
            self._clear_video_encoder()
            
            if self.recording_video_feedback == True:
                self._clear_video_feedback()
            
        if self.record_audio == True:
            self._clear_audio_source()
            self._clear_audio_encoder()

    def change_video_codec(self, new_vcodec):
        '''
        Change the video codec
        '''
        self.video_codec = new_vcodec
        
        # check if the new video codec is valid
        # if not return False
        try:
            self.core.logger.log.debug('checking availability of ' + self.video_codec)
            self.vidcodec = gst.element_factory_make(self.video_codec, 'vidcodec')
        except:
            self.core.logger.log.debug('Failed to load ' + self.soundsrc + '.')
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

    def enable_video_feedback(self, window_id):
        '''
        Activate video feedback. Will send video to a preview window.
        '''
        self.recording_video_feedback = True
        self.window_id = window_id

    def disable_video_feedback(self):
        '''
        Disable the video preview
        '''
        self.recording_video_feedback = False

    def enable_audio_feedback(self):
        '''
        Activate audio feedback.  Will send the recorded audio back out the speakers.
        '''
        self.recording_audio_feedback = True

    def disable_audio_feedback(self):
        '''
        Disable the audio feedback.
        '''
        self.recording_audio_feedback = False
        
