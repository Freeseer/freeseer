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
import copy
import os
import pytest

from PyQt4 import QtCore
from PyQt4 import QtSql

from freeseer.framework.database import QtDBConnector
from freeseer.framework.presentation import Presentation


def helper_presentation_record_to_presentation(query, record):
    """
    Takes a QSqlQuery object from the presentation table and a QSqlRecord and returns a Python Presentation object.
    """
    return Presentation(
        title=unicode(query.value(record.indexOf('title')).toString()),
        speaker=unicode(query.value(record.indexOf('speaker')).toString()),
        description=unicode(query.value(record.indexOf('description')).toString()),
        category=unicode(query.value(record.indexOf('category')).toString()),
        event=unicode(query.value(record.indexOf('event')).toString()),
        room=unicode(query.value(record.indexOf('room')).toString()),
        date=query.value(record.indexOf('date')).toDate(),
        startTime=query.value(record.indexOf('startTime')).toDateTime(),
        endTime=query.value(record.indexOf('endTime')).toDateTime()
    )


def test_get_presentation_id(db, fake_presentation):
    """Assert that a valid record id is returned for a given presntation object in the database"""
    assert not db.get_presentation_id(fake_presentation)  # Test that None is returned when a record does not exist.

    db.insert_presentation(fake_presentation)
    talk_id = db.get_presentation_id(fake_presentation)
    assert talk_id == 1


def test_add_talks_from_csv(db, presentation_sc2011_maxwell_csv):
    """Assert that presentations can be loaded to the database from a csv file"""
    dirname = os.path.dirname(__file__)
    fname = os.path.join(dirname, os.pardir, 'sample_talks.csv')

    assert not db._helper_presentation_exists(presentation_sc2011_maxwell_csv)
    db.add_talks_from_csv(fname)
    assert db._helper_presentation_exists(presentation_sc2011_maxwell_csv)


def test_add_talks_from_empty_csv(db):
    """Assert that no talks are added when an empty csv filename is passed to add_talks_from_csv()"""
    db.add_talks_from_csv('')  # This logs an exception.
    talk_ids = db.get_talk_ids()
    assert not talk_ids.first()


def test_export_talks_to_csv(db, tmpdir):
    """Assert that presentations from the database can be exported to a csv file"""
    temp_csv = str(tmpdir.join('temp.csv'))
    presentation1 = Presentation('Managing map data in a database', 'Andrew Ross')
    presentation2 = Presentation('Building NetBSD', 'David Maxwell')
    presentation3 = Presentation('Faking it till you make it', 'John Doe')
    db.insert_presentation(presentation1)
    db.insert_presentation(presentation2)
    db.insert_presentation(presentation3)
    db.export_talks_to_csv(temp_csv)

    expected_csv_lines = [
        'Title,Speaker,Abstract,Category,Event,Room,Date,StartTime,EndTime\r\n',
        'Managing map data in a database,Andrew Ross,,,Default,Default,{},{},{}\r\n'.format(
            Presentation.DEFAULT_DATE, Presentation.DEFAULT_TIME, Presentation.DEFAULT_TIME),
        'Building NetBSD,David Maxwell,,,Default,Default,{},{},{}\r\n'.format(
            Presentation.DEFAULT_DATE, Presentation.DEFAULT_TIME, Presentation.DEFAULT_TIME),
        'Faking it till you make it,John Doe,,,Default,Default,{},{},{}\r\n'.format(
            Presentation.DEFAULT_DATE, Presentation.DEFAULT_TIME, Presentation.DEFAULT_TIME)
    ]

    with open(temp_csv) as fd:
        assert fd.readlines() == expected_csv_lines


def test_insert_presentation(db, fake_presentation):
    """Assert that a presentation's fields are correctly inserted into the database"""
    assert not db._helper_presentation_exists(fake_presentation)
    db.insert_presentation(fake_presentation)

    talks = db.get_talks()
    assert talks.first()

    record = talks.record()
    inserted_presentation = helper_presentation_record_to_presentation(talks, record)
    assert inserted_presentation == fake_presentation

    # Check that no additional presentations were inserted.
    assert not talks.next()


