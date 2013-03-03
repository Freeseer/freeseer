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

import logging

from cmd import Cmd
from help import Help

from freeseer import project_info
from freeseer.framework.core import FreeseerCore

from freeseer_record_parser import FreeseerRecordParser
from freeseer_talk_parser import FreeseerTalkParser
from freeseer_config_parser import FreeseerConfigParser


class FreeseerShell(Cmd):
    """Freeseer Shell provides an interface to the CLI frontend.

    Note that help methods take precedence to method's doc strings.
    """
    def __init__(self):        
        Cmd.__init__(self)  
        
        self._disable_loggers()       
        self.core = FreeseerCore(self)  
        self.plugman = self.core.get_plugin_manager()
        self.db_connector = self.core.db  
        
        # Parsers
        self.config_parser = FreeseerConfigParser(self.core)
        self.record_parser = FreeseerRecordParser(self.core)
        self.talk_parser = FreeseerTalkParser(self.core)
        
        # Auto-complete modes
        self.TALK_MODES = ['show','remove','add','update']
        self.TALK_SHOW_MODES = ['event','events','room','id','all']

        self.HELP_MODES = ['talk', 'config', 'exit', 'quit', 'record']
        self.HELP_TALK_MODES = ['show', 'add', 'remove', 'update', 'show events']
        self.HELP_CONFIG_MODES = ['show', 'set']
        self.HELP_CONFIG_SET_MODES = ['audio', 'video', 'video resolution', 'dir', 'streaming', 'file']
        
        self.CONFIG_MODES = ['show','set']        
        self.CONFIG_SET_MODES = ['audio','video','dir','streaming','file']
        self.CONFIG_SHOW_MODES = ['audio','video','all']
        self.PLUGIN_CATEGORIES = self.plugman.plugmanc.getCategories()
        self.CONFIG_SET_MODES_EXTENDED = self.CONFIG_SET_MODES + self.PLUGIN_CATEGORIES
        self.CONFIG_SHOW_MODES_EXTENDED = self.CONFIG_SHOW_MODES + self.PLUGIN_CATEGORIES
        
        self.intro = """{} (v{}) - {}\n{}
        
        Basic commands:
            - record    # Initiates recording
            - config    # Configures settings
            - talk      # Configures the talk database
        
        Type "help <topic>", "credits", or "license" for more information.""".format(
            project_info.NAME, project_info.VERSION, project_info.DESCRIPTION,
            project_info.COPYRIGHT)
        self.prompt = '?- '

        # Modify help's documentation strings.
        #self.doc_header = 'doc_header'
        #self.misc_header = 'misc_header'
        #self.undoc_header = 'undoc_header'
        #ruler = '-'

        
    def do_exit(self, line):
        """Exits the interpreter."""
        return True
        
    def do_quit(self, line):
        """Exits the interpreter."""
        return True

    def precmd(self, line):
        """Exits the interpreter when Ctrl-D pressed.
         
        Note that do_EOF() can also be used, but shows up in the help.
        """
        if line == "EOF":
            print  # Ctrl-D is a command without a newline, so print one.
            return "exit"
        return line

    def emptyline(self):
        """Disables auto-repetition of last command when input is an empty line.

        Overrides emptyline's behaviour.
        """
        pass
    
    def default(self, line):
        print '{} is not a valid command.'.format(line)
        
    ###
    ### Help Commands
    ###
    
    def do_help(self, args):
        """Override the help command to handle cases of command arguments.
        
        General help is provided by help_*() methods."""
        if len(args.split()) < 2:
            Cmd.do_help(self, args)
        else:
            if args == 'talk show':
                print Help.TALK_SHOW_TALKS
            elif args == 'talk show events':
                print Help.TALK_SHOW_EVENTS
	    elif args == 'talk remove':
		print Help.TALK_REMOVE
	    elif args == 'talk add':
		print Help.TALK_ADD
	    elif args == 'talk update':
		print Help.TALK_UPDATE
	    elif args == 'config show':
		print Help.CONFIG_SHOW
	    elif args == 'config set audio':
		print Help.CONFIG_SET_AUDIO
	    elif args == 'config set video':
		print Help.CONFIG_VIDEO_SET
	    elif args == 'config set video resolution':
		print Help.CONFIG_VIDEO_RESOLUTION_SET
	    elif args == 'config set dir':
		print Help.CONFIG_DIR_SET
	    elif args == 'config set streaming':
		print Help.CONFIG_SET_STREAMING
	    elif args == 'config set file':
		print Help.CONFIG_SET_FILE
	    elif args == 'config set':
		print Help.CONFIG_SET
            else:
                print 'Unknown %s topic' % (args)
                
    def complete_help(self, text, line, start_index, end_index):
        if text:
          
            if len(line.split()) == 2:
                return [
                    mode for mode in self.HELP_MODES
                    if mode.startswith(text)
                ]
            elif len(line.split())==3:
                if (line.split()[1]=="talk"):
                    return[
                        mode for mode in self.HELP_TALK_MODES
                        if mode.startswith(text)
                    ]
                elif (line.split()[1]=="config"):
                    return[
                        mode for mode in self.HELP_CONFIG_MODES
                        if mode.startswith(text)
                    ]
            elif len(line.split())==4:
                if (line.split()[1]=="config") and (line.split()[2]=="set"):
                    return[
                        mode for mode in self.HELP_CONFIG_SET_MODES
                        if mode.startswith(text)
                    ]
        elif len(line.split()) == 1:
            return self.HELP_MODES
        elif len(line.split()) ==2:
            if line.split()[1]=="talk":
                return self.HELP_TALK_MODES
            elif line.split()[1]=="config":
                return self.HELP_CONFIG_MODES
        elif len(line.split()) == 3 and line.split()[1]=="config" and line.split()[2]=="set":
            return self.HELP_CONFIG_SET_MODES

    ###
    ### Record Tool Commands
    ###

    def do_record(self, line):
        """
        Record Tool
        
        Records a presentation with the respective id using the currently
        configured settings.
        
        Usage: record <id>
        """
        if line:
            self.record_parser.analyse_command(line)
        else:
            print 'Error: Please provide a valid talk ID.' # TODO: make error messages consistent
    
    ###
    ### Talk Editor Commands
    ###

    def do_talk(self, line):
        """
        Talk Editor
        
        Provides functions to configure the talk database in Freeseer.
        
        The following commands are supported:
            - show
            - show events
            - remove
            - add
            - update
            
        For detailed help on specific commands, type: help talk <topic>
        """
        if line:
            self.talk_parser.analyse_command(line)
        else:
            print 'Error: please provide a valid entry. '    

    def complete_talk(self, text, line, start_index, end_index):  
        if text:     
            if len(line.split()) == 2:
                   return [
                    mode for mode in self.TALK_MODES
                    if mode.startswith(text)
                ]
            elif len(line.split()) == 3:
                if(line.split()[1] == "show"):
                    return [
                        mode for mode in self.TALK_SHOW_MODES
                        if mode.startswith(text)
                    ]
        elif len(line.split()) == 1:
            return self.TALK_MODES
        elif len(line.split()) == 2 and (line.split()[1] == "show"):
            return self.TALK_SHOW_MODES
        
    ###
    ### Config Tool Commands
    ###
        
    def do_config(self, line):
        """
        Config Tool
        
        Provides options for configuring Freeseer.
        
        The following commands are supported:
            - show <option>
            - set <option>

        For detailed instructions, type: help config <topic>
        
        >>> Command line plugin support <<<
        Freeseer plugins can also be managed via config tool CLI. The general syntax
        used to get current plugin's information is the following:
            
        > config show [<PLUGIN CATEGORY> [[<PLUGIN NAME>] [<PLUGIN PROPERTY>]]]
        
        NOTE: In case only plugin category is provided, all plugins matched on this
        category are listed. In case category name and plugin name are provided, all plugin's
        properties are listed. In case category, plugin name and property are provided, the
        respective property from this plugin is listed side-by-side with its respective value.
        The general syntax used to set plugin's values is the following:
            
        > config set <PLUGIN CATEGORY> <PLUGIN NAME> <PLUGIN PROPERTY> <PLUGIN VALUE>
        """
        if line:
            self.config_parser.analyse_command(line) 
        else:
            print 'Error: please provide a valid entry.'

    def complete_config(self, text, line, start_index, end_index):        
        if text:
            if len(line.split()) == 2:
                return [
                    mode for mode in self.CONFIG_MODES
                    if mode.startswith(text)
                ]
            elif len(line.split()) == 3:
                if(line.split()[1] == "set"):                    
                    return [
                        mode for mode in self.CONFIG_SET_MODES_EXTENDED
                        if mode.upper().startswith(text.upper())
                    ]
                elif(line.split()[1] == "show"):                    
                    return [
                        mode for mode in self.CONFIG_SHOW_MODES_EXTENDED
                        if mode.upper().startswith(text.upper())
                    ]
            elif len(line.split()) == 4:
                plugin_category = line.split()[2]
                try:
                    plugins = plugin = self.plugman.plugmanc.getPluginsOfCategory(plugin_category)
                    return [
                        plugin.name.replace(" ","") for plugin in plugins
                        if plugin.name.upper().startswith(text.upper())
                    ]
                except:
                    return []
            elif len(line.split()) == 5:
                plugin_category = line.split()[2]
                plugin_name = line.split()[3]
                
                plugin = self.plugman.plugmanc.getPluginByName(self.config_parser.get_plugin_name(plugin_name), category=plugin_category)
                properties = plugin.plugin_object.get_properties()
                return [
                    property for property in properties
                    if property.upper().startswith(text.upper())
                ]
        elif len(line.split())==1:
            return self.CONFIG_MODES
        elif len(line.split()) ==2:
            if line.split()[1]=="set":
                return self.CONFIG_SET_MODES_EXTENDED
            elif line.split()[1]=="show":
                return self.CONFIG_SHOW_MODES_EXTENDED

    ###
    ### Misc Commands
    ###
           
    def do_license(self, line):
        """
        Prints the license information
        """
        print 'Freeseer is licensed under the GNU GPL version 3.\n' \
              'See https://raw.github.com/Freeseer/freeseer/master/src/LICENSE\n'

    def do_credits(self, line):
        """
        Prints the credits
        """
        print 'Freeseer is maintained by many voluntary contributors.\n' \
              'The project was started by Andrew Ross and Thanh Ha.\n'
        
    def _disable_loggers(self):
        """ Disables all logging calls of severity INFO and below.
        
        The order of logging levels (in increasing severity) is:
        DEBUG, INFO, WARNING, ERROR, CRITICAL.
        """
        logging.disable(logging.INFO)
        
    def _get_plugin_name(self, plugin_replaced):
        for entry in self.plugins:
            if entry[0].upper() == plugin_replaced.upper():
                return entry[1]
        return None
