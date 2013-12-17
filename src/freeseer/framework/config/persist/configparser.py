#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
# http://wiki.github.com/Freeseer/freeseer/

import ConfigParser

from freeseer.framework.config.core import ConfigStorage


class ConfigParserStorage(ConfigStorage):
    """Persists Configs to and from INI style config files."""

    def load(self, config_instance, section):
        parser = ConfigParser.ConfigParser()
        parser.read([self._filepath])

        for name, option in config_instance.options.iteritems():
            if parser.has_option(section, name):
                raw = parser.get(section, name)
                clean = option.decode(raw)
                config_instance.set_value(name, option, clean)

        return config_instance

    def store(self, config_instance, section):
        parser = ConfigParser.ConfigParser()
        parser.read([self._filepath])

        if not parser.has_section(section):
            parser.add_section(section)

        for name, option in config_instance.options.iteritems():
            raw = config_instance.get_value(name, option)
            clean = option.encode(raw)
            parser.set(section, name, clean)

        with open(self._filepath, 'w') as config_fd:
            parser.write(config_fd)
