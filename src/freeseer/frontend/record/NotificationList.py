#!/usr/bin/python
# -*- coding: utf-8 -*-

class NotificationList:
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    def add_notification(self, notification):
        if not self.head == None:
            if notification.priority == 2:
                self.tail.next = notification
                self.tail = notification
            else:
                notification.next = self.head
                self.head = notification
        else:
            self.head = notification
            self.tail = notification
        self.length = self.length + 1

    def delete_notification(self, keyword):
        if not self.head == None:
            prev = None
            current = self.head
            while not current.keyword == keyword and not current.next == None:
                prev = current
                current = current.next

            if not prev == None:
                prev.next = current.next
            else:
                self.head = current.next
            self.length = self.length - 1

    def get_length(self):
        return self.length

    def get_head(self):
        return self.head

class Notification:
    def __init__(self, message=None, priority=2, next=None, keyword=None):
        self.message = message
        self.priority = priority
        self.next = next
        self.keyword = keyword

    def get_message(self):
        return self.message
