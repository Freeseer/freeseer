#!/usr/bin/python
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
import logging
import os
import sys
import xml.etree.ElementTree as ET

from PyQt4 import QtCore
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.IPlugin import IPlugin

log = logging.getLogger(__name__)


class PluginManager(QtCore.QObject):
    '''
    Plugin Manager for Freeseer

    Provides the core functionality which enables plugin support in.
    '''

    def __init__(self, profile):
        QtCore.QObject.__init__(self)

        self.profile = profile
        self.firstrun = False
        self.plugmanc = PluginManagerSingleton.get()

        locator = self.plugmanc.getPluginLocator()
        locator.setPluginInfoExtension("freeseer-plugin")

        # Get the path where the installed plugins are located on systems where
        # freeseer is installed.
        pluginpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "plugins")

        self.plugmanc.setPluginPlaces([pluginpath,
                                       os.path.expanduser("~/.freeseer/plugins"),
                                       "freeseer/plugins"])
        self.plugmanc.setCategoriesFilter({
            "AudioInput": IAudioInput,
            "AudioMixer": IAudioMixer,
            "VideoInput": IVideoInput,
            "VideoMixer": IVideoMixer,
            "Importer": IImporter,
            "Output": IOutput})
        self.plugmanc.collectPlugins()

        for plugin in self.plugmanc.getAllPlugins():
            plugin.plugin_object.set_plugman(self)

        log.debug("Plugin manager initialized.")

    def __call__(self):
        pass

    ##
    ## Functions related to getting plugins supported by user's OS
    ##

    def _os_supported(self, plugin):
        """
        Determines if the user's OS as detected by sys.platform is supported by
        the plugin.

        Parameters: plugin - a plugin object
        Returns: true/false
        """
        return sys.platform in plugin.plugin_object.get_supported_os()

    def _get_supported_plugins(self, unfiltered_plugins):
        """
        Returns a list of plugins supported by the users OS as detected by
        python's sys.platform library.

        Parameters:
            unfiltered plugins - list of plugins to filter
        Returns:
            list of supported plugins
        """
        plugins = []

        for plugin in unfiltered_plugins:
            if self._os_supported(plugin):
                plugins.append(plugin)

        return plugins

    def get_plugin_by_name(self, name, category):
        """
        Takes a name & category and returns the plugin with that name.

        Parameters:
            name        - name of the plugin
            category    - category to search
        Returns:
            plugin
        """
        return self.plugmanc.getPluginByName(name, category)

    def get_all_plugins(self):
        """
        Returns a list of all plugins supported by the users OS as detected by
        python's sys.platform library.

        Parameters:
            none
        Returns:
            list of all supported plugins
        """
        unfiltered_plugins = self.plugmanc.getAllPlugins()
        return self._get_supported_plugins(unfiltered_plugins)

    def get_plugins_of_category(self, category):
        """
        Returns a list of all plugins in category supported by the users OS as
        detected by python's sys.platform library.

        Parameters:
            none
        Returns:
            list of all supported plugins
        """
        unfiltered_plugins = self.plugmanc.getPluginsOfCategory(category)
        return self._get_supported_plugins(unfiltered_plugins)

    def get_audioinput_plugins(self):
        """
        Returns a list of plugins that are supported by the users OS as
        detected by python's sys.platform library.

        Parameters:
            none
        Returns:
            list of supported AudioInput plugins
        """
        unfiltered_plugins = self.plugmanc.getPluginsOfCategory("AudioInput")
        return self._get_supported_plugins(unfiltered_plugins)

    def get_audiomixer_plugins(self):
        """
        Returns a list of plugins that are supported by the users OS as
        detected by python's sys.platform library.

        Parameters:
            none
        Returns:
            list of supported AudioMixer plugins
        """
        unfiltered_plugins = self.plugmanc.getPluginsOfCategory("AudioMixer")
        return self._get_supported_plugins(unfiltered_plugins)

    def get_videoinput_plugins(self):
        """
        Returns a list of plugins that are supported by the users OS as
        detected by python's sys.platform library.

        Parameters:
            none
        Returns:
            list of supported VideoInput plugins
        """
        unfiltered_plugins = self.plugmanc.getPluginsOfCategory("VideoInput")
        return self._get_supported_plugins(unfiltered_plugins)

    def get_videomixer_plugins(self):
        """
        Returns a list of plugins that are supported by the users OS as
        detected by python's sys.platform library.

        Parameters:
            none
        Returns:
            list of supported VideoMixer plugins
        """
        unfiltered_plugins = self.plugmanc.getPluginsOfCategory("VideoMixer")
        return self._get_supported_plugins(unfiltered_plugins)

    def get_importer_plugins(self):
        """Returns a list of plugins that are supported by the users OS as detected by python's sys.platform library

        Parameters:
            none
        Returns:
            list of supported Importer plugins
        """
        unfiltered_plugins = self.plugmanc.getPluginsOfCategory("Importer")
        return self._get_supported_plugins(unfiltered_plugins)

    def get_output_plugins(self):
        """
        Returns a list of plugins that are supported by the users OS as
        detected by python's sys.platform library.

        Parameters:
            none
        Returns:
            list of supported Output plugins
        """
        unfiltered_plugins = self.plugmanc.getPluginsOfCategory("Output")
        return self._get_supported_plugins(unfiltered_plugins)

    def load_plugin_config(self, config_class, section_name):
        """
        Return an instance of the config class for a plugin.

        Parameters:
            config_class: The CONFIG_CLASS of the plugin.
            section_name: The section_name string for the plugin.

        Returns:
            An instance of the plugin's config class, or None
            if no config class exists for this plugin.
        """
        if config_class:
            return self.profile.get_config('plugin.conf', config_class, storage_args=[section_name])
        else:
            return None


