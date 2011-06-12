#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011  Free and Open Source Software Learning Centre
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

from os import listdir;
from sys import *

from PyQt4 import QtGui, QtCore

from freeseer import project_info
from freeseer.framework.core import *

from configtoolui import *
from pluginloader import *

__version__ = project_info.VERSION

class ConfigTool(QtGui.QDialog):
    '''
    ConfigTool is used to tune settings used by the Freeseer Application
    '''

    def __init__(self, core=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_ConfigTool()
        self.ui.setupUi(self)

        self.currentWidget = None
        self.mainWidgetLayout = QtGui.QVBoxLayout()
        self.ui.mainWidget.setLayout(self.mainWidgetLayout)
        
        # Load Plugin Loader UI components
        self.pluginloaderWidget = QtGui.QWidget()
        self.pluginloader = Ui_PluginLoader()
        self.pluginloader.setupUi(self.pluginloaderWidget)

        self.connect(self.ui.optionsWidget, QtCore.SIGNAL('itemSelectionChanged()'), self.change_option)

        # load core
        self.core = FreeseerCore()
        # get the plugin manager
        self.plugman = self.core.get_plugin_manager()
        
    def change_option(self):
        option = self.ui.optionsWidget.currentItem().text(0)
        
        if self.currentWidget is not None:
            self.mainWidgetLayout.removeWidget(self.currentWidget)
            self.currentWidget.hide()
            
        if option == "Output":
            self.load_option_output_plugins()
        elif option == "Input":
            self.load_option_input_plugins()
        elif option == "Mixer":
            self.load_option_mixer_plugins()
        else:
            self.currentWidget = None
        
        
    def load_plugin_list(self, plugin_type):
        self.pluginloader.listWidget.clear()
        for plugin in self.plugman.getPluginsOfCategory(plugin_type):
            item = QtGui.QListWidgetItem()
            item.setText(plugin.plugin_object.get_name())
            
            flags = QtCore.Qt.ItemFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setFlags(flags)
            
            if plugin.is_activated:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            
            self.pluginloader.listWidget.addItem(item)
        
    def load_option_input_plugins(self):
        self.mainWidgetLayout.addWidget(self.pluginloaderWidget)
        self.currentWidget = self.pluginloaderWidget
        self.currentWidget.show()

        self.load_plugin_list("VideoInput")
            
    def load_option_output_plugins(self):
        self.mainWidgetLayout.addWidget(self.pluginloaderWidget)
        self.currentWidget = self.pluginloaderWidget
        self.currentWidget.show()
        
        self.load_plugin_list("Output")

    def load_option_mixer_plugins(self):
        self.mainWidgetLayout.addWidget(self.pluginloaderWidget)
        self.currentWidget = self.pluginloaderWidget
        self.currentWidget.show()

        self.load_plugin_list("VideoMixer")
            
            