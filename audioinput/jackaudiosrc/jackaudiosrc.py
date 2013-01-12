'''
freeseer - vga/presentation capture software

Copyright (C) 2011-2012  Free and Open Source Software Learning Centre
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

import ConfigParser

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IAudioInput

class JackAudioSrc(IAudioInput):
    name = "Jack Audio Source"
    os = ["linux", "linux2"]
    
    # jackaudio variables
    client = ""
    connect = ""
    server = ""
    clientname = ""
    
    def get_audioinput_bin(self):
        bin = gst.Bin() # Do not pass a name so that we can load this input more than once.
        
        audiosrc = gst.element_factory_make("jackaudiosrc", "audiosrc")
        bin.add(audiosrc)
        
        # Setup ghost pad
        pad = audiosrc.get_pad("src")
        ghostpad = gst.GhostPad("audiosrc", pad)
        bin.add_pad(ghostpad)
        
        return bin

    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.client = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Client")
            self.connect = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Connect")
            self.server = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Server")
            self.clientname = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "ClientName")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Client", self.client)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Connect", self.connect)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Server", self.server)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "ClientName", self.clientname)
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label_client = QtGui.QLabel("Client")
            self.lineedit_client = QtGui.QLineEdit()
            layout.addRow(self.label_client, self.lineedit_client)
            
            self.label_connect = QtGui.QLabel("Connect")
            self.lineedit_connect = QtGui.QLineEdit()
            layout.addRow(self.label_connect, self.lineedit_connect)
            
            self.label_server = QtGui.QLabel("Server")
            self.lineedit_server = QtGui.QLineEdit()
            layout.addRow(self.label_server, self.lineedit_server)
            
            self.label_clientname = QtGui.QLabel("Client Name")
            self.lineedit_clientname = QtGui.QLineEdit()
            layout.addRow(self.label_clientname, self.lineedit_clientname)
            
            self.widget.connect(self.lineedit_client, QtCore.SIGNAL('editingFinished()'), self.set_client)
            self.widget.connect(self.lineedit_connect, QtCore.SIGNAL('editingFinished()'), self.set_connect)
            self.widget.connect(self.lineedit_server, QtCore.SIGNAL('editingFinished()'), self.set_server)
            self.widget.connect(self.lineedit_clientname, QtCore.SIGNAL('editingFinished()'), self.set_clientname)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
            
        self.lineedit_client.setText(self.client)
        self.lineedit_connect.setText(self.connect)
        self.lineedit_server.setText(self.server)
        self.lineedit_clientname.setText(self.clientname)

    def set_client(self):
        client = str(self.lineedit_client.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Client", client)
        self.plugman.save()
        
    def set_connect(self):
        connect = str(self.lineedit_connect.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Connect", connect)
        self.plugman.save()
        
    def set_server(self):
        server = str(self.lineedit_server.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Server", server)
        self.plugman.save()
        
    def set_clientname(self):
        clientname = str(self.lineedit_clientname.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "ClientName", clientname)
        self.plugman.save()
