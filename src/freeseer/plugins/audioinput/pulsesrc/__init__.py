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
# http://github.com/Freeseer/freeseer/

'''
PulseAudio Source
-----------------

An audio plugin which uses PulseAudio as the audio input.

@author: Thanh Ha
'''

# python-libs
import logging

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin import IAudioInput
from freeseer.framework.config import Config, options

# .freeseer-plugin custom
from . import widget

log = logging.getLogger(__name__)


def get_sources():
    """
    Get a list of pairs in the form (name, description) for each pulseaudio source.
    """
    audiosrc = gst.element_factory_make("pulsesrc", "audiosrc")
    audiosrc.probe_property_name('device')
    names = audiosrc.probe_get_values_name('device')
    # TODO: should be getting actual device description, but .get_property('device-name') does not work
    return list(zip(names, names))


def get_default_source():
    """Returns the default audio source."""
    sources = get_sources()
    if not sources:
        return ''
    else:
        return sources[0][0]


class PulseSrcConfig(Config):
    """Default PulseSrc config settings."""
    source = options.StringOption('')


class PulseSrc(IAudioInput):
    name = "Pulse Audio Source"
    os = ["linux", "linux2"]
    CONFIG_CLASS = PulseSrcConfig

    def get_audioinput_bin(self):
        bin = gst.Bin()  # Do not pass a name so that we can load this input more than once.

        audiosrc = gst.element_factory_make("pulsesrc", "audiosrc")

        if not self.config.source:
            self.config.source = get_default_source()

        audiosrc.set_property('device', self.config.source)
        log.debug('Pulseaudio source is set to %s', audiosrc.get_property('device'))

        bin.add(audiosrc)

        # Setup ghost pad
        pad = audiosrc.get_pad("src")
        ghostpad = gst.GhostPad("audiosrc", pad)
        bin.add_pad(ghostpad)

        return bin

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.source_combobox, SIGNAL('currentIndexChanged(int)'), self.set_source)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        sources = get_sources()

        self.widget.source_combobox.clear()
        for i, source in enumerate(sources):
            self.widget.source_combobox.addItem(source[1], userData=source[0])
            if self.config.source == source[0]:
                self.widget.source_combobox.setCurrentIndex(i)

        # Finally connect the signals
        self.__enable_connections()

    def set_source(self, index):
        self.config.source = self.widget.source_combobox.itemData(index).toString()
        log.debug('Set pulseaudio source to %s', self.config.source)
        self.config.save()

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.source_label.setText(self.gui.app.translate('plugin-pulseaudio', 'Source'))
