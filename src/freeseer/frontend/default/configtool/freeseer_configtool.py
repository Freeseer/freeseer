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

from sys import *

from PyQt4 import QtGui, QtCore
from os import listdir;

from freeseer.framework.core import *
from freeseer.framework.qt_area_selector import *
from freeseer.framework.qt_key_grabber import *
from freeseer.framework.presentation import *

from freeseer_configtool_ui import *
#import qxtglobalshortcut

class ConfigTool(QtGui.QDialog):
    '''
    ConfigTool is the window to change the program performace
    '''

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_ConfigureTool()
        self.ui.setupUi(self)
	self.default_language = 'en';
	self.ui.groupBox_hardware.hide()
	
	self.core = FreeseerCore(self)
	
	#Setup the translator and populate the language menu under options
	#self.uiTranslator = QtCore.QTranslator();
	
	# get supported video sources and enable the UI for supported devices.
        self.configure_supported_video_sources()
        
        #Setup the translator and populate the language menu under options
	self.uiTranslator = QtCore.QTranslator();
	self.langActionGroup = QtGui.QActionGroup(self);
	QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'));
	#self.setupLanguageMenu();
	
        # get available audio sources
        sndsrcs = self.core.get_audio_sources()
        for src in sndsrcs:
            self.ui.comboBox_audioSourceList.addItem(src)
       
        self.load_settings()
	
	
	# configure tab connections
        self.connect(self.ui.groupBox_videoSource, QtCore.SIGNAL('toggled(bool)'), self.toggle_video_recording)
        self.connect(self.ui.groupBox_soundSource, QtCore.SIGNAL('toggled(bool)'), self.toggle_audio_recording)
        self.connect(self.ui.comboBox_videoDeviceList, QtCore.SIGNAL('activated(int)'), self.change_video_device)
        self.connect(self.ui.comboBox_audioSourceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_audio_device)
      
	# connections for video source radio buttons
        #self.connect(self.ui.radioButton_localDesktop, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.radioButton_recordLocalDesktop, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.radioButton_recordLocalArea, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        #self.connect(self.ui.radioButton_hardware, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.radioButton_USBsrc, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.radioButton_firewiresrc, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.pushButton_setArea, QtCore.SIGNAL('clicked()'), self.area_select)
        self.connect(self.ui.pushButton_reset, QtCore.SIGNAL('clicked()'), self.load_settings)
        self.connect(self.ui.pushButton_apply, QtCore.SIGNAL('clicked()'), self.save_settings)
        
        # connections for configure > Extra Settings > Shortkeys
        #self.short_rec_key = qxtglobalshortcut.QxtGlobalShortcut(self)
        #self.short_stop_key = qxtglobalshortcut.QxtGlobalShortcut(self)
        #self.short_rec_key.setShortcut(QtGui.QKeySequence(self.core.config.key_rec))
        #self.short_stop_key.setShortcut(QtGui.QKeySequence(self.core.config.key_stop))
        #self.short_rec_key.setEnabled(True)
        #self.short_stop_key.setEnabled(True)
        #self.connect(self.short_rec_key, QtCore.SIGNAL('activated()'), self.recContextM)
        #self.connect(self.short_stop_key, QtCore.SIGNAL('activated()'), self.stopContextM)
        self.connect(self.ui.pushButton_recodrdKey, QtCore.SIGNAL('clicked()'), self.grab_rec_key)
        self.connect(self.ui.pushButton_StopKey, QtCore.SIGNAL('clicked()'), self.grab_stop_key)
        
        # connections for Extra Settings > File Locations
        self.connect(self.ui.pushButton_open, QtCore.SIGNAL('clicked()'), self.browse_video_directory)
        
        # extra tab connections
        self.connect(self.ui.checkbox_autoHide, QtCore.SIGNAL('toggled(bool)'), self.toggle_auto_hide)
        
        # set default source
        self.toggle_video_source()
        if (self.core.config.audiosrc == 'none'):
            self.core.change_soundsrc(str(self.ui.comboBox_audioSourceList.currentText()))
        else: self.core.change_soundsrc(self.core.config.audiosrc)

            
    def configure_supported_video_sources(self):
        vidsrcs = self.core.get_video_sources()
        for src in vidsrcs:
            if (src == 'desktop'):
                self.ui.radioButton_recordLocalDesktop.setEnabled(True)
            elif (src == 'usb'):
                self.ui.radioButton_hardware.setEnabled(True)
                self.ui.radioButton_USBsrc.setEnabled(True)
            elif (src == 'firewire'):
                self.ui.radioButton_hardware.setEnabled(True)
                self.ui.radioButton_firewiresrc.setEnabled(True)
                
        if (self.core.config.videosrc == 'desktop'):
            self.ui.radioButton_recordLocalDesktop.setChecked(True)
            if (self.core.config.videodev == 'local area'):
                self.ui.radioButton_recordLocalArea.setChecked(True)
                self.desktopAreaEvent(int(self.core.config.start_x), int(self.core.config.start_y), int(self.core.config.end_x), int(self.core.config.end_y))
        elif (self.core.config.videosrc == 'usb'):
            self.ui.radioButton_hardware.setChecked(True)
            self.ui.radioButton_USBsrc.setChecked(True)
        elif (self.core.config.videosrc == 'firewire'):
            self.ui.radioButton_hardware.setChecked(True)
            self.ui.radioButton_firewiresrc.setChecked(True)

    def toggle_video_recording(self, state):
        '''
        Enables / Disables video recording depending on if the user has
        checked the video box in configuration mode.
        '''
        self.core.set_video_mode(state)

    def toggle_audio_recording(self, state):
        '''
        Enables / Disables audio recording depending on if the user has
        checked the audio box in configuration mode.
        '''
        self.core.set_audio_mode(state)

    def toggle_video_source(self):
        '''
        Updates the GUI when the user selects a different video source and
        configures core with new video source information
        '''
        # recording the local desktop
        if (self.ui.radioButton_localDesktop.isChecked()): 
            self.ui.checkbox_autoHide.setChecked(True)
            if (self.ui.radioButton_recordLocalDesktop.isChecked()):
                self.videosrc = 'desktop'
                self.core.config.videodev = 'default'
            elif (self.ui.radioButton_recordLocalArea.isChecked()):
                self.videosrc = 'desktop'
                self.core.config.videodev = 'local area'
                self.core.set_record_area(True)

        # recording from hardware such as usb or fireware device
        elif (self.ui.radioButton_hardware.isChecked()):
            self.ui.checkbox_autoHide.setChecked(False)
            self.core.set_record_area(False)
            if (self.ui.radioButton_USBsrc.isChecked()): self.videosrc = 'usb'
            elif (self.ui.radioButton_firewiresrc.isChecked()): self.videosrc = 'firewire'
            else: return

            # add available video devices for selected source
            viddevs = self.core.get_video_devices(self.videosrc)
            self.ui.comboBox_videoDeviceList.clear()
            for dev in viddevs:
                self.ui.comboBox_videoDeviceList.addItem(dev)
            self.core.config.videodev = str(self.ui.comboBox_videoDeviceList.currentText())

        # invalid selection (this should never happen)
        else: return

        # finally load the changes into core
        self.core.change_videosrc(self.videosrc, self.core.config.videodev)
    
    def toggle_auto_hide(self):
        '''
        This function disables the preview when auto-hide box is checked.
        '''
        #if self.ui.checkBox_autoHide.isChecked():
            #self.core.preview(False, MainApp.ui.previewWidget.winId())
        #else: self.core.preview(True, MainApp.ui.previewWidget.winId())
        
    def load_settings(self):
        self.ui.lineEdit_videoDirectory.setText(self.core.config.videodir)
        self.ui.lineEdit_recordKey.setText(self.core.config.key_rec)
        self.ui.lineEdit_stopKey.setText(self.core.config.key_stop)

        if self.core.config.resolution == '0x0':
            resolution = 0
        else:
            resolution = self.ui.comboBox_videoQualityList.findText(self.core.config.resolution)
        if not (resolution < 0): self.ui.comboBox_videoQualityList.setCurrentIndex(resolution)
        
    def save_settings(self):
        self.core.config.videodir = str(self.ui.lineEdit_videoDirectory.text())
        self.core.config.resolution = str(self.ui.comboBox_videoQualityList.currentText())
        if self.core.config.resolution == 'NONE':
            self.core.config.resolution = '0x0'
        self.core.config.writeConfig()
        
        self.change_output_resolution()
        
    def browse_video_directory(self):
        directory = self.ui.lineEdit_videoDirectory.text()
        videodir = QtGui.QFileDialog.getExistingDirectory(self, 'Select Video Directory', directory) + '/'
        self.ui.lineEdit_videoDirectory.setText(videodir)

    def change_video_device(self):
        '''
        Function for changing video device
        eg. /dev/video1
        '''
        dev = self.core.config.videodev = str(self.ui.comboBox_videoDeviceList.currentText())
        src = self.videosrc
        self.core.logger.log.debug('Changing video device to ' + dev)
        self.core.change_videosrc(src, dev)
        
    def change_output_resolution(self):
        res = str(self.ui.comboBox_videoQualityList.currentText())
        if res == 'NONE':
            s = '0x0'.split('x')
        else:
            s = res.split('x')
        width = s[0]
        height = s[1]
        self.core.change_output_resolution(width, height)

        
    def area_select(self):
        self.area_selector = QtAreaSelector(self)
        self.area_selector.show()
        self.core.logger.log.info('Desktop area selector started.')
        self.hide()
    
    def desktopAreaEvent(self, start_x, start_y, end_x, end_y):
        self.start_x = self.core.config.start_x = start_x
        self.start_y = self.core.config.start_y = start_y
        self.end_x = self.core.config.end_x = end_x
        self.end_y = self.core.config.end_y = end_y
        self.core.set_recording_area(self.start_x, self.start_y, self.end_x, self.end_y)
        self.core.logger.log.debug('area selector start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
        self.show()

    def change_audio_device(self):
        src = self.core.config.audiosrc = str(self.ui.comboBox_audioSourceList.currentText())
        self.core.logger.log.debug('Changing audio device to ' + src)
        self.core.change_soundsrc(src)
    
    
    def grab_rec_key(self):
        '''
        When the button is pressed, it will call the keygrabber widget and log keys
        '''
        self.core.config.key_rec = 'Ctrl+Shift+R'
        self.core.config.writeConfig()
        self.key_grabber = QtKeyGrabber(self)
        self.hide()
        self.core.logger.log.info('Storing keys.')
        self.key_grabber.show()
        
    def grab_rec_set(self, key):
        '''
        Keygrabber widget calls this function to set and store the hotkey.
        '''
        self.ui.lineEdit_recordKey.setText(key)
        self.core.config.key_rec = key
        self.core.config.writeConfig()
        self.short_rec_key.setShortcut(QtGui.QKeySequence(self.core.config.key_rec))
        self.show()
            
    def grab_stop_key(self):
        '''
        When the button is pressed, it will call the keygrabber widget and log keys
        '''
        self.core.config.key_stop = 'Ctrl+Shift+E'
        self.core.config.writeConfig()
        self.key_grabber = QtKeyGrabber(self)
        self.hide()
        self.core.logger.log.info('Storing keys.')
        self.key_grabber.show()

    def grab_stop_set(self, key):
        '''
        Keygrabber widget calls this function to set and store the hotkey.
        '''
        self.ui.LineEdit_stopKey.setText(key)
        self.core.config.key_stop = key
        self.core.config.writeConfig()
        self.short_stop_key.setShortcut(QtGui.QKeySequence(self.core.config.key_stop))
        self.show()
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ConfigTool()
    myapp.show()
    sys.exit(app.exec_())
