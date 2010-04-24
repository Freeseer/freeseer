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
# http://wiki.github.com/fosslc/freeseer/

import sys
from PyQt4 import QtCore, QtGui

class QtAreaSelector(QtGui.QWidget):
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
        QtGui.QWidget.__init__(self, None, QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # Translucent
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        
        self.parent = parent
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.current_x = 0
        self.current_y = 0

    def mousePressEvent(self, event):
        '''
        Save the users starting x/y points.
        '''
        self.start_x = event.globalX()
        self.start_y = event.globalY()
        
    def mouseReleaseEvent(self, event):
        '''
        Save the users end x/y points and close the area selector app.
        '''
        self.end_x = event.globalX()
        self.end_y = event.globalY()
        if not self.parent == None:
            self.parent.desktopAreaEvent(self.start_x, self.start_y, self.end_x, self.end_y)
        self.close()

    def mouseMoveEvent(self, event):
        self.current_x = event.globalX()
        self.current_y = event.globalY()
        self.repaint()

        text = "Start: %sx%s \nEnd: %sx%s" % (self.start_x, self.start_y, self.current_x, self.current_y)
        QtGui.QToolTip.showText(event.pos(), text)
        
    def paintEvent(self, event):
        '''
        Paints area the user is currently selecting starting from point
        start_x and, start_y ending at the position of the user's mouse
        currently on screen.
        '''
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setPen(QtCore.Qt.blue)
        rectangle = QtCore.QRect()
        rectangle.setLeft(self.start_x)
        rectangle.setTop(self.start_y)
        rectangle.setRight(self.current_x)
        rectangle.setBottom(self.current_y)
        paint.drawRect(rectangle)
        paint.end()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = QtAreaSelector()
    main.show()
    sys.exit(app.exec_())