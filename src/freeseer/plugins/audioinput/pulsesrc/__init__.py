'''
freeseer - vga/presentation capture software

Copyright (C) 2011, 2013  Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/Freeseer/freeseer/

@author: Thanh Ha
'''

# python-libs
import ConfigParser
import logging

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin import IAudioInput

# .freeseer-plugin custom
import widget

log = logging.getLogger(__name__)


class PulseSrc(IAudioInput):
    name = "Pulse Audio Source"
    os = ["linux", "linux2"]

    #config variables
    source = ''

    def get_audioinput_bin(self):
        bin = gst.Bin()  # Do not pass a name so that we can load this input more than once.

        audiosrc = gst.element_factory_make("pulsesrc", "audiosrc")
        if self.source != '':
            audiosrc.set_property('device', self.source)
            log.debug('Pulseaudio source is set to %s' % str(audiosrc.get_property('device')))
        bin.add(audiosrc)

        # Setup ghost pad
        pad = audiosrc.get_pad("src")
        ghostpad = gst.GhostPad("audiosrc", pad)
        bin.add_pad(ghostpad)

        return bin

    def __get_sources(self):
        """
        Get a list of pairs in the form (name, description) for each pulseaudio source.
        """
        result = []
        audiosrc = gst.element_factory_make("pulsesrc", "audiosrc")
        audiosrc.probe_property_name('device')
        names = audiosrc.probe_get_values_name('device')
        #should be getting actual device description, but .get_property('device-name') does not work
        result = [(name, name) for name in names]
        return result

    def load_config(self, plugman):
        self.plugman = plugman

        try:
            self.source = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), 'Source')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), 'Source', self.source)

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.source_combobox, SIGNAL('currentIndexChanged(int)'), self.set_source)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        sources = self.__get_sources()

        self.widget.source_combobox.clear()
        for i, source in enumerate(sources):
            self.widget.source_combobox.addItem(source[1], userData=source[0])
            if self.source == source[0]:
                self.widget.source_combobox.setCurrentIndex(i)

        # Finally connect the signals
        self.__enable_connections()

    def set_source(self, index):
        self.source = self.widget.source_combobox.itemData(index).toString()
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), 'Source', self.source)
        self.plugman.save()
        log.debug('Set pulseaudio source to %s' % self.source)

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.source_label.setText(self.gui.app.translate('plugin-pulseaudio', 'Source'))
