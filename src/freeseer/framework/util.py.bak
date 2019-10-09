#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2013, 2014  Free and Open Source Software Learning Centre
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
import os
import shutil
import sys
import unicodedata


def format_size(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
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


def get_record_name(extension, presentation=None, filename=None, path="."):
    """Returns the filename to use when recording.

    If a record name with a .None extension is returned, the record name
    will just be ignored by the output plugin (e.g. Video Preview plugin).

    Function will return None if neither presentation nor filename is passed.
    """
    if presentation is not None:
        recordname = make_record_name(presentation)
    elif filename is not None:
        recordname = filename
    else:
        return None

    count = 0
    tempname = recordname

    # Add a number to the end of a duplicate record name so we don't
    # overwrite existing files
    while(os.path.exists(os.path.join(path, "%s.%s" % (tempname, extension)))):
        tempname = "{0}-{1}".format(recordname, count)
        count += 1

    recordname = "%s.%s" % (tempname, extension)

    return recordname


def make_record_name(presentation):
    """Create an 'EVENT-ROOM-SPEAKER-TITLE' record name using presentation metadata."""
    tags = [
        make_shortname(presentation.event),
        make_shortname(presentation.room),
        make_shortname(presentation.speaker),
        make_shortname(presentation.title),
    ]
    record_name = unicode('-'.join(tag for tag in tags if tag))

    # Convert unicode filenames to their equivalent ascii so that
    # we don't run into issues with gstreamer or filesystems.
    safe_record_name = unicodedata.normalize('NFKD', record_name).encode('ascii', 'ignore')

    return safe_record_name or 'default'


def make_shortname(string):
    """Returns the first 6 characters of a string in uppercase.

    Strip out non alpha-numeric characters, spaces, and most punctuation.
    """
    bad_chars = set("!@#$%^&*()+=|:;{}[]',? <>~`/\\")
    string = "".join(ch for ch in string if ch not in bad_chars)
    return string[0:6].upper()


###
### Handy functions for reseting Freeseer configuration
###


def reset(configdir):
    """Deletes the Freeseer configuration directory"""
    if validate_configdir(configdir):
        print('This will wipe out your freeseer configuration directory.')
        if confirm_yes() is True:
            shutil.rmtree(configdir)
    else:
        print("%s is not a invalid configuration directory." % configdir)


def reset_configuration(configdir, profile='default'):
    """Deletes the Freeseer configuration files freeseer.conf and plugin.conf"""
    if profile is None:
        profile = 'default'

    if validate_configdir(configdir):
        freeseer_conf = os.path.join(configdir, 'profiles', profile, 'freeseer.conf')
        plugin_conf = os.path.join(configdir, 'profiles', profile, 'plugin.conf')

        if os.path.exists(freeseer_conf):
            os.remove(freeseer_conf)

        if os.path.exists(plugin_conf):
            os.remove(plugin_conf)
    else:
        print("%s is not a invalid configuration directory." % configdir)


def reset_database(configdir, profile='default'):
    """Deletes the Freeseer database file"""
    if profile is None:
        profile = 'default'

    if validate_configdir(configdir):
        dbfile = os.path.join(configdir, 'profiles', profile, 'presentations.db')

        if os.path.exists(dbfile):
            os.remove(dbfile)
    else:
        print("%s is not a invalid configuration directory." % configdir)


def validate_configdir(configdir):
    """Validate that the configdir is not one of the blacklisted directories"""
    if (configdir and configdir != '/' and
                      configdir != '~' and
                      configdir != os.path.abspath(os.path.expanduser('~'))):
        return True

    return False


def confirm_yes():
    """Prompts the user to confirm by typing 'yes' in response"""
    confirm = raw_input("Enter 'yes' to confirm: ")
    if confirm == 'yes':
        return True
    return False
