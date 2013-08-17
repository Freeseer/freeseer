'''
freeseer - vga/presentation capture software

Copyright (C) 2011-2013  Free and Open Source Software Learning Centre
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

# python-lib
import ConfigParser

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin import IOutput

# .freeseer-plugin custom
import widget

class OggIcecast(IOutput):
    name = "Ogg Icecast"
    os = ["linux", "linux2"]
    type = IOutput.BOTH
    recordto = IOutput.STREAM
    extension = "ogg"
    tags = None
    
    # Icecast server variables
    ip = "127.0.0.1"
    port = 8000
    password = "hackme"
    mount = "stream.ogg"
    
    def get_output_bin(self, audio=True, video=True, metadata=None):
        bin = gst.Bin()
        
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
    
            if metadata is not None:
                # Only set tag if metadata is set
                vorbistag.merge_tags(self.tags, merge_mode)
            vorbistag.set_tag_merge_mode(merge_mode)
            bin.add(vorbistag)
            
            # Setup ghost pads
            audiopad = audioqueue.get_pad("sink")
            audio_ghostpad = gst.GhostPad("audiosink", audiopad)
            bin.add_pad(audio_ghostpad)
            
            # Link elements
            audioqueue.link(audioconvert)
            audioconvert.link(audiocodec)
            audiocodec.link(vorbistag)
            vorbistag.link(muxer)
        
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
            
            videoqueue.link(videocodec)
            videocodec.link(muxer)
        
        #
        # Link muxer to icecast
        #
        muxer.link(icecast)
        
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
            self.ip = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "IP")
            self.port = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Port"))
            self.password = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Password")
            self.mount = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Mount")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "IP", self.ip)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Port", self.port)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Password", self.password)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Mount", self.mount)
        except TypeError:
            # Temp fix for issue when reading framerate the 2nd time causes TypeError
            pass
    
    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.lineedit_ip, SIGNAL('editingFinished()'), self.set_ip)
        self.widget.connect(self.widget.spinbox_port, SIGNAL('valueChanged(int)'), self.set_port)
        self.widget.connect(self.widget.lineedit_password, SIGNAL('editingFinished()'), self.set_password)
        self.widget.connect(self.widget.lineedit_mount, SIGNAL('editingFinished()'), self.set_mount)

    def widget_load_config(self, plugman):
        self.load_config(plugman)
            
        self.widget.lineedit_ip.setText(self.ip)
        self.widget.spinbox_port.setValue(self.port)
        self.widget.lineedit_password.setText(self.password)
        self.widget.lineedit_mount.setText(self.mount)

        # Finally enable connections
        self.__enable_connections()

    def set_ip(self):
        ip = str(self.widget.lineedit_ip.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "IP", ip)
        
    def set_port(self, port):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Port", port)
        
    def set_password(self):
        password = str(self.widget.lineedit_password.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Password", password)
        
    def set_mount(self):
        mount = str(self.widget.lineedit_mount.text())
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Mount", mount)

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.label_ip.setText(self.gui.app.translate('plugin-icecast', 'IP'))
        self.widget.label_port.setText(self.gui.app.translate('plugin-icecast', 'Port'))
        self.widget.label_password.setText(self.gui.app.translate('plugin-icecast', 'Password'))
        self.widget.label_mount.setText(self.gui.app.translate('plugin-icecast', 'Mount'))