def test_insert_presentation_empty_arguments(db):
    """Test that the worst case input to the database insert_presentation() method does not throw exceptions"""
    db.insert_presentation(Presentation('', room='', event=''))


def test_update_presentation_real_and_fake(db, fake_presentation):
    """
    Assert that a given presentation is updated without side effects given its record id and that a fake
    presentation update does not impact the existing database presentation.
    """
    db.insert_presentation(fake_presentation)
    # Update the inserted presentation
    fake_presentation.title = 'Presentation Title Redacted'
    db.update_presentation(1, fake_presentation)

    updated_talks = db.get_talks()
    updated_talks.first()
    # Check the update worked.
    updated_presentation = helper_presentation_record_to_presentation(updated_talks, updated_talks.record())
    assert updated_presentation == fake_presentation

    # Try to update fake presentations, this case should never actually arise if the code is using the model objects
    db.update_presentation(100, fake_presentation)
    assert not db.get_presentation(100)

    # Make sure that the talk that was originally inserted has not changed and that no other rows have been added to the db.
    talks = db.get_talks()
    talks.first()
    inserted_presentation = helper_presentation_record_to_presentation(talks, talks.record())
    assert inserted_presentation == fake_presentation
    assert not talks.next()  # there should be no other presentations


def test_delete_presentation_valid(db, fake_presentation):
    """Assert that a presentation is removed without side effects from the database"""
    db.insert_presentation(fake_presentation)
    db.delete_presentation(1)
    assert not db.get_presentation(1)


def test_delete_presentation_fake(db):
    """Try to delete a fake presentation and assert that no errors occurred"""
    assert not db.get_presentation(1)
    db.delete_presentation(1)
    assert not db.get_presentation(1)


def test_delete_presentation_side_effects(db, fake_presentation):
    """Delete an invalid presentation and make sure any valid presentations are not affected"""
    db.insert_presentation(fake_presentation)
    db.delete_presentation(100)
    assert db._helper_presentation_exists(fake_presentation)


def test_clear_database(db, fake_presentation):
    """Assert that the presentation table is cleared"""
    db.insert_presentation(fake_presentation)
    db.clear_database()
    assert not db._helper_presentation_exists(fake_presentation)


def test_get_talk_ids(db, fake_presentation, presentation_sc2010, presentation_sc2011_maxwell_rss, presentation_sc2011_dixon):
    """
    Assert that presentation record ids are returned from the database presentation table. It is expected that the
    first talk inserted into the database will have an id of 1. Otherwise, tests will start failing.
    """
    db.insert_presentation(fake_presentation)
    db.insert_presentation(presentation_sc2010)
    db.insert_presentation(presentation_sc2011_maxwell_rss)
    db.insert_presentation(presentation_sc2011_dixon)

    talk_ids = db.get_talk_ids()
    expected_id = 1
    while talk_ids.next():
        talk_id_record = talk_ids.record()
        assert talk_id_record.value(talk_id_record.indexOf('id')).toString() == str(expected_id)
        expected_id += 1
    if expected_id != 5:
        pytest.fail("Expected 4 talks to be returned from the database but only saw: {}".format(expected_id - 1))


def test_get_talks_by_event(db, fake_presentation):
    """Assert that presentations can be retrieved from the database given an event name"""
    db.insert_presentation(fake_presentation)
    talk_by_event = db.get_talks_by_event(fake_presentation.event)
    assert talk_by_event.first()
    record = talk_by_event.record()
    assert talk_by_event.value(record.indexOf('title')).toString() == fake_presentation.title
    assert not talk_by_event.next()


def test_get_talks_by_event_fake(db):
    """Assert that presentations are not retrieved from the database given a fake event name"""
    fake_talk_by_event = db.get_talks_by_event('Fake event.')
    assert not fake_talk_by_event.first()


def test_get_talks_by_room(db, fake_presentation):
    """Assert that presentations can be retrieved from the database given a room"""
    db.insert_presentation(fake_presentation)
    talk_by_room = db.get_talks_by_room(fake_presentation.room)
    assert talk_by_room.first()
    record = talk_by_room.record()
    assert talk_by_room.value(record.indexOf('category')).toString() == fake_presentation.category
    assert not talk_by_room.next()


