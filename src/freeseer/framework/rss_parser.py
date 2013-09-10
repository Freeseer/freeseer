#!/usr/bin/python
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

from feedparser import parse


class FeedParser:
    '''
    A RSS parser used when adding presentations
    '''

    def __init__(self, feed_url):
        self.parsed = parse(feed_url)

    '''
    Gets all presentations stored on the RSS
    '''
    def get_entries(self):
        return self.parsed.entries

    '''
    Gets a certain presentation stored on the RSS
    '''
    def get_entry(self, index):
        return self.get_entries()[index]

    '''
    Gets the presentation title
    '''
    def get_entry_title(self, index):
        return self.get_entry(index).title

    '''
    Gets the presentation speaker
    '''
    def get_entry_speaker(self, index):
        list = self._clear_list(self.get_entry(index)["summary_detail"]["value"].split("   "))
        for i in range(len(list)):
            if "field-field-speaker" in list[i]:
                return list[i + 4]

    '''
    Gets the presentation abstract
    '''
    def get_entry_abstract(self, index):
        list = self._clear_list(self.get_entry(index)["summary_detail"]["value"].split("   "))
        for i in range(len(list)):
            if "field-field-abstract" in list[i]:
                return list[i + 4]

    '''
    Gets the presentation level
    '''
    def get_entry_level(self, index):
        list = self._clear_list(self.get_entry(index)["summary_detail"]["value"].split("   "))
        for i in range(len(list)):
            if "field-field-level" in list[i]:
                return list[i + 4]

    '''
    Gets the presentation status
    '''
    def get_entry_status(self, index):
        list = self._clear_list(self.get_entry(index)["summary_detail"]["value"].split("   "))
        for i in range(len(list)):
            if "field-field-status" in list[i]:
                return list[i + 4]

    '''
    Gets the presentation time
    '''
    def get_entry_time(self, index):
        list = self._clear_list(self.get_entry(index)["summary_detail"]["value"].split("   "))
        for i in range(len(list)):
            if "field-field-time" in list[i]:
                return list[i + 4]

    '''
    Gets the presentation event
    '''
    def get_entry_event(self, index):
        list = self._clear_list(self.get_entry(index)["summary_detail"]["value"].split("   "))
        for i in range(len(list)):
            if "field-field-event" in list[i]:
                return list[i + 4]

    '''
    Gets the presentation room
    '''
    def get_entry_room(self, index):
        list = self._clear_list(self.get_entry(index)["summary_detail"]["value"].split("   "))
        for i in range(len(list)):
            if "field-field-room" in list[i]:
                return list[i + 4]

    '''
    An auxiliary function that cleans the list resultant by the feed parser.
    '''
    def _clear_list(self, list):
        final_list = []
        for item in list:
            if len(item) > 0:
                final_list.append(item)
        return final_list

    '''
    An auxiliary function that removes tag indicators from any entry.
    '''
    def _remove_tag_indicators(self, string):
        inside_tag = False
        final_string = ""
        for letter in string:
            if letter == "<":
                inside_tag = True
            elif letter == ">":
                inside_tag = False
            else:
                if not inside_tag:
                    final_string += letter
        return final_string

    '''
    Builds a list with all presentations stored on the RSS.
    '''
    def build_data_dictionary(self):
        presentations_list = []

        for i in range(len(self.get_entries())):

            title = unicode(self.get_entry_title(i))
            title = title.encode('ascii', 'replace')

            speaker = unicode(self.get_entry_speaker(i))
            abstract = unicode(self._remove_tag_indicators(self.get_entry_abstract(i)))
            level = unicode(self.get_entry_level(i))
            status = unicode(self.get_entry_status(i))
            time = unicode(self._remove_tag_indicators(str(self.get_entry_time(i))))
            event = unicode(self.get_entry_event(i))
            room = unicode(self.get_entry_room(i))

            presentation = {}

            presentation["Title"] = title.strip()
            presentation["Speaker"] = speaker.strip()
            presentation["Abstract"] = abstract.strip()
            presentation["Level"] = level.strip()
            presentation["Status"] = status.strip()
            presentation["Time"] = time.strip()
            presentation["Event"] = event.strip()
            presentation["Room"] = room.strip()

            presentations_list.append(presentation)

        return presentations_list


#if __name__ == "__main__":
    #a = FeedParser("http://www.fosslc.org/drupal/presentations_rss/Summercamp2011")
    #print a.build_data_dictionary()
