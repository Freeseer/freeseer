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
import os
import sys

from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer import project_info
from freeseer.framework.core import FreeseerCore
from freeseer.framework.presentation import Presentation
from freeseer.frontend.qtcommon.AboutDialog import AboutDialog

from EditorWidget import EditorWidget
from AddTalkWidget import AddTalkWidget

__version__ = project_info.VERSION

LANGUAGE_DIR = 'freeseer/frontend/talkeditor/languages/'

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
            files = os.listdir(LANGUAGE_DIR)
            files = map(lambda x: x.split('.') , files)
            qm_files = filter(lambda x:x[len(x) - 1] == 'qm', files)
            language_prefix = map(lambda x: x[0].split("tr_")[1], qm_files)
        except:
            return []
        return language_prefix
        
class TalkEditorMainApp(QtGui.QMainWindow):
    '''
    Freeseer talk database editor main gui class
    '''
    def __init__(self, core=None):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle(QtGui.QApplication.translate("TalkEditorMainWindow", 
                                                         "Freeseer Talk Editor", 
                                                         None, 
                                                         QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/freeseer_logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(960, 400)
        
        self.mainWidget = QtGui.QWidget()
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        
        self.editorWidget = EditorWidget()
        self.addTalkWidget = AddTalkWidget()
        self.aboutDialog = AboutDialog()
        
        self.mainLayout.addWidget(self.editorWidget)
        self.mainLayout.addWidget(self.addTalkWidget)
        
        #
        # Setup Menubar
        #
        self.menubar = QtGui.QMenuBar()
        self.setMenuBar(self.menubar)
        
        self.menubar.setGeometry(QtCore.QRect(0, 0, 884, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(QtGui.QApplication.translate("TalkEditorMainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setTitle(QtGui.QApplication.translate("TalkEditorMainWindow", "&Options", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menuLanguage = QtGui.QMenu(self.menuOptions)
        self.menuLanguage.setTitle(QtGui.QApplication.translate("TalkEditorMainWindow", "&Language", None, QtGui.QApplication.UnicodeUTF8))
        self.menuLanguage.setObjectName(_fromUtf8("menuLanguage"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setTitle(QtGui.QApplication.translate("TalkEditorMainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        
        self.actionExit = QtGui.QAction(self)
        self.actionExit.setText(QtGui.QApplication.translate("TalkEditorMainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("TalkEditorMainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setText(QtGui.QApplication.translate("TalkEditorMainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        
        # Actions
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.menuLanguage.menuAction())
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())    
        # --- End Menubar
        
        self.editorWidget.editor.setColumnHidden(5, True)
        self.default_language = 'en'
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        # Only instantiate a new Core if we need to
        if core is not None:
            self.core = core
        else:
            self.core = FreeseerCore(self)
        
        #Setup the translator and populate the language menu under options
        self.uiTranslator = QtCore.QTranslator()
        self.langActionGroup = QtGui.QActionGroup(self)
        QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'))
        self.setupLanguageMenu()

        #
        # Talk Editor Connections
        #
        # Add Talk Widget
        self.connect(self.addTalkWidget.addButton, QtCore.SIGNAL('clicked()'), self.add_talk)
        self.connect(self.addTalkWidget.cancelButton, QtCore.SIGNAL('clicked()'), self.hide_add_talk_widget)
        self.addTalkWidget.setHidden(True)
        
        # Editor Widget
        self.connect(self.editorWidget.rssPushButton, QtCore.SIGNAL('clicked()'), self.add_talks_from_rss)
        self.connect(self.editorWidget.addButton, QtCore.SIGNAL('clicked()'), self.show_add_talk_widget)
        self.connect(self.editorWidget.removeButton, QtCore.SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.editorWidget.clearButton, QtCore.SIGNAL('clicked()'), self.confirm_reset)
        self.connect(self.editorWidget.closeButton, QtCore.SIGNAL('clicked()'), self.close)
        
        # Main Window Connections
        self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        
        self.load_presentations_model()

    # TODO fix this
    def setupLanguageMenu(self):

        #Add Languages to the Menu Ensure only one is clicked 
        self.langActionGroup.setExclusive(True)
        system_ending = QtCore.QLocale.system().name()  #Retrieve Current Locale from the operating system         
        active_button = None        #the current active menu item (menu item for default language)
        current_lang_length = 0     #Used to determine the length of prefix that match for the current default language
        default_ending = self.default_language
        '''
        Current Lang Length
        0 -  No Common Prefix
        1 -  Common Language 
        2 -  Common Language and Country
        '''
        language_table = SystemLanguages()      #Load all languages from the language folder 
             
    
        for language_name in language_table.languages:
            translator = QtCore.QTranslator()   #Create a translator to translate names
            data = translator.load(LANGUAGE_DIR+'tr_'+language_name)
            #Create the button
            if(data == False):    
                continue
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
        
    def load_presentations_model(self):
        # Load Presentation Model
        self.presentationModel = self.core.db.get_presentations_model()
        self.editorWidget.editor.setModel(self.presentationModel)
    
    def show_add_talk_widget(self):
        self.editorWidget.setHidden(True)
        self.addTalkWidget.setHidden(False)
        
    def hide_add_talk_widget(self):
        self.editorWidget.setHidden(False)
        self.addTalkWidget.setHidden(True)
    
    def add_talk(self):
        date = self.addTalkWidget.dateEdit.date()
        time = self.addTalkWidget.timeEdit.time()
        datetime = QtCore.QDateTime(date, time)
        presentation = Presentation(unicode(self.addTalkWidget.titleLineEdit.text()),
                                    unicode(self.addTalkWidget.presenterLineEdit.text()),
                                    "", # description
                                    "", # level
                                    unicode(self.addTalkWidget.eventLineEdit.text()),
                                    unicode(self.addTalkWidget.roomLineEdit.text()),
                                    unicode(datetime.toString()))
        
        # Do not add talks if they are empty strings
        if (len(presentation.title) == 0): return

        self.core.db.insert_presentation(presentation)

        # cleanup
        self.addTalkWidget.titleLineEdit.clear()
        self.addTalkWidget.presenterLineEdit.clear()

        self.presentationModel.select()
        
        self.hide_add_talk_widget()

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
        
    def confirm_reset(self):
        """
        Presents a confirmation dialog to ask the user if they are sure they
        wish to remove the talk database.
        
        If Yes call the reset() function.
        """
        confirm = QtGui.QMessageBox.question(self,
                    "Clear Database",
                    "Are you sure you want to clear the DB?",
                    QtGui.QMessageBox.Yes | 
                    QtGui.QMessageBox.No,
                    QtGui.QMessageBox.No)
        
        if confirm == QtGui.QMessageBox.Yes:
            self.reset()
            
    def add_talks_from_rss(self):
        rss_url = unicode(self.editorWidget.rssLineEdit.text())
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

        language_prefix = action.data().toString()  
        self.translateFile(language_prefix)
      
    def translateFile(self, file_ending):
        '''
    	Actually perfoms the translation. This is called by the handler for the language menu
    	Note: If the language file can not be loaded then the default language is english 
    	'''
        load_string = LANGUAGE_DIR + 'tr_' + file_ending        #create language file path
        loaded = self.uiTranslator.load(load_string)

        if(loaded == True):
            #self.ui.retranslateUi(self)    #Translate both the ui and the about page
            pass
        else:
            print("Invalid Locale Resorting to Default Language: English")
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = TalkEditorMainApp()
    main.show()
    sys.exit(app.exec_())
