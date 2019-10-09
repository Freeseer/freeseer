#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2013  Free and Open Source Software Learning Centre
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

"""
CSV Importer
--------------

An import plugin for CSV files used when adding presentations

@author: Rio Lowry
"""

import csv
import logging

from freeseer.framework.plugin import IImporter

log = logging.getLogger(__name__)


class CsvImporter(IImporter):
    """CSV Importer plugin for Freeseer

    Provides functionality to import presentations from a CSV file
    """

    name = "CSV Importer"
    os = ["linux", "linux2"]

    def get_presentations(self, fname):
        """Returns list of dictionaries of all presentations in the csv file."""
        presentations = []

        try:
            with open(fname) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    talk = {
                        'Title': str(row.get('Title', ''), 'utf-8'),
                        'Speaker': str(row.get('Speaker', ''), 'utf-8'),
                        'Abstract': str(row.get('Abstract', ''), 'utf-8'),  # Description
                        'Level': str(row.get('Level', ''), 'utf-8'),
                        'Event': str(row.get('Event', ''), 'utf-8'),
                        'Room': str(row.get('Room', ''), 'utf-8'),
                        'Time': str(row.get('Time', ''), 'utf-8'),  # Legacy csv time field
                        'Date': str(row.get('Date', ''), 'utf-8'),
                        'StartTime': str(row.get('StartTime', ''), 'utf-8'),
                        'EndTime': str(row.get('EndTime', ''), 'utf-8')
                    }

                    presentations.append(talk)

        except IOError:
            log.exception("CSV: File %s not found", csv_file)

        return presentations
