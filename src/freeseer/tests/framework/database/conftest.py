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


# TODO: Give these presentation fixutres meaningful names
@pytest.fixture
def presentation1():
    """Returns a made-up presentation object. Also demonstrates how to construct time values for presentations"""
    today = QtCore.QDateTime().currentDateTime()  # today
    current_time = QtCore.QDateTime().currentDateTime()  # yyyy-mm-ddThh:mm:ss
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


@pytest.fixture
def presentation2():
    """Presentation object from the Summercamp2010 rss feed."""
    return Presentation(
        title='Managing map data in a database',
        speaker='Andrew Ross',
        description='''This talk will provide a brief introduction to geospatial technologies. It will focus on '''
        '''managing map data with a relational database. Managing map data with a database provides the atomicity, '''
        '''security, access that is difficult to achieve otherwise. It also provides powerful techniques for querying'''
        ''' spatial aware data which can enable new insights.''',
        category='Intermediate',
        event='Summercamp2010',
        room='Rom AB113',
        date='2010-05-14T10:45',
        startTime='2010-05-14T10:45'
    )


@pytest.fixture
def presentation3():
    """Creates a presentation from the summercamp2011 csv file"""
    return Presentation(
        title='Building NetBSD',
        speaker='David Maxwell',
        description='''People who are interested in learning about operating systems have a lot of topics to absorb,'''
        ''' but the very first barrier that gets in people's way is that you need to be able to build the software. '''
        '''If you can't build it, you can't make changes. If building it is painful, you'll find other things to do '''
        '''with your time.\n'''
        '''\tThe NetBSD Project has a build system that goes far beyond what many other projects implement. Come to '''
        '''this talk about learn about\n'''
        '''\tbuild.sh and the features available that make multi-architecture and embedded development environments '''
        '''a breeze with NetBSD.\n'''
        '''\tNetBSD website: http://www.NetBSD.org/''',
        event='SC2011',
        category='Beginner',
        room=unicode(''),
        date='2011-08-17T20:29',
        startTime='2011-08-17T20:29'
    )


@pytest.fixture
def presentation4():
    """Presentation from the Summercamp2011 csv file"""
    return Presentation(
        title='Lecture Broadcast and Capture using BigBlueButton',
        speaker='Fred Dixon',
        description='''BigBlueButton is an open source web conferencing system for distance education. It's goal is '''
        '''to enable remote students to have a high-quality learning experience. The #1 requested feature we've had '''
        '''over the last year is to integrate record and playback of a session.\n'''
        '''\n'''
        '''\t\n'''
        '''\tFred Dixon and Richard Alam, two of the BigBlueButton committers, will describe the architecture and '''
        '''implementation of record and playback as well as demonstrate the integration with Moodle to show how an '''
        '''educational institution can use BigBlueButton to setup virtual classrooms, record lectures, and provide '''
        '''students access to the recorded content from within the Moodle interface.\n'''
        '''\n'''
        '''\tWe will also demonstrate an prototype integration with popcorn.js (Mozilla project) using it as a '''
        '''playback client for the recorded content.''',
        event='SC2011',
        category='Intermediate',
        room='',
        date='',
        startTime=''
    )
