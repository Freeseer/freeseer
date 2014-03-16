#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software

# Copyright (C) 2014  Free and Open Source Software Learning Centre
# http://fosslc.org

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

'''
@author: Mia Kilborn
'''
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QTreeWidget
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget


class PluginWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.pluginMetadata = {}

        # Main layout
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        # Define size used for the underlines
        self.underlineSize = QSize()
        self.underlineSize.setHeight(1)

        # Define font used for headers
        self.font = QFont()
        self.font.setPointSize(11)
        self.font.setBold(True)
        self.font.setUnderline(True)

        # Plugins Description
        self.pluginDescription = QLabel()
        self.pluginDescription.setText("Click a plugin to see more information." +
            " Plugins can be configured from the Recording tab. \n")
        self.pluginDescription.setWordWrap(True)

        # Plugins GroupBox
        self.pluginLayout = QVBoxLayout()
        self.pluginGroupBox = QGroupBox("Plugins extend the functionality of Freeseer")
        self.pluginGroupBox.setLayout(self.pluginLayout)
        self.pluginLayout.insertWidget(0, self.pluginDescription)
        self.mainLayout.insertWidget(0, self.pluginGroupBox)

        # Plugins list
        self.list = QTreeWidget()
        self.list.setHeaderHidden(True)
        self.list.headerItem().setText(0, "1")
        self.pluginLayout.insertWidget(1, self.list)

        # Details
        self.detailPane = QGroupBox()
        self.detailLayout = QVBoxLayout()
        self.detailPane.setLayout(self.detailLayout)
        self.detailPaneDesc = QLabel()
        self.detailPaneDesc.setWordWrap(True)
        self.detailLayout.addWidget(self.detailPaneDesc)
        self.pluginLayout.insertWidget(2, self.detailPane)

        self.list.itemSelectionChanged.connect(self.treeViewSelect)

    def treeViewSelect(self):
        item = self.list.currentItem()
        key = str(item.text(0))
        if key in self.pluginMetadata.keys():
            self.showDetails(key)
        else:
            self.hideDetails()

    def showDetails(self, key):
        self.detailPane.setTitle(key)
        self.detailPaneDesc.setText(self.pluginMetadata[key])
        self.detailPane.show()

    def hideDetails(self):
        self.detailPane.hide()

    def getWidgetPlugin(self, plugin, plugin_category, plugman):
        plugin_name = plugin.plugin_object.get_name()
        item = QTreeWidgetItem()

        # Display Plugin's meta data in a tooltip
        pluginDetails = """
        <table>
        <tr>
            <td>Name: </td>
            <td><b>%(name)s</b></td>
        </tr>
        <tr>
            <td>Version: </td>
            <td><b>%(version)s</b></td>
        <tr>
            <td>Author: </td>
            <td><b>%(author)s</b></td>
        </tr>
        <tr>
            <td>Website: </td>
            <td><b>%(website)s</b></td>
        </tr>
        <tr>
            <td>Description: </td>
            <td><b>%(description)s</b></td>
        </tr>
        </table>
        """ % {"name": plugin.name,
               "version": plugin.version,
               "author": plugin.author,
               "website": plugin.website,
               "description": plugin.description}

        # put the details in the hash table
        self.pluginMetadata[plugin_name] = pluginDetails

        item.setText(0, plugin_name)
        return item


if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = PluginWidget()
    main.show()
    sys.exit(app.exec_())
