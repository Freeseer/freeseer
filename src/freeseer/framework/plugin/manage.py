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

import imp
import inspect
import fnmatch
import os
from freeseer.framework.plugin.plugin import Plugin


class PluginManager(object):

    def __init__(self, dir_path):
        self.plugins = {}

        for module_path in self.find_module_files(dir_path):
            for obj_in_module in self.find_object(module_path):
                if self.check_plugin(obj_in_module):
                    obj = obj_in_module
                    category_name = obj.CATEGORY
                    self.add_plugin(category_name, obj)

    def find_module_files(self, dir_path):
        for dirpath, _dirnames, filenames in os.walk(dir_path):
            for filename in fnmatch.filter(filenames, '*.py'):
                if filename == "__init__.py":
                    yield dirpath
                else:
                    yield os.path.join(dirpath, filename)

    def find_object(self, module_path):
        if os.path.isdir(module_path):
            module = imp.load_module("name", None, module_path, ("py", "r", imp.PKG_DIRECTORY))
        else:
            module = imp.load_source(module_path, module_path)

        for attr_name in dir(module):
            obj_in_module = getattr(module, attr_name)
            if inspect.isclass(obj_in_module):
                yield obj_in_module

    def check_plugin(self, obj_in_module):
        flag = False
        obj = obj_in_module()
        if issubclass(obj_in_module, Plugin):
            if hasattr(obj, "NAME") and hasattr(obj, "CATEGORY"):
                flag = True
        return flag

    def add_plugin(self, category_name, plugin_obj):
        if category_name not in self.plugins:
            self.plugins[category_name] = []

        self.plugins[category_name].append(plugin_obj)


def main():
    test = PluginManager("/home/sephallia/git/freeseer/src/freeseer/plugins/")
    print (test.plugins)

if __name__ == '__main__':
    main()
