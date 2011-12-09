#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011  Free and Open Source Software Learning Centre
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

import ConfigParser
import logging
import os
import functools

import pygst
pygst.require("0.10")
import gst

from yapsy.PluginManager import PluginManagerSingleton
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.IPlugin import IPlugin
from PyQt4 import QtCore, QtGui

class PluginManager(QtCore.QObject):
    '''
    @signal pluginActivated(plugin_name, plugin_category)
    Emitted when a plugin is activated.
    
    @signal pluginDectivated(plugin_name, plugin_category)
    Emitted when a plugin is deactivated.
    '''
    
    def __init__(self, configdir):
        QtCore.QObject.__init__(self)
        
        self.firstrun = False
        plugman = PluginManagerSingleton().get()
        
        self.configdir = configdir
        self.configfile = os.path.abspath("%s/plugin.conf" % self.configdir)
        
        self.config = ConfigParser.ConfigParser()
        self.load()
        self.plugmanc = ConfigurablePluginManager(self.config, self, plugman)
        
        # Get the path where the installed plugins are located on systems where
        # freeseer is installed.
        pluginpath = "%s/../plugins" % os.path.dirname(os.path.abspath(__file__))
        
        self.plugmanc.setPluginPlaces([pluginpath, 
                                       "~/.freeseer/plugins", 
                                       "freeseer/plugins"])
        self.plugmanc.setCategoriesFilter({
            "AudioInput" : IAudioInput,
            "AudioMixer" : IAudioMixer,
            "VideoInput" : IVideoInput,
            "VideoMixer" : IVideoMixer,
            "Output" : IOutput,
            IMetadataReader.CATEGORY: IMetadataReader
            })
        self.plugmanc.collectPlugins()
        
        # If config was corrupt or did not exist, reset default plugins.
        if self.firstrun == True:
            self.set_default_plugins()
        else:
            # activate the default metadata reader plugins if none are active
            if not any(p.is_activated for p in 
                       plugman.getPluginsOfCategory(IMetadataReader.CATEGORY)):
                self._activate_default_metadata_plugins()
            
        for plugin in self.plugmanc.getAllPlugins():
            plugin.plugin_object.set_plugman(self)
            
        logging.debug("Plugin manager initialized.")
        
    def __call__(self):
        pass
    
    def load(self):
        try:
            self.config.readfp(open(self.configfile))
        # Config file does not exist, create a default
        except IOError:
            logging.debug("First run scenario detected. Creating new configuration files.")
            self.firstrun = True # If config was corrupt or did not exist, reset defaults.
            self.save()
            return
        
    def set_default_plugins(self):
        """
        Default the passthrough mixers and ogg output plugins.
        """
        
        self.activate_plugin("Audio Passthrough", "AudioMixer")
        
        # Set Pulse Source as default if available. Else default to ALSA.
        try:
            gst.element_factory_make('pulsesrc', 'testsrc')
            self.activate_plugin("Pulse Audio Source", "AudioInput")
            self.plugmanc.registerOptionFromPlugin("AudioMixer", "Audio Passthrough", "Audio Input", "Pulse Audio Source")
        except:
            self.activate_plugin("ALSA Source", "AudioInput")
            self.plugmanc.registerOptionFromPlugin("AudioMixer", "Audio Passthrough", "Audio Input", "ALSA Source")
            
        self.activate_plugin("Video Passthrough", "VideoMixer")
        self.activate_plugin("USB Source", "VideoInput")
        self.plugmanc.registerOptionFromPlugin("VideoMixer", "Video Passthrough", "Video Input", "USB Source")
        self.activate_plugin("Ogg Output", "Output")
        self._activate_default_metadata_plugins()
        logging.debug("Default plugins activated.")
        
    def _activate_default_metadata_plugins(self):
        self.activate_plugin("Filename Parser", IMetadataReader.CATEGORY)
        self.activate_plugin("GstDiscoverer Parser", IMetadataReader.CATEGORY)
        self.activate_plugin("os.stat Parser", IMetadataReader.CATEGORY)
        
    def save(self):
        with open(self.configfile, 'w') as configfile:
            self.config.write(configfile)
        
    def activate_plugin(self, plugin_name, plugin_category):
        self.plugmanc.activatePluginByName(plugin_name, plugin_category, True)
        self.save()
        self.plugin_activated.emit(plugin_name, plugin_category)
        logging.debug("Plugin %s activated." % plugin_name)
        
    def deactivate_plugin(self, plugin_name, plugin_category):
        self.plugmanc.deactivatePluginByName(plugin_name, plugin_category, True)
        self.save()
        self.plugin_deactivated.emit(plugin_name, plugin_category)
        logging.debug("Plugin %s deactivated." % plugin_name)
        
    # the arguments are plugin_name, plugin_category
    plugin_activated = QtCore.pyqtSignal(
            "QString", "QString", name="pluginActivated")
    plugin_deactivated = QtCore.pyqtSignal(
            "QString", "QString", name="pluginDectivated")
    

