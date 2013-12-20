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

import os

from freeseer.framework.config.core import Config
from freeseer.framework.config.profile import ProfileManager
import freeseer.framework.config.options as options

# TODO: change to config_dir when all the pull requests from UCOSP Fall 2013 are merged in
configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
default_profile_name = 'default'
default_config_file = 'freeseer.conf'

profile_manager = ProfileManager(os.path.join(configdir, 'profiles'))


class FreeseerConfig(Config):
    """General Freeseer profile settings."""

    resmap = {
        # No Scaling
        'default': '0x0',

        # Scaling
        '240p': '320x240',
        '360p': '480x360',
        '480p': '640x480',
        '720p': '1280x720',
        '1080p': '1920x1080'
    }

    videodir = options.FolderOption('~/Videos', auto_create=True)
    auto_hide = options.BooleanOption(False)
    resolution = options.ChoiceOption(resmap.keys(), 'default')
    enable_audio_recording = options.BooleanOption(True)
    enable_video_recording = options.BooleanOption(True)
    videomixer = options.StringOption('Video Passthrough')
    audiomixer = options.StringOption('Audio Passthrough')
    record_to_file = options.BooleanOption(True)
    record_to_file_plugin = options.StringOption('Ogg Output')
    record_to_stream = options.BooleanOption(False)
    record_to_stream_plugin = options.StringOption('RTMP Streaming')
    audio_feedback = options.BooleanOption(False)
    video_preview = options.BooleanOption(True)
    default_language = options.StringOption('tr_en_US.qm')
