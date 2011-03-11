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

from configcore import *
from freeseer_configtool_ui import *


class ConfigTool(QtGui.QDialog):
    '''
    ConfigTool is the window to change the program performace
    '''

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_ConfigureTool()
        self.ui.setupUi(self)
	self.default_language = 'en';
	
	self.ui.groupBox_hardware.hide()
	
	self.ui.label_check_1.setVisible(False)
        self.ui.label_check_2.setVisible(False)
        self.ui.label_check_3.setVisible(False)
        self.ui.label_check_4.setVisible(False)
 
        
	#self.ui.pushButton_testStreaming.setEnabled(False)
	
	self.core = ConfigCore(self)
	self.desktop = QtGui.QApplication.desktop()	
	# get supported video sources and enable the UI for supported devices.
        self.configure_supported_video_sources()
        
        #Setup the translator and populate the language menu under options
	self.uiTranslator = QtCore.QTranslator();
	self.langActionGroup = QtGui.QActionGroup(self);
	QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'));
	
	#load setting for the config data
        self.load_settings()
	
	
	# configure tab connections
        self.connect(self.ui.groupBox_videoSource, QtCore.SIGNAL('toggled(bool)'), self.toggle_video_recording)
        self.connect(self.ui.groupBox_soundSource, QtCore.SIGNAL('toggled(bool)'), self.toggle_audio_recording)
        self.connect(self.ui.comboBox_videoDeviceList, QtCore.SIGNAL('activated(int)'), self.change_video_device)
        self.connect(self.ui.comboBox_audioSourceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_audio_device)

	# connections for video source radio buttons
        self.connect(self.ui.radioButton_localDesktop, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.radioButton_recordLocalDesktop, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.radioButton_recordLocalArea, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.radioButton_hardware, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.radioButton_USBsrc, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.radioButton_firewiresrc, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.pushButton_setArea, QtCore.SIGNAL('clicked()'), self.area_select)
        self.connect(self.ui.pushButton_reset, QtCore.SIGNAL('clicked()'), self.load_settings)
        self.connect(self.ui.pushButton_apply, QtCore.SIGNAL('clicked()'), self.save_settings)
        
        self.connect(self.ui.pushButton_derectScreenResoltion,QtCore.SIGNAL('clicked()'),self.screen_size)
        self.connect(self.desktop ,QtCore.SIGNAL('resized(int)'),self.screen_size)
        self.connect(self.desktop ,QtCore.SIGNAL('screenCountChanged(int)'),self.screen_size)
        #connections for Video Setting -> Enable Streaming

        self.connect(self.ui.groupBox_enableStreaming,QtCore.SIGNAL('toggle(bool)'), self.toggle_enable_streaming)
        '''
        self.connect(self.ui.lineEdit_URL_IP,QtCore.SIGNAL('textChanged(bool)'),self.change_enable_streaming)
        self.connect(self.ui.lineEdit_port,QtCore.SIGNAL('textChanged(bool)'),self.change_enable_streaming)
        self.connect(self.ui.lineEdit_mountPoint,QtCore.SIGNAL('textChanged(bool)'),self.change_enable_streaming)
        self.connect(self.ui.lineEdit_password,QtCore.SIGNAL('textChanged(bool)'),self.change_enable_streaming)
	'''
        self.connect(self.ui.pushButton_testStreaming,QtCore.SIGNAL('clicked()'),self.test_streaming)
        
        # connections for Extra Setting -> ShortKeys
        self.connect(self.ui.pushButton_recodrdKey, QtCore.SIGNAL('clicked()'), self.grab_rec_key)
        self.connect(self.ui.pushButton_StopKey, QtCore.SIGNAL('clicked()'), self.grab_stop_key)
       
	
        # connections for Extra Settings > File Locations
        self.connect(self.ui.pushButton_open, QtCore.SIGNAL('clicked()'), self.browse_video_directory)
        
 
        
        # get available audio sources
        sndsrcs = self.core.get_audio_sources()
        for src in sndsrcs:
            self.ui.comboBox_audioSourceList.addItem(src)
        
        # set default source
        self.toggle_video_source()
        if (self.core.config.audiosrc == 'none'):
            self.core.change_soundsrc(str(self.ui.audioSourceList.currentText()))
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

    def toggle_audio_recording(self,state):
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

    
    def toggle_enable_streaming(self,state):
	'''
	Enable /Disables streaming if the user has checked the
	enable streaming box in config tool
	'''
	pass

	
    def test_streaming(self):
	self.ui.label_check_1.setPixmap(QtGui.QPixmap(":/streamingCheck/pass.png"))
	self.ui.label_check_1.show()
	self.ui.label_check_2.setPixmap(QtGui.QPixmap(":/streamingCheck/error.png"))
	self.ui.label_check_2.show()
	
    def load_settings(self):
        self.ui.lineEdit_videoDirectory.setText(self.core.config.videodir)
        self.ui.lineEdit_recordKey.setText(self.core.config.key_rec)
        self.ui.lineEdit_stopKey.setText(self.core.config.key_stop)
	
	self.screen_size()
	screenres = self.primary_screen_size()

        if self.core.config.resolution == '0x0':
            resolution = self.ui.comboBox_videoQualityList.findText(screenres)
        else:
            resolution = self.ui.comboBox_videoQualityList.findText(self.core.config.resolution)
        if not (resolution < 0): self.ui.comboBox_videoQualityList.setCurrentIndex(resolution)
        
        if self.core.config.resolution == '0x0':
	    streaming_resolution = 0
	else:
	    streaming_resolution = self.ui.comboBox_streamingQualityList.findText(self.core.config.streaming)
	if not (streaming_resolution < 0):
	    self.ui.comboBox_streamingQualityList.setCurrentIndex(streaming_resolution)
        
    def screen_size(self):

	self.ui.tableWidget_screenResolution.setRowCount(self.desktop.screenCount())
	i = 0
	while i < self.desktop.screenCount():
	  newItem = QtGui.QTableWidgetItem(str(self.desktop.screenGeometry(i).width()) + 'x' + str(self.desktop.screenGeometry(i).height()))
	  self.ui.tableWidget_screenResolution.setItem(i,0,newItem)
	  i = i + 1
	  
    def screen_resize(self):
	self.core.logger.log.info('resized')

    def primary_screen_size(self):
	width = self.desktop.screenGeometry(self.desktop.primaryScreen ()).width()
	height = self.desktop.screenGeometry(self.desktop.primaryScreen ()).height()
	return str(width) + 'x' + str(height)
	
	  
    def save_settings(self):
        self.core.config.videodir = str(self.ui.lineEdit_videoDirectory.text())
        self.core.config.resolution = str(self.ui.comboBox_videoQualityList.currentText())
        if self.core.config.resolution == 'NONE':
            self.core.config.resolution = '0x0'
	self.core.config.streaming = str(self.ui.comboBox_streamingQualityList.currentText())
	if self.core.config.streaming == 'NONE':
	    self.core.config.streaming == '0x0'
	
        self.core.config.writeConfig()
        
        self.change_output_resolution()
        self.change_streaming_resoltion()
        
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

    def change_streaming_resoltion(self):
	res = str(self.ui.comboBox_streamingQualityList.currentText())
        if res == 'NONE':
            s = '0x0'.split('x')
        else:
            s = res.split('x')
        width = s[0]
        height = s[1]
        #need change here
        #self.core.change_output_resolution(width, height)
        
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
        #self.show()
            
    
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
        self.ui.lineEdit_stopKey.setText(key)
        self.core.config.key_stop = key
        self.core.config.writeConfig()
        self.show()
       
    def translate(self):
	self.ui.retranslateUi(self);

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = ConfigTool()
    main.show()
    sys.exit(app.exec_())
	