class IBackendPlugin(IPlugin):
    name = None
    widget = None
    
    def __init__(self):
        IPlugin.__init__(self)
    
    def get_name(self):
        return self.name
    
    def load_config(self, plugman):
        pass
    
    def set_plugman(self, plugman):
        self.plugman = plugman
        
    def set_gui(self, gui):
        self.gui = gui
    
    def get_dialog(self):
        widget = self.get_widget()
        if widget is not None:
            self.gui.show_plugin_widget_dialog(widget)
            self.widget_load_config(self.plugman)
    
    def get_widget(self):
        """
        Implement this method to return the settings widget (Qt based).
        Used by Freeseer configtool 
        """
        return None
    
    def widget_load_config(self, plugman):
        """
        Implement this when using a plugin widget. This function should be used
        to load any required configurations for the plugin widget.
        """
        pass

class IAudioInput(IBackendPlugin):
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_audioinput_bin(self):
        pass
    
class IAudioMixer(IBackendPlugin):
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_audiomixer_bin(self):
        pass
    
class IVideoInput(IBackendPlugin):
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_videoinput_bin(self):
        """
        Returns the Gstreamer Bin for the video input plugin.
        MUST be overridded when creating a video input plugin.
        """
        pass
    
class IVideoMixer(IBackendPlugin):
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_videomixer_bin(self):
        """
        Returns the Gstreamer Bin for the video mixer plugin.
        MUST be overridded when creating a video mixer plugin.
        """
        pass

class IOutput(IBackendPlugin):
    type = None # Types: audio, video, both
    extension = None
    location = None
    
    def __init__(self):
        IBackendPlugin.__init__(self)
    
    def get_type(self):
        return self.type
    
    def get_output_bin(self, metadata=None):
        """
        Returns the Gstreamer Bin for the output plugin.
        MUST be overridded when creating an output plugin.
        """
        pass
    
    def get_extension(self):
        return self.extension
    
    def set_recording_location(self, location):
        self.location = location

    def set_metadata(self, data):
        """
        Set the metadata if supported by Output plugin. 
        """
        pass

