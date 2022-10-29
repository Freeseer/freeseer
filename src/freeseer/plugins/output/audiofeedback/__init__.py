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
Audio Feedback
--------------

An output plugin which routes sound to the device's available
speakers.

@author: Thanh Ha
'''

# GStreamer
import pygst
pygst.require("0.10")
import gst

# PyQt
from PyQt4.QtCore import SIGNAL

# Freeseer
from freeseer.framework.plugin import IOutput
from freeseer.framework.config import Config, options

# .freeseer-plugin
from . import widget


class AudioFeedbackConfig(Config):
    """Configuration class for AudioFeedback plugin."""
    feedbacksink = options.StringOption("autoaudiosink")


class AudioFeedback(IOutput):
    name = "Audio Feedback"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]
    type = IOutput.AUDIO
    recordto = IOutput.OTHER
    CONFIG_CLASS = AudioFeedbackConfig

    def get_output_bin(self, audio=True, video=False, metadata=None):
        bin = gst.Bin()

        audioqueue = gst.element_factory_make("queue", "audioqueue")
        bin.add(audioqueue)

        audiosink = gst.element_factory_make(self.config.feedbacksink, "audiosink")
        bin.add(audiosink)

        # Setup ghost pad
        pad = audioqueue.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        bin.add_pad(ghostpad)

        audioqueue.link(audiosink)

        return bin

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.feedbackComboBox, SIGNAL('currentIndexChanged(const QString&)'), self.set_feedbacksink)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        feedbackIndex = self.widget.feedbackComboBox.findText(self.config.feedbacksink)
        self.widget.feedbackComboBox.setCurrentIndex(feedbackIndex)

        # Finally enable connections
        self.__enable_connections()

    def set_feedbacksink(self, feedbacksink):
        self.config.feedbacksink = feedbacksink
        self.config.save()

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.feedbackLabel.setText(self.gui.app.translate('plugin-audiofeedback', 'Feedback'))
