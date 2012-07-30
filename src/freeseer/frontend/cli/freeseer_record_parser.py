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
    def __init__(self, core):
        
        self.core = core  
        self.core.config.video_preview  = False
        self.core.config.writeConfig()
        self.db_connector = self.core.db
     
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
        if(namespace.id):
            self.record_by_id(namespace.id)
        elif(namespace.path):
            self.record_by_path(namespace.path)
        else:
            self.default_record()
            
    
    def record_by_id(self,id):
        '''
        Records the presentation with the specified id
        '''        
        prs = self.db_connector.get_presentation(id)  
        if(prs):
            self.core.load_backend(prs)
            self.core.record()
            print "\n Recording on progress, press <space> to stop \n"          
      
            while(self.getchar() != " "):            
                continue
        
            self.core.stop();
        
        else:
            print "\n*** Error: There's no presentation with such id\n"
        
         
          
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