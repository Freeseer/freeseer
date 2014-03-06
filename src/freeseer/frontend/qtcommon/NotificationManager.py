#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        if len(self.n_manager) and self.n_manager.has_key(name):
            del self.n_manager[name]

    def get_length(self):
        return len(self.n_manager)

    def get_notification(self):
        return self.n_manager.items()[0][1]

    def error_in_queue(self):
        return self.error
