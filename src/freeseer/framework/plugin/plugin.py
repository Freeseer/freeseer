#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014  Free and Open Source Software Learning Centre
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

import abc
import logging

log = logging.getLogger(__name__)


class Plugin(object):

    __metaclass__ = abc.ABCMeta

    # Is it OK to define an __init__ method?
    # It seems like all plugins will make use of the __init__ with parameters (manager and) config.
    # The current plugins do need to know about the manager, but will future plugins need to do so?
    # Keeping manager here for now.
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config


class AudioInputPlugin(Plugin):

    @abc.abstractmethod
    def get_audioinput_bin(self):
        pass


class AudioMixerPlugin(Plugin):

    @abc.abstractmethod
    def get_audiomixer_bin(self):
        pass

    @abc.abstractmethod
    def get_inputs(self):
        # Returns a list of tuples containing the input name and instance number that the audio mixer needs
        # in order to initalize it's pipelines.
        #
        # This should be used so that the code that calls it can
        # gather the required inputs before calling load_inputs().
        pass

    @abc.abstractmethod
    def load_inputs(self, player, mixer, inputs):
        # Returns the Gstreamer Bin for the video input plugin.
        pass


class VideoMixerPlugin(Plugin):

    @abc.abstractmethod
    def get_videomixer_bin(self):
        # Returns the Gstreamer Bin for the video mixer plugin.
        pass

    @abc.abstractmethod
    def get_inputs(self):
        # Returns a list of tuples containing the input name and instance number that the video mixer needs
        # in order to initialize it's pipelines.
        pass

    @abc.abstractmethod
    def load_inputs(self, player, mixer, inputs):
        # This method is responsible for loading the inputs needed.
        pass


class OuputPlugin(Plugin):

        # This class has a lot of (not sure if this is the correct terminology)
        # attributes defined at the beginning of that. Is that something that
        # will be defined later? Or should I carry those over?
        # Examples are... FILE = 0      STREAM = 1      OTHER = 2       etc...

        @abc.abstractmethod
        def get_recordto(self):
            pass

        @abc.abstractmethod
        def get_type(self):
            pass

        @abc.abstractmethod
        def get_output_bin(self, audio=True, video=True, metadata=None):
            pass

        @abc.abstractmethod
        def get_extension(self):
            pass

        @abc.abstractmethod
        def set_recording_location(self, location):
            pass

        @abc.abstractmethod
        def set_metadata(self, data):
            # Set the metadata if supported by Output plugin
            pass

        @abc.abstractmethod
        def generate_xml_metadata(self, metadata):
            # There is code in this method in the other file. What do I do?
            pass


class ImporterPlugin(Plugin):

    @abc.abstractmethod
    def get_presentations(self):
        #Builds a list with all presentations
        pass
