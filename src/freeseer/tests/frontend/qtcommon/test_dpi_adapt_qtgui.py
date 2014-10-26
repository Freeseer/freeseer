#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014  Free and Open Source Software Learning Centre
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


import pytest

from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QPaintDevice

from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QtGuiWithDpi
from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QWidgetWithDpi
from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QMainWindowWithDpi
from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QDialogWithDpi
from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QGroupBoxWithDpi
from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QPushButtonWithDpi
from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QToolButtonWithDpi


@pytest.fixture(autouse=True)
def set_logical_dpi(monkeypatch):
    ''' This method used monkeypatch to reset the logical DPI of the system for other tests '''
    DEFAULT_DPI = 96
    monkeypatch.setattr(QPaintDevice, 'logicalDpiX', lambda x: round(DEFAULT_DPI * 1.5))  # DPI ratio for x is 1.5
    monkeypatch.setattr(QPaintDevice, 'logicalDpiY', lambda x: round(DEFAULT_DPI * 1.25))  # DPI ratio for y is 1.25


class TestQtGuiWithDpi:

    @classmethod
    def setup_class(cls):
        ''' Initializes a QtGui.QApplication '''
        cls.app = QApplication([])

    @classmethod
    def teardown_class(cls):
        ''' Destruct the QtGui.QApplication '''
        cls.app.deleteLater()

    def setup(self):
        ''' Construct a tested class '''
        self.tested_cls = QtGuiWithDpi()

    def test_set_width_with_dpi(self):
        assert self.tested_cls.set_width_with_dpi(300) == round(300 * 1.5)

    def test_set_height_with_dpi(self):
        assert self.tested_cls.set_height_with_dpi(300) == round(300 * 1.25)

    def test_adjust_dpi(self):
        assert self.tested_cls.adjust_dpi(100, 40) == QSize(round(100 * 1.5), round(40 * 1.25))
        assert self.tested_cls.adjust_dpi(QSize(40, 100)) == QSize(round(40 * 1.5), round(100 * 1.25))

    def test_qspacer_item_with_dpi(self):
        dummy_qspace_item = self.tested_cls.qspacer_item_with_dpi(100, 100)
        assert dummy_qspace_item.sizeHint() == QSize(round(100 * 1.5), round(100 * 1.25))

    def test_qrect_with_dpi(self):
        dummy_qrect = self.tested_cls.qrect_with_dpi(10, 10, 100, 100)
        assert dummy_qrect.topLeft() == QPoint(round(10 * 1.5), round(10 * 1.25))
        assert dummy_qrect.size() == QSize(round(100 * 1.5), round(100 * 1.25))


class TestQWidgetWithDpi:

    @classmethod
    def setup_class(cls):
        ''' Initializes a QtGui.QApplication '''
        cls.app = QApplication([])

    @classmethod
    def teardown_class(cls):
        ''' Destruct the QtGui.QApplication '''
        cls.app.deleteLater()

    def setup(self):
        ''' Construct a tested class '''
        self.tested_cls = QWidgetWithDpi()

    def test_setMinimumSize(self):
        self.tested_cls.setMinimumSize(300, 220)
        assert self.tested_cls.minimumSize() == QSize(round(300 * 1.5), round(220 * 1.25))

    def test_resize(self):
        self.tested_cls.resize(400, 400)
        assert self.tested_cls.size() == QSize(round(400 * 1.5), round(400 * 1.25))


class TestQMainWindowWithDpi:

    @classmethod
    def setup_class(cls):
        ''' Initializes a QtGui.QApplication '''
        cls.app = QApplication([])

    @classmethod
    def teardown_class(cls):
        ''' Destruct the QtGui.QApplication '''
        cls.app.deleteLater()

    def setup(self):
        ''' Construct a tested class '''
        self.tested_cls = QMainWindowWithDpi()

    def test_resize(self):
        self.tested_cls.resize(400, 400)
        assert self.tested_cls.size() == QSize(round(400 * 1.5), round(400 * 1.25))


class TestQDialogWithDpi:
    ''' The test class that helps do the unit test for QDialogWithDpi '''

    @classmethod
    def setup_class(cls):
        ''' Initializes a QtGui.QApplication '''
        cls.app = QApplication([])

    @classmethod
    def teardown_class(cls):
        ''' Destruct the QtGui.QApplication '''
        cls.app.deleteLater()

    def setup(self):
        ''' Construct a tested class '''
        self.tested_cls = QDialogWithDpi()

    def test_resize(self):
        self.tested_cls.resize(400, 400)
        assert self.tested_cls.size() == QSize(round(400 * 1.5), round(400 * 1.25))


class TestQGroupBoxWithDpi:
    ''' The test class that helps do the unit test for QGroupBoxWithDpi '''

    @classmethod
    def setup_class(cls):
        ''' Initializes a QtGui.QApplication '''
        cls.app = QApplication([])

    @classmethod
    def teardown_class(cls):
        ''' Destruct the QtGui.QApplication '''
        cls.app.deleteLater()

    def setup(self):
        ''' Construct a tested class '''
        self.tested_cls = QGroupBoxWithDpi()

    def test_setFixedSize(self):
        self.tested_cls.setFixedSize(100, 100)
        assert self.tested_cls.size() == QSize(round(100 * 1.5), round(100 * 1.25))


class TestQPushButtonWithDpi:
    ''' The test class that helps do the unit test for QPushButtonWithDpi '''

    @classmethod
    def setup_class(cls):
        ''' Initializes a QtGui.QApplication '''
        cls.app = QApplication([])

    @classmethod
    def teardown_class(cls):
        ''' Destruct the QtGui.QApplication '''
        cls.app.deleteLater()

    def setup(self):
        ''' Construct a tested class '''
        self.tested_cls = QPushButtonWithDpi()

    def test_setFixedSize(self):
        self.tested_cls.setFixedSize(100, 100)
        assert self.tested_cls.size() == QSize(round(100 * 1.5), round(100 * 1.25))


class TestQToolButtonWithDpi:
    ''' The test class that helps do the unit test for QToolButtonWithDpi '''

    @classmethod
    def setup_class(cls):
        ''' Initializes a QtGui.QApplication '''
        cls.app = QApplication([])

    @classmethod
    def teardown_class(cls):
        ''' Destruct the QtGui.QApplication '''
        cls.app.deleteLater()

    def setup(self):
        ''' Construct a tested class '''
        self.tested_cls = QToolButtonWithDpi()

    def test_setFixedSize(self):
        self.tested_cls.setFixedSize(100, 100)
        assert self.tested_cls.size() == QSize(round(100 * 1.5), round(100 * 1.25))
