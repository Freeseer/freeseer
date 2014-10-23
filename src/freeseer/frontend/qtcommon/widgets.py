#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

 Copyright (C) 2014  Free and Open Source Software Learning Centre
 http://fosslc.org

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/Freeseer/freeseer/

@author: Faraz Sherwani
'''

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QLabel


class ClickableLabel(QLabel):
    """QLabel that supports handling click events

    Produces a 'clicked()' signal for clicks on the label,
    and produces a 'double_clicked()' signal for double
    clicks"""

    clicked = pyqtSignal()
    double_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def mouseDoubleClickEvent(self, event):
        self.double_clicked.emit()
