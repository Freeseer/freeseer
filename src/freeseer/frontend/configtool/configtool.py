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

import logging
from os import listdir;
from sys import *

from PyQt4 import QtGui, QtCore

from freeseer import project_info
from freeseer.framework.core import *

from ConfigToolWidget import ConfigToolWidget
from GeneralWidget import GeneralWidget
from PluginLoaderWidget import PluginLoaderWidget

__version__ = project_info.VERSION

LANGUAGE_DIR = 'freeseer/frontend/configtool/languages/'

class ConfigTool(ConfigToolWidget):
    '''
    ConfigTool is used to tune settings used by the Freeseer Application
    '''

    def __init__(self, core=None):
        ConfigToolWidget.__init__(self)
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        self.currentWidget = None
        self.mainWidgetLayout = QtGui.QVBoxLayout()
        self.rightPanelWidget.setLayout(self.mainWidgetLayout)
        
        # Load the General UI Widget
        self.generalWidget = GeneralWidget()
        
        # Load Plugin Loader UI components
        self.pluginloaderWidget = PluginLoaderWidget()

        # connections
        self.connect(self.closePushButton, QtCore.SIGNAL('clicked()'), self.close)
        self.connect(self.optionsTreeWidget, QtCore.SIGNAL('itemSelectionChanged()'), self.change_option)
        
        #
        # general tab connections
        #
        self.connect(self.generalWidget.recordAudioCheckbox, QtCore.SIGNAL('toggled(bool)'), self.toggle_audiomixer_state)
        self.connect(self.generalWidget.audioMixerComboBox, QtCore.SIGNAL('activated(const QString&)'), self.change_audiomixer)
        self.connect(self.generalWidget.audioMixerSetupPushButton, QtCore.SIGNAL('clicked()'), self.setup_audio_mixer)
        self.connect(self.generalWidget.recordVideoCheckbox, QtCore.SIGNAL('toggled(bool)'), self.toggle_videomixer_state)
        self.connect(self.generalWidget.videoMixerComboBox, QtCore.SIGNAL('activated(const QString&)'), self.change_videomixer)
        self.connect(self.generalWidget.videoMixerSetupPushButton, QtCore.SIGNAL('clicked()'), self.setup_video_mixer)
        self.connect(self.generalWidget.recordDirPushButton, QtCore.SIGNAL('clicked()'), self.browse_video_directory)
        self.connect(self.generalWidget.recordDirLineEdit, QtCore.SIGNAL('editingFinished()'), self.update_record_directory)
        self.connect(self.generalWidget.autoHideCheckBox, QtCore.SIGNAL('toggled(bool)'), self.toggle_autohide)
        # GUI Disabling/Enabling Connections
        self.connect(self.generalWidget.recordAudioCheckbox, QtCore.SIGNAL("toggled(bool)"), self.generalWidget.audioMixerLabel.setEnabled)
        self.connect(self.generalWidget.recordAudioCheckbox, QtCore.SIGNAL("toggled(bool)"), self.generalWidget.audioMixerComboBox.setEnabled)
        self.connect(self.generalWidget.recordAudioCheckbox, QtCore.SIGNAL("toggled(bool)"), self.generalWidget.audioMixerSetupPushButton.setEnabled)
        self.connect(self.generalWidget.recordVideoCheckbox, QtCore.SIGNAL("toggled(bool)"), self.generalWidget.videoMixerLabel.setEnabled)
        self.connect(self.generalWidget.recordVideoCheckbox, QtCore.SIGNAL("toggled(bool)"), self.generalWidget.videoMixerComboBox.setEnabled)
        self.connect(self.generalWidget.recordVideoCheckbox, QtCore.SIGNAL("toggled(bool)"), self.generalWidget.videoMixerSetupPushButton.setEnabled)
        
        #
        # plugin loader connections
        #
        self.connect(self.pluginloaderWidget.listWidget, QtCore.SIGNAL('itemChanged(QListWidgetItem *)'), self.set_plugin_state)

        # load core
        if core is None:
            self.core = FreeseerCore()
        else:
            self.core = core
        
        # get the config
        self.config = self.core.get_config()
        # get the plugin manager
        self.plugman = self.core.get_plugin_manager()
        
        # load active plugin widgets
        self.load_plugin_widgets()
        
        # Start off with displaying the General Settings
        items = self.optionsTreeWidget.findItems("General", QtCore.Qt.MatchExactly)
        if len(items) > 0:
            item = items[0]
            self.optionsTreeWidget.setCurrentItem(item)
        
    ###
    ### General
    ###
        
    def change_option(self):
        option = self.optionsTreeWidget.currentItem().text(0)
        
        if self.currentWidget is not None:
            self.mainWidgetLayout.removeWidget(self.currentWidget)
            self.currentWidget.hide()
          
        if option == "General":
            self.load_general_widget()
        elif option == "Plugins":
            pass
        elif option == "AudioInput":
            self.load_option_audioinput_plugins()
        elif option == "AudioMixer":
            self.load_option_audiomixer_plugins()
        elif option == "VideoInput":
            self.load_option_videoinput_plugins()
        elif option == "VideoMixer":
            self.load_option_videomixer_plugins()
        elif option == "Output":
            self.load_option_output_plugins()
        else:
            pass
        
    def load_general_widget(self):
        self.mainWidgetLayout.addWidget(self.generalWidget)
        self.currentWidget = self.generalWidget
        self.currentWidget.show()
        
        # Set up Audio
        if self.config.enable_audio_recoding == True:
            self.generalWidget.recordAudioCheckbox.setChecked(True)
        else:
            self.generalWidget.recordAudioCheckbox.setChecked(False)
            self.generalWidget.audioMixerComboBox.setEnabled(False)
            self.generalWidget.audioMixerSetupPushButton.setEnabled(False)
            
        n = 0 # Counter for finding Audio Mixer to set as current.
        self.generalWidget.audioMixerComboBox.clear()
        plugins = self.plugman.plugmanc.getPluginsOfCategory("AudioMixer")
        for plugin in plugins:
            if plugin.is_activated:
                self.generalWidget.audioMixerComboBox.addItem(plugin.plugin_object.get_name())
                if plugin.plugin_object.get_name() == self.config.audiomixer:
                    self.generalWidget.audioMixerComboBox.setCurrentIndex(n)
                n += 1
        
        # Set up Video
        if self.config.enable_video_recoding == True:
            self.generalWidget.recordVideoCheckbox.setChecked(True)
        else:
            self.generalWidget.recordVideoCheckbox.setChecked(False)
            self.generalWidget.videoMixerComboBox.setEnabled(False)
            self.generalWidget.videoMixerSetupPushButton.setEnabled(False)
            
        n = 0 # Counter for finding Video Mixer to set as current.
        self.generalWidget.videoMixerComboBox.clear()
        plugins = self.plugman.plugmanc.getPluginsOfCategory("VideoMixer")
        for plugin in plugins:
            if plugin.is_activated:
                self.generalWidget.videoMixerComboBox.addItem(plugin.plugin_object.get_name())
                if plugin.plugin_object.get_name() == self.config.videomixer:
                    self.generalWidget.videoMixerComboBox.setCurrentIndex(n)
                n += 1
        
        # Recording Directory Settings
        self.generalWidget.recordDirLineEdit.setText(self.config.videodir)
        
        # Load Auto Hide Settings
        if self.config.auto_hide == True:
            self.generalWidget.autoHideCheckBox.setChecked(True)
        else:
            self.generalWidget.autoHideCheckBox.setChecked(False)

    def toggle_audiomixer_state(self, state):
        self.config.enable_audio_recoding = state
        self.config.writeConfig()
        
    def change_audiomixer(self, audiomixer):
        self.config.audiomixer = audiomixer
        self.config.writeConfig()

    def setup_audio_mixer(self):
        mixer = str(self.generalWidget.audioMixerComboBox.currentText())
        items = self.optionsTreeWidget.findItems(mixer, QtCore.Qt.MatchExactly)
        if len(items) > 0:
            item = items[0]
            self.optionsTreeWidget.setCurrentItem(item)
            
    def toggle_videomixer_state(self, state):
        self.config.enable_video_recoding = state
        self.config.writeConfig()
        
    def change_videomixer(self, videomixer):
        self.config.videomixer = videomixer
        self.config.writeConfig()
    
    def setup_video_mixer(self):
        mixer = str(self.generalWidget.videoMixerComboBox.currentText())
        items = self.optionsTreeWidget.findItems(mixer, QtCore.Qt.MatchExactly)
        if len(items) > 0:
            item = items[0]
            self.optionsTreeWidget.setCurrentItem(item)

    def browse_video_directory(self):
        directory = self.generalWidget.recordDirLineEdit.text()
        videodir = os.path.abspath(str(QtGui.QFileDialog.getExistingDirectory(self, "Select Video Directory", directory)))
        self.generalWidget.recordDirLineEdit.setText(videodir)
        self.generalWidget.recordDirLineEdit.emit(QtCore.SIGNAL("editingFinished()"))

    def update_record_directory(self):
        self.config.videodir = str(self.generalWidget.recordDirLineEdit.text())
        self.config.writeConfig()

    def toggle_autohide(self, state):
        self.config.auto_hide = state
        self.config.writeConfig()

    ###
    ### Plugin Loader Related
    ###
        
    def load_plugin_list(self, plugin_type):
        self.pluginloaderWidget.listWidget.clear()
        for plugin in self.plugman.plugmanc.getPluginsOfCategory(plugin_type):
            item = QtGui.QListWidgetItem()
            
            size = QtCore.QSize(64, 64)
            item.setSizeHint(size)
            self.pluginloaderWidget.listWidget.addItem(item)
            
            # The list item will be a fancy widget.
            widget = self.pluginloaderWidget.getListWidgetPlugin(plugin,
                                                                 plugin_type,
                                                                 self.plugman)
            self.pluginloaderWidget.listWidget.setItemWidget(item, widget)

    def load_option_audioinput_plugins(self):
        self.mainWidgetLayout.addWidget(self.pluginloaderWidget)
        self.currentWidget = self.pluginloaderWidget
        self.currentWidget.show()

        self.load_plugin_list("AudioInput")
            
    def load_option_audiomixer_plugins(self):
        self.mainWidgetLayout.addWidget(self.pluginloaderWidget)
        self.currentWidget = self.pluginloaderWidget
        self.currentWidget.show()

        self.load_plugin_list("AudioMixer")
        
    def load_option_videoinput_plugins(self):
        self.mainWidgetLayout.addWidget(self.pluginloaderWidget)
        self.currentWidget = self.pluginloaderWidget
        self.currentWidget.show()

        self.load_plugin_list("VideoInput")
            
    def load_option_videomixer_plugins(self):
        self.mainWidgetLayout.addWidget(self.pluginloaderWidget)
        self.currentWidget = self.pluginloaderWidget
        self.currentWidget.show()

        self.load_plugin_list("VideoMixer")
    
    def load_option_output_plugins(self):
        self.mainWidgetLayout.addWidget(self.pluginloaderWidget)
        self.currentWidget = self.pluginloaderWidget
        self.currentWidget.show()
        
        self.load_plugin_list("Output")

    def set_plugin_state(self, plugin):
        
        plugin_name = str(plugin.text())
        plugin_category = str(self.optionsTreeWidget.currentItem().text(0))
        
        if plugin.checkState() == 2:
            self.plugman.activate_plugin(plugin_name, plugin_category)
            self.add_plugin_widget(plugin_name, plugin_category)
            if plugin_category == "AudioMixer" and self.config.audiomixer == "None":
                self.change_audiomixer(plugin_name)
            elif plugin_category == "VideoMixer" and self.config.videomixer == "None":
                self.change_videomixer(plugin_name)
        else:
            self.plugman.deactivate_plugin(plugin_name, plugin_category)
    
    def load_plugin_widgets(self):
        for plugin in self.plugman.plugmanc.getAllPlugins():
            plugin.plugin_object.set_gui(self)

    def show_plugin_widget_dialog(self, widget):
        self.dialog = QtGui.QDialog(self)
    
        self.dialog_layout = QtGui.QHBoxLayout()
        self.dialog.setLayout(self.dialog_layout)
        self.dialog_layout.addWidget(widget)
        self.dialog.show()
            
    def get_plugin_settings_widget(self, plugin):
        widget = plugin.plugin_object.get_widget()
        return widget

    # Override
    
#    def area_select(self):
#        self.area_selector = QtAreaSelector(self)
#        self.area_selector.show()
#        self.core.logger.log.info('Desktop area selector started.')
#        self.hide()
#
#    def desktopAreaEvent(self, start_x, start_y, end_x, end_y):
#        self.start_x = self.core.config.start_x = start_x
#        self.start_y = self.core.config.start_y = start_y
#        self.end_x = self.core.config.end_x = end_x
#        self.end_y = self.core.config.end_y = end_y
#        self.core.logger.log.debug('area selector start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
#        self.show()
#    
    def translateFile(self,file_ending):
        load_string = LANGUAGE_DIR+'tr_'+ file_ending; #create language file path
        #loaded = self.uiTranslator.load(load_string);
        # Temporary place holder until we fix translations for configtool
        loaded = False
        if (loaded == True):
            self.retranslateUi(self);
        else:
            print("Configtool Can Not Load language file, Invalid Locale Resorting to Default Language: English");

    def closeEvent(self, event):
        logging.info('Exiting configtool...')
        self.geometry = self.saveGeometry()
        event.accept()
