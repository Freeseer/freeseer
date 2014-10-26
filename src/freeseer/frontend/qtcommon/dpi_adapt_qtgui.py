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
    '''This class is used as a base class for other DPI adatping QtGui classes.

    Use the QWidget as the base class so it will be compatible with the inherited classes.
    The original QtWidget class is not DPI adapting. The widget resizing functions are DPI independent.
    The methods been defined or overrided in this class can help scale the arguments according to system logical Dpis.
    As a result, the resizing functions called via this class can give a result that fits the system environment best.
    Call the classes inherited from this class when the target widget should be DPI adapting.
    '''
    def __init__(self, *args, **kwargs):
        '''
        Directly pass the arguments to QWidget Constructor, also set the logical dpi rate
        using the QWidget.logicalDpiX/logicalDpiY APIs for further methods.
        The standard DPI is the system default DPI value for Linux, Windows and Mac.
        A DPI adapting application should use system DPI for the size of fonts, icons, windows, etc.
        The default value for standard DPI is 96 for Linux, Windows and Mac. And Freeseer is designed under this DPI.
        The logical DPI is the DPI the users defined for their computer to get large and clearer fonts and pictures.
        This value is changed mostly on the computers will high resolution but small scale screen.
        Please notice that this value is just "logical", it is not the actual DPI of the user's screen.
        '''
        super(QtGuiWithDpi, self).__init__(*args, **kwargs)

        STANDARD_DPI = 96.0
        self.logical_dpi_x = self.logicalDpiX() / STANDARD_DPI
        self.logical_dpi_y = self.logicalDpiY() / STANDARD_DPI

    def adjust_dpi(self, *args):
        '''Returns a QSize with adjusted width and height values based on the system logical DPI

        The Qt sizing methods that are used in Freeseer takes integers or a QSize to specify width and height.
        It is needed to handle both cases in one method.
        '''
        try:  # (QSize) input
            width, height = args[0].width(), args[0].height()
        except AttributeError:  # (width, height) input
            width, height = args[0], args[1]
        return QSize(self.set_width_with_dpi(width), self.set_height_with_dpi(height))

    def set_width_with_dpi(self, width):
        '''Return the multiplication of the input width with the horizontal DPI rate.

        Use for the classes/methods that cannot be included into the DPI adapting class.
        '''
        return round(width * self.logical_dpi_x)

    def set_height_with_dpi(self, height):
        '''Return the multiplication of the input height with the vertical DPI rate.

        Use for the classes/methods that cannot be included into the DPI adapting class.
        '''
        return round(height * self.logical_dpi_y)

    def qspacer_item_with_dpi(self, width, height):
        '''The interlayer method that change QSpacerItem class to a DPI adapting
        method under QtGuiWithDpi

        Read in width and height value and create a white space in window.
        This method change the origin fixed width and height to DPI adatping
        value and pass them to QSpacerItem constructor.
        '''
        return QSpacerItem(self.set_width_with_dpi(width), self.set_height_with_dpi(height))

    def qrect_with_dpi(self, left, top, width, height):
        '''The interlayer method that change QRect class to a DPI adapting
        method under QtGuiWithDpi

        Read in left, top, width and height value and create a rect in window.
        This method change the origin fixed size to DPI adatping value and
        pass them to QRect constructor.
        '''
        return QRect(self.set_width_with_dpi(left),
                     self.set_height_with_dpi(top),
                     self.set_width_with_dpi(width),
                     self.set_height_with_dpi(height))


class QWidgetWithDpi(QtGuiWithDpi):
    '''The interlayer class that change the methods in QWidget to DPI adapting version.'''

    def __init__(self, *args, **kwargs):
        ''' Pass the arguments directly to QtGuiWithDpi '''
        super(QWidgetWithDpi, self).__init__(*args, **kwargs)

    def setMinimumSize(self, *args):
        '''Set the minimum size of the window with DPI adapting

        The interlayer for QWidget.setMinimumSize(). Read in fixed size of min
        width and min height and transfer to DPI adatping values
        '''
        # Call using the origin arguments as the TypeError filter.
        super(QWidgetWithDpi, self).setMinimumSize(*args)
        super(QWidgetWithDpi, self).setMinimumSize(self.adjust_dpi(*args))

    def resize(self, *args):
        '''Resize the window with DPI adapting

        The interlayer for QWidget.resize(). Read in fixed size of the target
        width and height and transfer to DPI adapting values.
        '''
        # Call using the origin arguments as the TypeError filter.
        super(QWidgetWithDpi, self).resize(*args)
        super(QWidgetWithDpi, self).resize(self.adjust_dpi(*args))


