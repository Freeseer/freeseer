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

import avahi
import dbus


class ServiceAnnouncer:
    def __init__(self, name, service, port, txt):
        """Creates a ServiceAnnouncer that publishes Freeseer service on Zeroconf/Avahi

        Args:
            name - instance name i.e Freeseer Host
            service - service type i.e _freeseer._tcp
            port - port number
            info_list - List containing strings of information you wish to include.
        """
        bus = dbus.SystemBus()
        server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), avahi.DBUS_INTERFACE_SERVER)
        self.group = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew()), avahi.DBUS_INTERFACE_ENTRY_GROUP)
        self.service = service
        self.name = name
        self.port = port
        self.txt = txt

    def add_service(self):
        """Announces Freeseer service over Zeroconf/Avahi"""
        self.group.AddService(avahi.IF_UNSPEC, avahi.PROTO_INET, 0,
                              self.name, self.service, '', '', self.port,
                              avahi.string_array_to_txt_array(self.txt))
        self.group.Commit()

    def remove_service(self):
        """Removes service from Zeroconf/Avahi"""
        self.group.Reset()