def test_get_talks_by_room_fake(db):
    """Assert that presentations are not retrieved from the database given a fake room"""
    fake_talk_by_room = db.get_talks_by_room('1234567890')
    assert not fake_talk_by_room.first()


def test_get_talks_by_room_and_time(db, fake_presentation):
    """Assert that presentations starting after the current date can be retrieved from the database given a room"""
    db.insert_presentation(fake_presentation)
    old_presentation = copy.deepcopy(fake_presentation)
    old_presentation.startTime = QtCore.QDateTime().addSecs(60 * -100)
    db.insert_presentation(old_presentation)

    # fake_presentation should be returned because it starts later than the current date.
    # old_presentation should not be returned since it starts in the past
    talks = db.get_talks_by_room_and_time(fake_presentation.room)
    assert talks.first()
    inserted_presentation = helper_presentation_record_to_presentation(talks, talks.record())
    assert inserted_presentation == fake_presentation
    assert not talks.next()


def test_get_talks_by_room_and_time_no_results(db, fake_presentation):
    """Assert that old presentations are not returned by get_talks_by_room_and_time()"""
    fake_presentation.startTime = QtCore.QDateTime().addSecs(60 * -100)
    db.insert_presentation(fake_presentation)

    # Nothing should be returned. fake_presentation is should be too old.
    talks = db.get_talks_by_room_and_time(fake_presentation.room)
    assert not talks.first()


def test_get_talks_by_room_and_time_fake_room(db, fake_presentation, presentation_sc2010):
    """
    Assert that nothing is returned when a room with no data associated with it is given to
    get_talks_by_room_and_time()
    """
    db.insert_presentation(fake_presentation)
    db.insert_presentation(presentation_sc2010)
    talks = db.get_talks_by_room_and_time('made up room')
    assert not talks.first()


def test_get_talks_between_dates(db, fake_presentation):
    """Assert that presentations from the database can be retrieved given two dates"""
    db.insert_presentation(fake_presentation)

    old_presentation = copy.deepcopy(fake_presentation)
    old_presentation.date = QtCore.QDate().addDays(-1)
    db.insert_presentation(old_presentation)

    current_time = QtCore.QDateTime().currentDateTime()
    time_before_presentation = current_time.date()
    time_after_presentation = current_time.addSecs(60 * 60).date()

    # The old presentation should not be returned.
    talk_id = db.get_talk_between_dates(fake_presentation.event, fake_presentation.room,
                                       time_before_presentation, time_after_presentation)
    assert talk_id == '1'


def test_get_talks_between_dates_empty_date_range(db, fake_presentation):
    """
    Assert that no presentations are retrieved from the database when get_talk_between_dates() is given a time period
    which contains no presentations
    """
    db.insert_presentation(fake_presentation)
    # Assert that nothing is returned when there is an invalid range
    assert not db.get_talk_between_dates(fake_presentation.event, fake_presentation.room,
                                         QtCore.QDateTime().addDays(-100).toString(),
                                         QtCore.QDateTime().addDays(-100).toString())


def test_helper_presentation_exists(db, fake_presentation):
    """Assert that a given presentation exists in the database"""
    empty_result = QtSql.QSqlQuery('SELECT * FROM presentations')
    assert not empty_result.first()  # There should be no presentations
    db.insert_presentation(fake_presentation)
    result = QtSql.QSqlQuery('SELECT * FROM presentations')
    assert result.first()
    inserted_presentation = helper_presentation_record_to_presentation(result, result.record())
    assert inserted_presentation == fake_presentation
    assert db._helper_presentation_exists(fake_presentation)  # This should now be true as the above is

    db.clear_database()
    assert not db._helper_presentation_exists(fake_presentation)


def test_get_presentation(db, fake_presentation):
    """Assert that a presentation can be retrieved from the database by using its record id"""
    assert not db.get_presentation(1)
    db.insert_presentation(fake_presentation)
    inserted_presentation = db.get_presentation(1)
    assert inserted_presentation == fake_presentation


def test_get_presentation_fake(db):
    """Assert that a presentation is not retrieved from the database given a fake record id"""
    assert not db.get_presentation(-1)


