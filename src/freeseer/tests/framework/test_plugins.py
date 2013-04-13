#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2013 Free and Open Source Software Learning Centre
# http://fosslc.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

import os
import unittest

import pygst
pygst.require("0.10")
import gst

from freeseer import settings
from freeseer.framework.plugin import PluginManager

class TestPlugins(unittest.TestCase):

    def setUp(self):
        '''
        Stardard init method: runs before each test_* method

        Initializes a PluginManager

        '''
        configdir = os.path.abspath(".")
        self.manager = PluginManager(configdir)

    def tearDown(self):
        '''
        Generic unittest.TestCase.tearDown()
        '''
        del self.manager

    def test_audio_input_bin(self):
        '''Check that audio input plugins are returning a gst.Bin object

        Verifies that get_audioinput_bin() is returning the proper object.
        '''
        plugins = self.manager.get_plugins_of_category("AudioInput")

        for plugin in plugins:
            plugin_bin = plugin.plugin_object.get_audioinput_bin()
            self.assertIsInstance(plugin_bin, gst.Bin,
                "%s did not return a gst.Bin object" % plugin.name)

    def test_audio_mixer_bin(self):
        '''Check that audio mixer plugins are returning a gst.Bin object

        Verifies that get_audioinput_bin() is returning the proper object.
        '''
        plugins = self.manager.get_plugins_of_category("AudioMixer")

        for plugin in plugins:
            plugin_bin = plugin.plugin_object.get_audiomixer_bin()
            self.assertIsInstance(plugin_bin, gst.Bin,
                "%s did not return a gst.Bin object" % plugin.name)

    def test_video_input_bin(self):
        '''Check that video input plugins are returning a gst.Bin object

        Verifies that get_videoinput_bin() is returning the proper object.
        '''
        plugins = self.manager.get_plugins_of_category("VideoInput")

        for plugin in plugins:
            if plugin.name == "Firewire Source":
                # There is an issue with Firewire Source in testing
                # Skip until this is resolved
                continue

            plugin_bin = plugin.plugin_object.get_videoinput_bin()
            self.assertIsInstance(plugin_bin, gst.Bin,
                "%s did not return a gst.Bin object" % plugin.name)

    def test_video_mixer_bin(self):
        '''Check that video mixer plugins are returning a gst.Bin object

        Verifies that get_videomixer_bin() is returning the proper object.
        '''
        plugins = self.manager.get_plugins_of_category("VideoMixer")

        for plugin in plugins:
            plugin_bin = plugin.plugin_object.get_videomixer_bin()
            self.assertIsInstance(plugin_bin, gst.Bin,
                "%s did not return a gst.Bin object" % plugin.name)

    def test_output_bin(self):
        '''Check that output plugins are returning a gst.Bin object

        Verifies that get_output_bin() is returning the proper object.
        '''
        plugins = self.manager.get_plugins_of_category("Output")

        for plugin in plugins:
            plugin_bin = plugin.plugin_object.get_output_bin()
            self.assertIsInstance(plugin_bin, gst.Bin,
                "%s did not return a gst.Bin object" % plugin.name)
