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
from freeseer.framework.plugin import IPlugin


class Manager(object):

    def __init__(self, dir_path):
        self.plugins = {}

        for module_path in self.find_module_files(dir_path):
            self.find_plugin(module_path)
            self.find_module_files(dir_path)

    def find_module_files(self, dir_path):
        for (dirpath, dirnames, filenames) in os.walk(dir_path):
            for filename in fnmatch.filter(filenames, '*.py'):
                if filename == "__init__.py":
                    yield dirpath
                else:
                    yield os.path.join(dirpath, filename)

    def find_plugin(self, module_path):
        module = None
        if (os.path.isdir(module_path)):
            module = imp.load_module("name", None, module_path, ("py", "r", imp.PKG_DIRECTORY))
        else:
            module = imp.load_source(module_path, module_path)

        for attr_name in dir(module):
            module_obj = getattr(module, attr_name)
            self.check_plugin(module_obj)

    def check_plugin(self, module_obj):
        if inspect.isclass(module_obj) and issubclass(module_obj, IPlugin):
            obj = module_obj()
            if hasattr(obj, "NAME") and hasattr(obj, "CATEGORY"):
                category_name = getattr(obj, "CATEGORY")

                if category_name not in self.plugins:
                    self.plugins[category_name] = []

                self.plugins[category_name].append(obj)


def main():
    test = Manager("/home/sephallia/git/freeseer/src/freeseer/plugins/")
    print (test.plugins)

if __name__ == '__main__':
    main()
