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


class StorageNotSetError(Exception):

    def __init__(self):
        super(StorageNotSetError, self).__init__('no ConfigStorage was given to this Config')


class OptionError(Exception):

    def __init__(self, name, option):
        super(OptionError, self).__init__(name)


class InvalidOptionValueError(OptionError):
    pass


class InvalidOptionDefaultValueError(OptionError):
    pass


class OptionValueNotSetError(OptionError):
    pass


class InvalidDecodeValueError(Exception):

    def __init__(self, value):
        message = 'Unable to decode value "{}"'.format(value)
        super(InvalidDecodeValueError, self).__init__(message)
