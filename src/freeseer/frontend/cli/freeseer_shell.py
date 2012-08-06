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

from freeseer.framework.core import FreeseerCore
from freeseer_record_parser import FreeSeerRecordParser
from freeseer_talk_parser import FreeSeerTalkParser
from freeseer_config_parser import FreeSeerConfigParser

class FreeSeerShell(cmd.Cmd):
    '''
    Freeseer Shell. Used to provide an interface to the CLI frontend
    '''
    def __init__(self):
        cmd.Cmd.__init__(self)        
        self.core = FreeseerCore(self)   
       
        #Not working. TODO Check why
        self._set_loggers(False)
               
        self.db_connector = self.core.db  
        
        self.prompt = "freeseer> "
        self.intro = "\nfreeseer - video recording and streaming software\n" \
        "Copyright (C) 2011  Free and Open Source Software Learning Centre\n"       
        
    def do_exit(self, line):
        """
        Exits the interpreter.
        """
        self._set_loggers(True)
        sys.exit()
        
    def do_quit(self, line):
        sys.exit()
        
    def do_record(self, line):
        parser = FreeSeerRecordParser(self.core)
        parser.analyse_command(line)
    
    def help_record(self):
        print open(os.path.join("freeseer","frontend","cli","help","record.txt"), 'r').read()


    #TODO   
    def complete_record(self, text, line, start_index, end_index):        
        pass
  
    #TODO         
    def do_talk(self, line):
        parser = FreeSeerTalkParser(self.core)
        parser.analyse_command(line)
    
    def help_talk(self):
        print open(os.path.join("freeseer","frontend","cli","help","talkeditor.txt"), 'r').read()

    #TODO   
    def complete_talk(self, text, line, start_index, end_index):        
        pass
    
    #TODO          
    def do_config(self, line):
        parser = FreeSeerConfigParser(self.core)
        parser.analyse_command(line)
    
    def help_config(self):
        print open(os.path.join("freeseer","frontend","cli","help","config.txt"), 'r').read()

    #TODO   
    def complete_config(self, text, line, start_index, end_index):        
        pass
        
    def run(self):
        self.cmdloop()
        
    def _set_loggers(self, enabled):
        self.core.logger.set_console_logger(enabled)
        self.core.logger.set_syslog_logger(enabled)

        
