#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011  Free and Open Source Software Learning Centre
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

import argparse

import sys,os

from freeseer.framework.core import FreeseerCore

class FreeSeerRecordParser(argparse.ArgumentParser):
    def __init__(self):  
        self.core = FreeseerCore(self)          
        
        argparse.ArgumentParser.__init__(self)
        
        # command line arguments supported
        self.add_argument('-p',dest='id',type=int,
                          help='starts recording the talk with the specified presentation id')
        self.add_argument('-o',dest='path',type=str,
                          help="records the currently set video source (default:desktop) to a video file called" \
                          "myvideo.ogg in the /mypath directory.")
        
    def analyse_command(self, command):  
        '''
        Analyses the command typed by the user
        ''' 
        namespace = self.parse_args(command.split())
        self.perform_task(namespace)
            
    def perform_task(self, namespace):
        '''
        Perform the specific task typed by the user
        '''
        
        self.load_settings()        
           
        if(namespace.id):
            self.record_by_id(namespace.id)
        elif(namespace.path):
            self.record_by_path(namespace.path)
        else:
            self.default_record()
            
    def default_record(self):    
        '''
        Records to the default video folder a default filename
        '''                    
        self.core.record()
        print "\n Recording on progress, press <space> to stop \n"   
        
        while(self.getchar() != " "):            
            continue
        
        self.core.stop();
    
    def record_by_id(self,id):
        '''
        Records the presentation with the specified id
        '''        
        prs = self.db_connector.get_presentation(id)  
        if(prs):
            self.core.record(presentation=prs)   
            print "\n Recording on progress, press <space> to stop \n"          
      
            while(self.getchar() != " "):            
                continue
        
            self.core.stop();
        
        else:
            print "\n*** Error: There's no presentation with such id\n"
        
    def record_by_path(self,path):
        '''
        Records to the specific path
        '''        
        if self._is_valid_filename(path):
            self.core.record(record_location=path)
            print "\n Recording on progress, press <space> to stop \n"   

            while(self.getchar() != " "):            
                continue
        
            self.core.stop();                 
          
    def _is_valid_filename(self, path):
        if not path.endswith(".ogg"):
            print "\n*** Error: The file must be an ogg file\n"
            return False
        
        elif not self._is_valid_path(path):
            print "\n*** Error: This path doesn't exist\n"
            return False
        
        else:
            return True
        
    def _is_valid_path(self, path):
        return os.path.exists(os.path.expanduser(os.path.dirname(path)))

              
    def getchar(self):
        '''
        Gets the key pressed by the user
        '''        
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
        
    def load_settings(self): 
        '''
        Loads the video e audio settings required by the recording
        '''
        
        self.core.logger.log.info('loading setting...')

        #load the config file
        self.core.config.readConfig()

        #load enable_video_recoding setting
        if self.core.config.enable_video_recoding == False:
            self.core.set_video_mode(False)
        else:
            self.core.set_video_mode(True)
                        
            # load video source setting
            vidsrcs = self.core.get_video_sources()
            src = self.core.config.videosrc
            if src in vidsrcs:
                if (src == 'desktop'):
                    self.videosrc = 'desktop'
                    self.core.change_videosrc(self.videosrc, self.core.config.videodev)

                elif (src == 'usb'):
                    self.videosrc = 'usb'

                elif (src == 'firewire'):
                    self.videosrc = 'fireware'
                else:
                    self.core.logger.log.debug('Can NOT find video source: '+ src)
    
                if src == 'usb' or src == 'fireware':
                    dev = self.core.config.videodev
                    viddevs = self.core.get_video_devices(self.videosrc)

                    if dev in viddevs:
                        self.core.change_videosrc(self.videosrc, self.core.config.videodev)

                    else:
                        self.core.logger.log.debug('Can NOT find video device: '+ dev)
            self.core.set_audio_mode(False)