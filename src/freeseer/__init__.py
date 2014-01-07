# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2013  Free and Open Source Software Learning Centre
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

"""
vga/presentation capture software

Freeseer (pronounced free-see-ar) is a free, open source, cross-platform
application that captures or streams your desktop. It’s designed for capturing
presentations, and has been succesfully used at many open source conferences
to record hundreds of talks (which can be seen at fosslc.org). Though designed
for capturing presentations, it can also be used to capture demos, training
materials, lectures, and other videos.

Freeseer is written in Python, uses Qt4 for its GUI, and Gstreamer for
video/audio processing. Freeseer is based on open standards and supports
royalty free audio and video codecs.

Freeseer’s source code is licensed under the GNU General Public License and
is available on GitHub.
"""

NAME = 'freeseer'
__version__ = '3.0.9999'
SCHEMA_VERSION = 310
__author__ = "Free and Open Source Software Learning Center"
__email__ = "fosslc@gmail.com"
URL = 'http://github.com/Freeseer/freeseer'
WWW = 'http://freeseer.github.com'
BLOG = 'http://fosslc.org'
DESCRIPTION = 'Video recording and streaming software'
LONG_DESCRIPTION = '''
Freeseer is a tool for capturing or streaming video.

It enables you to capture great presentations, demos, training material,
and other videos. It handles desktop screen-casting with ease.

Freeseer is one of a few such tools that can also record vga output
or video from external sources such as firewire, usb, s-video, or rca.

It is particularly good at handling very large conferences with hundreds
of talks and speakers using varied hardware and operating systems.

Freeseer itself can run on commodity hardware such as a laptop or desktop.
'''
COPYRIGHT = 'Copyright (c) 2011-2013 Free and Open Source Software Learning Centre'

# Setup Default Logger configuration
import logging
import logging.handlers
import os

from freeseer import settings

logging.getLogger("").setLevel(logging.NOTSET)
logging.getLogger("yapsy").setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s (%(levelname)8s) %(name)-40s: %(message)s')
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logging.getLogger("").addHandler(consoleHandler)

# Log to rotating file logger
logdir = os.path.abspath(os.path.join(settings.configdir, "logs"))
if not os.path.exists(logdir):
    os.makedirs(logdir)
logfile = os.path.abspath(os.path.join(settings.configdir, "logs", "freeseer.log"))
fileHandler = logging.handlers.RotatingFileHandler(logfile, maxBytes=50000, backupCount=5)
fileHandler.setFormatter(formatter)
logging.getLogger("").addHandler(fileHandler)
