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
# the #freeseer channel on IRC (freenode.net)

import os

import gobject
gobject.threads_init()
import pygst
pygst.require("0.10")
import gst

from freeseer.framework.backend_interface import *

__version__=u'2.0.1'

class Freeseer_gstreamer(BackendInterface):
    '''
    Freeseer backend class using gstreamer to record video and audio.
    '''
    def __init__(self, core):
        '''
        Initializes the gstreamer pipeline.
        '''
        self.core = core
        self.window_id = None

        ##
        ## Global State Variables
        ##
        self.record_video = True
        self.record_audio = True
        self.record_desktop_area = False
        self.record_desktop_area_start_x = 0
        self.record_desktop_area_start_y = 0
        self.record_desktop_area_end_x = 0
        self.record_desktop_area_end_y = 0

        # Video Related
        self.recording_video_bitrate = 2400
        self.recording_video_codec = 'theoraenc'
        self.recording_video_feedback = False
        self.recording_width = 0
        self.recording_height = 0

        # Audio Related
        self.recording_audio_codec = 'vorbisenc'
        self.recording_audio_feedback = False

        # Icecast Related
        self.icecast = False
        self.icecast_ip = '127.0.0.1'
        self.icecast_port = 8000
        self.icecast_password = 'hackme'
        self.icecast_mount = 'freeseer.ogg'
        self.icecast_video_codec = 'theoraenc'
        self.icecast_muxer = 'oggmux'
        self.icecast_audio_codec = 'vorbisenc'
        self.icecast_audio_src = 'alsasrc'
        self.icecast_width = 0
        self.icecast_height = 0
        self.icecast_vidbitrate = 0

        # Initialize Player
        self.player = gst.Pipeline('player')
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('message', self.on_message)
        bus.connect('sync-message::element', self.on_sync_message)

    ##
    ## GST Player Functions
    ##
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
                    self.change_video_source('usb_fallback', self.video_device)
                    self.record(self.filename)
                    
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

    ###
    ### Muxer Functions
    ###
    def _set_muxer(self, filename):
        '''
        Sets up the filesink and muxer.
        '''
        self.mux = gst.element_factory_make('oggmux', 'mux')
        filequeue = gst.element_factory_make('queue', 'filequeue')
        filesink = gst.element_factory_make('filesink', 'filesink')
        filesink.set_property('location', filename)

        self.player.add(self.mux, filequeue, filesink)
        gst.element_link_many(self.mux, filequeue, filesink)

    def _clear_muxer(self):
        '''
        Frees up the muxer and filesink from the pipeline.
        '''
        filesink = self.player.get_by_name('filesink')
        filequeue = self.player.get_by_name('filequeue')
        self.player.remove(self.mux, filequeue, filesink)

    ###
    ### Video Functions
    ###
    def _set_video_source(self):
        video_src = gst.element_factory_make(self.video_source, 'video_src')
        if (self.video_source_type.startswith('usb')):
            # not sure about device format on windows. for now lets just use the default
            if os.name == 'posix': # only set device for linux systems.
                video_src.set_property('device', self.video_device)
            

            
        video_rate = gst.element_factory_make('videorate', 'video_rate')
        video_rate_cap = gst.element_factory_make('capsfilter',
                                                    'video_rate_cap')
        video_rate_cap.set_property('caps',
                        gst.caps_from_string('video/x-raw-rgb, framerate=10/1'))
        video_scale = gst.element_factory_make('videoscale', 'video_scale')
        video_scale_cap = gst.element_factory_make('capsfilter',
                                                    'video_scale_cap')
        video_cspace = gst.element_factory_make('ffmpegcolorspace',
                                                    'video_cspace')
        self.video_tee = gst.element_factory_make('tee', 'video_tee')

        if self.recording_width != '0':
            self.core.logger.log.debug('Recording will be scaled to %sx%s'
                % (self.recording_width, self.recording_height))
            video_scale_cap.set_property('caps',
                gst.caps_from_string('video/x-raw-rgb, width=%s, height=%s'
                % (self.recording_width, self.recording_height)))

        self.player.add(video_src,
                        video_rate,
                        video_rate_cap,
                        video_scale,
                        video_scale_cap,
                        video_cspace,
                        self.video_tee)
        
        if ( self.icecast ):
            # Add a "tee" component so that the icecast components can be built at the end
            self.src_tee = gst.element_factory_make('tee', 'src_tee')
            self.player.add( self.src_tee )
            video_src.link( self.src_tee )


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
            
            if ( self.icecast ):
                # The "src_tee" was added so link from it
                self.src_tee.link(self.dv1394dvdemux)
            else:                
                video_src.link(self.dv1394dvdemux)
            
                self.dv1394dvdemux.connect('pad-added', self._dvdemux_padded)
                gst.element_link_many(self.dv1394q1, self.dv1394dvdec, video_rate)
        else:
            if ( self.icecast ):
                # The "src_tee" was added so link from it
                self.src_tee.link(video_rate)
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
        
        if ( self.icecast ):
            # The "src_tee" was added so remove it
            self.player.remove(self.src_tee)

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

    def _set_recording_area(self):
        video_src = self.player.get_by_name('video_src')
        video_src.set_property('startx', self.record_desktop_area_start_x)
        video_src.set_property('starty', self.record_desktop_area_start_y)
        video_src.set_property('endx', self.record_desktop_area_end_x)
        video_src.set_property('endy', self.record_desktop_area_end_y)
        print 'success'

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

        # create a VorbisTag element and merge tags from tag list
        audioenc_tags = gst.element_factory_make("vorbistag", "audioenc_tags")

        # set tag merge mode to GST_TAG_MERGE_REPLACE
        merge_mode = gst.TagMergeMode.__enum_values__[2]

        audioenc_tags.merge_tags(self.tags, merge_mode)
        audioenc_tags.set_tag_merge_mode(merge_mode)
        self.player.add(audioenc_queue,
                        audioenc_convert,
                        audioenc_level,
                        audioenc_codec,
                        audioenc_tags)

        gst.element_link_many(self.audio_tee,
                              audioenc_queue,
                              audioenc_convert,
                              audioenc_level,
                              audioenc_codec,
                              audioenc_tags,
                              self.mux)
                              
    def _clear_audio_encoder(self):
        '''
        Clears the audio encoder pipeline
        '''
        audioenc_queue = self.player.get_by_name('audioenc_queue')
        audioenc_convert = self.player.get_by_name('audioenc_convert')
        audioenc_level = self.player.get_by_name('audioenc_level')
        audioenc_codec = self.player.get_by_name('audioenc_codec')
        audioenc_tags = self.player.get_by_name('audioenc_tags')

        self.player.remove(audioenc_queue,
                           audioenc_convert,
                           audioenc_level,
                           audioenc_codec,
                           audioenc_tags)

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
    ### Icecast Functions
    ###
    def _set_icecast_streaming(self):
        '''
        Sets up the icecast stream pipeline.
        '''
        icecast = gst.element_factory_make('shout2send', 'icecast')
        icecast.set_property('ip', self.icecast_ip)
        icecast.set_property('port', self.icecast_port)
        icecast.set_property('password', self.icecast_password)
        icecast.set_property('mount', self.icecast_mount)

        # Need to add "ffmpegcolorspace" to the player again, after "src_tee"
        icecast_colorspace = gst.element_factory_make('ffmpegcolorspace', 'icecast_colorspace')

        icecast_queue = gst.element_factory_make('queue', 'icecast_queue')
        icecast_scale = gst.element_factory_make('videoscale', 'icecast_scale')
        icecast_scale_cap = gst.element_factory_make('capsfilter', 'icecast_scale_cap')
        #icecast_gst_caps = gst.Caps('video/x-raw-yuv,width=320,height=240')
        #icecast_scale_cap.set_property('caps', icecast_gst_caps)

        #icecast_video_codec = gst.element_factory_make(self.icecast_video_codec, 'icecast_video_codec')
        #icecast_video_codec.set_property('quality',16)

        icecast_gst_caps = gst.Caps('video/x-raw-yuv,width=' + str(self.icecast_width) + ',height=' + str(self.icecast_height))
        icecast_scale_cap.set_property('caps', icecast_gst_caps)

        icecast_video_codec = gst.element_factory_make(self.icecast_video_codec, 'icecast_video_codec')
        icecast_video_codec.set_property('bitrate',self.icecast_vidbitrate)

        icecast_muxer = gst.element_factory_make(self.icecast_muxer, 'icecast_muxer')

        icecast_audio_src = gst.element_factory_make(self.icecast_audio_src,'icecast_audio_src')
        icecast_queue2 = gst.element_factory_make('queue','icecast_queue2')
        icecast_audioconvert = gst.element_factory_make('audioconvert','icecast_audioconvert')
        icecast_audio_codec = gst.element_factory_make(self.icecast_audio_codec,'icecast_audio_codec')
        icecast_audio_codec.set_property('quality',0.2)
        icecast_queue3 = gst.element_factory_make('queue','icecast_queue3')
        icecast_queue4 = gst.element_factory_make('queue','icecast_queue4')

        self.player.add(icecast,
                        icecast_queue,
                        icecast_queue2,
                        icecast_queue3,
                        icecast_queue4,
                        icecast_colorspace,
                        icecast_video_codec,
                        icecast_muxer,
                        icecast_audio_src,
                        icecast_audioconvert,
                        icecast_audio_codec,
                        icecast_scale,
                        icecast_scale_cap)

        gst.element_link_many(self.src_tee,
                              icecast_queue,
                              icecast_colorspace,
                              icecast_scale,
                              icecast_scale_cap,
                              icecast_video_codec,
                              icecast_muxer)

        gst.element_link_many(icecast_audio_src,
                              icecast_queue2,
                              icecast_audioconvert,
                              icecast_audio_codec,
                              icecast_queue3,
                              icecast_muxer,
                              icecast_queue4,
                              icecast)

    def _clear_icecast_streaming(self):
        '''
        Clears the icecast stream pipeline
        '''
        icecast = self.player.get_by_name('icecast')
        icecast_queue = self.player.get_by_name('icecast_queue')
        icecast_queue2 = self.player.get_by_name('icecast_queue2')
        icecast_queue3 = self.player.get_by_name('icecast_queue3')
        icecast_queue4 = self.player.get_by_name('icecast_queue4')
        icecast_colorspace = self.player.get_by_name('icecast_colorspace')
        icecast_audio_src = self.player.get_by_name('icecast_audio_src')
        icecast_audioconvert = self.player.get_by_name('icecast_audioconvert')
        icecast_audio_codec = self.player.get_by_name('icecast_audio_codec')
        icecast_scale = self.player.get_by_name('icecast_scale')
        icecast_scale_cap = self.player.get_by_name('icecast_scale_cap')
        icecast_video_codec = self.player.get_by_name('icecast_video_codec')
        icecast_muxer = self.player.get_by_name('icecast_muxer')

        self.player.remove(icecast,
                        icecast_queue,
                        icecast_queue2,
                        icecast_queue3,
                        icecast_queue4,
                        icecast_colorspace,
                        icecast_video_codec,
                        icecast_muxer,
                        icecast_audio_src,
                        icecast_audioconvert,
                        icecast_audio_codec,
                        icecast_scale,
                        icecast_scale_cap)

    ###
    ### Framework Required Functions
    ###
    def test_feedback_start(self, video=False, audio=False):
        self.test_video = video
        self.test_audio = audio
        
        if self.test_video == True:
            self._set_video_source()
            self._set_video_feedback()

        if self.test_audio == True:
            self._set_audio_source()
            self._set_audio_feedback()

        self.player.set_state(gst.STATE_PLAYING)

    def test_feedback_stop(self):
        self.player.set_state(gst.STATE_NULL)
        
        if self.test_video == True:
            self._clear_video_source()
            self._clear_video_feedback()
            
        if self.test_audio == True:
            self._clear_audio_source()
            self._clear_audio_feedback()

        del self.test_video
        del self.test_audio

    def populate_metadata(self, data):
        '''
        Populate global tag list variable with file metadata for
        vorbistag audio element
        '''
        self.tags = gst.TagList()

        for tag in data.keys():
            if(gst.tag_exists(tag)):
                self.tags[tag] = data[tag]
            else:
                self.core.logger.log.debug("WARNING: Tag \"" + str(tag) + "\" is not registered with gstreamer.")

    def record(self, filename):
        '''
        Start recording to a file.

        filename: filename to record to
        '''
        self.filename = filename
        self._set_muxer(filename)

        if self.record_video == True:
            self._set_video_source()
            self._set_video_encoder()

            if self.recording_video_feedback == True:
                self._set_video_feedback()

            if self.record_desktop_area == True:
                self._set_recording_area()

        if self.record_audio == True:
            self._set_audio_source()
            self._set_audio_encoder()

            if self.recording_audio_feedback == True:
                self._set_audio_feedback()
                
        if self.icecast == True:
            self._set_icecast_streaming()
            
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

            if self.recording_audio_feedback == True:
                self._clear_audio_feedback()

        if self.icecast == True:
            self._clear_icecast_streaming()

    def get_video_sources(self):
        '''
        Returns the supported video sources by this backend.
        '''
        return ['desktop', 'usb', 'firewire']

    def get_video_devices(self, videosrc):
        '''
        Returns the supported video devices by this backend.
        '''
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

    def _get_devices(self, path, index):
        '''
        Returns devices that are found to exist.
        '''
        i = index
        devices = []
        devpath=path + str(i)

        while os.path.exists(devpath):
            i=i+1
            devices.append(devpath)
            devpath=path + str(i)

        return devices

    def get_audio_sources(self):
        '''
        Returns the supported audio sources by this backend.
        '''
        snd_sources_list = ['pulsesrc', 'alsasrc', 'autoaudiosrc']

        snd_sources = []
        for src in snd_sources_list:
            try:
                gst.element_factory_make(src, 'testsrc')
                snd_sources.append(src)
                self.core.logger.log.debug(src + ' is available.')
            except:
                self.core.logger.log.debug(src + ' is not available')

        return snd_sources

    def change_video_source(self, source_type, source_device):
        '''
        Changes the video source
        '''
        self.video_source_type = source_type
        self.video_device = source_device

        if (source_type == 'desktop'):
            if os.name == 'posix':
                self.video_source = 'ximagesrc'
            elif os.name == 'nt':
                self.video_source = 'dx9screencapsrc'
        elif (source_type == 'usb'):
            if os.name == 'posix':
                self.video_source = 'v4l2src'
            elif os.name == 'nt':
                self.video_source = 'dshowvideosrc'
        elif (source_type == 'usb_fallback'):
            self.video_source = 'v4lsrc'
        elif (source_type == 'firewire'):
            self.video_source = 'dv1394src'

    def set_record_area(self, enabled):
        self.record_desktop_area = enabled

    def set_recording_area(self, start_x, start_y, end_x, end_y):
        '''
        Sets the area on the desktop to be recorded.
        '''
        self.record_desktop_area_start_x = start_x
        self.record_desktop_area_start_y = start_y
        self.record_desktop_area_end_x = end_x
        self.record_desktop_area_end_y = end_y

    def change_output_resolution(self, width, height):
        '''
        Sets the resolution of the recorded video.
        '''
        self.recording_width = width
        self.recording_height = height
        # If streaming is being done, reset the bitrate according to the new resolution
        if self.icecast:
            self.change_stream_resolution(self.icecast_width, self.icecast_height, width, height)
    
    def change_stream_resolution(self, width, height, record_width, record_height):
        '''
        Sets the resolution of the streamed video, and attempts to choose the ideal bitrate for the given resolutions.
        '''
        # The dictionary bitmap contains a mapping from known pairing of stream resolution
        # and recording resolution to the ideal bitrate as determined by testing.
        # It uses a string of form <stream_width>,<record_width> (i.e., '320,640') to uniquely identify combinations
        bitmap = {  '320,640': 400, '320,800': 400, '320,1024': 400,    # bit rates for 320x240 stream
                    '480,640': 800, '480,800': 800, '480,1024': 350,    # bit rates for 480x360 stream
                    '640,640': 1250, '640,800': 1000, '640,1024': 500,  # bit rates for 640x480 stream
                    '800,640': 1250, '800,800': 1000, '800,1024': 750   # bit rates for 800x600 stream
                 }                  
        
        # If the pairing cannot be found, we back off to the average best bitrate at each resolution
        default_bitmap = { 320: 400, # resolution of 320x240 - 400 kbps
                            480: 500, # resolution of 480x360 - 500 kbps
                            640: 750, # resolution of 640x480 - 750 kbps
                            800: 1000 # resolution of 800x600 - 1000 kbps
        }

        # Creates the string of the pairing <stream width>,<record width>
        stream_rec_pair = str(width) + ',' + str(record_width)

        # Sets the width & height of streaming
        self.icecast_width = width
        self.icecast_height = height

        # If the pairing is found in bitmap, use the given bitrate
        if stream_rec_pair in bitmap:         
            self.icecast_vidbitrate = bitmap[stream_rec_pair]
        elif self.icecast_width in default_bitmap:              # Else, if the stream resolution is in default_bitmap, use that bitrate
            self.icecast_vidbitrate = default_bitmap[width]
        else:                                                   # If pairing not in default_bitmap, use default value of 1000
            self.icecast_vidbitrate = 1000                      

    def change_audio_source(self, new_source):
        '''
        Changes the audio source
        '''

        # Ensure the new sound source is valid
        try:
            self.core.logger.log.debug('loading ' + new_source)
            gst.element_factory_make(new_source, 'test_src')
        except:
            self.core.logger.log.debug('Failed to load ' + new_source + '.')
            return False

        self.audio_source = new_source
        self.core.logger.log.debug(self.audio_source + ' loaded.')
        return True

    def set_video_mode(self, mode):
        '''
        Activates video recording when mode = True
        Disables video recording when mode = False
        '''
        self.record_video = mode

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

    def set_audio_mode(self, mode):
        '''
        Activates audio recording when mode = True
        Disables audio recording when mode = False
        '''
        self.record_audio = mode

    def enable_audio_feedback(self):
        '''
        Activate audio feedback.
        Will send the recorded audio back out the speakers.
        '''
        self.recording_audio_feedback = True

    def disable_audio_feedback(self):
        '''
        Disable the audio feedback.
        '''
        self.recording_audio_feedback = False
        
    def enable_icecast_streaming(self, ip='127.0.0.1',
                                       port=8000,
                                       password='hackme',
                                       mount='freeseer.ogg', resolution='320x240'):
        self.icecast = True
        self.icecast_ip = ip
        self.icecast_port = port
        self.icecast_password = password
        self.icecast_mount = mount
        res = resolution.split('x')
        self.change_stream_resolution(res[0], res[1], self.recording_width, self.recording_height)
        self.core.logger.log.debug(u"Icecast streaming enabled")

    def disable_icecast_streaming(self):
        self.icecast = False
        self.core.logger.log.debug(u"Icecast streaming disabled")
