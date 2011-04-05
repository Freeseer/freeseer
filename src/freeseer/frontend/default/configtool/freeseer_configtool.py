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

from freeseer.framework.qt_area_selector import *
from freeseer.framework.qt_key_grabber import *
from freeseer.framework.core import *
#from configcore import *
from freeseer_configtool_ui import *

LANGUAGE_DIR = 'freeseer/frontend/default/configtool/languages/'

class ConfigTool(QtGui.QDialog):
    '''
    ConfigTool is the window to change the program performace
    '''

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_ConfigureTool()
        self.ui.setupUi(self)
	
	self.ui.groupBox_hardware.hide()
	
	self.core = FreeseerCore(self)
	# get QT desktop to get screen size
	self.desktop = QtGui.QApplication.desktop()	
	
	# get supported video sources and enable the UI for supported devices.
        self.configure_supported_video_sources()
        
        #load setting for the config data
        self.load_settings()
	
        #Setup the translator and populate the language menu under options
	self.uiTranslator = QtCore.QTranslator();
	self.langActionGroup = QtGui.QActionGroup(self);
	QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'));
	

	
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

        self.connect(self.ui.groupBox_streaming, QtCore.SIGNAL('toggled(bool)'), self.toggle_streaming)
        
        self.connect(self.ui.lineEdit_URL_IP, QtCore.SIGNAL('textEdited(QString)'),self.change_streaming_url)
        self.connect(self.ui.lineEdit_port,QtCore.SIGNAL('textEdited(QString)'),self.change_streaming_port)
        self.connect(self.ui.lineEdit_mountPoint,QtCore.SIGNAL('textEdited(QString)'),self.change_streaming_mount)
        self.connect(self.ui.lineEdit_password,QtCore.SIGNAL('textEdited(QString)'),self.change_streaming_password)
        
        # connections for Extra setting -> auto hidden
        self.connect(self.ui.checkbox_autoHide, QtCore.SIGNAL('toggled(bool)'), self.toggle_auto_hide)
        
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
                
            
    def toggle_video_recording(self, state):
        '''
        Enables / Disables video recording depending on if the user has
        checked the video box in configuration mode.
        '''
        self.core.config.enable_video_recoding = state
	self.core.logger.log.debug('Enable video recoding: ' + str(state))
	
    def toggle_audio_recording(self,state):
        '''
        Enables / Disables audio recording depending on if the user has
        checked the audio box in configuration mode.
        '''
        self.core.config.enable_audio_recoding = state
	self.core.logger.log.debug('Enable audio recoding: ' + str(state))

    def toggle_video_source(self):
        '''
        Updates the GUI when the user selects a different video source and
        configures core with new video source information
        '''
        # recording the local desktop
        if (self.ui.radioButton_localDesktop.isChecked()): 
            self.ui.checkbox_autoHide.setChecked(True)
            self.core.config.videosrc = 'desktop'
            if (self.ui.radioButton_recordLocalDesktop.isChecked()):         
                self.core.config.videodev = 'default'
                self.videosrc = 'desktop'
                
            elif (self.ui.radioButton_recordLocalArea.isChecked()):
                self.core.config.videodev = 'local area'
		self.videosrc = 'desktop'
		
        # recording from hardware such as usb or fireware device
        elif (self.ui.radioButton_hardware.isChecked()):

            self.ui.checkbox_autoHide.setChecked(False)
            if (self.ui.radioButton_USBsrc.isChecked()): 
		self.videosrc = 'usb'
		self.core.config.videosrc = 'usb'
            elif (self.ui.radioButton_firewiresrc.isChecked()): 
		self.videosrc = 'firewire'
		self.core.config.videosrc = 'firewire'
            else: return

            # add available video devices for selected source
            viddevs = self.core.get_video_devices(self.videosrc)
            self.ui.comboBox_videoDeviceList.clear()
            for dev in viddevs:
                self.ui.comboBox_videoDeviceList.addItem(dev)
            self.core.config.videodev = str(self.ui.comboBox_videoDeviceList.currentText())
            
        # invalid selection (this should never happen)
        else: return
	
	self.core.logger.log.debug('Set video source  to ' + self.videosrc)

    def toggle_streaming(self,state):
	'''
	Enable /Disables streaming if the user has checked the
	enable streaming box in config tool
	'''
	self.core.logger.log.debug('Enable streaming: ' + str(state))
        self.core.config.enable_streaming = state
	
    def change_streaming_url(self):
	self.core.config.streaming_url = str(self.ui.lineEdit_URL_IP.text())
	#self.core.logger.log.debug('set streaming url to: ' + self.core.config.streaming_url)
	
    def change_streaming_port(self):	
	self.core.config.streaming_port = str(self.ui.lineEdit_port.text())
	#self.core.logger.log.debug('set streaming port to: ' + self.core.config.streaming_port)
	
    def change_streaming_mount(self):
	self.core.config.streaming_mount = str(self.ui.lineEdit_mountPoint.text())
	#self.core.logger.log.debug('set streaming mount point to: ' + self.core.config.streaming_mount)
    
    def change_streaming_password(self):
	self.core.config.streaming_password = str(self.ui.lineEdit_password.text())
	#passwd = '*' * len(self.core.config.streaming_password)
	#self.core.logger.log.debug('set streaming password: ' + passwd)
	
    def load_settings(self):
	#load enable video recoding setting
        if self.core.config.enable_video_recoding == 'False':
	  self.ui.groupBox_videoSource.setChecked(False)
	else:
	  self.ui.groupBox_videoSource.setChecked(True)
	#load enable audio recoding setting
	if self.core.config.enable_audio_recoding == 'False':
	  self.ui.groupBox_soundSource.setChecked(False)
	else:
	  self.ui.groupBox_soundSource.setChecked(True)
	  
	#load video source setting
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
	
	# detect screen display & load resolution
	screenres = self.primary_screen_size()
	self.screen_size()
        if self.core.config.resolution == '0x0':
            resolution = self.ui.comboBox_videoQualityList.findText(screenres)
        else:
            resolution = self.ui.comboBox_videoQualityList.findText(self.core.config.resolution)
        if not (resolution < 0): self.ui.comboBox_videoQualityList.setCurrentIndex(resolution)
        
        #load streaming resolution
        if self.core.config.enable_streaming == 'False':
	  self.ui.groupBox_streaming.setChecked(False)
	else:
	  self.ui.groupBox_streaming.setChecked(True)
	 
	self.ui.lineEdit_URL_IP.setText(self.core.config.streaming_url)
        self.ui.lineEdit_port.setText(self.core.config.streaming_port)
        self.ui.lineEdit_mountPoint.setText(self.core.config.streaming_mount)
        self.ui.lineEdit_password.setText(self.core.config.streaming_password)
        
        if self.core.config.streaming_resolution == '0x0':
	    streaming_resolution = 0
	else:
	    streaming_resolution = self.ui.comboBox_streamingQualityList.findText(self.core.config.streaming_resolution)
	if not (streaming_resolution < 0):
	    self.ui.comboBox_streamingQualityList.setCurrentIndex(streaming_resolution)
	    
        #load auto hidden setting
        if self.core.config.auto_hide == 'True':
	   self.ui.checkbox_autoHide.setChecked(True)
	else:
	   self.ui.checkbox_autoHide.setChecked(False)
	    
	#load shortkey and video directory
	self.ui.lineEdit_videoDirectory.setText(self.core.config.videodir)
        self.ui.lineEdit_recordKey.setText(self.core.config.key_rec)
        self.ui.lineEdit_stopKey.setText(self.core.config.key_stop)

    def screen_size(self):
	self.ui.tableWidget_screenResolution.setRowCount(self.desktop.screenCount())
	i = 0
	while i < self.desktop.screenCount():
	  newItem = QtGui.QTableWidgetItem(str(self.desktop.screenGeometry(i).width()) + 'x' + str(self.desktop.screenGeometry(i).height()))
	  self.ui.tableWidget_screenResolution.setItem(i,0,newItem)
	  i = i + 1

    def primary_screen_size(self):
	width = self.desktop.screenGeometry(self.desktop.primaryScreen ()).width()
	height = self.desktop.screenGeometry(self.desktop.primaryScreen ()).height()
	return str(width) + 'x' + str(height)
	
	  
    def save_settings(self):
        self.core.config.videodir = str(self.ui.lineEdit_videoDirectory.text())
        self.core.config.resolution = str(self.ui.comboBox_videoQualityList.currentText())
        if self.core.config.resolution == 'NONE':
            self.core.config.resolution = '0x0'
	self.core.config.streaming_resolution = str(self.ui.comboBox_streamingQualityList.currentText())
	if self.core.config.streaming_resolution == 'NONE':
	    self.core.config.streaming_resolution = '0x0'
	
        self.core.config.writeConfig()
        self.emit(QtCore.SIGNAL("changed"))
        
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
        self.core.config.video_device = src
     

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
        self.core.logger.log.debug('area selector start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
        self.show()

    def change_audio_device(self):
        src = self.core.config.audiosrc = str(self.ui.comboBox_audioSourceList.currentText())
        self.core.logger.log.debug('Changing audio device to ' + src)
        self.core.config.audio_source = src

    def toggle_auto_hide(self,state):
        '''
	when user toggle auto hidden, save it to conifg file
	'''
	self.core.config.auto_hide = state
	self.core.logger.log.debug('Set auto hidden to: ' + str(state))
	
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
        self.ui.lineEdit_stopKey.setText(key)
        self.core.config.key_stop = key
        self.core.config.writeConfig()
        self.show()
       
    def translateFile(self,file_ending):
	load_string = LANGUAGE_DIR+'tr_'+ file_ending; #create language file path
	loaded = self.uiTranslator.load(load_string);
	if(loaded == True):
	  self.ui.retranslateUi(self);
	else:
	  print("Configtool Can Not Load language file, Invalid Locale Resorting to Default Language: English");
	  
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = ConfigTool()
    main.show()
    sys.exit(app.exec_())
	
