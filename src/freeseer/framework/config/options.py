#!/usr/bin/env python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2013, 2014 Free and Open Source Software Learning Centre
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

import os

from freeseer.framework.config.core import Option
from freeseer.framework.config.exceptions import InvalidDecodeValueError


class StringOption(Option):
    """Represents a string value."""
    SCHEMA_TYPE = 'string'

    def is_valid(self, value):
        return isinstance(value, str) or hasattr(value, '__str__')

    def encode(self, value):
        return str(value)

    def decode(self, value):
        return str(value)


class IntegerOption(Option):
    """Represents an integer number value."""
    SCHEMA_TYPE = 'integer'

    def is_valid(self, value):
        return isinstance(value, int)

    def encode(self, value):
        return str(value)

    def decode(self, value):
        try:
            return int(value)
        except ValueError:
            raise InvalidDecodeValueError(value)


class FloatOption(Option):
    """Represents a floating point number value."""
    SCHEMA_TYPE = 'number'

    def is_valid(self, value):
        return isinstance(value, float)

    def encode(self, value):
        return str(value)

    def decode(self, value):
        try:
            return float(value)
        except ValueError:
            raise InvalidDecodeValueError(value)


class BooleanOption(Option):
    """Represents a boolean value."""
    SCHEMA_TYPE = 'boolean'

    def is_valid(self, value):
        return isinstance(value, bool)

    def encode(self, value):
        return value and 'true' or 'false'

    def decode(self, value):
        return value == 'true'


class FolderOption(Option):
    """Represents the path to a folder."""
    SCHEMA_TYPE = 'string'

    def __init__(self, default=Option.NotSpecified, auto_create=False):
        self.auto_create = auto_create
        super(FolderOption, self).__init__(default)

    def is_valid(self, value):
        return self.auto_create or os.path.isdir(value)

    def encode(self, value):
        return str(value)

    def decode(self, value):
        if self.is_valid(value):
            return value
        else:
            raise InvalidDecodeValueError(value)

    def presentation(self, value):
        """Returns the ~ expanded version of the path.

        When the value of this option is accessed by the user, special path characters like ~ will get expanded.
        """
        realpath = os.path.expanduser(value)
        if self.auto_create:
            if not os.path.exists(realpath):
                os.makedirs(realpath)
        return realpath


class ChoiceOption(StringOption):
    """Represents a selection from a pre-defined list of strings."""
    SCHEMA_TYPE = 'enum'

    def __init__(self, choices, default=Option.NotSpecified):
        self.choices = choices
        super(ChoiceOption, self).__init__(default)

    def is_valid(self, value):
        return value in self.choices

    def decode(self, value):
        choice = super(ChoiceOption, self).decode(value)
        if choice in self.choices:
            return choice
        else:
            raise InvalidDecodeValueError(value)

    def schema(self):
        schema = {'enum': self.choices}
        if self.default != Option.NotSpecified:
            schema['default'] = self.default
        return schema
