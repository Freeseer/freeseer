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

from PyQt4 import QtGui, QtCore
from os import listdir;
from freeseer.framework.core import *
from freeseer.framework.qt_area_selector import *
from freeseer.framework.qt_key_grabber import *
from freeseer.framework.presentation import *

from freeseer_ui_qt import *
from freeseer_about import *
import qxtglobalshortcut

__version__=u'2.0.0'

NAME=u'Freeseer'
URL=u'http://github.com/fosslc/freeseer'
RECORD_BUTTON_ARTIST=u'Sekkyumu'
RECORD_BUTTON_LINK=u'http://sekkyumu.deviantart.com/'
HEADPHONES_ARTIST=u'Ben Fleming'
HEADPHONES_LINK=u'http://mediadesign.deviantart.com/'
LANGUAGE_DIR = 'freeseer/frontend/default/languages/'
	

class AboutDialog(QtGui.QDialog):
    '''
    About dialog class for displaying app information
    '''

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_FreeseerAbout()
        self.ui.setupUi(self)
	self.translate();
	
	
    def	translate(self):
        '''
	 Translates the about dialog. Calls the retranslateUi function of the about dialog itself
        '''
	DESCRIPTION = self.tr('AboutDialog','Freeseer is a video capture utility capable of capturing presentations. It captures video sources such as usb, firewire, or local desktop along with audio and mixes them together to produce a video.')
	COPYRIGHT=self.tr('Copyright (C) 2010 The Free and Open Source Software Learning Centre')
	LICENSE_TEXT=self.tr("Freeseer is licensed under the GPL version 3. This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software.")
	
	ABOUT_INFO = u'<h1>'+NAME+u'</h1>' + \
	u'<br><b>'+ self.tr("Version")+":" + __version__ + u'</b>' + \
	u'<p>' + DESCRIPTION + u'</p>' + \
	u'<p>' +  COPYRIGHT + u'</p>' + \
	u'<p><a href="'+URL+u'">' + URL + u'</a></p>' \
	u'<p>' + LICENSE_TEXT + u'</p>' \
	u'<p>' +  self.tr("Record button graphics by")+ ': <a href="' + RECORD_BUTTON_LINK+ u'">' + RECORD_BUTTON_ARTIST + u'</a></p>' \
	u'<p>'+ self.tr("Headphones graphics by") + ': <a href="' + HEADPHONES_LINK+ u'">' + HEADPHONES_ARTIST + u'</a></p>'
 
	self.ui.retranslateUi(self);
	self.ui.aboutInfo.setText(ABOUT_INFO);
	
	
class SystemLanguages:
  '''
    Language system class that is responsible for retrieving valid languages in the system 
  '''
  def __init__(self):
    self.languages = []
    self.languages = self.getAllLanguages();
    
  def getAllLanguages(self):
    '''    
    Returns all the valid languages that have existing qm files. In other words languages 
    that can be loaded into the translator
    ''' 
    try:
      files = listdir(LANGUAGE_DIR);
      files = map(lambda x: x.split('.') , files);
      qm_files = filter(lambda x:x[len(x)-1] == 'qm',files);
      language_prefix = map(lambda x: x[0].split("tr_")[1],qm_files); 
    except:
      return [];
    return language_prefix;    
    
 
 
