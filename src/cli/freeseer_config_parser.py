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
import re
import getpass

from freeseer.framework.core import FreeseerCore
from freeseer.framework.presentation import Presentation

class FreeSeerConfigParser(argparse.ArgumentParser):
    def __init__(self, core):
        argparse.ArgumentParser.__init__(self)
        
        self.core = core 
        self.plugman = self.core.get_plugin_manager()
        self.db_connector = self.core.db 
        self.config = self.core.config 
        
        self.RESOLUTION_LIST = ['480p','360p','1080p','240p','720p']
        self.VIDEO_MIXERS = [plugin.name for plugin in self.plugman.plugmanc.getPluginsOfCategory("VideoMixer")]
        self.AUDIO_MIXERS = [plugin.name for plugin in self.plugman.plugmanc.getPluginsOfCategory("AudioMixer")]
        self.VIDEO_INPUTS = [plugin.name for plugin in self.plugman.plugmanc.getPluginsOfCategory("VideoInput")]
        self.AUDIO_INPUTS = [plugin.name for plugin in self.plugman.plugmanc.getPluginsOfCategory("AudioInput")]
        self.OUTPUT_PLUGINS = [plugin.name for plugin in self.plugman.plugmanc.getPluginsOfCategory("Output")]
        
        
        self.add_argument('mode',nargs = '+', metavar='talk mode')
        
        self.add_argument('-i', dest='index',type=str)
        self.add_argument('-u', dest='url', type=str)
        self.add_argument('-f', dest='filename', type=str)
        self.add_argument('-p', dest='password', type=str)
        self.add_argument('-d', dest='directory', type=str)
        
        self.add_argument('--all', dest='all', action='store_const',const=True, default=False)  
          
        
    
    def analyse_command(self, command):  
        '''
        Analyses the command typed by the user
        '''     
        namespace = self.parse_args(command.split())   
        
        mode = self._get_mode(namespace.mode)    
        print mode 
        
        if(mode == "show"):
            if(namespace.all):
                self.show_all_configs()
            else:
                print "*** Option missing"  
            
        elif (mode == "video show"):
            if(namespace.all):
                self.show_all_video_configs()
            elif(namespace.index):
                self.show_video_source_info(int(namespace.index))     
            else:
                print "*** Option missing"  
                
        elif (mode == "video set"):
            if(namespace.index):
                self.set_video_mixer(int(namespace.index))     
            else:
                print "*** Option missing" 
                
        elif (mode == "video resolution show"):
            self.show_all_resolutions()
            
        elif (mode == "video resolution set"):
            if(namespace.index):
                self.set_video_resolution(int(namespace.index))     
            else:
                print "*** Please specify the resolution index" 
                
        elif (mode == "audio show"):
            if(namespace.all):
                self.show_all_audio_configs()
            elif(namespace.index):
                self.show_audio_source_info(int(namespace.index))     
            else:
                print "*** Option missing"  
                
        elif (mode == "audio set"):
            if(namespace.index):
                self.set_audio_source(int(namespace.index))     
            else:
                print "*** Option missing"
                
                
        elif (mode == "streaming show"):
            self.show_streaming_settings()
            
        elif (mode == "streaming port show"):
            self.show_streaming_port()
            
        elif (mode == "streaming port set"):
            if(namespace.index):
                self.set_streaming_port(int(namespace.index))     
            else:
                print "*** Option missing"
                
        elif (mode == "streaming url show"):
            self.show_streaming_url()
            
        elif (mode == "streaming port set"):
            if(namespace.url):
                self.set_streaming_url((namespace.url))     
            else:
                print "*** Option missing"
                
        elif (mode == "streaming mount show"):
            self.show_streaming_mount()
            
        elif (mode == "streaming mount set"):
            if(namespace.filename):
                self.set_streaming_mount((namespace.filename))     
            else:
                print "*** Option missing"
                
        elif (mode == "streaming password show"):
            self.show_streaming_password()
            
        elif (mode == "streaming password set"):
            self.set_streaming_password()  
            
        elif (mode == "streaming resolution show"):
            self.show_streaming_resolution()
            
        elif (mode == "streaming resolution set"):
            if(namespace.index):
                self.set_streaming_resolution((namespace.index))     
            else:
                print "*** Option missing"  
        
        elif (mode == "dir show"):
            self.show_output_dir()
        elif (mode == "dir set"):
            if(namespace.directory):
                self.set_output_dir(namespace.directory)    
            else:
                print "*** Option missing" 
                
        elif (mode == "audio on"):
            self.turn_audio_on()
            
        elif (mode == "audio off"):
            self.turn_audio_off()
            
        elif(mode == "audio feedback off"):
            self.turn_audiofeedback_off()
            
        elif(mode == "audio feedback on"):
            self.turn_audiofeedback_on()
            
        elif (mode == "video on"):
            self.turn_video_on()
            
        elif (mode == "video off"):
            self.turn_video_off()
            
        elif (mode == "file on"):
            self.turn_file_record_off()
        
        elif (mode == "file off"):
            self.turn_file_record_on()
        
        elif (mode == "streaming on"):
            print "veio"
            self.turn_streaming_on()
            
        elif (mode == "streaming off"):
            self.turn_streaming_off()
                
        else:
            print "*** Unknown mode, please type one of the available modes or type 'help talk' to see all available modes"
                           
    def show_all_configs(self):
        self._show_video_configs()
        self._show_audio_config()
        self._show_output_configs()
        
    def show_all_video_configs(self):
        self._show_video_configs()
            
        
    def set_video_mixer(self, index):
        try:
            video_mixer_selected = self.VIDEO_MIXERS[index-1]
            self.config.videomixer = video_mixer_selected
            self.config.writeConfig()
        except:
            print "There's no video mixer plugin with this specified index" 
            
    def show_all_resolutions(self):
        self._show_resolutions()
    
    def set_video_resolution(self, index):
        resolution_selected = self.config.resmap[self.RESOLUTION_LIST[index-1]]
        self.config.resolution = resolution_selected
        self.config.writeConfig()
        
    def show_all_audio_configs(self):
        self._show_audio_config()
            
    def show_audio_source_info(self, index):
        try:
            videosrc_selected = self.core.get_audio_sources()[index-1]
        
            if(videosrc_selected == "pulsesrc"):
                print "########## Audio Source Selected: PulseSrc ##########"
                print "Get pulsesrc Info"
            elif(videosrc_selected == "alsvideo_mixer_selectedasrc"):
                print "########### Audio Source Selected: AlsaSrc ##########"
                print "Get alsasrc Info"
            elif(videosrc_selected == "autoaudiosrc"):
                print "######## Audio Source Selected: AutoAudiorc #########"
                print "Get autoaudiosrc Info"
        except:
            print "There's no audio source with this specified index" 
            
    def set_audio_mixer(self, index):
        try:
            audio_mixer_selected = self.AUDIO_MIXERS[index-1]
            self.config.audio = audio_mixer_selected
            self.config.writeConfig()
        except:
            print "There's no video source with this specified index"
            
    def show_streaming_settings(self):
        print " #################### Streaming Settings ##########################"
        print "Streaming enabled: " + str(self.config.enable_streaming)
        print "Streaming resolution: " + self.config.streaming_resolution
        print "Streaming mount: " + self.config.streaming_mount
        print "Streaming port: " + self.config.streaming_port
        print "Streaming password: " + self.config.streaming_password
        print "Streaming url: " + self.config.streaming_url
        
    def show_streaming_port(self):
        print "Streaming port: " + self.config.streaming_port
        
    def set_streaming_port(self, port):
        self.config.streaming_port = port
        self.config.writeConfig()
        
    def show_streaming_url(self):
        print "Streaming url: " + self.config.streaming_url
        
    def set_streaming_url(self, url):
        self.config.streaming_url = url
        self.config.writeConfig()
        
    def show_streaming_mount(self):
        print "Streaming mount: " + self.config.streaming_mount
        
    def set_streaming_url(self, mount):
        self.config.streaming_mount = mount
        self.config.writeConfig()
        
    def show_streaming_password(self):
        print "Streaming password: " + self.config.streaming_password
        
    def set_streaming_password(self):
        new_password = getpass.getpass("Type the new password: ")
        self.config.streaming_password = new_password
        self.config.writeConfig()
        
    def show_streaming_resolution(self):
        self.show_all_resolutions()
        
    def set_streaming_resolution(self, index):
        resolution_selected = self.config.resmap[self.RESOLUTION_LIST[index-1]]
        self.config.streaming_resolution = resolution_selected
        self.config.writeConfig()
        
    def show_output_dir(self):
        print "Output dir: " + self.config.videodir
        
    def set_output_dir(self, path):
        if(self._is_valid_path(path)):
            self.config.videodir = path
            self.config.writeConfig()
        else:
            print "'" + path + "' is not an available path"      
            
    def turn_audio_off(self):
        self.config.enable_audio_recoding = False
        self.config.writeConfig()
        
    def turn_audio_on(self):
        self.config.enable_audio_recoding = True
        self.config.writeConfig()
        
    def turn_video_on(self):
        self.config.enable_video_recoding = True
        self.config.writeConfig()
        
    def turn_video_off(self):
        self.config.enable_video_recoding = False
        self.config.writeConfig() 
        
    def turn_audiofeedback_off(self):
        self.config.audio_feedback = False
        self.config.writeConfig() 
        
    def turn_audiofeedback_on(self):
        self.config.audio_feedback = True
        self.config.writeConfig() 
        
    def turn_file_record_on(self):
        self.config.record_to_file = True
        self.config.writeConfig()
        
    def turn_file_record_off(self):
        self.config.record_to_file = False
        self.config.writeConfig()
    
    def turn_streaming_on(self):
        self.config.record_to_stream = True
        self.config.writeConfig()
        
    def turn_streaming_off(self): 
        self.config.record_to_stream = False
        self.config.writeConfig()   
    
    
    def _show_video_configs(self):
        print "-------------------------- Settings --------------------------------"
        print " ###################### Video Settings ############################"
        print "Video recoding enabled: Yes" if self.config.enable_video_recoding else "Video recoding enabled: No"
        print "Current Video Mixer: " + self.config.videomixer
        print "Available Video Mixers Plugins: "
        count = 1
        for video_mixer in self.plugman.plugmanc.getPluginsOfCategory("VideoMixer"):
            print "%d - %s" % (count, video_mixer.name)
            count += 1
        count = 1    
        print "Available Video Input Plugins: "
        for video_input in self.plugman.plugmanc.getPluginsOfCategory("VideoInput"):
            print "%d - %s" % (count, video_input.name)  
            count += 1      
        print "Current Video Resolution " + self.config.resolution
        print "Available Video Resolutions: "
        self._show_resolutions()
        print "Video preview enabled: Yes" if self.config.video_preview else "Video preview enabled: No"
        
    def _show_audio_config(self):
        print " ###################### Audio Settings ############################"        
        print "Audio recoding enabled: Yes" if self.config.enable_audio_recoding else "Audio recoding enabled: No"
        print "Available Audio Mixers: " 
        count = 1       
        for audio_mixer in self.plugman.plugmanc.getPluginsOfCategory("AudioMixer"):
            print "%d - %s" % (count, audio_mixer.name)  
            count += 1
        print "Current Audio Mixer: " + self.config.audiomixer
        print "Audio feedback enabled: Yes" if self.config.audio_feedback else "Audio feedback enabled: No"        
        
    def _show_output_configs(self):           
        print " ###################### Output Settings ############################"      
        print "Video Directory: " + self.config.videodir   
        print "Recording to File: Yes" if self.config.record_to_file else "Recording to File: No" 
        if self.config.record_to_file:
            print "Current record to file plugin: " + self.config.record_to_file_plugin
        count = 1
        print "Streaming: Yes" if self.config.record_to_stream else "Streaming: No"
        if self.config.record_to_stream:
            print "Current record to stream plugin: " + self.config.record_to_stream_plugin
        
    def _show_resolutions(self):
        count = 1
        for key in self.config.resmap:
             print "%d - %s:%s" % (count, key, self.config.resmap[key])
             count += 1
    def _show_video_mixers(self):
        count = 1
        for video_mixer in self.plugman.plugmanc.getPluginsOfCategory("VideoMixer"):
            print "%d - %s" % (count, video_mixer.name)
            count += 1
        
    def _is_valid_path(self, path):
        return os.path.exists(os.path.expanduser(path))
    
    def _get_mode(self, mode_list):
        mode = ""
        for item in mode_list:
            mode += item + " "
        return mode[0:len(mode)-1]        