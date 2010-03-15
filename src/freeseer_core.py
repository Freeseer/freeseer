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

import datetime

from freeseer_gstreamer import *

__version__=u'2.0'

class FreeseerCore:
    '''
    Freeseer core logic code.  Used to link a GUI frontend with a recording backend such as freeseer_gstreamer.py
    '''
    def __init__(self):
        self.freeseer = Freeseer()
        self.spaces = False

    def get_video_devices(self, device_type):
        '''
        Returns available video devices.
        '''
        return self.freeseer.get_video_devices(device_type)

    def get_video_sources(self):
        '''
        Returns supported video sources.
        '''
        return self.freeseer.get_video_sources('all')

    def get_audio_sources(self):
        '''
        Returns supported audio sources.
        '''
        return self.freeseer.get_audio_sources()

    def get_talk_titles(self):
        '''
        Returns the talk titles as listed in  talks.txt
        '''
        talk_titles = []
        f = open('talks.txt', 'r')
        lines = f.readlines()
        f.close()

        for line in lines:
            talk_titles.append(line.rstrip())
        return talk_titles

    def save_talk_titles(self, talk_list):
        '''
        Saves the talk titles received by talk_list variable.

        talk_list: a list of talk titles which will be saved..
        '''
        f = open('talks.txt', 'w')
        f.writelines(talk_list)
        f.close()

    def get_record_name(self, filename):
        '''
        Returns the filename to use when recording.
        This function checks to see if a file exists and increments index until a filename that does not exist is found
        '''
        i = 0
        recordname = self.make_record_name(filename, i)
        while os.path.exists(recordname):
            i=i+1
            recordname = self.make_record_name(filename, i)
        return recordname

    def make_record_name(self, filename, index):
        ''' Insert date and index to a filename '''
        date = datetime.date.today()
        recordname = date.isoformat() + ' ' + filename + ' (' + str(index) + ').ogg'
        if self.spaces == False:
            recordname = recordname.replace(' ', '_')
        return recordname

    def change_videosrc(self, vid_source, vid_device):
        ''' Informs backend of new video source to use when recording. '''
        self.freeseer.change_videosrc(vid_source, vid_device)
        print 'video source changed to ' + vid_source + ' using ' + vid_device

    def change_soundsrc(self, snd_source):
        ''' Informs backend of new audio source to use when recording. '''
        return self.freeseer.change_soundsrc(snd_source)

    def record(self, filename='default'):
        '''
        Informs backend to begin recording to filename.
        '''
        recordname = self.get_record_name(filename)
        self.freeseer.record(recordname)

    def stop(self):
        ''' Informs backend to stop recording. '''
        self.freeseer.stop()

    def preview(self, enable=False, window_id=None):
        ''' Enable/Disable the video preview window. '''
        if enable == True:
            self.freeseer.enable_preview(window_id)
            print 'Preview Activated'
        else:
            print 'Preview Deactivated'

    def audioFeedback(self, enable=False):
        ''' Enable/Disable the audio preview. '''
        if enable == True:
            self.freeseer.enable_audio_feedback()
            print 'Audio Feedback Activated'
        else:
            self.freeseer.disable_audio_feedback()
            print 'Audio Feedback Deactivated'
