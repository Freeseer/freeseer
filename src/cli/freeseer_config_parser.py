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
import freeseer.framework.presentation
import getpass



from freeseer.framework.core import FreeseerCore
from freeseer.framework.presentation import Presentation

class FreeSeerConfigParser(argparse.ArgumentParser):
    def __init__(self):
        argparse.ArgumentParser.__init__(self)
        
        self.core = FreeseerCore(self)  
        self.db_connector = self.core.db 
        self.config = self.core.config 
        
        self.RESOLUTION_LIST = ['240p','360p','480p','720p','1080p']
        
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
                self.set_video_source(int(namespace.index))     
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
            
        elif (mode == "video on"):
            self.turn_video_on()
            
        elif (mode == "video off"):
            self.turn_video_off()
                
        else:
            print "*** Unknown mode, please type one of the available modes or type 'help talk' to see all available modes"
             
            

                
    def show_all_configs(self):
        print "-------------------------- Settings --------------------------------"
        print " ###################### Video Settings ############################"
        print "Available Video Sources: "
        for videosrc in self.core.get_video_sources():
            print ">>> " + videosrc
        print "Current Video Source: " + self.config.videosrc
        print "Current Video Resolution " + self.config.resolution
        print " ###################### Audio Settings ############################"
        print "Available Audio Sources: "
        for audiosrc in self.core.get_audio_sources():
            print ">>> " + audiosrc
        print "Current Audio Source: " + self.config.audiosrc
        print "Audio Feedback Activated: " + self.config.audiofb
        print " ##################### General Settings ###########################"
        print "Current record hotkey: "+ self.config.key_rec
        print "Current stop hotkey: " + self.config.key_stop
        print "Current video dir: " + self.config.videodir
        print "Current config file " + self.config.configfile
        print "Auto-Hide enabled: " + str(self.config.auto_hide)
        print " #################### Streaming Settings ##########################"
        print "Streaming enabled: " + str(self.config.enable_streaming)
        print "Streaming resolution: " + self.config.streaming_resolution
        print "Streaming mount: " + self.config.streaming_mount
        print "Streaming port: " + self.config.streaming_port
        print "Streaming password: " + self.config.streaming_password
        print "Streaming url: " + self.config.streaming_url
        
    def show_all_video_configs(self):
        count = 1
        print "################## Available Video Sources ##################"
        for videosrc in self.core.get_video_sources():
            print "#" + str(count) + " " + videosrc
            count+=1
            
    def show_video_source_info(self, index):
        try:
            videosrc_selected = self.core.get_video_sources()[index-1]
        
            if(videosrc_selected == "desktop"):
                print "############ Video Source Selected: Desktop ############"
                print "Get Desktop Info"
            elif(videosrc_selected == "usb"):
                print "############ Video Source Selected: USB ############"
                print "GetUSB Info"
            elif(videosrc_selected == "firewire"):
                print "############ Video Source Selected: Firewire ############"
                print "Get Firewire Info"
        except:
            print "There's no video source with this specified index" 
        
    def set_video_source(self, index):
        try:
            videosrc_selected = self.core.get_video_sources()[index-1]
            self.config.videosrc = videosrc_selected
            self.config.writeConfig()
        except:
            print "There's no video source with this specified index" 
            
    def show_all_resolutions(self):
        count = 1
        print "############## Screen Resolutions #################"
        for res in self.config.resmap.keys():
            print "#" + str(count) + " " + res + ": " + self.config.resmap[res]
            count+=1
    
    def set_video_resolution(self, index):
        resolution_selected = self.config.resmap[self.RESOLUTION_LIST[index-1]]
        self.config.resolution = resolution_selected
        self.config.writeConfig()
        
    def show_all_audio_configs(self):
        count = 1
        print "################## Available Audio Sources ##################"
        for videosrc in self.core.get_audio_sources():
            print "#" + str(count) + " " + videosrc
            count+=1
            
    def show_audio_source_info(self, index):
        try:
            videosrc_selected = self.core.get_audio_sources()[index-1]
        
            if(videosrc_selected == "pulsesrc"):
                print "########## Audio Source Selected: PulseSrc ##########"
                print "Get pulsesrc Info"
            elif(videosrc_selected == "alsasrc"):
                print "########### Audio Source Selected: AlsaSrc ##########"
                print "Get alsasrc Info"
            elif(videosrc_selected == "autoaudiosrc"):
                print "######## Audio Source Selected: AutoAudiorc #########"
                print "Get autoaudiosrc Info"
        except:
            print "There's no audio source with this specified index" 
            
    def set_audio_source(self, index):
        try:
            audiosrc_selected = self.core.get_audio_sources()[index-1]
            self.config.audiosrc = audiosrc_selected
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
        self.config.enable_video_recoding_recoding = True
        self.config.writeConfig()
        
    def turn_video_off(self):
        self.config.enable_video_recoding_recoding = False    
        self.config.writeConfig()  
    
    def _is_valid_path(self, path):
        return os.path.exists(os.path.expanduser(os.path.dirname(path)))
    
    def _get_mode(self, mode_list):
        mode = ""
        for item in mode_list:
            mode += item + " "
        return mode[0:len(mode)-1]
        
    
        
            
                    
            
        
            
            
    
            
        
            
         