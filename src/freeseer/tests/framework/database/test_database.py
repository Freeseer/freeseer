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

import os

from PyQt4 import QtCore
from PyQt4 import QtSql

from freeseer.framework.database import QtDBConnector
from freeseer.framework.presentation import Presentation


def test_first_talk_id(db, presentation):
    """Assert the first presentation record id in the database is given the identity '1'"""
    no_ids = db.get_talk_ids()
    assert not no_ids.first()  # Assert that there are no ids in the database.

    db.insert_presentation(presentation)

    talk_ids = db.get_talk_ids()
    assert talk_ids.first()
    talk_id_record = talk_ids.record()
    talk_id = talk_ids.value(talk_id_record.indexOf('id')).toString()
    assert talk_id == '1'
    assert not talk_ids.next()  # there should be no additional records.


def test_get_presentation_id(db, presentation):
    """Assert that a valid record id is returned for a given presntation object in the database"""
    assert not db.get_presentation_id(presentation)  # Test that None is returned when a record does not exist.

    db.insert_presentation(presentation)
    talk_id = db.get_presentation_id(presentation)
    assert talk_id == '1'


def test_add_talks_from_csv(db):
    """Assert that presentations can be loaded to the database from a csv file"""
    dirname = os.path.dirname(__file__)
    fname = os.path.join(dirname, os.pardir, 'sample_talks.csv')

    presentation = Presentation('Building NetBSD', 'David Maxwell')

    assert not db.presentation_exists(presentation)
    db.add_talks_from_csv(fname)
    assert db.presentation_exists(presentation)


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
        'Managing map data in a database,Andrew Ross,,,Default,Default,,,\r\n',
        'Building NetBSD,David Maxwell,,,Default,Default,,,\r\n',
        'Faking it till you make it,John Doe,,,Default,Default,,,\r\n'
    ]

    with open(temp_csv) as fd:
        assert fd.readlines() == expected_csv_lines


def test_insert_presentation(db, presentation):
    """Assert that a presentation's fields are correctly inserted into the database"""
    assert not db.presentation_exists(presentation)
    db.insert_presentation(presentation)

    talks = db.get_talks()
    assert talks.first()

    record = talks.record()
    assert talks.value(record.indexOf('title')).toString() == presentation.title
    assert talks.value(record.indexOf('speaker')).toString() == presentation.speaker
    assert talks.value(record.indexOf('description')).toString() == presentation.description
    assert talks.value(record.indexOf('category')).toString() == presentation.category
    assert talks.value(record.indexOf('event')).toString() == presentation.event
    assert talks.value(record.indexOf('date')).toString() == presentation.date
    assert talks.value(record.indexOf('startTime')).toString() == presentation.startTime
    assert talks.value(record.indexOf('endTime')).toString() == presentation.endTime

    # Check that no additional presentations were inserted.
    assert not talks.next()


def test_insert_presentation_empty_arguments(db):
    """Test that the worst case input to the database insert_presentation() method does not throw exceptions"""
    db.insert_presentation(Presentation('', room='', event=''))


def test_update_presentation(db, presentation):
    """Assert that a given presentation is updated with out side effects given its record id"""
    assert not db.presentation_exists(presentation)
    db.insert_presentation(presentation)

    # Update the inserted presentation
    presentation.title = 'Presentation Title Redacted'
    db.update_presentation('1', presentation)

    updated_talks = db.get_talks()
    updated_talks.first()
    new_record = updated_talks.record()

    # Check the update worked.
    assert updated_talks.value(new_record.indexOf('title')).toString() == presentation.title
    assert updated_talks.value(new_record.indexOf('speaker')).toString() == presentation.speaker
    assert updated_talks.value(new_record.indexOf('room')).toString() == presentation.room


def test_update_fake_presentation(db, presentation):
    """Try to update a fake presentation. Assert this does not insert anything into the database"""
    db.update_presentation('100', presentation)
    assert not db.get_presentation('100')

    talks = db.get_talks()
    assert not talks.first()


