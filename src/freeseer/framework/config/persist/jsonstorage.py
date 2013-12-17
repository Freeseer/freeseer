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

import json
import os

from freeseer.framework.config.core import ConfigStorage


class JSONConfigStorage(ConfigStorage):
    """Persists Configs to and from JSON formatted config files."""

    def parse_json(self):
        if os.path.isfile(self._filepath):
            return json.load(open(self._filepath))
        else:
            return {}

    def write_json(self, dict_):
        with open(self._filepath, 'wc') as config_fd:
            config_fd.write(json.dumps(dict_,
                                       sort_keys=True,
                                       indent=4,
                                       separators=(',', ': ')))

    def load(self, config_instance, section):
        dict_ = self.parse_json()
        if section not in dict_:
            return config_instance

        for name, option in config_instance.options.iteritems():
            if name in dict_[section]:
                raw = dict_[section][name]
                clean = option.decode(raw)
                config_instance.set_value(name, option, clean)
        return config_instance

    def store(self, config_instance, section):
        dict_ = self.parse_json()
        if section not in dict_:
            dict_[section] = {}

        for name, option in config_instance.options.iteritems():
            raw = config_instance.get_value(name, option)
            clean = option.encode(raw)
            dict_[section][name] = clean

        self.write_json(dict_)
