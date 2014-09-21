#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2014 Free and Open Source Software Learning Centre
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

import pytest
from PyQt4 import QtCore

from freeseer.framework.config.profile import Profile
from freeseer.framework.presentation import Presentation


@pytest.fixture
def db(tmpdir):
    """Return a new empty QtDBConnector"""
    profile = Profile(str(tmpdir), 'testing')
    return profile.get_database()


@pytest.fixture
def presentation():
    """Returns a populated presentation object. Also demonstrates how to construct time values for presentations"""
    today = QtCore.QDateTime().currentDateTime()  # today
    current_time = QtCore.QDateTime().currentDateTime()  # hh:mm:ss
    return Presentation(
        title='MITM presentation attacks',
        speaker='Alice and Eve',
        description='Field survey of current MITM presentation attacks.',
        category='Security category',
        event='testing event',
        room='1300',
        date=today.date().toString(1),  # format date yyyy-mm-dd
        startTime=current_time.addSecs(60 * 5).toString(),  # Start in 5 minutes
        endTime=current_time.addSecs(60 * 10).toString()  # End time in 10 minutes
    )
