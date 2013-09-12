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
Auto Audio Source
-----------------

Very basic plugin which allows GStreamer to auto detect
which audio source to use. Not configurable.

@author: Thanh Ha
'''

import pygst
pygst.require("0.10")
import gst

from freeseer.framework.plugin import IAudioInput


class AutoAudioSrc(IAudioInput):
    name = "Auto Audio Source"
    os = ["linux", "linux2", "win32", "cygwin", "darwin"]

    def get_audioinput_bin(self):
        bin = gst.Bin()  # Do not pass a name so that we can load this input more than once.

        audiosrc = gst.element_factory_make("autoaudiosrc", "audiosrc")
        bin.add(audiosrc)

        # Setup ghost pad
        pad = audiosrc.get_pad("src")
        ghostpad = gst.GhostPad("audiosrc", pad)
        bin.add_pad(ghostpad)

        return bin
