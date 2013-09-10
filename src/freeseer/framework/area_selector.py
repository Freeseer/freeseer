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

import sys

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QRectF

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QTextOption
from PyQt4.QtGui import QToolTip
from PyQt4.QtGui import QWidget


class AreaSelector(QWidget):
    '''
    This class provides a simple app for allowing the user to select an area
    on the screen by pressing left click and dragging the mouse. The start
    points are recorded when the user presses the left mouse button and the
    end points are recorded when the user releases the mouse button. The
    result start and end points are then returned to the parent class as
    through the desktopAreaEvent() function.

    The parent class using this app must implement the deskopAreaEvent
    function.
    '''
    def __init__(self, parent=None):
        '''
        Create a translucent fullscreen widgit and initialize variables
        used in this app.
        '''
        QWidget.__init__(self, None, Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowState(Qt.WindowFullScreen)
        self.setAutoFillBackground(False)

        self.parent = parent
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.current_x = 0
        self.current_y = 0

    def showEvent(self, event):
        '''Update the screen BG when the selector is shown'''
        self.bg = QPixmap.grabWindow(QApplication.desktop().winId())
        self.screen_geometry = QApplication.desktop().screenGeometry(self)

    def mousePressEvent(self, event):
        '''Save the users starting x/y points'''
        self.start_x = event.globalX()
        self.start_y = event.globalY()

    def mouseReleaseEvent(self, event):
        '''Save the users end x/y points'''
        self.end_x = event.globalX()
        self.end_y = event.globalY()

    def mouseMoveEvent(self, event):
        '''Get the current mouse position and redraw the selection'''
        self.current_x = event.globalX()
        self.current_y = event.globalY()
        self.repaint()

        text = "Start: %sx%s \nEnd: %sx%s" % (self.start_x, self.start_y, self.current_x, self.current_y)
        QToolTip.showText(event.pos(), text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self._acceptSelection()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def _acceptSelection(self):
        '''Accept the selection and close the area selector app'''
        if not self.parent is None:
            self.parent.areaSelectEvent(self.start_x, self.start_y, self.end_x, self.end_y)
        self.close()

    def paintEvent(self, event):
        '''
        Paints area the user is currently selecting starting from point
        start_x and, start_y ending at the position of the user's mouse
        currently on screen.
        '''
        painter = QPainter()
        painter.begin(self)

        painter.fillRect(self.screen_geometry, QColor(10, 10, 10, 125))

        self._paint_selection(painter)
        self._paint_usage_text(painter)
        painter.end()

    ###
    ### Paint Objects
    ###
    def _paint_usage_text(self, painter):
        '''Draws the user notification on how to use the selector'''
        font = QFont("Helvetica [Cronyx]", 26, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255, 255))

        # Figure out text x-coordinates
        screen_width = self.screen_geometry.width()
        text_width = 800
        text_start_x = screen_width / 2 - text_width / 2

        # Figure out text y-coordinates
        screen_height = self.screen_geometry.height()
        text_height = 200
        text_start_y = screen_height / 2 - text_height / 2

        textoption = QTextOption(Qt.AlignCenter)
        textbox = QRectF(text_start_x, text_start_y, text_width, text_height)
        painter.drawText(textbox,
            "Click & Drag to select an area\n"
            "ENTER to confirm or ESC to cancel",
            textoption)
        painter.drawRoundedRect(textbox, 20, 20)

    def _paint_selection(self, painter):
        '''Draws the current user selection'''
        rectangle = QRectF()

        # User drags right to left
        if self.start_x > self.current_x:
            rectangle.setLeft(self.current_x)
            rectangle.setRight(self.start_x)
        # User drags left to right
        else:
            rectangle.setLeft(self.start_x)
            rectangle.setRight(self.current_x)

        # User drags bottom to top
        if self.start_y > self.current_y:
            rectangle.setTop(self.current_y)
            rectangle.setBottom(self.start_y)

        # User drags top to bottom
        else:
            rectangle.setTop(self.start_y)
            rectangle.setBottom(self.current_y)

        painter.drawPixmap(rectangle, self.bg, rectangle)
        painter.drawRect(rectangle)


# Useful for independently testing the area selector
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = AreaSelector()
    main.show()
    sys.exit(app.exec_())