def test_update_presentation_real_and_fake(db, presentation):
    """
    Assert that a given presentation is updated with out side effects given its record id and that a fake
    presentation update does not impact the existing database presentation.
    """
    assert not db.presentation_exists(presentation)
    db.insert_presentation(presentation)

    # Update the inserted presentation
    presentation.title = 'Presentation Title Redacted'
    db.update_presentation('1', presentation)

    updated_talks = db.get_talks()
    updated_talks.first()
    new_record = updated_talks.record()

    # Check the update worked.
    assert updated_talks.value(new_record.indexOf('title')).toString() == presentation.title
    assert updated_talks.value(new_record.indexOf('speaker')).toString() == presentation.speaker
    assert updated_talks.value(new_record.indexOf('room')).toString() == presentation.room

    # Try to update fake presentations, this case should never actually arise if the code is using the model objects
    db.update_presentation('100', presentation)
    assert not db.get_presentation('100')

    # Make sure that the talk that was originally inserted has not changed and that no other rows have been added to the db.
    talks = db.get_talks()
    talks.first()
    record = talks.record()
    assert talks.value(record.indexOf('title')).toString() == presentation.title
    assert talks.value(record.indexOf('speaker')).toString() == presentation.speaker
    assert talks.value(record.indexOf('room')).toString() == presentation.room
    assert not talks.next()  # there should be no other presentations


def test_delete_presentation_valid(db, presentation):
    """Assert that a presentation is removed with out side effects from the database"""
    # delete a valid presentation
    assert not db.presentation_exists(presentation)
    db.insert_presentation(presentation)
    assert db.presentation_exists(presentation)
    db.delete_presentation('1')
    assert not db.presentation_exists('1')


def test_delete_presentation_fake(db):
    """Try to delete a fake presentation and assert that no errors occurred"""
    assert not db.presentation_exists('1')
    db.delete_presentation('1')
    assert not db.presentation_exists('1')


def test_delete_presentation_side_effects(db, presentation):
    """Delete an invalid presentation and make sure any valid presentations are not affected"""
    db.insert_presentation(presentation)
    assert db.presentation_exists(presentation)
    db.delete_presentation('100')
    assert db.presentation_exists(presentation)


def test_clear_database(db, presentation):
    """Assert that the presentation table is cleared"""
    assert not db.presentation_exists(presentation)
    db.insert_presentation(presentation)
    assert db.presentation_exists(presentation)
    db.clear_database()
    assert not db.presentation_exists(presentation)


def test_get_talk_ids(db, presentation):
    """Assert that presentation record ids are returned from the database presentation table"""
    assert not db.presentation_exists(presentation)
    db.insert_presentation(presentation)

    talk_ids = db.get_talk_ids()
    talk_ids.next()
    talk_id_record = talk_ids.record()
    assert talk_id_record.value(talk_id_record.indexOf('id')).toString() == '1'
    assert not talk_ids.next()


def test_get_talks_by_event(db, presentation):
    """Assert that presentations can be retrieved from the database given an event name"""
    assert not db.presentation_exists(presentation)
    db.insert_presentation(presentation)

    talk_by_event = db.get_talks_by_event(presentation.event)
    assert talk_by_event.first()
    record = talk_by_event.record()
    assert talk_by_event.value(record.indexOf('title')).toString() == presentation.title
    assert not talk_by_event.next()


def test_get_talks_by_event_fake(db):
    """Assert that presentations are not retrieved from the database given a fake event name"""
    fake_talk_by_event = db.get_talks_by_event('Fake event.')
    assert not fake_talk_by_event.first()


def test_get_talks_by_room(db, presentation):
    """Assert that presentations can be retrieved from the database given a room"""
    assert not db.presentation_exists(presentation)
    db.insert_presentation(presentation)

    talk_by_room = db.get_talks_by_room(presentation.room)
    assert talk_by_room.first()
    record = talk_by_room.record()
    assert talk_by_room.value(record.indexOf('category')).toString() == presentation.category
    assert not talk_by_room.next()


def test_get_talks_by_room_fake(db):
    """Assert that presentations are not retrieved from the database given a fake room"""
    fake_talk_by_room = db.get_talks_by_room('1234567890')
    assert not fake_talk_by_room.first()


def test_get_talks_by_room_and_time(db, presentation):
    """Assert that presentations starting after the current date can be retrieved from the database given a room"""
    assert not db.presentation_exists(presentation)
    db.insert_presentation(presentation)

    # The presentation should be returned because it starts later than the current date.
    talks = db.get_talks_by_room_and_time(presentation.room)
    assert talks.first()
    record = talks.record()
    assert talks.value(record.indexOf('room')).toString() == presentation.room
    assert not talks.next()


