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

from PyQt4 import QtGui, QtCore, QtSql

from freeseer import project_info
from freeseer.framework.presentation import *
from freeseer.framework.core import *
from freeseer.framework.freeseer_about import *

from talkeditor_ui_qt import *

__version__ = project_info.VERSION

NAME = project_info.NAME
URL = project_info.URL
LANGUAGE_DIR = 'freeseer/frontend/talkeditor/languages/'


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

        DESCRIPTION = self.tr('AboutDialog', 'Freeseer Talk Database Editor is a  database utility capable of editing the presentation database. It allows users to add, remove and edit all the data fields of a presentation, and download a list of presentations from a RSS feed.')
        COPYRIGHT = self.tr('Copyright (C) 2011 The Free and Open Source Software Learning Centre')
        LICENSE_TEXT = self.tr("Freeseer Talk Database Editor is licensed under the GPL version 3. This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software.")

        ABOUT_INFO = u'<h1>' + NAME + u'</h1>' + \
        u'<br><b>' + self.tr("Version") + ":" + __version__ + u'</b>' + \
        u'<p>' + DESCRIPTION + u'</p>' + \
        u'<p>' + COPYRIGHT + u'</p>' + \
        u'<p><a href="' + URL + u'">' + URL + u'</a></p>' \
        u'<p>' + LICENSE_TEXT + u'</p>'
 
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
            qm_files = filter(lambda x:x[len(x) - 1] == 'qm', files);
            language_prefix = map(lambda x: x[0].split("tr_")[1], qm_files);
        except:
            return [];
        return language_prefix;
        
class TalkEditorMainApp(QtGui.QMainWindow):
    '''
    Freeseer talk database editor main gui class
    '''
    def __init__(self, core=None):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_TalkEditorMainWindow()
        self.ui.setupUi(self)
        self.aboutDialog = AboutDialog()    
        self.ui.editTable.setColumnHidden(5, True)
        self.default_language = 'en';
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        # Only instantiate a new Core if we need to
        if core is not None:
            self.core = core
        else:
            self.core = FreeseerCore(self)
        
        #Setup the translator and populate the language menu under options
        self.uiTranslator = QtCore.QTranslator();
        self.langActionGroup = QtGui.QActionGroup(self);
        QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'));
        self.setupLanguageMenu();

        #self.load_talks()
        
        # edit talks connections
        self.connect(self.ui.confirmAddTalkButton, QtCore.SIGNAL('clicked()'), self.add_talk)
        self.connect(self.ui.rssButton, QtCore.SIGNAL('clicked()'), self.add_talks_from_rss)
        self.connect(self.ui.removeTalkButton, QtCore.SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.ui.resetButton, QtCore.SIGNAL('clicked()'), self.reset)
        self.ui.addTalkGroupBox.setHidden(True)
        
        # Main Window Connections
        self.connect(self.ui.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        
        self.load_presentations_model()

    # TODO fix this
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
        
    def load_presentations_model(self):
        # Load Presentation Model
        self.presentationModel = self.core.db.get_presentations_model()
        self.ui.editTable.setModel(self.presentationModel)
    
    def add_talk(self):
        presentation = Presentation(str(self.ui.titleEdit.text()),
                                    str(self.ui.presenterEdit.text()),
                                    "", # description
                                    "", # level
                                    str(self.ui.eventEdit.text()),
                                    str(self.ui.dateTimeEdit.text()),
                                    str(self.ui.roomEdit.text()))
                
        # Do not add talks if they are empty strings
        if (len(presentation.title) == 0): return
        
        self.core.db.insert_presentation(presentation)

        # cleanup
        self.ui.titleEdit.clear()
        self.ui.presenterEdit.clear()
        self.ui.eventEdit.clear()
        self.ui.dateTimeEdit.clear()
        self.ui.roomEdit.clear()
        self.ui.checkBox.setChecked(False)
        self.ui.checkBox_2.setChecked(False)
        self.ui.checkBox_3.setChecked(False)
        self.ui.checkBox_4.setChecked(False)

        self.presentationModel.select()

    def remove_talk(self):
        try:
            row_clicked = self.ui.editTable.currentIndex().row()
        except:
            return
        
        self.presentationModel.removeRow(row_clicked)
        self.presentationModel.select()

    def reset(self):
        self.core.db.clear_database()
        self.presentationModel.select()
            
    def add_talks_from_rss(self):
        rss_url = str(self.ui.rssEdit.text())
        self.core.add_talks_from_rss(rss_url)
        self.presentationModel.select()

    def closeEvent(self, event):
        logging.info('Exiting talk database editor...')
        self.geometry = self.saveGeometry()
        event.accept()
    
    def translateAction(self , action):
        '''
    	When a language is selected from the language menu this function is called
    	The language to be changed to is retrieved
    	'''

        language_prefix = action.data().toString();  
        self.translateFile(language_prefix);
      
    def translateFile(self, file_ending):
        '''
    	Actually perfoms the translation. This is called by the handler for the language menu
    	Note: If the language file can not be loaded then the default language is english 
    	'''
        load_string = LANGUAGE_DIR + 'tr_' + file_ending; #create language file path
        loaded = self.uiTranslator.load(load_string);

        if(loaded == True):
            self.ui.retranslateUi(self); #Translate both the ui and the about page
        else:
            print("Invalid Locale Resorting to Default Language: English");
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = TalkEditorMainApp()
    main.show();
    sys.exit(app.exec_())
