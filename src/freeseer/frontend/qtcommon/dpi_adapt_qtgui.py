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


from PyQt4.QtCore import QRect
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QWidget


class QtGuiWithDpi(QWidget):
    """Base class to make QtGui classes adapt to the device's logical dots per inch (DPI).

    The methods defined in this class can be used to adjust sizing values according to system's logical DPI.
    Use the derived classes when the widget in question should auto-adjust to the system's logical DPI.

    Physical DPI is the actual physical resolution available on the device. Logical DPI on the other hand is set by
    the user via their desktop environment, to globally control UI and font size in different applications.
    Logical DPI is often used for increasing text size on high-resolution/retina screens.
    """
    def __init__(self, *args, **kwargs):
        super(QtGuiWithDpi, self).__init__(*args, **kwargs)

        STANDARD_DPI = 96.0  # 96 DPI is the default value for 100% scale on Linux, Windows, and OSX.
        self.dpi_x_ratio = self.logicalDpiX() / STANDARD_DPI
        self.dpi_y_ratio = self.logicalDpiY() / STANDARD_DPI

    def adjust_dpi(self, *args):
        """Returns a QSize which holds adjusted width and height values based on the systeam's logical DPI.

        Sizing can be given with a QSize object or width and height integers. Both cases are handled.
        """
        try:  # QSize
            width, height = args[0].width(), args[0].height()
        except AttributeError:  # width, height
            width, height = args[0], args[1]
        return QSize(self.set_width_with_dpi(width), self.set_height_with_dpi(height))

    def set_width_with_dpi(self, width):
        """"Returns a width value adjusted to the horizontal resolution of the device."""
        return round(width * self.dpi_x_ratio)

    def set_height_with_dpi(self, height):
        """"Returns a height value adjusted to the vertical resolution of the device."""
        return round(height * self.dpi_y_ratio)

    def qspacer_item_with_dpi(self, width, height):
        """Returns a QSpacerItem with DPI-adjusted width and height."""
        return QSpacerItem(self.set_width_with_dpi(width), self.set_height_with_dpi(height))

    def qrect_with_dpi(self, x, y, width, height):
        """Returns a QRect with DPI-adjusted width and height."""
        return QRect(self.set_width_with_dpi(x), self.set_height_with_dpi(y),
                     self.set_width_with_dpi(width), self.set_height_with_dpi(height))


class QWidgetWithDpi(QtGuiWithDpi):
    """An enhanced QWidget. Sizing methods are overridden to be DPI friendly."""

    def __init__(self, *args, **kwargs):
        super(QWidgetWithDpi, self).__init__(*args, **kwargs)

    def setMinimumSize(self, *args):
        """Sets the minimum size of the widget, adjusted to the logical DPI.

        Calls QWidget.setMinimumSize() with the given arguments in case it raises an exception.
        If it works, calls it again, but this time passing it a DPI-adjusted size.
        """
        super(QWidgetWithDpi, self).setMinimumSize(*args)
        super(QWidgetWithDpi, self).setMinimumSize(self.adjust_dpi(*args))

    def resize(self, *args):
        """Resizes the widget with a DPI-adjusted size.

        Calls QWidget.reize() with the given arguments in case it raises an exception.
        If it works, calls it again, but this time passing it a DPI-adjusted size.
        """
        super(QWidgetWithDpi, self).resize(*args)
        super(QWidgetWithDpi, self).resize(self.adjust_dpi(*args))


class QMainWindowWithDpi(QMainWindow, QtGuiWithDpi):
    """An enhanced QMainWindow. Sizing methods are overridden to be DPI friendly."""

    def __init__(self, *args, **kwargs):
        super(QMainWindowWithDpi, self).__init__(*args, **kwargs)

    def resize(self, *args):
        """Resizes the window with a DPI-adjusted size.

        Calls QMainWindow.reize() with the given arguments in case it raises an exception.
        If it works, calls it again, but this time passing it a DPI-adjusted size.
        """
        super(QMainWindowWithDpi, self).resize(*args)
        super(QMainWindowWithDpi, self).resize(self.adjust_dpi(*args))


class QDialogWithDpi(QDialog, QtGuiWithDpi):
    """An enhanced QDialog. Sizing methods are overridden to be DPI friendly."""

    def __init__(self, *args, **kwargs):
        super(QDialogWithDpi, self).__init__(*args, **kwargs)

    def resize(self, *args):
        """Resizes the widget with a DPI-adjusted size.

        Calls QDialog.reize() with the given arguments in case it raises an exception.
        If it works, calls it again, but this time passing it a DPI-adjusted size.
        """
        super(QDialogWithDpi, self).resize(*args)
        super(QDialogWithDpi, self).resize(self.adjust_dpi(*args))


class QGroupBoxWithDpi(QGroupBox, QtGuiWithDpi):
    """An enhanced QGroupBox. Sizing methods are overridden to be DPI friendly."""

    def __init__(self, *args, **kwargs):
        super(QGroupBoxWithDpi, self).__init__(*args, **kwargs)

    def setFixedSize(self, *args):
        """Sets a fixed size for the widget, adjusted to the logical DPI.

        Calls QGroupBox.setFixedSize() with the given arguments in case it raises an exception.
        If it works, calls it again, but this time passing it a DPI-adjusted size.
        """
        super(QGroupBoxWithDpi, self).setFixedSize(*args)
        super(QGroupBoxWithDpi, self).setFixedSize(self.adjust_dpi(*args))


class QPushButtonWithDpi(QPushButton, QtGuiWithDpi):
    """An enhanced QPushButton. Sizing methods are overridden to be DPI friendly."""

    def __init__(self, *args, **kwargs):
        super(QPushButtonWithDpi, self).__init__(*args, **kwargs)

    def setFixedSize(self, *args):
        """Sets a fixed size for the widget, adjusted to the logical DPI.

        Calls QPushButton.setFixedSize() with the given arguments in case it raises an exception.
        If it works, calls it again, but this time passing it a DPI-adjusted size.
        """
        super(QPushButtonWithDpi, self).setFixedSize(*args)
        super(QPushButtonWithDpi, self).setFixedSize(self.adjust_dpi(*args))


class QToolButtonWithDpi(QToolButton, QtGuiWithDpi):
    """An enhanced QToolButton. Sizing methods are overridden to be DPI friendly."""

    def __init__(self, *args, **kwargs):
        super(QToolButtonWithDpi, self).__init__(*args, **kwargs)

    def setFixedSize(self, *args):
        """Sets a fixed size for the widget, adjusted to the logical DPI.

        Calls QToolButton.setFixedSize() with the given arguments in case it raises an exception.
        If it works, calls it again, but this time passing it a DPI-adjusted size.
        """
        super(QToolButtonWithDpi, self).setFixedSize(*args)
        super(QToolButtonWithDpi, self).setFixedSize(self.adjust_dpi(*args))
