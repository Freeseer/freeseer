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
ALSA Source
-----------

An audio plugin which uses ALSA as the audio input.

@author: Thanh Ha
'''

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

from freeseer.framework.plugin import IAudioInput


class ALSASrc(IAudioInput):
    name = "ALSA Source"
    os = ["linux", "linux2"]

    def get_audioinput_bin(self):
        bin = Gst.Bin()  # Do not pass a name so that we can load this input more than once.

        audiosrc = Gst.ElementFactory.make("alsasrc", "audiosrc")
        bin.add(audiosrc)

        # Setup ghost pad
        pad = audiosrc.get_static_pad("src")
        ghostpad = Gst.GhostPad.new("audiosrc", pad)
        bin.add_pad(ghostpad)

        return bin
