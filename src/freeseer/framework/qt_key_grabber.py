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
from PyQt4 import QtCore, QtGui


class QtKeyGrabber(QtGui.QWidget):
    '''
    This class allows the user to press a combination of keys in order to
    set a shortkey.
    '''
    def __init__(self, parent=None):
        '''
        Create an active screen and initialize variables used in this
        class.
        '''
        QtGui.QWidget.__init__(self, None, QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowState(QtCore.Qt.WindowActive)

        self.parent = parent
        self.flag = False
        self.modifiers = {}
        self.setWindowOpacity(0.3)

    def keyPressEvent(self, event):
        other = None
        if event.key() == QtCore.Qt.Key_Shift:
            self.modifiers[QtCore.Qt.Key_Shift] = 'Shift'
        elif event.key() == QtCore.Qt.Key_Control:
            self.modifiers[QtCore.Qt.Key_Control] = 'Ctrl'
        elif event.key() == QtCore.Qt.Key_Alt:
            self.modifiers[QtCore.Qt.Key_Alt] = 'Alt'
        elif event.key() == QtCore.Qt.Key_Meta:
            self.modifiers[QtCore.Qt.Key_Meta] = 'Meta'
        else:
            other = event.text()
        if other:
            if QtCore.Qt.Key_Control in self.modifiers:
                self.key_string = '+'.join(list(self.modifiers.values()) + [str(chr(event.key()))])
            else:
                self.key_string = '+'.join(list(self.modifiers.values()) + [str(other)])
        else:
            self.key_string = '+'.join(list(self.modifiers.values()))
        if (self.parent.core.config.key_rec == 'Ctrl+Shift+R'):
            self.flag = True

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Shift:
            if QtCore.Qt.Key_Shift in self.modifiers:
                del self.modifiers[QtCore.Qt.Key_Shift]
        elif event.key() == QtCore.Qt.Key_Control:
            if QtCore.Qt.Key_Control in self.modifiers:
                del self.modifiers[QtCore.Qt.Key_Control]
        elif event.key() == QtCore.Qt.Key_Alt:
            if QtCore.Qt.Key_Alt in self.modifiers:
                del self.modifiers[QtCore.Qt.Key_Alt]
        elif event.key() == QtCore.Qt.Key_Meta:
            if QtCore.Qt.Key_Meta in self.modifiers:
                del self.modifiers[QtCore.Qt.Key_Meta]
        #print len(self.modifiers)
        if len(self.modifiers) == 0:
            if self.flag:
                self.parent.grab_rec_set(self.key_string)
            else:
                self.parent.grab_stop_set(self.key_string)
            self.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = QtKeyGrabber()
    main.show()
    sys.exit(app.exec_())
