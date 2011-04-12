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


from freeseer_ui_qt import *
from freeseer_about import *


from PyQt4 import QtGui, QtCore
from os import listdir;
from os import name;
from freeseer.framework.core import *
from freeseer.framework.qt_area_selector import *
from freeseer.framework.qt_key_grabber import *
from freeseer.framework.presentation import *
from freeseer.frontend.talkeditor.frontend.default.main import *
from configtool.freeseer_configtool import *
if os.name == 'posix': # Currently we only support LibQxt on linux
    import qxtglobalshortcut


__version__=u'2.0.1'

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
    
    
    def    translate(self):
        '''
        Translates the about dialog. Calls the retranslateUi function of the about dialog itself
        '''
        DESCRIPTION = self.tr('AboutDialog','Freeseer is a video capture utility capable of capturing presentations. It captures video sources such as usb, firewire, or local desktop along with audio and mixes them together to produce a video.')
        COPYRIGHT=self.tr('Copyright (C) 2011 The Free and Open Source Software Learning Centre')
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
        self.statusBar().showMessage('ready')
        self.aboutDialog = AboutDialog()
        self.configTool = ConfigTool()
        self.default_language = 'en';
        self.talks_to_save = []
        self.talks_to_delete = []

        self.core = FreeseerCore(self)
        
        # get supported video sources and enable the UI for supported devices.
        # self.configure_supported_video_sources()
        
        #Setup the translator and populate the language menu under options
        self.uiTranslator = QtCore.QTranslator();
        self.langActionGroup = QtGui.QActionGroup(self);
        QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'));
        self.setupLanguageMenu();
    
        self.load_talks()
        self.load_events()
        self.load_rooms()

        
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
        
        # connections for configure > Extra Settings > Shortkeys
        if os.name == 'posix': # Currently we only support LibQxt on linux
            self.short_rec_key = qxtglobalshortcut.QxtGlobalShortcut(self)
            self.short_stop_key = qxtglobalshortcut.QxtGlobalShortcut(self)
            self.short_rec_key.setShortcut(QtGui.QKeySequence(self.core.config.key_rec))
            self.short_stop_key.setShortcut(QtGui.QKeySequence(self.core.config.key_stop))
            self.short_rec_key.setEnabled(True)
            self.short_stop_key.setEnabled(True)
            self.connect(self.short_rec_key, QtCore.SIGNAL('activated()'), self.recContextM)
            self.connect(self.short_stop_key, QtCore.SIGNAL('activated()'), self.stopContextM)

        # Main Window Connections
        self.connect(self.ui.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        self.connect(self.ui.actionEdit_talks, QtCore.SIGNAL('triggered()'), self.run_talk_editor)
        self.connect(self.ui.actionPreferences, QtCore.SIGNAL('triggered()'),self.config_tool)
                
        self.load_settings()
        self.core.preview(True, self.ui.previewWidget.winId())
        # setup default sources
        if (self.core.config.audiofb == 'True'):
            self.ui.audioFeedbackCheckbox.toggle()

        # setup spacebar key
        self.ui.recordButton.setShortcut(QtCore.Qt.Key_Space)
        self.ui.recordButton.setFocus()

        # TODO: uncomment this and fix the issue with setupLanguageMenu
        #self.talkEditor = TalkEditorMainApp()

    def setupLanguageMenu(self):
        #Add Languages to the Menu Ensure only one is clicked 
        self.langActionGroup.setExclusive(True)
        system_ending = QtCore.QLocale.system().name();    #Retrieve Current Locale from the operating system         
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
            #print('There are no languages available in the system except english. Please check the language directory to ensure qm files exist');
        
        #Set up the event handling for each of the menu items
        self.connect(self.langActionGroup,QtCore.SIGNAL('triggered(QAction *)'), self.translateAction)
        
    def load_settings(self): 
        self.core.logger.log.info('loading setting...')

        #load the config file
        self.core.config.readConfig()

        #load enable_video_recoding setting
        if self.core.config.enable_video_recoding == 'False':
            self.core.set_video_mode(False)
        else:
            self.core.set_video_mode(True)
                        
            # load video source setting
            vidsrcs = self.core.get_video_sources()
            src = self.core.config.videosrc
            if src in vidsrcs:
                if (src == 'desktop'):
                    self.videosrc = 'desktop'

                    if (self.core.config.videodev == 'local area'):
                        self.desktopAreaEvent(int(self.core.config.start_x), int(self.core.config.start_y), int(self.core.config.end_x), int(self.core.config.end_y))

                    self.core.change_videosrc(self.videosrc, self.core.config.videodev)

                elif (src == 'usb'):
                    self.videosrc = 'usb'

                elif (src == 'firewire'):
                    self.videosrc = 'fireware'
                else:
                    self.core.logger.log.debug('Can NOT find video source: '+ src)
    
                if src == 'usb' or src == 'fireware':
                    dev = self.core.config.videodev
                    viddevs = self.core.get_video_devices(self.videosrc)

                    if dev in viddevs:
                        self.core.change_videosrc(self.videosrc, self.core.config.videodev)

                    else:
                        self.core.logger.log.debug('Can NOT find video device: '+ dev)

            #load audio setting
            if self.core.config.enable_audio_recoding == 'False':
                self.core.set_audio_mode(False)
            else:
                self.core.set_audio_mode(True)
                sndsrcs = self.core.get_audio_sources()
                src = self.core.config.audiosrc
                if src in sndsrcs:
                    self.core.change_soundsrc(src)
                else:
                    self.core.logger.log.debug('Can NOT find audio source: '+ src)
 
            # load resolution
            self.resolution =  self.core.config.resolution
            self.change_output_resolution()
        
            #load streaming resolution
            self.streaming_resolution =  self.core.config.streaming_resolution
            self.change_streaming_resolution()
            if self.core.config.enable_streaming == 'True': # == True and self.core.config.streaming_resolution != "0x0":
                url = str(self.core.config.streaming_url)
                port = str(self.core.config.streaming_port)
                mount = str(self.core.config.streaming_mount)
                password = str(self.core.config.streaming_password)
                resolution = str(self.core.config.streaming_resolution).strip(" ")
                
                if ( url == "" or port == "" or password == "" or mount == ""):
                    QtGui.QMessageBox.warning(self, self.tr("Incomplete Streaming Settings"), self.tr("Please ensure that all the input fields for streaming are complete or disable the streaming option") , QtGui.QMessageBox.Ok);
                else:
                    
                    if resolution in self.core.config.resmap:
                        res = self.core.config.resmap[resolution]
                        self.core.backend.disable_icecast_streaming()
                    else:
                        res = resolution
                        self.core.backend.enable_icecast_streaming(url, int(port), password, mount, res)
            self.core.backend.disable_icecast_streaming()

        #load auto hide setting and enable preview
        if self.core.config.auto_hide == 'True':
            self.autoHide =  True
        else:
            self.autoHide =  False
 
        #set short key
        if os.name == 'posix': # globalshortcuts are only supported on linux atm
            self.short_rec_key.setShortcut(QtGui.QKeySequence(self.core.config.key_rec))
            self.short_stop_key.setShortcut(QtGui.QKeySequence(self.core.config.key_stop))
            self.short_rec_key.setEnabled(True)
            self.short_stop_key.setEnabled(True)
        
    def change_output_resolution(self):
        res = str(self.resolution)
        if res in self.core.config.resmap:
            res_temp = self.core.config.resmap[res]
        else:
            res_temp = res

        #print "changing res to : ", res_temp
        s = res_temp.split('x')
        width = s[0]
        height = s[1]
        self.core.change_output_resolution(width, height)
    
    def change_streaming_resolution(self):
        res = str(self.streaming_resolution)
        if res in self.core.config.resmap:
            res_temp = self.core.config.resmap[res]
        else:
            res_temp = res

        #print "changing res to : ", res_temp
        s = res_temp.split('x')
        width = s[0]
        height = s[1]
        self.core.change_stream_resolution(width, height)
        
        
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
        
        title=unicode(self.ui.talkList.currentText())
        
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
            self.ui.eventList.setEnabled(False)
            self.ui.roomList.setEnabled(False)

            if (not self.autoHide):
                self.statusBar().showMessage('recording...')
            else:
                self.hide()
            #self.core.config.videosrc = self.videosrc
            #self.core.config.writeConfig()
            
        else: # Stop Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/freeseer_logo.png")
            sysIcon = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon)
            self.core.stop()
            self.ui.recordButton.setText(self.tr('Record'))
            self.ui.audioFeedbackSlider.setValue(0)
            self.ui.eventList.setEnabled(True)
            self.ui.roomList.setEnabled(True)
            self.statusBar().showMessage('ready')

    def test_sources(self, state):
        # Test video and audio sources
        if (self.ui.audioFeedbackCheckbox.isChecked()):
            self.core.test_sources(state, True, True)
        # Test only video source
        else:
            self.core.test_sources(state, True, False)

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

    def update_talk_views(self):
        '''
        This function reloads the lists of events, rooms and talks.
        '''
        self.load_events()
        self.load_rooms()
        self.load_talks()

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


    def coreEvent(self, event_type, value):
        if event_type == 'audio_feedback':
            self.ui.audioFeedbackSlider.setValue(value)

    def closeEvent(self, event):
        self.core.logger.log.info('Exiting freeseer...')
        #self.core.stop()
        event.accept()

    def run_talk_editor(self):
        self.connect(self.talkEditor, QtCore.SIGNAL('changed'), self.update_talk_views)
        self.talkEditor.show()
    
    def translateAction(self ,action):
        '''
        When a language is selected from the language menu this function is called
        The language to be changed to is retrieved
        '''
        language_prefix = action.data().toString();
        self.translateFile(language_prefix);
      
    def translateFile(self,file_ending):
        '''
        Actually performs the translation. This is called by the handler for the language menu
        Note: If the language file can not be loaded then the default language is English 
        '''
        load_string = LANGUAGE_DIR+'tr_'+ file_ending; #create language file path
        
        loaded = self.uiTranslator.load(load_string);

        if(loaded == True):
   
            self.ui.retranslateUi(self); #Translate both the ui and the about page
            self.aboutDialog.translate();
       
        else:
            print("Invalid Locale Resorting to Default Language: English");

        self.configTool.translateFile(file_ending);
      
    def config_tool(self):
        self.connect(self.configTool, QtCore.SIGNAL("changed"),self.load_settings)
        self.configTool.show()
          

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainApp()
    main.show();
    sys.exit(app.exec_())
