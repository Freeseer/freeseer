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

import cmd
import sys
import subprocess
import os
import logging

from freeseer.framework.core import FreeseerCore
from freeseer_record_parser import FreeSeerRecordParser
from freeseer_talk_parser import FreeSeerTalkParser
from freeseer_config_parser import FreeSeerConfigParser
from help import Help

class FreeSeerShell(cmd.Cmd):
    '''
    Freeseer Shell. Used to provide an interface to the CLI frontend
    '''
    def __init__(self):        
        cmd.Cmd.__init__(self)  
        
        self._disable_loggers()       
        self.core = FreeseerCore(self)                
        self.db_connector = self.core.db  
        
        self.prompt = "freeseer> "
        self.intro = "\nfreeseer - video recording and streaming software\n" \
        "Copyright (C) 2011-2012  Free and Open Source Software Learning Centre\n"       
        
    def do_exit(self, line):
        """
        Exits the interpreter.
        """
        sys.exit()
        
    def do_quit(self, line):
        sys.exit()
        
    def do_record(self, line):
        parser = FreeSeerRecordParser(self.core)
        if (line.split()[0] == "help"):
            help_topic = line.replace("help ", "")
            if (help_topic == 'record'):
                print Help.RECORD_HELP
            
        else:
            parser.analyse_command(line)
    
    def help_record(self):
        print Help.RECORD_GENERAL_HELP


    #TODO   
    def complete_record(self, text, line, start_index, end_index):        
        pass
  
    #TODO         
    def do_talk(self, line):
        parser = FreeSeerTalkParser(self.core)
        if (line.split()[0] == "help"):
            help_topic = line.replace("help ", "")
            if (help_topic == 'show'):
                print Help.TALK_SHOW_TALKS
            elif (help_topic == 'show events'):
                print Help.TALK_SHOW_EVENTS
            elif (help_topic == 'remove'):
                print Help.TALK_REMOVE
            elif (help_topic == 'add'):
                print Help.TALK_ADD
            elif (help_topic == 'update'):
                print Help.TALK_UPDATE            
            else:
                print "Unknow %s topic" % (help_topic)
            
        else:
            parser.analyse_command(line)
    
    def help_talk(self):
        print Help.TALK_GENERAL_HELP
        
    #TODO   
    def complete_talk(self, text, line, start_index, end_index):        
        pass
    
    #TODO          
    def do_config(self, line):
        parser = FreeSeerConfigParser(self.core)
        if (line.split()[0] == "help"):
            help_topic = line.replace("help ", "")
            if (help_topic == 'show'):
                print Help.CONFIG_SHOW
            elif (help_topic == 'set audio'):
                print Help.CONFIG_AUDIO_SET
            elif (help_topic == 'set video'):
                print Help.CONFIG_VIDEO_SET
            elif (help_topic == 'set video resolution'):
                print Help.CONFIG_VIDEO_RESOLUTION_SET
            elif (help_topic == 'set dir'):
                print Help.CONFIG_DIR_SET
            elif (help_topic == 'set audio'):
                print Help.CONFIG_SET_AUDIO
            elif (help_topic == 'set streaming'):
                print Help.CONFIG_SET_STREAMING
            elif (help_topic == 'set file'):
                print Help.CONFIG_SET_FILE
            elif (help_topic == 'set audio feedback'):
                print Help.CONFIG_SET_AUDIO_FEEDBACK
            elif (help_topic == 'set'):
                print Help.CONFIG_SET
            else:
                "Unknow %s topic" % (help_topic)
            
        else:
            parser.analyse_command(line)
            

    def help_config(self):
        print Help.CONFIG_GENERAL_HELP

    #TODO   
    def complete_config(self, text, line, start_index, end_index):        
        pass
        
    def run(self):
        self.cmdloop()
        
    def _disable_loggers(self):
        logging.disable(logging.CRITICAL)
        