class IBackendPlugin(IPlugin):
    instance = 0
    name = None
    widget = None
    CATEGORY = "Undefined"
    CONFIG_CLASS = None
    # list of supported OSes per:
    #    http://docs.python.org/2/library/sys.html#sys.platform
    os = []

    config_loaded = False
    widget_config_loaded = False

    def __init__(self):
        IPlugin.__init__(self)

    def get_name(self):
        return self.name

    def get_supported_os(self):
        """
        Returns a list of OSes supported by the plugin
        """
        return self.os

    def get_config_name(self):
        return "{}-{}".format(self.name, self.instance)

    def get_section_name(self):
        return "{} Plugin: {}".format(self.CATEGORY, self.get_config_name())

    def load_config(self, plugman, config=None):
        if not config:
            self.config = plugman.load_plugin_config(self.CONFIG_CLASS, self.get_section_name())
        else:
            self.config = config

    def set_plugman(self, plugman):
        self.plugman = plugman

    def set_instance(self, instance=0):
        self.instance = instance
        self.load_config(self.plugman)

    def set_gui(self, gui):
        self.gui = gui

    def get_dialog(self):
        widget = self.get_widget()
        self.retranslate()  # Translate the UI

        # Only load configuration the first time the user opens widget
        if not self.widget_config_loaded:
            log.debug("%s loading configuration into widget.", self.name)
            self.widget_config_loaded = True
            self.widget_load_config(self.plugman)

        if widget is not None:
            self.gui.show_plugin_widget_dialog(widget, self.name)

        if self.config is not None:
            self.config.save()

    def get_config(self):
        """Check if the config is loaded, if not then load it."""
        if not self.config_loaded:
            self.config_loaded = True
            self.load_config(self.plugman)

    def get_widget(self):
        """
        Implement this method to return the settings widget (Qt based).
        Used by Freeseer configtool
        """
        return None

    def __enable_connections(self):
        """
        Implement this method to setup Qt SIGNALs/SLOTS.

        This should be enabled after loading the widget config.
        """
        pass

    def widget_load_config(self, plugman):
        """
        Implement this when using a plugin widget. This function should be used
        to load any required configurations for the plugin widget.
        """
        pass

    def retranslate(self):
        """Implement this function to allow translation of UI components in the widget"""
        pass


class IAudioInput(IBackendPlugin):
    CATEGORY = "AudioInput"

    def __init__(self):
        IBackendPlugin.__init__(self)

    def get_audioinput_bin(self):
        raise NotImplementedError


