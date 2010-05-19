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
# http://wiki.github.com/fosslc/freeseer/

import codecs
import datetime
import time
import logging
import logging.config
import os
 
from backend.gstreamer import *
from framework.config import Config
from framework.logger import Logger

__version__=u'1.9.7'

class FreeseerCore:
    '''
    Freeseer core logic code.  Used to link a GUI frontend with a recording backend such as backend.gstreamer
    '''
    def __init__(self, ui):
        self.ui = ui
        
        # Read in config information
        configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
        self.config = Config(configdir)
        self.logger = Logger(configdir)

        # Start Freeseer Recording Backend
        self.freeseer = Freeseer_gstreamer(self)
        resolution = self.config.resolution.split('x')
        self.change_output_resolution(resolution[0], resolution[1])
        
        self.spaces = False
        self.logger.log.info(u"Core initialized")

    def get_video_devices(self, device_type):
        '''
        Returns available video devices.
        '''
        viddevs = self.freeseer.get_video_devices(device_type)
        self.logger.log.debug('Available video devices for ' + device_type + ': ' + str(viddevs))
        return viddevs

    def get_video_sources(self):
        '''
        Returns supported video sources.
        '''
        vidsrcs = self.freeseer.get_video_sources()
        self.logger.log.debug('Available video sources: ' + str(vidsrcs))
        return vidsrcs

    def get_audio_sources(self):
        '''
        Returns supported audio sources.
        '''
        sndsrcs = self.freeseer.get_audio_sources()
        self.logger.log.debug('Available audio sources: ' + str(sndsrcs))
        return sndsrcs

    def get_talk_titles(self):
        '''
        Returns the talk titles as listed in  talks.txt
        '''
        talk_titles = []
        try:
            f = codecs.open(self.config.talksfile, 'r', 'utf-8')
        except:
            self.logger.log.debug('talks.txt not found, creating default.')
            f = codecs.open(self.config.talksfile, 'w', 'utf-8')
            f.writelines('T103 - Thanh Ha - Intro to Freeseer')
            f.close()
            f = codecs.open(self.config.talksfile, 'r', 'utf-8')
            
        lines = f.readlines()
        f.close()

        for line in lines:
            talk_titles.append(line.rstrip())

        self.logger.log.debug('Available talk titles:')
        for talk in talk_titles:
            self.logger.log.debug('  ' + talk.encode('utf-8'))
        return talk_titles

    def save_talk_titles(self, talk_list):
        '''
        Saves the talk titles received by talk_list variable.

        talk_list: a list of talk titles which will be saved..
        '''
        f = codecs.open(self.config.talksfile, 'w', 'utf-8')
        f.writelines(talk_list)
        f.close()
        self.logger.log.debug('Saved talks to file')

    def get_record_name(self, filename):
        '''
        Returns the filename to use when recording.
        This function checks to see if a file exists and increments index until a filename that does not exist is found
        '''
        recordname = self.make_record_name(filename)
        self.logger.log.debug('Set record name to ' + recordname)
        return recordname

    def make_record_name(self, filename):
        ''' Insert date and index to a filename '''
        date = datetime.date.today()
        recordname = date.isoformat() + ' - ' + time.strftime('%H%M') + ' - ' + filename + '.ogg'
        if self.spaces == False:
            recordname = recordname.replace(' ', '_')
        return recordname

    def change_videosrc(self, vid_source, vid_device):
        ''' Informs backend of new video source to use when recording. '''
        self.freeseer.change_videosrc(vid_source, vid_device)
        self.logger.log.debug('Video source changed to ' + vid_source + ' using ' + vid_device)

    def set_recording_area(self, x1, y1, x2, y2):
        self.freeseer.set_recording_area(x1, y1, x2, y2)

    def change_output_resolution(self, width, height):
        self.freeseer.change_output_resolution(width, height)
        self.logger.log.debug('Video output resolution changed to ' + width + 'x' + height)

    def change_soundsrc(self, snd_source):
        ''' Informs backend of new audio source to use when recording. '''
        return self.freeseer.change_soundsrc(snd_source)

    def record(self, filename='default'):
        '''
        Informs backend to begin recording to filename.
        '''
        record_name = self.get_record_name(str(filename))
        record_location = os.path.abspath(self.config.videodir + '/' + record_name)
        self.freeseer.record(record_location)
        self.logger.log.info('Recording started')

    def stop(self):
        ''' Informs backend to stop recording. '''
        self.freeseer.stop()
        self.logger.log.info('Recording stopped')

    def preview(self, enable=False, window_id=None):
        ''' Enable/Disable the video preview window. '''
        if enable == True:
            self.freeseer.enable_preview(window_id)
            self.logger.log.info('Video Preview Activated')
        else:
            self.logger.log.info('Video Preview Deactivated')

    def audioFeedback(self, enable=False):
        ''' Enable/Disable the audio preview. '''
        if enable == True:
            self.freeseer.enable_audio_feedback()
            self.logger.log.info('Audio Feedback Activated')
        else:
            self.freeseer.disable_audio_feedback()
            self.logger.log.info('Audio Feedback Deactivated')

    def audioFeedbackEvent(self, percent):
        event_type = 'audio_feedback'
        self.ui.coreEvent(event_type, percent)
