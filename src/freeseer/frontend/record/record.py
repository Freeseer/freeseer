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
from os import listdir, name
import sys

from PyQt4 import QtGui, QtCore, QtSql

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer import project_info
from freeseer.framework.core import *
from freeseer.framework.presentation import *
from freeseer.framework.QtDBConnector import *
from freeseer.frontend.qtcommon.AboutDialog import AboutDialog

from RecordingWidget import RecordingWidget

__version__= project_info.VERSION

LANGUAGE_DIR = 'freeseer/frontend/default/languages/'

class SystemLanguages:
    '''
    Language system class that is responsible for retrieving valid languages in the system 
    '''
    def __init__(self):
        self.languages = []
        self.languages = self.getAllLanguages()
    
    def getAllLanguages(self):
        '''    
        Returns all the valid languages that have existing qm files. In other words languages 
        that can be loaded into the translator
        ''' 
        try:
            files = listdir(LANGUAGE_DIR)
            files = map(lambda x: x.split('.') , files)
            qm_files = filter(lambda x:x[len(x)-1] == 'qm',files)
            language_prefix = map(lambda x: x[0].split("tr_")[1],qm_files)
        except:
            return []
        return language_prefix

class MainApp(QtGui.QMainWindow):
    '''
    Freeseer main gui class
    '''

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle(QtGui.QApplication.translate("FreeseerMainWindow", 
                                                         "Freeseer - portable presentation recording station", 
                                                         None, 
                                                         QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/freeseer_logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(400, 400)
        
        
        self.statusBar().showMessage('ready')
        self.aboutDialog = AboutDialog()
        self.default_language = 'en'
        self.talks_to_save = []
        self.talks_to_delete = []
        
        self.mainWidget = RecordingWidget()
        self.setCentralWidget(self.mainWidget)
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        self.core = FreeseerCore(self.mainWidget.previewWidget.winId(), self.audio_feedback)
        
        #Setup the translator and populate the language menu under options
        self.uiTranslator = QtCore.QTranslator()
        self.langActionGroup = QtGui.QActionGroup(self)
        QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'))
        self.setupLanguageMenu()
        
        #
        # Setup Menubar
        #
        self.menubar = QtGui.QMenuBar()
        self.setMenuBar(self.menubar)
        
        self.menubar.setGeometry(QtCore.QRect(0, 0, 566, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(QtGui.QApplication.translate("FreeseerMainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setTitle(QtGui.QApplication.translate("FreeseerMainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menuLanguage = QtGui.QMenu(self.menuOptions)
        self.menuLanguage.setTitle(QtGui.QApplication.translate("FreeseerMainWindow", "Language", None, QtGui.QApplication.UnicodeUTF8))
        self.menuLanguage.setObjectName(_fromUtf8("menuLanguage"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setTitle(QtGui.QApplication.translate("FreeseerMainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        
        self.actionOpenVideoFolder = QtGui.QAction(self)
        self.actionOpenVideoFolder.setText(QtGui.QApplication.translate("FreeseerMainWindow", 
                                                                        "Open Video Directory", 
                                                                        None, 
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.actionOpenVideoFolder.setShortcut(QtGui.QApplication.translate("FreeseerMainWindow", 
                                                                            "Ctrl+O", 
                                                                            None, 
                                                                            QtGui.QApplication.UnicodeUTF8))
        self.actionOpenVideoFolder.setObjectName(_fromUtf8("actionOpenVideoFolder"))
        
        self.actionExit = QtGui.QAction(self)
        self.actionExit.setText(QtGui.QApplication.translate("FreeseerMainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("FreeseerMainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setText(QtGui.QApplication.translate("FreeseerMainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        
        # Actions
        self.menuFile.addAction(self.actionOpenVideoFolder)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuOptions.addAction(self.menuLanguage.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

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
        self.connect(self.mainWidget.eventComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_rooms_from_event)
        self.connect(self.mainWidget.roomComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_talks_from_room)
        self.connect(self.mainWidget.dateComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_talks_from_date)
        self.connect(self.mainWidget.recordPushButton, QtCore.SIGNAL('toggled(bool)'), self.capture)

        # Main Window Connections
        self.connect(self.actionOpenVideoFolder, QtCore.SIGNAL('triggered()'), self.open_video_directory)
        self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        
        # GUI Disabling/Enabling Connections
        self.connect(self.mainWidget.recordPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.eventComboBox.setDisabled)
        self.connect(self.mainWidget.recordPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.roomComboBox.setDisabled)
        self.connect(self.mainWidget.recordPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.talkComboBox.setDisabled)
                
        self.load_settings()

        #if (self.core.config.audiofb == True):
        #    self.ui.audioFeedbackCheckbox.toggle()

        # setup spacebar key
        self.mainWidget.recordPushButton.setShortcut(QtCore.Qt.Key_Space)
        self.mainWidget.recordPushButton.setFocus()

    def setupLanguageMenu(self):
        #Add Languages to the Menu Ensure only one is clicked 
        self.langActionGroup.setExclusive(True)
        system_ending = QtCore.QLocale.system().name()    #Retrieve Current Locale from the operating system         
        active_button = None        #the current active menu item (menu item for default language)
        current_lang_length = 0     #Used to determine the length of prefix that match for the current default language
        default_ending = self.default_language
        '''
        Current Lang Length
        0 -  No Common Prefix
        1 -  Common Language 
        2 -  Common Language and Country
        '''
        language_table = SystemLanguages(); #Load all languages from the language folder 
    
        for language_name in language_table.languages:
            translator = QtCore.QTranslator()         #Create a translator to translate names
            data = translator.load(LANGUAGE_DIR+'tr_'+language_name)  
            #Create the button
            if(data == False):    
                continue;
            language_display_text = translator.translate("MainApp","language_name")
            if(language_display_text!=''):
                language_menu_button = QtGui.QAction(self)
                language_menu_button.setCheckable(True)
            #Dialect handling for locales from operating system. Use possible match
            if(language_name == system_ending): #direct match
                active_button = language_menu_button
                current_lang_length = 2
                self.default_language = system_ending
            else:
                if(language_name.split("_")[0] == system_ending.split("_")[0]): #If language matches but not country
                    if(current_lang_length < 1): #if there has been no direct match yet.
                        active_button = language_menu_button
                        current_lang_length = 1
                        self.default_language = language_name
                if(language_name.split("_")[0] == default_ending): #default language hit and no other language has been set
                    if(current_lang_length == 0):
                        active_button = language_menu_button
                        self.default_language = language_name
            #language_name is a holder for the language name in the translation file tr_*.ts
            language_menu_button.setText(language_display_text)
            language_menu_button.setData(language_name)
            self.menuLanguage.addAction(language_menu_button)
            self.langActionGroup.addAction(language_menu_button)
        if(active_button!=None):
            active_button.setChecked(True)
            #print('There are no languages available in the system except english. Please check the language directory to ensure qm files exist')
        
        #Set up the event handling for each of the menu items
        self.connect(self.langActionGroup,QtCore.SIGNAL('triggered(QAction *)'), self.translateAction)
        
    def load_settings(self): 
        logging.info('Loading settings...')

        #load the config file
        self.core.config.readConfig()
        
        
        # Load Talks as a SQL Data Model
        #self.load_talks_db()
        self.load_event_list()
        self.load_date_list()

    def current_presentation(self):
        '''
        Creates a presentation object from the currently selected title on the GUI
        '''
        p_id = self.mainWidget.talkComboBox.model().index(0, 1).data(QtCore.Qt.DisplayRole).toString()
        return self.core.db.get_presentation(p_id)

    def capture(self, state):
        '''
        Function for recording and stopping recording.
        '''


        if (state): # Start Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/freeseer_logo_rec.png")
            sysIcon2 = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon2)

            self.core.record(self.current_presentation())    
            self.mainWidget.recordPushButton.setText(self.tr('Stop'))
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
            self.mainWidget.recordPushButton.setText(self.tr('Record'))
            self.mainWidget.audioSlider.setValue(0)
            self.statusBar().showMessage('ready')
            # for stop recording, we'll keep whatever window state
            # we have - hidden or showing
            

    ###
    ### Talk Related
    ###
    
    def load_date_list(self):
        model = self.core.db.get_dates_model()
        self.mainWidget.dateComboBox.setModel(model)
    
    def load_event_list(self):
        model = self.core.db.get_events_model()
        self.mainWidget.eventComboBox.setModel(model)

    def load_rooms_from_event(self, event):
        self.current_event = event

        model = self.core.db.get_rooms_model(self.current_event)
        self.mainWidget.roomComboBox.setModel(model)
        
    def load_talks_from_room(self, room):
        self.current_room = room
        self.current_date = str(self.mainWidget.dateComboBox.currentText())

        model = self.core.db.get_talks_model(self.current_event, self.current_room, self.current_date)
        self.mainWidget.talkComboBox.setModel(model)
        
    def load_talks_from_date(self, date):
        self.current_date = date
        
        model = self.core.db.get_talks_model(self.current_event, self.current_room, self.current_date)
        self.mainWidget.talkComboBox.setModel(model)

    ###
    ### Misc
    ###
    
#    def area_select(self):
#        self.area_selector = QtAreaSelector(self)
#        self.area_selector.show()
#        logging.info('Desktop area selector started.')
#        self.hide_window()
    
    def desktopAreaEvent(self, start_x, start_y, end_x, end_y):
        self.start_x = self.core.config.start_x = start_x
        self.start_y = self.core.config.start_y = start_y
        self.end_x = self.core.config.end_x = end_x
        self.end_y = self.core.config.end_y = end_y
        self.core.set_recording_area(self.start_x, self.start_y, self.end_x, self.end_y)
        logging.debug('area selector start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
        self.show_window()

    def _icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.hide_window() 
            
            
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.mainWidget.recordPushButton.toggle()

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
        if not self.mainWidget.recordPushButton.isChecked():
            self.mainWidget.recordPushButton.toggle()

    def stopContextM(self):
        if self.mainWidget.recordPushButton.isChecked():
            self.mainWidget.recordPushButton.toggle()

    def audio_feedback(self, value):
        self.mainWidget.audioSlider.setValue(value)
        
    def open_video_directory(self):
        if sys.platform.startswith("linux"):
            os.system("xdg-open %s" % self.core.config.videodir)
        else:
            logging.INFO("Error: This command is not supported on the current OS.")

    def closeEvent(self, event):
        logging.info('Exiting freeseer...')
        event.accept()
        
    def keyPressEvent(self, event):
        logging.debug("Keypressed: %s" % event.key())
        self.core.backend.keyboard_event(event.key())

    def translateAction(self ,action):
        '''
        When a language is selected from the language menu this function is called
        The language to be changed to is retrieved
        '''
        language_prefix = action.data().toString()
        self.translateFile(language_prefix)
      
    def translateFile(self,file_ending):
        '''
        Actually performs the translation. This is called by the handler for the language menu
        Note: If the language file can not be loaded then the default language is English 
        '''
        load_string = LANGUAGE_DIR+'tr_'+ file_ending #create language file path
        
        loaded = self.uiTranslator.load(load_string)

        if(loaded == True):
   
            #self.ui.retranslateUi(self) #Translate both the ui and the about page
            #self.aboutDialog.translate()
            pass
       
        else:
            print("Invalid Locale Resorting to Default Language: English")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())
