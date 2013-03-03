#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011-2013  Free and Open Source Software Learning Centre
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
# http://wiki.github.com/Freeseer/freeseer/

import argparse
import getpass
import os
import re
import sys

from freeseer.framework.presentation import Presentation

class FreeseerConfigParser(argparse.ArgumentParser):
    def __init__(self, config, db, plugman):
        argparse.ArgumentParser.__init__(self)
        
        self.config = config
        self.db = db
        self.plugman = plugman 
        self.plugins = self._get_plugins()
        
        self.RESOLUTION_LIST = self._get_resolution_list(self.config.resmap)
        self.VIDEO_MIXERS = [plugin.name for plugin in self.plugman.get_videomixer_plugins()]
        self.AUDIO_MIXERS = [plugin.name for plugin in self.plugman.get_audiomixer_plugins()]
        self.VIDEO_INPUTS = [plugin.name for plugin in self.plugman.get_videoinput_plugins()]
        self.AUDIO_INPUTS = [plugin.name for plugin in self.plugman.get_audioinput_plugins()]
        self.OUTPUT_PLUGINS = [plugin.name for plugin in self.plugman.get_output_plugins()]
        
        self.add_argument('mode',nargs = '+', metavar='talk mode')

    def analyse_command(self, command):  
        '''
        Analyses the command typed by the user
        '''     
        namespace = self.parse_args(command.split())   
        
        mode = self._get_mode(namespace.mode)
        config_mode = mode.split(" ")[0]        
        
        if(config_mode == "show"):
            try:
                show_mode = mode.split(" ")[1]
            except:
                print "*** Please provide the show mode. To see all available modes type'help config show'"
                return 
            
            if(show_mode == "all"):
                self.show_all_configs()
            elif(show_mode == "video"):
                self.show_all_video_configs()
            elif(show_mode == "audio"):
                self.show_all_audio_configs()      
                          
            #Plugin support
            else:
                args = mode.split(" ")                
                try:     
                    if(len(args) == 2):
                            for plugin in self.plugman.get_plugins_of_category(args[1]):
                                print plugin.name.replace(" ","")
                            return               
                    plugin_name = self.get_plugin_name(args[2])
                    plugin = self.plugman.get_plugin_by_name(plugin_name, category=args[1])
                    if plugin:
                        plugin.plugin_object.load_config(self.plugman)
                        if(len(args) == 3):                
                            try:
                                for property in plugin.plugin_object.get_properties():
                                    print property
                            except NotImplementedError:
                                print "This plugin is not supported by CLI"
                        elif(len(args) == 4):
                            try:
                                print plugin.plugin_object.get_property_value(args[3])
                            except NotImplementedError:
                                print "This plugin is not supported by CLI"
                        elif(len(args) == 5):
                            try:
                                plugin.plugin_object.set_property_value(args[3], args[4])
                            except NotImplementedError:
                                print "This plugin is not supported by CLI"
                    else:
                        print "There's no plugin with such informations"
                except IndexError:
                    print "*** Invalid Syntax"
                except KeyError:
                    print "*** There's no category with such name"
            
        elif(config_mode == "set"):
            try:
                set_mode = mode.split(" ")[1]
            except:
                print "*** Please provide the set mode. To see all available modes type'help config set'"
                return 
            try:
                set_value = mode.split(" ")[2]
            except:
                print "*** Please provide the set value"
                return 
            

            if (set_mode == "video" ):
                try:
                    self.set_video_mixer(int(set_value))
                except:
                    if(set_value == "on"):
                        self.turn_video_on()                
                    elif (set_value == "off"):
                        self.turn_video_off()
                    else:
                        print "*** Please provide property value as on/off"
                
            elif (set_mode == "resolution"):                
                self.set_video_resolution(int(set_value)) 
                

            elif (set_mode == "audio"):
                try:
                    self.set_audio_source(set_value)
                except:
                    if(set_value == "on"):
                        self.turn_audio_on()                
                    elif (set_value == "off"):
                        self.turn_audio_off()
                    else:
                        print "*** Please provide property value as on/off"
                
            elif (set_mode == "dir"):
                self.set_output_dir(set_value) 
                
            elif (set_mode == "feedback"):
                if(set_value == "on"):
                    self.turn_audiofeedback_on()                
                elif (set_value == "off"):
                    self.turn_audiofeedback_off()
                else:
                    print "*** Please provide property value as on/off"
                    
            elif (set_mode == "file"):
                if(set_value == "on"):
                    self.turn_file_record_on()                
                elif (set_value == "off"):
                    self.turn_file_record_off()
                else:
                    print "*** Please provide property value as on/off"
                    
            elif (set_mode == "streaming"):
                if(set_value == "on"):
                    self.turn_streaming_on()                
                elif (set_value == "off"):
                    self.turn_streaming_off()
                else:
                    print "*** Please provide property value as on/off"
            
            else:
                try:
                    args = mode.split(" ")
                    plugin_name = self.get_plugin_name(args[2])
                    plugin = self.plugman.get_plugin_by_name(plugin_name, category=args[1])
                    if plugin:
                        plugin.plugin_object.load_config(self.plugman)
                        if(len(args) == 5):
                            try:
                                plugin.plugin_object.set_property_value(args[3], args[4])
                            except NotImplementedError:
                                print "This plugin is not supported by CLI"
                    else:
                        print "There's no plugin with such informations"
                except:
                    print "Invalid Syntax"     

                           
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
        self.config.enable_audio_recording = False
        self.config.writeConfig()
        
    def turn_audio_on(self):
        self.config.enable_audio_recording = True
        self.config.writeConfig()
        
    def turn_video_on(self):
        self.config.enable_video_recording = True
        self.config.writeConfig()
        
    def turn_video_off(self):
        self.config.enable_video_recording = False
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
        print "Video recording enabled: Yes" if self.config.enable_video_recording else "Video recording enabled: No"
        print "Current Video Mixer: " + self.config.videomixer
        print "Available Video Mixers Plugins: "
        count = 1
        for video_mixer in self.plugman.get_videomixer_plugins():
            print "%d - %s" % (count, video_mixer.name)
            count += 1
        count = 1    
        print "Available Video Input Plugins: "
        for video_input in self.plugman.get_videoinput_plugins():
            print "%d - %s" % (count, video_input.name)  
            count += 1      
        print "Current Video Resolution " + self.config.resolution
        print "Available Video Resolutions: "
        self._show_resolutions()
        print "Video preview enabled: Yes" if self.config.video_preview else "Video preview enabled: No"
        
    def _show_audio_config(self):
        print " ###################### Audio Settings ############################"
        print "Audio recording enabled: Yes" if self.config.enable_audio_recording else "Audio recording enabled: No"
        print "Available Audio Mixers: " 
        count = 1       
        for audio_mixer in self.plugman.get_audiomixer_plugins():
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
        for video_mixer in self.plugman.get_videomixer_plugins():
            print "%d - %s" % (count, video_mixer.name)
            count += 1
        
    def _is_valid_path(self, path):
        return os.path.exists(os.path.expanduser(path))
    
    def _get_mode(self, mode_list):
        mode = ""
        for item in mode_list:
            mode += item + " "
        return mode[0:len(mode)-1]     
    
    def _get_resolution_list(self, resmap):
        list = []
        for key in self.config.resmap:
            list.append(key)
        return list
    
    def _get_plugins(self):
        plugins = self.plugman.get_all_plugins()
        plugins_data = []
        
        for plugin in plugins:
            plugin_info = []
            plugin_info.append(plugin.name.replace(" ",""))
            plugin_info.append(plugin.name)
            properties = []
            try:
                for property in plugin.plugin_object.get_properties():
                    properties.append(property)
            except:
                pass
            plugin_info.append(properties)
            plugins_data.append(plugin_info)
            
        return plugins_data

    def get_plugin_name(self, plugin_replaced):
        for entry in self.plugins:
            if entry[0].upper() == plugin_replaced.upper():
                return entry[1]
        return None
        
