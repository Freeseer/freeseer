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

# GStreamer modules
import pygst
pygst.require("0.10")
import gst

# PyQt4 modules
from PyQt4.QtCore import SIGNAL

# Freeseer modules
from freeseer.framework.plugin import IVideoInput
from freeseer.framework.config import Config, options

# .freeseer-plugin custom modules
import widget

# Patterns
PATTERNS = ["smpte", "snow", "black", "white", "red", "green", "blue",
            "circular", "blink", "smpte75", "zone-plate", "gamut",
            "chroma-zone-plate", "ball", "smpte100", "bar"]


class VideoTestSrcConfig(Config):
    """Config settings for VideoTestSrc plugin."""
    live = options.BooleanOption(False)
    pattern = options.ChoiceOption(PATTERNS, default="smpte")


class VideoTestSrc(IVideoInput):
    name = "Video Test Source"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    CONFIG_CLASS = VideoTestSrcConfig

    def get_videoinput_bin(self):
        bin = gst.Bin()  # Do not pass a name so that we can load this input more than once.

        videosrc = gst.element_factory_make("videotestsrc", "videosrc")
        videosrc.set_property("pattern", self.config.pattern)
        videosrc.set_property("is-live", self.config.live)
        bin.add(videosrc)

        # Setup ghost pad
        pad = videosrc.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)

        return bin

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

            for i in PATTERNS:
                self.widget.patternComboBox.addItem(i)

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.liveCheckBox, SIGNAL('toggled(bool)'), self.set_live)
        self.widget.connect(self.widget.patternComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.set_pattern)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        self.widget.liveCheckBox.setChecked(bool(self.config.live))
        patternIndex = self.widget.patternComboBox.findText(self.config.pattern)
        self.widget.patternComboBox.setCurrentIndex(patternIndex)

        # Finally enable connections
        self.__enable_connections()

    def set_live(self, checked):
        self.config.live = checked
        self.config.save()

    def set_pattern(self, pattern):
        self.config.pattern = pattern
        self.config.save()

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.patternLabel.setText(self.gui.app.translate('plugin-videotest', 'Pattern'))
        self.widget.liveCheckBox.setText(self.gui.app.translate('plugin-videotest', 'Live Source'))
        self.widget.liveCheckBox.setToolTip(self.gui.app.translate('plugin-videotest', 'Act as a live video source'))
