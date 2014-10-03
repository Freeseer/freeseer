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
Video Test Source
-----------------

A video input plugin that displays a test pattern to the screen. Useful for
testing and debugging Freeseer.

@author: Thanh Ha
'''

# python-libs
try:  # Import using Python3 module name
    import configparser
except ImportError:
    import ConfigParser as configparser

# GStreamer modules
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

# PyQt4 modules
from PyQt4.QtCore import SIGNAL

# Freeseer modules
from freeseer.framework.plugin import IVideoInput

# .freeseer-plugin custom modules
import widget


class VideoTestSrc(IVideoInput):
    name = "Video Test Source"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]

    # variables
    live = False
    pattern = "smpte"

    # Patterns
    PATTERNS = ["smpte", "snow", "black", "white", "red", "green", "blue",
                "circular", "blink", "smpte75", "zone-plate", "gamut",
                "chroma-zone-plate", "ball", "smpte100", "bar"]

    def get_videoinput_bin(self):
        bin = Gst.Bin()  # Do not pass a name so that we can load this input more than once.

        videosrc = Gst.ElementFactory.make("videotestsrc", "videosrc")
        videosrc.set_property("pattern", self.pattern)
        videosrc.set_property("is-live", self.live)
        bin.add(videosrc)

        # Setup ghost pad
        pad = videosrc.get_static_pad("src")
        ghostpad = Gst.GhostPad.new("videosrc", pad)
        bin.add_pad(ghostpad)

        return bin

    def load_config(self, plugman):
        self.plugman = plugman

        try:
            live = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Live")
            if live == "True":
                self.live = True
            self.pattern = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Pattern")
        except (configparser.NoSectionError, configparser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Live", self.live)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Pattern", self.pattern)
        except TypeError:
            # Temp fix for issue where reading checkbox the 2nd time causes TypeError.
            pass

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

            for i in self.PATTERNS:
                self.widget.patternComboBox.addItem(i)

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.liveCheckBox, SIGNAL('toggled(bool)'), self.set_live)
        self.widget.connect(self.widget.patternComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.set_pattern)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        self.widget.liveCheckBox.setChecked(bool(self.live))
        patternIndex = self.widget.patternComboBox.findText(self.pattern)
        self.widget.patternComboBox.setCurrentIndex(patternIndex)

        # Finally enable connections
        self.__enable_connections()

    def set_live(self, checked):
        self.live = checked
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Live", self.live)

    def set_pattern(self, pattern):
        self.pattern = pattern
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Pattern", self.pattern)

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.patternLabel.setText(self.gui.app.translate('plugin-videotest', 'Pattern'))
        self.widget.liveCheckBox.setText(self.gui.app.translate('plugin-videotest', 'Live Source'))
        self.widget.liveCheckBox.setToolTip(self.gui.app.translate('plugin-videotest', 'Act as a live video source'))
