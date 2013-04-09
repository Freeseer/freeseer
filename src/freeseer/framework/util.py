#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2013  Free and Open Source Software Learning Centre
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

import ctypes
import logging
import os
import sys
import unicodedata

def format_size(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def get_free_space(directory):
        """ Return directory free space (in human readable form) """
        if sys.platform in ["win32", "cygwin"]:
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(directory), 
                                                       None, None, ctypes.pointer(free_bytes))
            space = free_bytes.value
        else:
            space = os.statvfs(directory).f_bfree * os.statvfs(directory).f_frsize
            
        return format_size(space)

###
### Filename related functions
###

def get_record_name(presentation, extension, path="."):
    """Returns the filename to use when recording.
    
    If a record name with a .None extension is returned, the record name
    will just be ignored by the output plugin (e.g. Video Preview plugin).
    """
    if presentation:
        recordname = make_record_name(presentation)
        
        count = 0
        tempname = recordname
        
        # Add a number to the end of a duplicate record name so we don't
        # overwrite existing files
        while(os.path.exists(os.path.join(path, "%s.%s" % (tempname, extension)))):
            tempname = "{0}-{1}".format(recordname, count)
            count+=1

    recordname = "%s.%s" % (tempname, extension)

    # This is to ensure that we don't log a message when extension is None
    if extension is not None:
        logging.debug('Set record name to %s', recordname)        

    return recordname

def make_record_name(presentation):
    """Create an 'EVENT-ROOM-SPEAKER-TITLE' record name.

    If any information is missing, we blank it out intelligently
    And if we have nothing for some reason, we use "default"
    """    
    event = make_shortname(presentation.event)
    title = make_shortname(presentation.title)
    room = make_shortname(presentation.room)
    speaker = make_shortname(presentation.speaker)

    recordname = ""  # TODO: add substrings to a list then ''.join(list) -- better practice

    if event != "": # TODO: empty strings are falsy, use 'if not string:'
        if recordname != "":
            recordname = recordname + "-" + event
        else:
            recordname = event

    if room != "":
        if recordname != "":
            recordname = recordname + "-" + room
        else:
            recordname = room

    if speaker != "":
        if recordname != "":
            recordname = recordname + "-" + speaker
        else:
            recordname = speaker

    if title != "":
        if recordname != "":
            recordname = recordname + "-" + title
        else:
            recordname = title

    # Convert unicode filenames to their equivalent ascii so that
    # we don't run into issues with gstreamer or filesystems.
    recordname = unicodedata.normalize('NFKD', recordname).encode('ascii','ignore')

    if recordname != "":
        return recordname

    return "default"

def make_shortname(string):
    """Returns the first 6 characters of a string in uppercase.

    Strip out non alpha-numeric characters, spaces, and most punctuation.
    """
    bad_chars = set("!@#$%^&*()+=|:;{}[]',? <>~`/\\")
    string = "".join(ch for ch in string if ch not in bad_chars)
    return string[0:6].upper()
