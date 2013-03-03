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

class Help():
    '''
    Contains all help texts used on Freeseer CLI help section
    '''
    
    HEADER = 'Freeseer Shell, version 1.0\n' \
    'Copyright (C) 2011-2012  Free and Open Source Software Learning Centre\n\n'   
    
    # Talk Help
    TALK_SHOW_TALKS = '\tLists all talks stored on database. If mode/value are ' \
    'provided, the talks are filtered. \n\n' \
    '\n\tAvailable modes:\n\t\tevent: Talk Event\n\t\troom: Talk Room\n\t\tid: Talk Id\n\t\tall: All talks' \
     '\n\n\tUSAGE: talk show [<mode> [<value>]]'
     
    TALK_SHOW_EVENTS = '\tLists all different events with presentations assigned to' \
    '\n\tUSAGE:talk show events'
    
    TALK_REMOVE = '\tRemoves a presentation from database.' \
    '\n\n\tAvailable options:all: All talks' \
    '\n\n\tUSAGE: talk remove <id>|all'
    
    TALK_ADD = '\tAllows the user to add a new talk by providing its informations' \
    '\n\n\tUSAGE: talk add'
    
    TALK_UPDATE = '\tAllows the user to update an existent talk by providing its ' \
    'news informations\n\n\tAvailable options:\n\t\t Talk Id' \
    '\n\n\tUSAGE: talk update <id>'
    
    # Config Help
    
    CONFIG_SHOW = '\tLists all available configurations and their respective values.' \
    '\n\n\tAvailable options:\n\t\tvideo: Video configuration\n\t\taudio: Audio configurations' \
    '\n\t\tall: All configurations \n\n\tUSAGE: config show [video] [audio] [all]'
    
    """CONFIG_AUDIO_SET = '\tSets the current audio mixer to the specified index.' \
    'The list of available line mixers can be obtained in the "config show audio" command' \
    '\n\n\tAvailable options:\n\tAudio mixer index \n\n\tUSAGE: config set audio <index>'i
    """
    
    CONFIG_VIDEO_SET = '\tSets the current video mixer to the specified index.' \
    'The list of available mixers can be obtained in the "config show video" command' \
    '\n\n\tAvailable options:\n\tVideo mixer index \n\n\tUSAGE: config set video <index>'

    CONFIG_VIDEO_RESOLUTION_SET = '\tSets the current video resolution to the specified index.' \
    'The list of available resolutions can be obtained in the "config show video" command' \
    '\n\n\tAvailable options:\n\tResolution index \n\n\tUSAGE: config set video resolution <index>'
    
    CONFIG_DIR_SET = '\tSets the output directory to the specified path' \
    '\n\n\tAvailable options:\n\tAbsolute path \n\n\tUSAGE: config set dir <path>'
    
    CONFIG_SET_AUDIO = '\tTurns audio on or off' \
    '\n\n\tAvailable options:\n\ton: Turns on \n\toff: Turns off \n\n\tUSAGE: config set audio [on|off]'\
    '\n\n\tSets the current audio mixer to the specified index.'\
    'The list of available line mixers can be obtained in the "config show audio" command'\
    '\n\n\tAvailable options:\n\tAudio mixer index \n\n\tUsage:config set audio  <index>'
    
    CONFIG_SET_STREAMING = '\tTurns streaming on or off' \
    '\n\n\tAvailable options:\n\ton: Turns on \n\toff: Turns off \n\n\tUSAGE: config set streaming [on|off]'
    
    CONFIG_SET_FILE = '\tTurns file plugin on or off' \
    '\n\n\tAvailable options:\n\ton: Turns on \n\toff: Turns off \n\n\tUSAGE: config set file [on|off]'
    
    CONFIG_SET = '\tThe setter commands provide an interface to modify the original values ' \
    'of some configurations. The configurations available for setting are:' \
    '\n\n\t\taudio: Audio Mixer\n\t\tvideo: Video Mixer\n\t\tvideo resolution: Resolution changes' \
    '\n\t\tdir: Output directory\n\t\tstreaming: Video streaming\n\t\tfile: File plugin' \
    '\n\n\tIn order to get more informations about each config setter, type "help config set <config>"'
    
    
    
    
    
