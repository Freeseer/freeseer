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
USB Source
----------

A video input plugin that uses USB video devices as the video input source.

Devices such as Webcams and vga2usb frame grabbers.

@author: Thanh Ha
'''
import sys

# GStreamer modules
import pygst
pygst.require("0.10")
import gst

# PyQt modules
from PyQt4.QtCore import SIGNAL

# Freeseer modules
from freeseer.framework.plugin import IVideoInput
from freeseer.framework.config import Config, options

# .freeseer-plugin custom modules
from . import widget


def get_devices():
    """
    Returns a list of possible devices detected as a dictionary

    On Linux the dictionary is a key, value pair of:
        Device Name : Device Path

    On Windows the dictionary is a key, value pair of:
        Device Name : Device Name

    NOTE: GstPropertyProbe has been removed in later versions of Gstreamer
          When a new method is available this function will need to be
          redesigned:
              https://bugzilla.gnome.org/show_bug.cgi?id=678402
    """

    devicemap = {}

    if sys.platform.startswith("linux"):
        videosrc = gst.element_factory_make("v4l2src", "videosrc")
        videosrc.probe_property_name('device')
        devices = videosrc.probe_get_values_name('device')

        for device in devices:
            videosrc.set_property('device', device)
            devicemap[videosrc.get_property('device-name')] = device

    elif sys.platform in ["win32", "cygwin"]:
        videosrc = gst.element_factory_make("dshowvideosrc", "videosrc")
        videosrc.probe_property_name('device-name')
        devices = videosrc.probe_get_values_name('device-name')

        for device in devices:
            devicemap[device] = device

    return devicemap


def get_default_device():
    """Returns a default recording device from get_devices()."""
    devicemap = get_devices()
    if not devicemap:
        return ''
    default = next(iter(devicemap.values()))
    return default


class USBSrcConfig(Config):
    """USBSrc Configuration settings."""
    device = options.StringOption('')


class USBSrc(IVideoInput):
    name = "USB Source"
    os = ["linux", "linux2", "win32", "cygwin"]
    CONFIG_CLASS = USBSrcConfig

    def __init__(self):
        super(USBSrc, self).__init__()

    def get_videoinput_bin(self):
        """
        Return the video input object in gstreamer bin format.
        """
        bin = gst.Bin()  # Do not pass a name so that we can load this input more than once.

        videosrc = None

        if not self.config.device:
            self.config.device = get_default_device()

        if sys.platform.startswith("linux"):
            videosrc = gst.element_factory_make("v4l2src", "videosrc")
            videosrc.set_property("device", self.config.device)
        elif sys.platform in ["win32", "cygwin"]:
            videosrc = gst.element_factory_make("dshowvideosrc", "videosrc")
            videosrc.set_property("device-name", self.config.device)
        bin.add(videosrc)

        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)
        videosrc.link(colorspace)

        # Setup ghost pad
        pad = colorspace.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)

        return bin

    def get_widget(self):
        if self.widget is None:
            self.widget = widget.ConfigWidget()

        return self.widget

    def __enable_connections(self):
        self.widget.connect(self.widget.devicesCombobox, SIGNAL('activated(int)'), self.set_device)

    def widget_load_config(self, plugman):
        self.load_config(plugman)

        # Load the combobox with inputs
        self.widget.devicesCombobox.clear()
        n = 0
        for device, devurl in list(get_devices().items()):
            self.widget.devicesCombobox.addItem(device, devurl)
            if devurl == self.config.device:
                self.widget.devicesCombobox.setCurrentIndex(n)
            n += 1

        # Finally enable connections
        self.__enable_connections()

    def set_device(self, device):
        self.config.device = self.widget.devicesCombobox.itemData(device).toString()
        self.config.save()

    ###
    ### Translations
    ###
    def retranslate(self):
        self.widget.devicesLabel.setText(self.gui.app.translate('plugin-usb', 'Video Device'))
