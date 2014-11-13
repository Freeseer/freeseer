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

from PyQt4.QtCore import QLocale

from freeseer.settings import detect_system_language


class TestSettings:
    """ Test Class for settings.py unit test"""

    def test_detect_system_language_translation_found(self, monkeypatch):
        """Tests detect_system_language() returns the appropriate translation filename for the system language."""
        locales = ("ar_EG", "de_DE", "en_US", "fr_CA", "ja_JP", "nl_NL", "sv_SE", "zh_CN", "zh_HK")
        for locale in locales:
            monkeypatch.setattr(QLocale, "name", lambda x: locale)
            assert detect_system_language() == "tr_{}.qm".format(locale)

    def test_detect_system_language_translation_not_found(self, monkeypatch):
        """Tests detect_system_language() returns default if no translation found for system language."""
        monkeypatch.setattr(QLocale, "name", lambda x: "fr_FR")
        assert detect_system_language() == "tr_en_US.qm"
