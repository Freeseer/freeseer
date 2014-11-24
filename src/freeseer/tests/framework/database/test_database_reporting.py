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

from freeseer.framework.failure import Failure
from freeseer.framework.presentation import Presentation


def test_insert_failure(db):
    """Assert that a failure can be inserted in the database failure table"""
    failure = Failure(talkID='1',
                      comment='Fake presentation',
                      indicator='It is a fixture',
                      release=True)

    db.insert_failure(failure)

    report = db.get_report('1')

    assert report.talkId == failure.talkId
    assert report.comment == failure.comment
    assert report.release == failure.release


def test_get_reports(db, presentation):
    """Assert that failure reports may be fetched from the database"""
    failure1 = Failure(talkID='1',
                       comment='Fake presentation',
                       indicator='It is a fixture',
                       release=True)
    failure2 = Failure(talkID='2',
                       comment='Non-existant failure',
                       indicator='It is not in the database',
                       release=True)

    db.insert_presentation(presentation)
    db.insert_failure(failure1)
    db.insert_failure(failure2)  # There is no presentation associated with failure2.talkId

    reports = db.get_reports()

    assert len(reports) == 2
    assert reports[0].presentation.title == presentation.title
    assert reports[0].failure.talkId == failure1.talkId
    assert not reports[1].presentation
    assert reports[1].failure.talkId == failure2.talkId


def test_export_reports_to_csv(db, tmpdir):
    """Assert that failure reports from the database can exported to a csv file"""
    presentation1 = Presentation(title='Fake it',
                                 speaker='John Doe',
                                 room='200')
    presentation2 = Presentation(title='A fake presentation',
                                 speaker='No one',
                                 room='Mystery')

    temp_csv = str(tmpdir.join('reports.csv'))
    failure1 = Failure(talkID='1',
                       comment='Fake presentation',
                       indicator='It is a fixture',
                       release=True)
    failure2 = Failure(talkID='2',
                       comment='Non-existant failure',
                       indicator='This is a fake failure',
                       release=True)

    db.insert_presentation(presentation1)
    db.insert_presentation(presentation2)
    db.insert_failure(failure1)
    db.insert_failure(failure2)
    db.export_reports_to_csv(temp_csv)

    expected_csv_lines = [
        'Title,Speaker,Abstract,Category,Event,Room,Date,StartTime,EndTime,Problem,Error\r\n',
        'Fake it,John Doe,,,Default,200,,,,It is a fixture,Fake presentation\r\n',
        'A fake presentation,No one,,,Default,Mystery,,,,This is a fake failure,Non-existant failure\r\n'
    ]

    with open(temp_csv) as fd:
        assert fd.readlines() == expected_csv_lines


def test_delete_failure(db):
    """Assert that failure reports can be deleted, without side effects, from the database"""
    failure = Failure(talkID='1',
                      comment='Fake presentation',
                      indicator='It is a fixture',
                      release=True)

    db.insert_failure(failure)
    db.delete_failure('1')
    assert not db.get_report('1')


def test_update_failure(db):
    """Assert that a given failure can be updated without causing side effects, in the database"""
    failure1 = Failure(talkID='1',
                       comment='Fake presentation',
                       indicator='It is a fixture',
                       release=True)
    failure2 = Failure(talkID='1',
                       comment='Super fake presentation',
                       indicator='It is not really real',
                       release=True)

    db.insert_failure(failure1)  # make sure that failure1 is actually in the database
    assert db.get_report('1') == failure1
    db.update_failure('1', failure2)  # replace failure1 with failure2
    assert db.get_report('1') == failure2