class QMainWindowWithDpi(QMainWindow, QtGuiWithDpi):
    '''The interlayer class that change the methods in QMainWindow to DPI adapting version.'''

    def __init__(self, *args, **kwargs):
        ''' Pass the arguments directly to QMainWindow and QtGuiWithDpi '''
        super(QMainWindowWithDpi, self).__init__(*args, **kwargs)

    def resize(self, *args):
        '''Resize the window with DPI adapting

        The interlayer for QMainWindow.resize(). Read in fixed size of the target
        width and height and transfer to DPI adapting values.
        '''
        # Call using the origin arguments as the TypeError filter.
        super(QMainWindowWithDpi, self).resize(*args)
        super(QMainWindowWithDpi, self).resize(self.adjust_dpi(*args))


class QDialogWithDpi(QDialog, QtGuiWithDpi):
    '''The interlayer class that change the methods in QDialog to DPI adapting version.'''

    def __init__(self, *args, **kwargs):
        ''' Pass the arguments directly to QDialogWithDpi and QtGuiWithDpi '''
        super(QDialogWithDpi, self).__init__(*args, **kwargs)

    def resize(self, *args):
        '''Resize the window with DPI adapting

        The interlayer for QDialog.resize(). Read in fixed size of the target
        width and height and transfer to DPI adapting values.
        '''
        # Call using the origin arguments as the TypeError filter.
        super(QDialogWithDpi, self).resize(*args)
        super(QDialogWithDpi, self).resize(self.adjust_dpi(*args))


class QGroupBoxWithDpi(QGroupBox, QtGuiWithDpi):
    '''The interlayer class that change the methods in QGroupBox to DPI adapting version.'''
    def __init__(self, *args, **kwargs):
        ''' Pass the arguments directly to QGroupBoxWithDpi and QtGuiWithDpi '''
        super(QGroupBoxWithDpi, self).__init__(*args, **kwargs)

    def setFixedSize(self, *args):
        '''Set the size of the QGroupBox with DPI adapting

        The method is overwritten QWidget.setFixedSize(). Since QGroupBox is
        inherit from QWidget instead of QWidgetWithDpi, this method needs to
        be rewrite here. It resize the input value using system DPI rate and
        pass the changed arguments to QWidget.setFixedSize()
        '''
        # Call using the origin arguments as the TypeError filter.
        super(QGroupBoxWithDpi, self).setFixedSize(*args)
        super(QGroupBoxWithDpi, self).setFixedSize(self.adjust_dpi(*args))


class QPushButtonWithDpi(QPushButton, QtGuiWithDpi):
    '''The interlayer class that change the methods in QPushButton to DPI adapting version.'''
    def __init__(self, *args, **kwargs):
        ''' Pass the arguments directly to QPushButtonWithDpi and QtGuiWithDpi '''
        super(QPushButtonWithDpi, self).__init__(*args, **kwargs)

    def setFixedSize(self, *args):
        '''Set the size of the QPushButton with DPI adapting

        The method is overwritten QWidget.setFixedSize(). Since QPushButton is
        inherit from QWidget instead of QWidgetWithDpi, this method needs to
        be rewrite here. It resize the input value using system DPI rate and
        pass the changed arguments to QWidget.setFixedSize()
        '''
        # Call using the origin arguments as the TypeError filter.
        super(QPushButtonWithDpi, self).setFixedSize(*args)
        super(QPushButtonWithDpi, self).setFixedSize(self.adjust_dpi(*args))


class QToolButtonWithDpi(QToolButton, QtGuiWithDpi):
    '''The interlayer class that change the methods in QToolButton to DPI adapting version.'''
    def __init__(self, *args, **kwargs):
        ''' Pass the arguments directly to QToolButtonWithDpi and QtGuiWithDpi '''
        super(QToolButtonWithDpi, self).__init__(*args, **kwargs)

    def setFixedSize(self, *args):
        '''Set the size of the QToolButton with DPI adapting

        The method is overwritten QWidget.setFixedSize(). Since QToolButton is
        inherit from QWidget instead of QWidgetWithDpi, this method needs to
        be rewrite here. It resize the input value using system DPI rate and
        pass the changed arguments to QWidget.setFixedSize()
        '''
        # Call using the origin arguments as the TypeError filter.
        super(QToolButtonWithDpi, self).setFixedSize(*args)
        super(QToolButtonWithDpi, self).setFixedSize(self.adjust_dpi(*args))
