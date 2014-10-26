#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

Copyright (C) 2011  Free and Open Source Software Learning Centre
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

@author: Thanh Ha
'''

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QWidgetWithDpi
from freeseer.frontend.qtcommon import resource  # noqa


class ConfigToolWidget(QWidgetWithDpi):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(ConfigToolWidget, self).__init__(parent)

        self.setMinimumSize(800, 400)
        self.mainLayout = QtGui.QHBoxLayout()
        self.setLayout(self.mainLayout)

        #
        # Left panel
        #

        self.leftPanelLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(self.leftPanelLayout)

        self.optionsTreeWidget = QtGui.QTreeWidget()
        self.optionsTreeWidget.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.optionsTreeWidget.setHeaderHidden(True)
        self.optionsTreeWidget.headerItem().setText(0, "1")

        # General
        QtGui.QTreeWidgetItem(self.optionsTreeWidget)
        self.optionsTreeWidget.topLevelItem(0).setText(0, "General")

        # AV
        QtGui.QTreeWidgetItem(self.optionsTreeWidget)
        self.optionsTreeWidget.topLevelItem(1).setText(0, "AV Config")

        # Plugins
        QtGui.QTreeWidgetItem(self.optionsTreeWidget)
        self.optionsTreeWidget.topLevelItem(2).setText(0, "Plugins")

        # About
        QtGui.QTreeWidgetItem(self.optionsTreeWidget)
        self.optionsTreeWidget.topLevelItem(3).setText(0, "About")

        closeIcon = QtGui.QIcon.fromTheme("application-exit")
        self.closePushButton = QtGui.QPushButton("Close")
        self.closePushButton.setIcon(closeIcon)
        self.leftPanelLayout.addWidget(self.optionsTreeWidget)
        self.leftPanelLayout.addWidget(self.closePushButton)

        self.optionsTreeWidget.expandAll()

        #
        # Right panel
        #
        self.rightPanelWidget = QtGui.QWidget()
        self.rightPanelWidget.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        self.mainLayout.addWidget(self.rightPanelWidget)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = ConfigToolWidget()
    main.show()
    sys.exit(app.exec_())
