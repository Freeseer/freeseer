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

from freeseer.framework.plugin import IOutput

class OggIcecast(IOutput):
    name = "Ogg Icecast"
    os = ["linux2"]
    type = IOutput.BOTH
    recordto = IOutput.STREAM
    extension = "ogg"
    tags = None
    
    # Icecast server variables
    ip = "127.0.0.1"
    port = "8000"
    password = "hackme"
    mount = "stream.ogg"
    
    def get_output_bin(self, audio=True, video=True, metadata=None):
        bin = gst.Bin(self.name)
        
        if metadata is not None:
            self.set_metadata(metadata)
            
        # Muxer
        muxer = gst.element_factory_make("oggmux", "muxer")
        bin.add(muxer)
        
        icecast = gst.element_factory_make("shout2send", "icecast")
        icecast.set_property("ip", self.ip)
        icecast.set_property("port", self.port)
        icecast.set_property("password", self.password)
        icecast.set_property("mount", self.mount)
        bin.add(icecast)
        
        #
        # Setup Audio Pipeline
        #
        if audio:
            audioqueue = gst.element_factory_make("queue", "audioqueue")
            bin.add(audioqueue)
            
            audioconvert = gst.element_factory_make("audioconvert", "audioconvert")
            bin.add(audioconvert)
            
            audiocodec = gst.element_factory_make("vorbisenc", "audiocodec")
            bin.add(audiocodec)
            
            # Setup metadata
            vorbistag = gst.element_factory_make("vorbistag", "vorbistag")
            # set tag merge mode to GST_TAG_MERGE_REPLACE
            merge_mode = gst.TagMergeMode.__enum_values__[2]
    
            vorbistag.merge_tags(self.tags, merge_mode)
            vorbistag.set_tag_merge_mode(merge_mode)
            bin.add(vorbistag)
            
            # Setup ghost pads
            audiopad = audioqueue.get_pad("sink")
            audio_ghostpad = gst.GhostPad("audiosink", audiopad)
            bin.add_pad(audio_ghostpad)
            
            gst.element_link_many(audioqueue, audioconvert, audiocodec, vorbistag, muxer)
        
        #
        # Setup Video Pipeline
        #
        if video:
            videoqueue = gst.element_factory_make("queue", "videoqueue")
            bin.add(videoqueue)
            
            videocodec = gst.element_factory_make("theoraenc", "videocodec")
            bin.add(videocodec)
            
            videopad = videoqueue.get_pad("sink")
            video_ghostpad = gst.GhostPad("videosink", videopad)
            bin.add_pad(video_ghostpad)
            
            gst.element_link_many(videoqueue, videocodec, muxer)
        
        #
        # Link muxer to icecast
        #
        gst.element_link_many(muxer, icecast)
        
        return bin
    
    def set_metadata(self, data):
        '''
        Populate global tag list variable with file metadata for
        vorbistag audio element
        '''
        self.tags = gst.TagList()

        for tag in data.keys():
            if(gst.tag_exists(tag)):
                self.tags[tag] = data[tag]
            else:
                #self.core.logger.log.debug("WARNING: Tag \"" + str(tag) + "\" is not registered with gstreamer.")
                pass

    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.ip = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "IP")
            self.port = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Port")
            self.password = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Password")
            self.mount = self.plugman.plugmanc.readOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Mount")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "IP", self.ip)
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Port", self.port)
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Password", self.password)
            self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Mount", self.mount)
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label_ip = QtGui.QLabel("IP")
            self.lineedit_ip = QtGui.QLineEdit()
            layout.addRow(self.label_ip, self.lineedit_ip)
            
            self.label_port = QtGui.QLabel("Port")
            self.lineedit_port = QtGui.QLineEdit()
            layout.addRow(self.label_port, self.lineedit_port)
            
            self.label_password = QtGui.QLabel("Password")
            self.lineedit_password = QtGui.QLineEdit()
            layout.addRow(self.label_password, self.lineedit_password)
            
            self.label_mount = QtGui.QLabel("Mount")
            self.lineedit_mount = QtGui.QLineEdit()
            layout.addRow(self.label_mount, self.lineedit_mount)
            
            self.widget.connect(self.lineedit_ip, QtCore.SIGNAL('editingFinished()'), self.set_ip)
            self.widget.connect(self.lineedit_port, QtCore.SIGNAL('editingFinished()'), self.set_port)
            self.widget.connect(self.lineedit_password, QtCore.SIGNAL('editingFinished()'), self.set_password)
            self.widget.connect(self.lineedit_mount, QtCore.SIGNAL('editingFinished()'), self.set_mount)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
            
        self.lineedit_ip.setText(self.ip)
        self.lineedit_port.setText(self.port)
        self.lineedit_password.setText(self.password)
        self.lineedit_mount.setText(self.mount)

    def set_ip(self):
        ip = str(self.lineedit_ip.text())
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "IP", ip)
        self.plugman.save()
        
    def set_port(self):
        port = str(self.lineedit_port.text())
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Port", port)
        self.plugman.save()
        
    def set_password(self):
        password = str(self.lineedit_password.text())
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Password", password)
        self.plugman.save()
        
    def set_mount(self):
        mount = str(self.lineedit_mount.text())
        self.plugman.plugmanc.registerOptionFromPlugin(self.CATEGORY, self.get_config_name(), "Mount", mount)
        self.plugman.save()
