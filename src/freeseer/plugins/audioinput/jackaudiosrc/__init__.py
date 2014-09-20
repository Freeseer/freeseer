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
Jack Audio Source
-----------------

An audio plugin which uses JACK as the audio input.

@author: Thanh Ha
'''
# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin import IAudioInput
from freeseer.framework.config import Config
import freeseer.framework.config.options as options

# .freeseer-plugin custom
import widget


class JackAudioConfig(Config):
    """Default Jackaudio Config settings"""

    client = options.StringOption('')
    connect = options.StringOption('')
    server = options.StringOption('')
    clientname = options.StringOption('')


class JackAudioSrc(IAudioInput):
    name = "Jack Audio Source"
    os = ["linux", "linux2"]
    CONFIG_CLASS = JackAudioConfig

    def get_audioinput_bin(self):
        bin = gst.Bin()  # Do not pass a name so that we can load this input more than once.

        audiosrc = gst.element_factory_make("jackaudiosrc", "audiosrc")
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
        self.widget.connect(self.widget.lineedit_client, SIGNAL('editingFinished()'), self.set_client)
        self.widget.connect(self.widget.lineedit_connect, SIGNAL('editingFinished()'), self.set_connect)
        self.widget.connect(self.widget.lineedit_server, SIGNAL('editingFinished()'), self.set_server)
        self.widget.connect(self.widget.lineedit_clientname, SIGNAL('editingFinished()'), self.set_clientname)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        self.widget.lineedit_client.setText(self.config.client)
        self.widget.lineedit_connect.setText(self.config.connect)
        self.widget.lineedit_server.setText(self.config.server)
        self.widget.lineedit_clientname.setText(self.config.clientname)

        # Finally enable connections
        self.__enable_connections()

    def set_client(self):
        self.config.client = str(self.widget.lineedit_client.text())
        self.config.save()

    def set_connect(self):
        self.config.connect = str(self.widget.lineedit_connect.text())
        self.config.save()

    def set_server(self):
        self.config.server = str(self.widget.lineedit_server.text())
        self.config.save()

    def set_clientname(self):
        self.config.clientname = str(self.widget.lineedit_clientname.text())
        self.config.save()

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.label_client.setText(self.gui.app.translate('plugin-jackaudio', 'Client'))
        self.widget.label_connect.setText(self.gui.app.translate('plugin-jackaudio', 'Connect'))
        self.widget.label_server.setText(self.gui.app.translate('plugin-jackaudio', 'Server'))
        self.widget.label_clientname.setText(self.gui.app.translate('plugin-jackaudio', 'Client Name'))
