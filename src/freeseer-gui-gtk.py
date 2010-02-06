#!/usr/bin/python

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2010  Free and Open Source Software Learning Centre
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
# the #fosslc channel on IRC (freenode.net)

from freeseer import *
import sys, os
import pygtk, gtk

class GTK_Main:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("FreeSeeR GTK GUI - example")
        window.set_default_size(480,320)
        window.connect("destroy", gtk.main_quit, "WM destroy")
        vbox = gtk.VBox()
        window.add(vbox)
        self.button = gtk.Button("Record")
        self.button.connect("clicked", self.record)
        vbox.add(self.button)
        self.videosrc_list = gtk.combo_box_new_text()
        self.videosrc_list.append_text('v4lsrc')
        self.videosrc_list.append_text('v4l2src')
        vbox.add(self.videosrc_list)
        self.videobox = gtk.DrawingArea()
        vbox.add(self.videobox)
        window.show_all()

        self.freeseer = FreeSeeR()
        self.freeseer.enable_preview(self.videobox.window.xid)

    def record(self, w):
        self.freeseer.change_videosrc(self.videosrc_list.get_active_text(), '/dev/video0')
        self.freeseer.record('default.mkv')

GTK_Main()
gtk.gdk.threads_init()
gtk.main()

