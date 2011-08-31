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
from os import name;

from PyQt4 import QtGui, QtCore, QtSql

from freeseer import project_info
from freeseer.framework.core import *
from freeseer.framework.presentation import *
from freeseer.framework.freeseer_about import *
from freeseer.frontend.talkeditor.talkeditor import *
from freeseer.frontend.configtool.configtool import *

from freeseer_ui_qt import *

__version__= project_info.VERSION

NAME = project_info.NAME
URL = project_info.URL
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

    def translate(self):
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
        self.default_language = 'en';
        self.talks_to_save = []
        self.talks_to_delete = []
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        self.core = FreeseerCore(self.ui.previewWidget.winId())
        
        #Setup the translator and populate the language menu under options
        self.uiTranslator = QtCore.QTranslator();
        self.langActionGroup = QtGui.QActionGroup(self);
        QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'));
        self.setupLanguageMenu();

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
        self.connect(showWinCM, QtCore.SIGNAL('triggered()'), self.toggle_window_visibility)
        self.connect(recordCM, QtCore.SIGNAL('triggered()'), self.recContextM)
        self.connect(stopCM, QtCore.SIGNAL('triggered()'), self.stopContextM)
        self.connect(self.systray, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self._icon_activated)

        # main tab connections
        self.connect(self.ui.eventList, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_rooms_and_talks_from_event)
        self.connect(self.ui.roomList, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_talks_from_room)
        self.connect(self.ui.recordButton, QtCore.SIGNAL('toggled(bool)'), self.capture)

        # Main Window Connections
        self.connect(self.ui.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        self.connect(self.ui.actionEdit_talks, QtCore.SIGNAL('triggered()'), self.run_talk_editor)
        self.connect(self.ui.actionPreferences, QtCore.SIGNAL('triggered()'),self.run_config_tool)
                
        self.load_settings()

        #if (self.core.config.audiofb == True):
        #    self.ui.audioFeedbackCheckbox.toggle()

        # setup spacebar key
        self.ui.recordButton.setShortcut(QtCore.Qt.Key_Space)
        self.ui.recordButton.setFocus()

        self.talkEditor = TalkEditorMainApp(self.core)
        self.configTool = ConfigTool(self.core)
        self.configTool.hide()

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
        self.core.logger.log.info('Loading settings...')

        #load the config file
        self.core.config.readConfig()
        
        
        # Load Talks as a SQL Data Model
        self.load_talks_db()
        self.load_event_list()
        

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
            # check if auto-hide is set and if so hide
            if(self.core.config.auto_hide == True):
                self.hide_window()


            if (self.core.config.delay_recording>0):
                time.sleep(float(self.core.config.delay_recording))


            self.statusBar().showMessage('recording...')
            self.core.config.writeConfig()
            
        else: # Stop Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/freeseer_logo.png")
            sysIcon = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon)
            self.core.stop()
            self.ui.recordButton.setText(self.tr('Record'))
            self.ui.audioFeedbackSlider.setValue(0)
            self.statusBar().showMessage('ready')
            # for stop recording, we'll keep whatever window state
            # we have - hidden or showing
            

    ###
    ### Talk Related
    ###
    
    def load_talks_db(self):
        # Open the database
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.core.config.presentations_file)
        self.db.open()
        
    def load_event_list(self):
        # Set the Events Data Model
        self.eventsModel = QtSql.QSqlQueryModel()
        self.eventsModel.setQuery("SELECT DISTINCT Event FROM presentations")
        self.ui.eventList.setModel(self.eventsModel)

    def load_rooms_and_talks_from_event(self, event):
        self.current_event = event

        # Set the Room Data Model
        self.roomsModel = QtSql.QSqlQueryModel()
        self.roomsModel.setQuery("SELECT DISTINCT Room FROM presentations WHERE Event='%s' ORDER BY TIME ASC" % event)
        self.ui.roomList.setModel(self.roomsModel)
        
        room = str(self.ui.roomList.currentText())
        self.get_talks_at_room(room)
        
    def load_talks_from_room(self, room):
        self.current_room = room
        
        # Load the Talks Data Model
        self.talksModel = QtSql.QSqlQueryModel()
        self.talksModel.setQuery("SELECT (Speaker || ' - ' || Title) FROM presentations \
                                       WHERE Event='%s' and Room='%s' ORDER BY Time ASC" % (self.current_event, self.current_room))
        self.ui.talkList.setModel(self.talksModel)


    ###
    ### Misc
    ###
    
    def area_select(self):
        self.area_selector = QtAreaSelector(self)
        self.area_selector.show()
        self.core.logger.log.info('Desktop area selector started.')
        self.hide_window()
    
    def desktopAreaEvent(self, start_x, start_y, end_x, end_y):
        self.start_x = self.core.config.start_x = start_x
        self.start_y = self.core.config.start_y = start_y
        self.end_x = self.core.config.end_x = end_x
        self.end_y = self.core.config.end_y = end_y
        self.core.set_recording_area(self.start_x, self.start_y, self.end_x, self.end_y)
        self.core.logger.log.debug('area selector start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
        self.show_window()

    def _icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.hide_window() 
            
            
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.ui.recordButton.toggle()

    def hide_window(self):
        self.geometry = self.saveGeometry()
        self.hide()


    def show_window(self):
        if (self.geometry is not None):
            self.restoreGeometry(self.geometry)
        self.show()  
        
        
    def toggle_window_visibility(self):
        if self.isHidden():
            self.show_window()
        else:
            self.hide_window()

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
        event.accept()
        
    def keyPressEvent(self, event):
        self.core.logger.log.debug("Keypressed: %s" % event.key())
        self.core.backend.keyboard_event(event.key())

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
      
    def run_config_tool(self):
        self.connect(self.configTool, QtCore.SIGNAL("changed"),self.load_settings)
        self.configTool.show()
        
        # Restore window positioning if one was saved.
        if (self.configTool.geometry is not None):
            self.configTool.restoreGeometry(self.configTool.geometry)
        
    def run_talk_editor(self):
        self.connect(self.talkEditor, QtCore.SIGNAL('changed'), self.update_talk_views)
        self.talkEditor.show()
        
        # Restore window positioning if one was saved.
        if (self.talkEditor.geometry is not None):
            self.talkEditor.restoreGeometry(self.talkEditor.geometry)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainApp()
    main.show();
    sys.exit(app.exec_())