def test_get_presentations_model(db, fake_presentation):
    """Assert that a presentations model can be retrieved from the database"""
    db.insert_presentation(fake_presentation)
    presentations_model = db.get_presentations_model()
    assert presentations_model.rowCount() == 1
    record = presentations_model.record(0)  # database index 0 is the first record

    inserted_presentation = helper_presentation_record_to_presentation(record, record)
    assert inserted_presentation == fake_presentation

    fake_record = presentations_model.record(1)
    assert not fake_record.value(record.indexOf('id')).toString()


def test_get_empty_presentations_model(db, fake_presentation):
    """
    Assert that when a new presentation model is created, when there is nothing in the database, that there is nothing
    in the created model.
    """
    empty_presentations_model = db.get_presentations_model()  # The get_presentations_model produces a singleton
    assert empty_presentations_model.rowCount() == 0


def test_get_dates_from_event_room_model(db, fake_presentation):
    """Assert that a filtered by event and room presentation model can be retrieved from the database"""
    empty_dates_from_room_model = db.get_dates_from_event_room_model(fake_presentation.event, fake_presentation.room)
    assert empty_dates_from_room_model.rowCount() == 0

    db.insert_presentation(fake_presentation)
    dates_model = db.get_dates_from_event_room_model(fake_presentation.event, fake_presentation.room)
    assert dates_model.rowCount() == 1
    record = dates_model.record(0)

    assert record.value(record.indexOf('Date')) == fake_presentation.date


def test_get_rooms_model(db, fake_presentation):
    """Assert that a model of presentation rooms can be retrieved from the database"""
    empty_rooms_model = db.get_rooms_model(fake_presentation.event)
    assert empty_rooms_model.rowCount() == 0

    db.insert_presentation(fake_presentation)
    rooms_model = db.get_rooms_model(fake_presentation.event)
    assert rooms_model.rowCount() == 1
    record = rooms_model.record(0)
    assert record.value(record.indexOf('Room')).toString() == fake_presentation.room


def test_get_talks_model(db, fake_presentation):
    """Assert that a talk list model can be retrieved from the database"""
    empty_talks_model = db.get_talks_model(fake_presentation.event, fake_presentation.room, fake_presentation.date)
    assert empty_talks_model.rowCount() == 0

    db.insert_presentation(fake_presentation)
    talks_model = db.get_talks_model(fake_presentation.event, fake_presentation.room, fake_presentation.date)

    assert talks_model.rowCount() == 1
    record = talks_model.record(0)
    assert (record.value(record.indexOf("(Speaker || ' - ' || Title)")).toString() ==
           "{0} - {1}".format(fake_presentation.speaker, fake_presentation.title))


def test_upgrade_database(db, monkeypatch):
    """Assert that older databases can be upgraded to the most recent schema"""
    QtSql.QSqlQuery('DROP TABLE presentations')
    # Create a 2x table.
    QtSql.QSqlQuery('''
        CREATE TABLE presentations
            (Id Integer Primary Key,
             Title varchar(255),
             Speaker varchar(100),
             Description text,
             Level varchar(25),
             Event varchar(100),
             Room varchar(25),
             Time timestamp)
    ''')
    # Insert a 2x value.
    QtSql.QSqlQuery('''
        INSERT INTO presentations
        VALUES(1, 'An Old Title', 'Old Speaker', 'This is an example presentation from 2x', 'level 9',
            'Winter conference', '12', '2002-10-05T10:45')
    ''')
    inserted_presentation = Presentation(
        title='An Old Title',
        speaker='Old Speaker',
        description='This is an example presentation from 2x',
        category='level 9',
        event='Winter conference',
        room='12',
        date=QtCore.QVariant('2002-10-05T00:00').toDate(),
        startTime=QtCore.QVariant('2002-10-05T10:45').toDateTime(),
        endTime=QtCore.QVariant('2002-10-05T10:45').toDateTime()
    )

    # Mock out the db schema version to a 2x version.
    def mock_version(self):
        return 0
    monkeypatch.setattr(QtDBConnector, '_get_db_version_int', mock_version)

    db._update_version()
    assert db.get_presentation(1) == inserted_presentation