class IMetadataReaderBase(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
    
    class header(object):
        '''
        defines the data that is being depicted by the metadata
        @ivar name:Human readable name of the field
        @ivar type:expected type (not used)
        @ivar position:where the field should go in relation to the others
                        (we sort by this value when populating the headers)
        @ivar visible:if the field is currently visible (get from settings)
        '''
        # todo: load visibility from settings.
        def __init__(self, name, typ=None, pos=0, visible=True):
            self.name = name
            self.type = typ
            self.position = pos
            self.visible = visible
            
    def retrieve_metadata(self, filepath):
        raise NotImplementedError
    
    def retrieve_metadata_batch(self, filepath_list):
        raise NotImplementedError
    
    def get_fields(self):
        raise NotImplementedError
            
    field_visibility_changed = QtCore.pyqtSignal(
            "QString", bool, name="fieldVisibilityChanged")

class IMetadataReader(IBackendPlugin, IMetadataReaderBase):
    ## abstract class members/methods
    # this dict should be of type {string:header}
    # Don't use externally! use get_fields() instead
    fields_provided = {}
    
    def retrieve_metadata_internal(self, filepath):
        raise NotImplementedError
    
    def retrieve_metadata_batch_begin(self):
        '''
        Optional abstract method
        '''
    
    def retrieve_metadata_batch_end(self):
        '''
        Optional abstract method
        '''
    
    ## concrete class members/methods
    CATEGORY = "Metadata"
    
    def __init__(self):
        IBackendPlugin.__init__(self)
        IMetadataReaderBase.__init__(self)
        self.checkboxes = {}
    
    def retrieve_metadata(self, filepath):
        '''
        @return: Dict of field: data
        '''
        n = type(self).__name__
        return dict((".".join((n,k)),v) for (k,v) in 
                    self.retrieve_metadata_internal(filepath).iteritems())
    
    def retrieve_metadata_batch(self, filepath_list):
        self.retrieve_metadata_batch_begin()
        for filepath in filepath_list:
            yield self.retrieve_metadata(filepath)
        self.retrieve_metadata_batch_end()
    
    def load_config(self, plugman):
        self.plugman.plugmanc = plugman
        for key in self.fields_provided.iterkeys():
            try:
                self.set_visible(key, self.plugman.readOptionFromPlugin(
                        self.CATEGORY, self.name, key))
            except ConfigParser.NoSectionError:
                self.set_visible(key, self.plugman.registerOptionFromPlugin(
                        self.CATEGORY, self.name, key, True))
    
    def set_visible(self, option_name, option_value):
        self.plugman.plugmanc.registerOptionFromPlugin(
                self.CATEGORY, self.name, option_name, option_value)
        self.plugman.save()
        # dispatch signal to notify any slots of changes
#        self.field_visibility_changed.emit(option_name, option_value)
        self.field_visibility_changed.emit(
                ".".join(type(self).__name__, option_name),
                option_value)
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QVBoxLayout(self.widget)
            self.widget.setLayout(layout)
            
            for key in self.fields_provided:
                cbox = QtGui.QCheckBox(
                        self.fields_provided[key].name, self.widget)
                layout.addWidget(cbox)
                cbox.toggled.connect(functools.partial(self.set_visible, key))
                self.checkboxes[key] = cbox
            
        return self.widget
    
    def widget_load_config(self, plugman):
        self.load_config(plugman)
        for key in self.fields_provided:
            self.checkboxes[key].setChecked(self.plugman.readOptionFromPlugin(
                self.CATEGORY, self.name, key))
    
    @classmethod
    def get_fields(cls):
        '''
        ensures that the field dictionary is unique
        @return: Dict of field: IMetadataReader.header
        '''
        return dict((".".join((cls.__name__,k)),v) for (k,v) in cls.fields_provided.iteritems())
        #python 2.7+ only
#        return {".".join((cls.__name__,k)) : v for k in cls.fields_provided.iteritems()} 

    # the following commented code precaches unique names for fields
#    ufields_provided = {}
#    @classmethod
#    def get_fields(cls):
#        '''
#        @return: Dict of field: header
#        '''
#        return cls.ufields_provided
#    
#    @staticmethod
#    def setup_ufields_on_subclasses(name, bases, attrs):
#        cls = type(name, bases, attrs)
#        
#        cls.ufields_provided = dict((".".join((name,k)),v) for (k,v) in cls.fields_provided)
#        #cls.ufields_provided = {".".join((name,k)) : v for k in cls.fields_provided} #python 2.7+ only
#    __metaclass__ = setup_ufields_on_subclasses
        
        
    