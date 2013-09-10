#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2013 Free and Open Source Software Learning Centre
# http://fosslc.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

pep8_options = {'max_line_length': 160,
                'ignore': ['E128',   # Ignore under indents
                           'E221',   # Multiple whitespace before operator
                           'E241']}  # Ignore multiple whitespaces after :


def pep8_report(test, report):
    output = ''
    for line in report.get_statistics(''):
        output += '\t%s\n' % line

    test.assertEqual(report.total_errors, 0,
                     "Found %s code style errors (and warnings):\n\n%s" % (report.total_errors, output))
