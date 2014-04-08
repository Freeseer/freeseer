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

import freeseer.framework.config.options as options

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin.plugin import AudioInputPlugin
from freeseer.framework.config.core import Config

# .freeseer-plugin custom
import widget


class JackAudioSrcConfig(Config):
    # I'm not sure if they're supposed to be string options, but the default value previously was
    # "" so I think that's appropriate.
    client = options.StringOption()
    connect = options.StringOption()
    server = options.StringOption()
    clientname = options.StringOption()


class JackAudioSrc(AudioInputPlugin):
    name = "Jack Audio Source"
    os = ["linux", "linux2"]

    CONFIG_CLASS = JackAudioSrcConfig

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

        self.widget.lineedit_client.setText(self.client)
        self.widget.lineedit_connect.setText(self.connect)
        self.widget.lineedit_server.setText(self.server)
        self.widget.lineedit_clientname.setText(self.clientname)

        # Finally enable connections
        self.__enable_connections()

    def set_client(self):
        client = str(self.widget.lineedit_client.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Client", client)

    def set_connect(self):
        connect = str(self.widget.lineedit_connect.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Connect", connect)

    def set_server(self):
        server = str(self.widget.lineedit_server.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Server", server)

    def set_clientname(self):
        clientname = str(self.widget.lineedit_clientname.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "ClientName", clientname)

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.label_client.setText(self.gui.app.translate('plugin-jackaudio', 'Client'))
        self.widget.label_connect.setText(self.gui.app.translate('plugin-jackaudio', 'Connect'))
        self.widget.label_server.setText(self.gui.app.translate('plugin-jackaudio', 'Server'))
        self.widget.label_clientname.setText(self.gui.app.translate('plugin-jackaudio', 'Client Name'))
