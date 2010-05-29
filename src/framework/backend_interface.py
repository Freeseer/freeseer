#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2010  Free and Open Source Software Learning Centre
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
# the #fosslc channel on IRC (freenode.net)

class BackendInterface:
    def test_feedback_start(self, video=False, audio=False):
        raise NotImplementedError('This method must be implemented.')
    
    def test_feedback_stop(self):
        raise NotImplementedError('This method must be implemented.')

    def record(self):
        raise NotImplementedError('This method must be implemented.')

    def stop(self):
        raise NotImplementedError('This method must be implemented.')

    def get_video_sources(self):
        raise NotImplementedError('This method must be implemented.')

    def get_video_devices(self):
        raise NotImplementedError('This method must be implemented.')

    def get_audio_sources(self):
        raise NotImplementedError('This method must be implemented.')

    def change_video_source(self, new_source):
        raise NotImplementedError('This method must be implemented.')

    def set_recording_area(self, start_x, start_y, end_x, end_y):
        raise NotImplementedError('This method must be implemented.')

    def change_output_resolution(self, width, height):
        raise NotImplementedError('This method must be implemented.')

    def change_audio_source(self, new_source):
        raise NotImplementedError('This method must be implemented.')

    def enable_video_feedback(self):
        raise NotImplementedError('This method must be implemented.')

    def disable_video_feedback(self):
        raise NotImplementedError('This method must be implemented.')

    def enable_audio_feedback(self):
        raise NotImplementedError('This method must be implemented.')

    def disable_audio_feedback(self):
        raise NotImplementedError('This method must be implemented.')
    