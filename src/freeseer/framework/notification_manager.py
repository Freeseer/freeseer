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

import logging
import collections

log = logging.getLogger(__name__)


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

    def add_notification(self, event, notification):
        if len(self.callbacks[event]) > 0:
            self.keyword = "{}-{}".format(self.keyword_counter, event)
            self.notifications[self.keyword] = notification
            self.keyword_counter = self.keyword_counter + 1
            for func in self.callbacks[event]:
                func(notification)
            return self.keyword
        else:
            log.error("There are no callback functions registered in {}".format(event))

    def delete_notification(self, event, keyword):
        if len(self.callbacks[event]) > 0:
            self.message = self.notifications[keyword]
            del self.notifications[keyword]
            for func in self.callbacks[event]:
                func(self.message)
        else:
            log.error("There are no callback functions registered in {}".format(event))

    def register(self, event, func):
        self.callbacks[event].append(func)

    def deregister(self, event, func):
        if func in self.callbacks[event]:
            self.callbacks[event].remove(func)
        else:
            log.error("Callback function {} is not registered in {}".format(func, event))
