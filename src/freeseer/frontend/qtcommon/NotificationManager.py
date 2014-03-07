#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2014  Free and Open Source Software Learning Centre
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
# http://wiki.github.com/Freeseer/freeseer/

import collections


class NotificationManager:
    def __init__(self):
        self.n_manager = collections.OrderedDict()
        self.error = False

    def add_warning(self, name, message):
        self.n_manager[name] = message

    def add_error(self, name, message):
        self.n_manager.clear()
        self.n_manager[name] = message
        self.error = True

    def delete_warning(self, name):
        if len(self.n_manager) and name in self.n_manager:
            del self.n_manager[name]

    def get_length(self):
        return len(self.n_manager)

    def get_notification(self):
        return self.n_manager.items()[0][1]

    def error_in_queue(self):
        return self.error
