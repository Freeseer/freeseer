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

from PyQt4.QtCore import QLocale

from freeseer.framework.config.core import Config
from freeseer.framework.config.profile import ProfileManager
from freeseer.framework.multimedia import Quality
import freeseer.framework.config.options as options

# TODO: change to config_dir when all the pull requests from UCOSP Fall 2013 are merged in
configdir = os.path.abspath(os.path.expanduser('~/.freeseer/'))
default_profile_name = 'default'
default_config_file = 'freeseer.conf'

profile_manager = ProfileManager(os.path.join(configdir, 'profiles'))


def detect_system_language():
    """Returns the matching Qt linguist filename for the user's system language.

    The default is to use en_US if a matching translation does not exist.
    """
    translation = 'tr_{}'.format(QLocale.system().name())
    translation_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    'frontend', 'qtcommon', 'languages', '{}.ts'.format(translation))
    return '{}.qm'.format(translation) if os.path.isfile(translation_file) else 'tr_en_US.qm'


class FreeseerConfig(Config):
    """General Freeseer profile settings."""

    videodir = options.FolderOption('~/Videos', auto_create=True)
    auto_hide = options.BooleanOption(False)
    enable_audio_recording = options.BooleanOption(True)
    enable_video_recording = options.BooleanOption(True)
    videomixer = options.StringOption('Video Passthrough')
    video_quality = options.IntegerOption(Quality.CUSTOM)
    audiomixer = options.StringOption('Audio Passthrough')
    audio_quality = options.IntegerOption(Quality.CUSTOM)
    record_to_file = options.BooleanOption(True)
    record_to_file_plugin = options.StringOption('Ogg Output')
    record_to_stream = options.BooleanOption(False)
    record_to_stream_plugin = options.StringOption('RTMP Streaming')
    audio_feedback = options.BooleanOption(False)
    video_preview = options.BooleanOption(True)
    default_language = options.StringOption(detect_system_language())
