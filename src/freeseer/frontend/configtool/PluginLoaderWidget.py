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
http://wiki.github.com/fosslc/freeseer/

@author: Thanh Ha
'''

from PyQt4 import QtCore, QtGui

class PluginLoaderWidget(QtGui.QWidget):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.listWidget = QtGui.QListWidget()
        self.listWidget.setAlternatingRowColors(True)
        self.mainLayout.addWidget(self.listWidget)
        
    def getListWidgetPlugin(self, plugin, plugin_category, plugman):
        plugin_name = plugin.plugin_object.get_name()
        
        widget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        widget.setLayout(layout)
        
        # Display Plugin's meta data in a tooltip
        pluginTooltip = """
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
        """ % {"name" : plugin.name,
               "version" : plugin.version,
               "author" : plugin.author,
               "website" : plugin.website,
               "description" : plugin.description}
        widget.setToolTip(pluginTooltip)
        
        # Checkbox, set the proper state on load
        pluginCheckBox = QtGui.QCheckBox()
        pluginCheckBox.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        
        if plugin.is_activated:
            pluginCheckBox.setCheckState(QtCore.Qt.Checked)
        else:
            pluginCheckBox.setCheckState(QtCore.Qt.Unchecked)
        
        layout.addWidget(pluginCheckBox)

        # Plugin Label / Description
        textLayout = QtGui.QVBoxLayout()
        layout.addLayout(textLayout)
        
        pluginLabel = QtGui.QLabel(plugin_name)
        pluginLabel.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        pluginLabelFont = QtGui.QFont()
        pluginLabelFont.setPointSize(11)
        pluginLabelFont.setBold(True)
        pluginLabel.setFont(pluginLabelFont)
        
        pluginDescLabel = QtGui.QLabel(plugin.description)
        pluginDescLabel.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        pluginDescLabelFont = QtGui.QFont()
        pluginDescLabelFont.setPointSize(10)
        pluginDescLabelFont.setItalic(True)
        pluginDescLabel.setFont(pluginDescLabelFont)
        
        textLayout.addWidget(pluginLabel)
        textLayout.addWidget(pluginDescLabel)
        # --- End Label / Description
        
        # Signal to activate/deactivate a plugin.
        def set_plugin_state():
            if pluginCheckBox.checkState() == 2:
                plugman.activate_plugin(plugin_name, plugin_category)
            else:
                plugman.deactivate_plugin(plugin_name, plugin_category)
        
        widget.connect(pluginCheckBox, QtCore.SIGNAL('clicked()'), set_plugin_state)
        
        # If plugin supports configuration, show a configuration button.
        if plugin.plugin_object.get_widget() is not None:
            pluginConfigToolButton = QtGui.QToolButton()
            pluginConfigToolButton.setText("Settings")
            configIcon = QtGui.QIcon.fromTheme("preferences-other")
            pluginConfigToolButton.setIcon(configIcon)
            pluginConfigToolButton.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
            pluginConfigToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
            
            layout.addWidget(pluginConfigToolButton)
            self.connect(pluginConfigToolButton, QtCore.SIGNAL('clicked()'), plugin.plugin_object.get_dialog)
        
        return widget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = PluginLoaderWidget()
    main.show()
    sys.exit(app.exec_())