class MainApp(QtGui.QMainWindow):
    '''
    Freeseer main gui class
    '''
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_FreeseerMainWindow()
        self.ui.setupUi(self)
        self.ui.hardwareBox.hide()
        self.statusBar().showMessage('ready')
        self.aboutDialog = AboutDialog()    
        self.ui.editTable.setColumnHidden(3,True)
        self.default_language = 'en';
        self.talks_to_save = []
        self.talks_to_delete = []

        self.core = FreeseerCore(self)
        
        # get supported video sources and enable the UI for supported devices.
        self.configure_supported_video_sources()
        
        #Setup the translator and populate the language menu under options
	self.uiTranslator = QtCore.QTranslator();
	self.langActionGroup = QtGui.QActionGroup(self);
	QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'));
	self.setupLanguageMenu();
	
        # get available audio sources
        sndsrcs = self.core.get_audio_sources()
        for src in sndsrcs:
            self.ui.audioSourceList.addItem(src)
            
        self.load_talks()
        self.load_events()
        self.load_rooms()
        self.load_settings()
        
        # setup systray
        logo = QtGui.QPixmap(":/freeseer/freeseer_logo.png")
        sysIcon = QtGui.QIcon(logo)
        self.systray = QtGui.QSystemTrayIcon(sysIcon)
        self.systray.show()
        self.systray.menu = QtGui.QMenu()
        showWinCM = self.systray.menu.addAction("Hide/Show Main Window")
        recordCM = self.systray.menu.addAction("Record")
        stopCM = self.systray.menu.addAction("Stop")
        self.systray.setContextMenu(self.systray.menu)
        self.connect(showWinCM, QtCore.SIGNAL('triggered()'), self.showMainWin)
        self.connect(recordCM, QtCore.SIGNAL('triggered()'), self.recContextM)
        self.connect(stopCM, QtCore.SIGNAL('triggered()'), self.stopContextM)
        self.connect(self.systray, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self._icon_activated)

        # main tab connections
        self.connect(self.ui.eventList, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.get_rooms_and_talks_at_event)
        self.connect(self.ui.roomList, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.get_talks_at_room)
        self.connect(self.ui.recordButton, QtCore.SIGNAL('toggled(bool)'), self.capture)
        self.connect(self.ui.testButton, QtCore.SIGNAL('toggled(bool)'), self.test_sources)
        self.connect(self.ui.audioFeedbackCheckbox, QtCore.SIGNAL('stateChanged(int)'), self.toggle_audio_feedback)

        # configure tab connections
        self.connect(self.ui.videoConfigBox, QtCore.SIGNAL('toggled(bool)'), self.toggle_video_recording)
        self.connect(self.ui.soundConfigBox, QtCore.SIGNAL('toggled(bool)'), self.toggle_audio_recording)
        self.connect(self.ui.videoDeviceList, QtCore.SIGNAL('activated(int)'), self.change_video_device)
        self.connect(self.ui.audioSourceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_audio_device)
        
        # connections for video source radio buttons
        self.connect(self.ui.localDesktopButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.recordLocalDesktopButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.recordLocalAreaButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.hardwareButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.usbsrcButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.firewiresrcButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.areaButton, QtCore.SIGNAL('clicked()'), self.area_select)
        self.connect(self.ui.resetSettingsButton, QtCore.SIGNAL('clicked()'), self.load_settings)
        self.connect(self.ui.applySettingsButton, QtCore.SIGNAL('clicked()'), self.save_settings)
        
        # connections for configure > Extra Settings > Shortkeys
        self.short_rec_key = qxtglobalshortcut.QxtGlobalShortcut(self)
        self.short_stop_key = qxtglobalshortcut.QxtGlobalShortcut(self)
        self.short_rec_key.setShortcut(QtGui.QKeySequence(self.core.config.key_rec))
        self.short_stop_key.setShortcut(QtGui.QKeySequence(self.core.config.key_stop))
        self.short_rec_key.setEnabled(True)
        self.short_stop_key.setEnabled(True)
        self.connect(self.short_rec_key, QtCore.SIGNAL('activated()'), self.recContextM)
        self.connect(self.short_stop_key, QtCore.SIGNAL('activated()'), self.stopContextM)
        self.connect(self.ui.shortRecordButton, QtCore.SIGNAL('clicked()'), self.grab_rec_key)
        self.connect(self.ui.shortStopButton, QtCore.SIGNAL('clicked()'), self.grab_stop_key)
        
        # connections for configure > Extra Settings > File Locations
        self.connect(self.ui.videoDirectoryButton, QtCore.SIGNAL('clicked()'), self.browse_video_directory)

        # edit talks tab connections
        self.connect(self.ui.confirmAddTalkButton, QtCore.SIGNAL('clicked()'), self.add_talk)
        self.connect(self.ui.rssButton, QtCore.SIGNAL('clicked()'), self.add_talks_from_rss)
        self.connect(self.ui.removeTalkButton, QtCore.SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.ui.resetButton, QtCore.SIGNAL('clicked()'), self.reset)
        self.ui.addTalkGroupBox.setHidden(True)
        
        # extra tab connections
        self.connect(self.ui.autoHideCheckbox, QtCore.SIGNAL('toggled(bool)'), self.toggle_auto_hide)

        # Main Window Connections
        self.connect(self.ui.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        
        # editTable Connections
        self.connect(self.ui.editTable, QtCore.SIGNAL('cellChanged(int, int)'), self.edit_talk)

        # setup video preview widget
        self.core.preview(True, self.ui.previewWidget.winId())

        # setup default sources
        self.toggle_video_source()
        if (self.core.config.audiosrc == 'none'):
            self.core.change_soundsrc(str(self.ui.audioSourceList.currentText()))
        else: self.core.change_soundsrc(self.core.config.audiosrc)
        if (self.core.config.audiofb == 'True'):
            self.ui.audioFeedbackCheckbox.toggle()

        # setup spacebar key
        self.ui.recordButton.setShortcut(QtCore.Qt.Key_Space)
        self.ui.recordButton.setFocus()
	
    def setupLanguageMenu(self):
	#Add Languages to the Menu Ensure only one is clicked 
	self.langActionGroup.setExclusive(True)
	system_ending = QtCore.QLocale.system().name();	#Retrieve Current Locale from the operating system         
	active_button = None; #the current active menu item (menu item for default language)
	current_lang_length = 0; #Used to determine the length of prefix that match for the current default language
	default_ending = self.default_language;
	'''
	  Current Lang Length
	    0 -  No Common Prefix
	    1 -  Common Language 
	    2 -  Common Language and Country
	'''
	language_table = SystemLanguages(); #Load all languages from the language folder 
	
	for language_name in language_table.languages:
	  translator = QtCore.QTranslator(); #Create a translator to translate names
	  data = translator.load(LANGUAGE_DIR+'tr_'+language_name);  
	  #Create the button
	  if(data == False):	
	    continue;
	  language_display_text = translator.translate("MainApp","language_name");
	  if(language_display_text!=''):
	    language_menu_button = QtGui.QAction(self);
	    language_menu_button.setCheckable(True);
	    #Dialect handling for locales from operating system. Use possible match
	    if(language_name == system_ending): #direct match 
	      active_button = language_menu_button;
	      current_lang_length = 2; 
	      self.default_language = system_ending;
	    else:
	      if(language_name.split("_")[0] == system_ending.split("_")[0]): #If language matches but not country 
		if(current_lang_length < 1): #if there has been no direct match yet.
		 active_button = language_menu_button;
		 current_lang_length = 1;
		 self.default_language = language_name
	      if(language_name.split("_")[0] == default_ending): #default language hit and no other language has been set
		if(current_lang_length == 0):
		  active_button = language_menu_button;
		  self.default_language = language_name;  
	  #language_name is a holder for the language name in the translation file tr_*.ts   
	    language_menu_button.setText(language_display_text);
	    language_menu_button.setData(language_name);
	    self.ui.menuLanguage.addAction(language_menu_button); 
	    self.langActionGroup.addAction(language_menu_button);	 
	if(active_button!=None):	
	  active_button.setChecked(True);
	  print('There are no languages available in the system except english. Please check the language directory to ensure qm files exist');  
	#Set up the event handling for each of the menu items  
        self.connect(self.langActionGroup,QtCore.SIGNAL('triggered(QAction *)'), self.translateAction)
	
    def configure_supported_video_sources(self):
        vidsrcs = self.core.get_video_sources()
        for src in vidsrcs:
            if (src == 'desktop'):
                self.ui.localDesktopButton.setEnabled(True)
            elif (src == 'usb'):
                self.ui.hardwareButton.setEnabled(True)
                self.ui.usbsrcButton.setEnabled(True)
            elif (src == 'firewire'):
                self.ui.hardwareButton.setEnabled(True)
                self.ui.firewiresrcButton.setEnabled(True)
                
        if (self.core.config.videosrc == 'desktop'):
            self.ui.localDesktopButton.setChecked(True)
            if (self.core.config.videodev == 'local area'):
                self.ui.recordLocalAreaButton.setChecked(True)
                self.desktopAreaEvent(int(self.core.config.start_x), int(self.core.config.start_y), int(self.core.config.end_x), int(self.core.config.end_y))
        elif (self.core.config.videosrc == 'usb'):
            self.ui.hardwareButton.setChecked(True)
            self.ui.usbsrcButton.setChecked(True)
        elif (self.core.config.videosrc == 'firewire'):
            self.ui.hardwareButton.setChecked(True)
            self.ui.firewiresrcButton.setChecked(True)

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
        if (self.ui.localDesktopButton.isChecked()): 
            self.ui.autoHideCheckbox.setChecked(True)
            if (self.ui.recordLocalDesktopButton.isChecked()):
                self.videosrc = 'desktop'
                self.core.config.videodev = 'default'
            elif (self.ui.recordLocalAreaButton.isChecked()):
                self.videosrc = 'desktop'
                self.core.config.videodev = 'local area'
                self.core.set_record_area(True)

        # recording from hardware such as usb or fireware device
        elif (self.ui.hardwareButton.isChecked()):
            self.ui.autoHideCheckbox.setChecked(False)
            self.core.set_record_area(False)
            if (self.ui.usbsrcButton.isChecked()): self.videosrc = 'usb'
            elif (self.ui.firewiresrcButton.isChecked()): self.videosrc = 'firewire'
            else: return

            # add available video devices for selected source
            viddevs = self.core.get_video_devices(self.videosrc)
            self.ui.videoDeviceList.clear()
            for dev in viddevs:
                self.ui.videoDeviceList.addItem(dev)
            self.core.config.videodev = str(self.ui.videoDeviceList.currentText())

        # invalid selection (this should never happen)
        else: return

        # finally load the changes into core
        self.core.change_videosrc(self.videosrc, self.core.config.videodev)
        
    def load_settings(self):
        self.ui.videoDirectoryLineEdit.setText(self.core.config.videodir)
        self.ui.shortRecordLineEdit.setText(self.core.config.key_rec)
        self.ui.shortStopLineEdit.setText(self.core.config.key_stop)

        if self.core.config.resolution == '0x0':
            resolution = 0
        else:
            resolution = self.ui.resolutionComboBox.findText(self.core.config.resolution)
        if not (resolution < 0): self.ui.resolutionComboBox.setCurrentIndex(resolution)
        
    def save_settings(self):
        self.core.config.videodir = str(self.ui.videoDirectoryLineEdit.text())
        self.core.config.resolution = str(self.ui.resolutionComboBox.currentText())
        if self.core.config.resolution == 'NONE':
            self.core.config.resolution = '0x0'
        self.core.config.writeConfig()
        
        self.change_output_resolution()
        
    def browse_video_directory(self):
        directory = self.ui.videoDirectoryLineEdit.text()
        videodir = QtGui.QFileDialog.getExistingDirectory(self, 'Select Video Directory', directory) + '/'
        self.ui.videoDirectoryLineEdit.setText(videodir)

    def change_video_device(self):
        '''
        Function for changing video device
        eg. /dev/video1
        '''
        dev = self.core.config.videodev = str(self.ui.videoDeviceList.currentText())
        src = self.videosrc
        self.core.logger.log.debug('Changing video device to ' + dev)
        self.core.change_videosrc(src, dev)
        
    def change_output_resolution(self):
        res = str(self.ui.resolutionComboBox.currentText())
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
        src = self.core.config.audiosrc = str(self.ui.audioSourceList.currentText())
        self.core.logger.log.debug('Changing audio device to ' + src)
        self.core.change_soundsrc(src)

    def toggle_audio_feedback(self):
        if (self.ui.audioFeedbackCheckbox.isChecked()):
            self.core.audioFeedback(True)
            self.core.config.audiofb = 'True'
            self.core.config.writeConfig()
            return
        self.core.config.audiofb = 'False'
        self.core.audioFeedback(False)
        self.core.config.writeConfig()

    def current_presentation(self):
	'''
	Creates a presentation object from the currently selected title on the GUI
	'''
        title = str(self.ui.talkList.currentText().toUtf8())
	p_id = self.core.get_presentation_id_by_selected_title(title)
	return self.core.get_presentation(p_id)

    def capture(self, state):
        '''
        Function for recording and stopping recording.
        '''
        if (state): # Start Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/freeseer_logo_rec.png")
            sysIcon2 = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon2)


            self.core.record(self.current_presentation())	
            self.ui.recordButton.setText(self.tr('Stop'))

            if (not self.ui.autoHideCheckbox.isChecked()):
                self.statusBar().showMessage('recording...')
            else:
                self.hide()
            self.core.config.videosrc = self.videosrc
            self.core.config.writeConfig()
            
        else: # Stop Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/freeseer_logo.png")
            sysIcon = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon)
            self.core.stop()
            self.ui.recordButton.setText(self.tr('Record'))
            self.ui.audioFeedbackSlider.setValue(0)
            self.statusBar().showMessage('ready')

    def test_sources(self, state):
        # Test video and audio sources
        if (self.ui.audioFeedbackCheckbox.isChecked()):
            self.core.test_sources(state, True, True)
        # Test only video source
        else:
            self.core.test_sources(state, True, False)

    def add_talk(self):
        presentation = Presentation(str(self.ui.titleEdit.text()),
                                    str(self.ui.presenterEdit.text()),
                                    "",         # description
                                    "",         # level
                                    str(self.ui.eventEdit.text()),
                                    str(self.ui.dateTimeEdit),
                                    str(self.ui.roomEdit.text()))
                
        # Do not add talks if they are empty strings
        if (len(presentation.title) == 0): return
        
        self.core.add_talk(presentation)

        # cleanup
        self.ui.titleEdit.clear()
        self.ui.presenterEdit.clear()
        self.ui.eventEdit.clear()
        self.ui.dateTimeEdit.clear()
        self.ui.roomEdit.clear()
        
        self.update_talk_views()

    def remove_talk(self): 
        try:
            row_clicked = self.ui.editTable.currentRow()
        except:            
            return
        
        id = self.ui.editTable.item(row_clicked, 3).text() 
        self.core.delete_talk(str(id))
        self.ui.editTable.removeRow(row_clicked)

        self.update_talk_views()

    # This method currently causing performance issues.
    def edit_talk(self, row, col):
        try:
            speaker = self.ui.editTable.item(row, 0).text()
            title = self.ui.editTable.item(row, 1).text()
            room = self.ui.editTable.item(row, 2).text()
            talk_id = self.ui.editTable.item(row, 3).text()
        except:
            return

        self.core.update_talk(talk_id, speaker, title, room)

        # Update the main tab
        self.load_events()
        self.load_rooms()
        
        event = str(self.ui.eventList.currentText())
        room = str(self.ui.roomList.currentText())
        talk_list = self.core.filter_talks_by_event_room(event, room)
        self.update_talk_list(talk_list)
   
    def reset(self):
        self.core.clear_database()
        self.update_talk_views()

    def get_rooms_and_talks_at_event(self, event):        
        room_list = self.core.filter_rooms_by_event(self.ui.eventList.currentText())        
        self.update_room_list(room_list)
        
        room = str(self.ui.roomList.currentText())
        talk_list = self.core.filter_talks_by_event_room(event, room)
        
        self.update_talk_list(talk_list)
        
    def get_talks_at_room(self, room):
        event = str(self.ui.eventList.currentText())
        talk_list = self.core.filter_talks_by_event_room(event, room)
        self.update_talk_list(talk_list)

    def update_talk_list(self, talk_list):
        self.ui.talkList.clear()
        
        for talk in talk_list:
            self.ui.talkList.addItem(talk)
            
    def update_room_list(self, room_list):
        self.ui.roomList.clear()
    
        for room in room_list:
            self.ui.roomList.addItem(room)
                  
    def load_talks(self):
        '''
        This method updates the GUI with the available presentation titles.
        '''
        
        # Update the main tab
        event = str(self.ui.eventList.currentText())
        room = str(self.ui.roomList.currentText())
        talk_list = self.core.filter_talks_by_event_room(event, room)
        self.update_talk_list(talk_list)

        # Update the Edit Talks Table
        talklist = self.core.get_talk_titles()
        
        self.ui.editTable.clearContents()
        self.ui.editTable.setRowCount(0)    
       
        for talk in talklist:          
            index = self.ui.editTable.rowCount()
            self.ui.editTable.insertRow(index)
            
            for i in range(len(talk)):                
                self.ui.editTable.setItem(index,i,QtGui.QTableWidgetItem(unicode(talk[i])))                         
        
        self.ui.editTable.resizeRowsToContents()
            
    def load_events(self):
        '''
        This method updates the GUI with the available presentation events.
        '''
        event_list = self.core.get_talk_events()
        self.ui.eventList.clear()
        self.ui.eventList.addItem("All")
        
        for event in event_list:
            if len(event)>0:
                self.ui.eventList.addItem(event)   
            
    def load_rooms(self):
        '''
        This method updates the GUI with the available presentation rooms.
        '''
        room_list = self.core.get_talk_rooms()
        self.ui.roomList.clear()
        self.ui.roomList.addItem("All")
        
        for room in room_list:
            if len(room)>0:
                self.ui.roomList.addItem(room)

    def add_talks_from_rss(self):
        rss_url = str(self.ui.rssEdit.text())
        self.core.add_talks_from_rss(rss_url)
        self.update_talk_views()

    def update_talk_views(self):
        # disconnect the editTable signal before we refresh the views
        self.disconnect(self.ui.editTable, QtCore.SIGNAL('cellChanged(int, int)'), self.edit_talk)

        # finish up
        self.load_events()
        self.load_rooms()
        self.load_talks()

        # lets not forget to reactivate the editTable signal
        self.connect(self.ui.editTable, QtCore.SIGNAL('cellChanged(int, int)'), self.edit_talk)
        
    def toggle_auto_hide(self):
        '''
        This function disables the preview when auto-hide box is checked.
        '''
        if self.ui.autoHideCheckbox.isChecked():
            self.core.preview(False, self.ui.previewWidget.winId())
        else: self.core.preview(True, self.ui.previewWidget.winId())

    def _icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.show()
            else: self.hide()
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.ui.recordButton.toggle()

    def showMainWin(self):
        if self.isHidden():
            self.show()
        else: self.hide()

    def recContextM(self):
        if not self.ui.recordButton.isChecked():
            self.ui.recordButton.toggle()

    def stopContextM(self):
        if self.ui.recordButton.isChecked():
            self.ui.recordButton.toggle()

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
        self.ui.shortRecordLineEdit.setText(key)
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
        self.ui.shortStopLineEdit.setText(key)
        self.core.config.key_stop = key
        self.core.config.writeConfig()
        self.short_stop_key.setShortcut(QtGui.QKeySequence(self.core.config.key_stop))
        self.show()

    def coreEvent(self, event_type, value):
        if event_type == 'audio_feedback':
            self.ui.audioFeedbackSlider.setValue(value)

    def closeEvent(self, event):
        self.core.logger.log.info('Exiting freeseer...')
        #self.core.stop()
        event.accept()
    
    def translateAction(self ,action):
     '''
      When a language is selected from the language menu this function is called
      The language to be changed to is retrieved
     '''
     language_prefix = action.data().toString();  
     self.translateFile(language_prefix);
      
    def translateFile(self,file_ending):
      '''
      Actually perfoms the translation. This is called by the handler for the language menu
      Note: If the language file can not be loaded then the default language is english 
      '''
      load_string = LANGUAGE_DIR+'tr_'+ file_ending; #create language file path
      loaded = self.uiTranslator.load(load_string);
  
      if(loaded == True):
   
       self.ui.retranslateUi(self); #Translate both the ui and the about page
       self.aboutDialog.translate();
       
      else:
       print("Invalid Locale Resorting to Default Language: English");
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainApp()
    main.show();
    sys.exit(app.exec_())