def test_get_talks_between_dates(db, presentation):
    """Assert that presentations from the database can be retrieved given two dates"""
    db.insert_presentation(presentation)

    current_time = QtCore.QDateTime().currentDateTime()
    time_before_presentation = current_time.date().toString(1)
    time_after_presentation = current_time.addSecs(60 * 60).date().toString(1)

    talk_id = db.get_talk_between_dates(presentation.event, presentation.room,
                                       time_before_presentation, time_after_presentation)
    assert talk_id == '1'


def test_get_talks_between_dates_no_presentations(db, presentation):
    """
    Assert that no presentations are retrieved from the database when get_talk_between_dates() is given a time period
    which contains no presentations
    """
    db.insert_presentation(presentation)

    no_talk_id = db.get_talk_between_dates(presentation.event, presentation.room, 0, 0)
    assert not no_talk_id


def test_presentation_exists(db, presentation):
    """Assert that a given presentation exists in the database"""
    empty_result = QtSql.QSqlQuery('SELECT * FROM presentations')
    assert not empty_result.first()  # There should be no presentations
    assert not db.presentation_exists(presentation)  # This should also be false
    db.insert_presentation(presentation)
    result = QtSql.QSqlQuery('SELECT * FROM presentations')
    assert result.first()
    assert unicode(result.value(1).toString()) == unicode(presentation.title)
    assert unicode(result.value(2).toString()) == unicode(presentation.speaker)
    assert db.presentation_exists(presentation)  # This should now be true as the above is

    db.clear_database()
    assert not db.presentation_exists(presentation)


def test_get_presentation(db, presentation):
    """Assert that a presentation can be retrieved from the database by using its record id"""
    assert not db.get_presentation('1')
    db.insert_presentation(presentation)
    inserted_presentation = db.get_presentation('1')
    assert inserted_presentation.title == presentation.title
    assert inserted_presentation.room == presentation.room


def test_get_presentation_fake(db):
    """Assert that a presentation is not retrieved from the database given a fake record id"""
    assert not db.get_presentation('')


def test_get_presentations_model(db, presentation):
    """Assert that a presentations model can be retrieved from the database"""
    db.insert_presentation(presentation)

    presentations_model = db.get_presentations_model()
    assert presentations_model.rowCount() == 1
    record = presentations_model.record(0)  # database index 0 is the first record

    assert record.value(record.indexOf('id')).toString() == '1'
    assert record.value(record.indexOf('title')).toString() == presentation.title

    fake_record = presentations_model.record(1)
    assert not fake_record.value(record.indexOf('id')).toString()


def test_get_dates_from_event_room_model(db, presentation):
    """Assert that a filtered by event and room presentation model can be retrieved from the database"""
    db.insert_presentation(presentation)
    dates_model = db.get_dates_from_event_room_model(presentation.event, presentation.room)
    assert dates_model.rowCount() == 1
    record = dates_model.record(0)

    assert record.value(record.indexOf('Date')).toString() == presentation.date


def test_get_rooms_model(db, presentation):
    """Assert that a model of presentation rooms can be retrieved from the database"""
    db.insert_presentation(presentation)
    rooms_model = db.get_rooms_model(presentation.event)
    assert rooms_model.rowCount() == 1
    record = rooms_model.record(0)
    assert record.value(record.indexOf('Room')).toString() == presentation.room


def test_get_talks_model(db, presentation):
    """Assert that a talk list model can be retrieved from the database"""
    empty_talks_model = db.get_talks_model(presentation.event, presentation.room, presentation.date)
    assert empty_talks_model.rowCount() == 0

    db.insert_presentation(presentation)
    talks_model = db.get_talks_model(presentation.event, presentation.room, presentation.date)

    assert talks_model.rowCount() == 1
    record = talks_model.record(0)
    assert (record.value(record.indexOf("(Speaker || ' - ' || Title)")).toString() ==
           "{0} - {1}".format(presentation.speaker, presentation.title))


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
            'Winter conference', '12', '2002-10-05')
    ''')

    # Mock out the db schema version to a 2x version.
    def mock_version(self):
        return 0
    monkeypatch.setattr(QtDBConnector, '_get_db_version_int', mock_version)

    db._update_version()
    presentation = db.get_presentation('1')
    assert presentation
    assert presentation.title == 'An Old Title'