class IAudioMixer(IBackendPlugin):
    CATEGORY = "AudioMixer"

    def __init__(self):
        IBackendPlugin.__init__(self)

    def get_audiomixer_bin(self):
        raise NotImplementedError

    def get_inputs(self):
        """
        Returns a list of tuples containing the input name and instance number that the audio mixer needs
        in order to initialize it's pipelines.

        This should be used so that the code that calls it can
        gather the required inputs before calling load_inputs().
        """
        raise NotImplementedError

    def load_inputs(self, player, mixer, inputs):
        """
        This method is responsible for loading the inputs needed
        by the mixer.
        """
        raise NotImplementedError


class IVideoInput(IBackendPlugin):
    CATEGORY = "VideoInput"

    def __init__(self):
        IBackendPlugin.__init__(self)

    def get_videoinput_bin(self):
        """
        Returns the Gstreamer Bin for the video input plugin.
        MUST be overridded when creating a video input plugin.
        """
        raise NotImplementedError

    def get_resolution_pixels(self):
        raise NotImplementedError


class IVideoMixer(IBackendPlugin):
    CATEGORY = "VideoMixer"

    def __init__(self):
        IBackendPlugin.__init__(self)

    def get_videomixer_bin(self):
        """
        Returns the Gstreamer Bin for the video mixer plugin.
        MUST be overridded when creating a video mixer plugin.
        """
        raise NotImplementedError

    def get_inputs(self):
        """
        Returns a list of tuples containing the input name and instance number that the video mixer needs
        in order to initialize it's pipelines.

        This should be used so that the code that calls it can
        gather the required inputs before calling load_inputs().
        """
        raise NotImplementedError

    def load_inputs(self, player, mixer, inputs):
        """
        This method is responsible for loading the inputs needed
        by the mixer.
        """
        raise NotImplementedError

    def get_resolution_pixels(self):
        """
        Returns the total number of pixels in the selected from the video input plugin.
        """
        raise NotImplementedError

    def supports_video_quality(self):
        """
        Returns True if the current video input plugin supports video quality else returns False.
        """
        return False


class IOutput(IBackendPlugin):
    #
    # static variables
    #
    CATEGORY = "Output"

    # recordto
    FILE = 0
    STREAM = 1
    OTHER = 2

    # type
    AUDIO = 0
    VIDEO = 1
    BOTH = 2

    #
    # variables
    #
    recordto = None  # recordto: FILE, STREAM, OTHER
    type = None  # Types: AUDIO, VIDEO, BOTH
    extension = None
    location = None
    configurable = False

    metadata_order = [
        "title",
        "artist",
        "performer",
        "album",
        "location",
        "date",
        "comment"]

    def __init__(self):
        IBackendPlugin.__init__(self)

    def get_recordto(self):
        return self.recordto

    def get_type(self):
        return self.type

    def get_output_bin(self, audio=True, video=True, metadata=None):
        """
        Returns the Gstreamer Bin for the output plugin.
        MUST be overridded when creating an output plugin.
        """
        raise NotImplementedError

    def get_extension(self):
        return self.extension

    def set_recording_location(self, location):
        self.location = location

    def set_metadata(self, data):
        """
        Set the metadata if supported by Output plugin.
        """
        pass

    def generate_xml_metadata(self, metadata):
        root = ET.Element('metadata')

        for key in self.metadata_order:
            node = ET.SubElement(root, key)
            node.text = metadata[key]

        return ET.ElementTree(root)

    def set_audio_quality(self, quality):
        """Implement this to set the audio quality of the plugin.

        Input quality is either LOW, MEDIUM, or HIGH.
        """
        pass

    def set_video_bitrate(self, bitrate):
        """Implement this to set the bitrate of the plugin.

        Only implement if the bitrate of the plugin can be specified.
        """
        pass


class IImporter(IBackendPlugin):
    CATEGORY = "Importer"

    def get_presentations(self):
        """Builds a list with all presentations"""
        raise NotImplementedError


class PluginError(Exception):
    def __init__(self, message):
        self.message = message
