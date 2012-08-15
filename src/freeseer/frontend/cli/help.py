#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011-2012  Free and Open Source Software Learning Centre
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

class Help():
    '''
    Contains all help texts used on FreeSeer CLI help section
    '''
    
    HEADER = 'FreeSeer Shell, version 1.0\n' \
    'Copyright (C) 2011-2012  Free and Open Source Software Learning Centre\n\n'
    
    # Record help
    RECORD_HELP = '\tRecords the presentation with the respective id using ' \
    'the current settings\n\tUSAGE: record -p <id>'
    
    # Talk Help
    TALK_SHOW_TALKS = '\tLists all talks stored on database. If mode/value are ' \
    'provided, the talks are filtered. \n\n' \
    '\n\tAvailable modes:\n\t\tevent: Talk Event\n\t\troom: Talk Room\n\t\tid: Talk Id\n\t\tall: All talks' \
     '\n\n\tUSAGE: talk show [<mode> [<value>]]'
     
    TALK_SHOW_EVENTS = '\tLists all different events with presentations assigned to' \
    '\n\tUSAGE:talk show events'
    
    TALK_REMOVE = '\tRemoves a presentation from database.' \
    '\n\n\tAvailable options:\n\t\t-p: Talk Id\n\t\t--all: All talks' \
    '\n\n\tUSAGE: talk remove [-p <id] [--all]'
    
    TALK_ADD = '\tAllows the user to add a new talk by providing its informations' \
    '\n\n\tUSAGE: talk add'
    
    TALK_UPDATE = '\tAllows the user to update an existent talk by providing its ' \
    'news informations\n\n\tAvailable options:\n\t\t-p: Talk Id' \
    '\n\n\tUSAGE: talk update -p <id>'
    
    # Config Help
    
    CONFIG_SHOW = '\tLists all available configurations and their respective values.' \
    '\n\n\tAvailable options:\n\t\tvideo: Video configuration\n\t\taudio: Audio configurations' \
    '\n\t\t--all: All configurations \n\n\tUSAGE: config show [video] [audio] [--all]'
    
    CONFIG_AUDIO_SET = '\tSets the current audio mixer to the specified index.' \
    'The list of availablLINEe mixers can be obtained in the "config show audio" command' \
    '\n\n\tAvailable options:\n\t-i: Audio mixer index \n\n\tUSAGE: config set audio -i <index>'
    
    CONFIG_VIDEO_SET = '\tSets the current video mixer to the specified index.' \
    'The list of available mixers can be obtained in the "config show video" command' \
    '\n\n\tAvailable options:\n\t-i: Video mixer index \n\n\tUSAGE: config set video -i <index>'

    CONFIG_VIDEO_RESOLUTION_SET = '\tSets the current video resolution to the specified index.' \
    'The list of available resolutions can be obtained in the "config show video" command' \
    '\n\n\tAvailable options:\n\t-i: Resolution index \n\n\tUSAGE: config set video resolution -i <index>'
    
    CONFIG_DIR_SET = '\tSets the output directory to the specified path' \
    '\n\n\tAvailable options:\n\t-p: Absolute path \n\n\tUSAGE: config set dir -p <path>'
    
    CONFIG_SET_AUDIO = '\tTurns audio on or off' \
    '\n\n\tAvailable options:\n\ton: Turns on \n\toff: Turns off \n\n\tUSAGE: config set audio [on|off]'
    
    CONFIG_SET_STREAMING = '\tTurns streaming on or off' \
    '\n\n\tAvailable options:\n\ton: Turns on \n\toff: Turns off \n\n\tUSAGE: config set streaming [on|off]'
    
    CONFIG_SET_FILE = '\tTurns file plugin on or off' \
    '\n\n\tAvailable options:\n\ton: Turns on \n\toff: Turns off \n\n\tUSAGE: config set file [on|off]'
    
    CONFIG_SET_AUDIO_FEEDBACK = '\tTurns audio feedback on or off' \
    '\n\n\tAvailable options:\n\ton: Turns on \n\toff: Turns off \n\n\tUSAGE: config set audio feedback [on|off]'
    
    CONFIG_SET = '\tThe setter commands provide an interface to modify the original values ' \
    'of some configurations. The configurations available for setting are:' \
    '\n\n\t\taudio: Audio Mixer\n\t\tvideo: Video Mixer\n\t\tdir: Output directory' \
    '\n\t\tstreaming: Video streaming\n\t\tself.file: File plugin\n\t\taudio feedback: Audio Feedback' \
    '\n\n\tIn order to get more informations about each config setter, type "config help set <config>"'
    
    # General help
    
    CONFIG_GENERAL_HELP = HEADER + 'Talk Editor Tool Command Line Interface\n' \
    'This CLI defines all commands provided by the configtool on FreeSeer.\n' \
    'The following commands are supported:\n\n' \
    '> show \n> set\n\nFor further information, type config help <command>\n\n' \
    '>>> Command line plugin support <<< \n\n' \
    "FreeSeer plugins can also be managed via config tool CLI. The general syntax " \
    "used to get current plugin's information is the following:\n\n" \
    '> config show [<PLUGIN CATEGORY>] [<PLUGIN NAME>] [<PLUGIN PROPERTY>]\n\n' \
    "NOTE: In case only plugin category is provided, all plugins matched on this " \
    "category are listed. In case category name and plugin name are provided, all plugin's" \
    "properties are listed. In case category, plugin name and property are provided, the" \
    "respective property from this plugin is listed side-by-side with its respective value.\n\n" \
    "The general syntax used to set plugin's values is the following:\n\n" \
    "> config set <PLUGIN CATEGORY> <PLUGIN NAME> <PLUGIN PROPERTY> <PLUGIN VALUE>"
    
    RECORD_GENERAL_HELP = HEADER + 'Record Tool Command Line Interface\n' \
    'This CLI defines all commands provided by the record tool on FreeSeer.\n' \
    'The following commands are supported:\n\n' \
    "> record\n\nFor further information, type 'record help <command>'"
    
    TALK_GENERAL_HELP = HEADER + 'Talk Editor Tool Command Line Interface\n' \
    'This CLI defines all commands provided by the talk editor tool on FreeSeer.\n' \
    'The following commands are supported:\n\n' \
    '> show\n> show events\n> remove\n> add\n> update\n\n' \
    "For further information, type 'talk help <command>'"
    
    
    
    