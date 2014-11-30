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

import socket
from time import sleep

from zeroconf import ServiceBrowser, Zeroconf


class Listener(object):

    def __init__(self):
        self.servers = {}

    def removeService(self, zeroconf, type, name):
        """Updates dictionary of available freeseer servers"""
        info = zeroconf.getServiceInfo(type, name)
        ipaddr = socket.inet_ntoa(info.getAddress())
        port = info.getPort()
        del self.servers[(ipaddr, port)]

    def addService(self, zeroconf, type, name):
        """Updates dictionary of available freeseer servers"""
        info = zeroconf.getServiceInfo(type, name)
        if info:
            ipaddr = socket.inet_ntoa(info.getAddress())
            port = info.getPort()
            self.servers[(ipaddr, port)] = {
                'name': name,
                'type': type,
            }


def search(timeout):
    results = []
    zeroconf = Zeroconf(socket.gethostbyname(socket.gethostname()))
    listener = Listener()
    ServiceBrowser(zeroconf, '_freeseer._tcp.local.', listener)
    sleep(timeout)
    for (ipaddr, port), value in listener.servers.iteritems():
        results.append('{}\t{}:{}'.format(value['name'].split('.')[0], ipaddr, port))
    zeroconf.close()
    return results
