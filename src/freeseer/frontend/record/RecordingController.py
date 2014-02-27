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

import datetime
import logging

from freeseer.framework.multimedia import Multimedia
from freeseer.framework.plugin import PluginManager
from freeseer.framework.util import make_record_name

log = logging.getLogger(__name__)


class RecordingController:
    def __init__(self, profile, db, config, cli=False):
        self.config = config
        self.db = db
        self.plugman = PluginManager(profile)
        self.media = Multimedia(self.config, self.plugman, cli=cli)

    def set_window_id(self, window_id):
        """Sets the Window ID which GStreamer should paint on"""
        self.media.set_window_id(window_id)

    def set_audio_feedback_handler(self, audio_feedback_handler):
        """Sets the handler for Audio Feedback levels"""
        self.media.set_audio_feedback_handler(audio_feedback_handler)

    def record(self):
        """Start Recording"""
        self.media.record()

    def stop(self):
        """Stop Recording"""
        self.media.stop()

    def pause(self):
        """Pause Recording"""
        self.media.pause()

    def load_backend_with_filename(self, filename):
        """Prepares the backend for recording using a filename"""
        initialized, filename_for_frontend = self.media.load_backend(filename)

        if initialized:
            return filename_for_frontend
        else:
            log.error('Failed to load backend using filename "{filename}".'.format(filename=filename))
            return None

    def load_backend_with_presentation(self, presentation):
        """Prepares the backend for recording using a presentation"""
        if presentation is not None:
            record_name = make_record_name(presentation)
            metadata = self.prepare_metadata(presentation)
            initialized, filename_for_frontend = self.media.load_backend(record_name, metadata)

            if initialized:
                return filename_for_frontend
            else:
                log.error('Failed to load backend using the given presentation.')
                return None
        else:
            log.error("Failed to configure recording name. No presentation provided.")
            return None

    def print_talks(self):
        query = self.db.get_talks()

        # Print the header
        print("\n")
        print("ID: Speaker - Title")
        print("-------------------")

        while(query.next()):
            talkid = unicode(query.value(0).toString())
            title = unicode(query.value(1).toString())
            speaker = unicode(query.value(2).toString())

            print("{talkid}: {speaker} - {title}".format(talkid=talkid, speaker=speaker, title=title))

    def prepare_metadata(self, presentation):
        """Returns a dictionary of tags and tag values.

        To be used for populating the current recording's file metadata.
        """
        return {
            'title':     presentation.title,
            'artist':    presentation.speaker,
            'performer': presentation.speaker,
            'album':     presentation.event,
            'location':  presentation.room,
            'date':      str(datetime.date.today()),
            'comment':   presentation.description
        }

    ###
    ### Convenience commands
    ###
    def record_talk_id(self, talk_id):
        """Records using a known Talk ID

        Returns True if recording is successfully started
        Returns False if any issues arise
        """
        presentation = self.db.get_presentation(talk_id)
        if self.load_backend_with_presentation(presentation):
            # Only record if the backend successfully loaded
            # No need to print error on failure since load_backend already
            # prints an error message
            self.record()
            return True

        else:
            return False

    def record_filename(self, filename):
        """Records to a specific filename

        Returns True if recording is successfully started
        Returns False if any issues arise
        """
        if self.load_backend_with_filename(filename):
            self.record()
            return True

        else:
            return False
