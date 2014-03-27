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
        self.notifications = collections.OrderedDict()
        self.callbacks = {
            'warning': [],
            'error': [],
            'remove-error': [],
            'remove-warning': [],
        }

        # temp way of assigning unique keywords to notifications
        self.keyword_counter = 0

    def add_warning(self, notification):
        if not len(self.callbacks['warning']) == 0:
            self.notifications[self.keyword_counter] = notification
            self.keyword_counter = self.keyword_counter + 1
            for func in self.callbacks['warning']:
                func(notification)
            return self.keyword_counter - 1
        else:
            pass  # error

    def add_error(self, notification):
        if not len(self.callbacks['error']) == 0:
            self.notifications[self.keyword_counter] = notification
            self.keyword_counter = self.keyword_counter + 1
            for func in self.callbacks['error']:
                func(notification)
            return self.keyword_counter - 1
        else:
            pass  # error

    def delete_warning(self, keyword):
        if not len(self.callbacks['remove-warning']) == 0:
            del self.notifications[keyword]
            for func in self.callbacks['remove-warning']:
                func()
        else:
            pass  #

    def delete_error(self, keyword):
        if not len(self.callbacks['remove-error']) == 0:
            del self.notifications[keyword]
            for func in self.callbacks['remove-error']:
                func()
        else:
            pass  #

    def register(self, event, func):
        if event in self.callbacks:
            self.callbacks[event].append(func)
        else:
            pass  # error

    def deregister(self, event, func):
        if event in self.callbacks:
            if func in self.callbacks[event]:
                self.callbacks[event].remove(func)
            else:
                pass  # error
        else:
            pass  # error
