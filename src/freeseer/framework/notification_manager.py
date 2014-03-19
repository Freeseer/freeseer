#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014  Free and Open Source Software Learning Centre
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
    """stores and manages notifications"""

    def __init__(self):
        self.n_manager = collections.OrderedDict()
        self.callback_list = []

        self.event_warning = "warning"
        self.event_error = "error"
        self.event_remove = "remove"

        # temp way of assigning unique keywords to notifications
        self.keyword_counter = 0

    def add_notification(self, notification):
        self.n_manager[self.keyword_counter] = notification
        self.keyword_counter = self.keyword_counter + 1
        return self.keyword_counter - 1

    def delete_notification(self, keyword):
        del self.n_manager[keyword]

    def register_callback(self, event, func):
        if not event in self.callback_list:
            self.callback_list[event] = []
        if not func in self.callback_list[event]:
            self.callback_list[event].append(func)

    def deregister_callback(self, event, func):
        if event in self.callback_list:
            if func in self.callback_list[event]:
                self.callback_list[event].remove(func)

    def notify(self, event, argv):
        if event == self.event_warning or event == self.event_error:
            key = self.add_notification(argv)
            for func in self.callback_list[event]:
                func(argv)
            return key
        elif event == self.event_remove:
            self.delete_notification(argv)
            for func in self.callback_list[event]:
                func(argv)
            return argv
