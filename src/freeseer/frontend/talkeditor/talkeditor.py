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
        
class TalkEditorApp(QtGui.QMainWindow):
    '''
    Freeseer talk database editor main gui class
    '''
    def __init__(self, core=None):
        QtGui.QMainWindow.__init__(self)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        # Translator
        #
        self.current_language = None
        self.uiTranslator = QtCore.QTranslator()
        self.uiTranslator.load(":/languages/tr_en_US.qm")
        self.langActionGroup = QtGui.QActionGroup(self)
        QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'))
        self.connect(self.langActionGroup, QtCore.SIGNAL('triggered(QAction *)'), self.translate)
        # --- End Translator
        
        #
        # Setup Menubar
        #
        self.menubar = QtGui.QMenuBar()
        self.setMenuBar(self.menubar)
        
        self.menubar.setGeometry(QtCore.QRect(0, 0, 884, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menuLanguage = QtGui.QMenu(self.menuOptions)
        self.menuLanguage.setObjectName(_fromUtf8("menuLanguage"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        
        self.actionExit = QtGui.QAction(self)
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        
        # Actions
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.menuLanguage.menuAction())
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        self.setupLanguageMenu()
        # --- End Menubar
        
        self.editorWidget.editor.setColumnHidden(5, True)
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        # Only instantiate a new Core if we need to
        if core is not None:
            self.core = core
        else:
            self.core = FreeseerCore(self)

        #
        # Talk Editor Connections
        #
        # Add Talk Widget
        self.connect(self.addTalkWidget.addButton, QtCore.SIGNAL('clicked()'), self.add_talk)
        self.connect(self.addTalkWidget.cancelButton, QtCore.SIGNAL('clicked()'), self.hide_add_talk_widget)
        self.addTalkWidget.setHidden(True)
        
        # Editor Widget
        self.connect(self.editorWidget.rssLineEdit, QtCore.SIGNAL('returnPressed()'), self.editorWidget.rssPushButton.click)
        self.connect(self.editorWidget.rssPushButton, QtCore.SIGNAL('clicked()'), self.add_talks_from_rss)
        self.connect(self.editorWidget.addButton, QtCore.SIGNAL('clicked()'), self.show_add_talk_widget)
        self.connect(self.editorWidget.removeButton, QtCore.SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.editorWidget.clearButton, QtCore.SIGNAL('clicked()'), self.confirm_reset)
        self.connect(self.editorWidget.closeButton, QtCore.SIGNAL('clicked()'), self.close)
        
        # Main Window Connections
        self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        
        self.load_presentations_model()
        
        self.retranslate()

    ###
    ### Translation
    ###
    def retranslate(self):
        self.setWindowTitle(self.uiTranslator.translate("TalkEditorApp", "Freeseer Talk Editor"))
        
        #
        # Reusable Strings
        #
        self.confirmDBClearTitleString = self.uiTranslator.translate("TalkEditorApp", "Clear Database")
        self.confirmDBClearQuestionString = self.uiTranslator.translate("TalkEditorApp", "Are you sure you want to clear the DB?")
        # --- End Reusable Strings
        
        #
        # Menubar
        #
        self.menuFile.setTitle(self.uiTranslator.translate("TalkEditorApp", "&File"))
        self.menuOptions.setTitle(self.uiTranslator.translate("TalkEditorApp", "&Options"))
        self.menuLanguage.setTitle(self.uiTranslator.translate("TalkEditorApp", "&Language"))
        self.menuHelp.setTitle(self.uiTranslator.translate("TalkEditorApp", "&Help"))
        self.actionExit.setText(self.uiTranslator.translate("TalkEditorApp", "&Quit"))
        self.actionAbout.setText(self.uiTranslator.translate("TalkEditorApp", "&About"))
        # --- End Menubar
        
        #
        # AddTalkWidget
        #
        self.addTalkWidget.addTalkGroupBox.setTitle(self.uiTranslator.translate("TalkEditorApp", "Add Talk"))
        self.addTalkWidget.titleLabel.setText(self.uiTranslator.translate("TalkEditorApp", "Title"))
        self.addTalkWidget.presenterLabel.setText(self.uiTranslator.translate("TalkEditorApp", "Presenter"))
        self.addTalkWidget.eventLabel.setText(self.uiTranslator.translate("TalkEditorApp", "Event"))
        self.addTalkWidget.roomLabel.setText(self.uiTranslator.translate("TalkEditorApp", "Room"))
        self.addTalkWidget.dateLabel.setText(self.uiTranslator.translate("TalkEditorApp", "Date"))
        self.addTalkWidget.timeLabel.setText(self.uiTranslator.translate("TalkEditorApp", "Time"))
        self.addTalkWidget.addButton.setText(self.uiTranslator.translate("TalkEditorApp", "Add"))
        self.addTalkWidget.cancelButton.setText(self.uiTranslator.translate("TalkEditorApp", "Cancel"))
        # --- End AddTalkWidget
        
        #
        # EditorWidget
        #
        self.editorWidget.rssLabel.setText(self.uiTranslator.translate("TalkEditorApp", "URL"))
        self.editorWidget.rssPushButton.setText(self.uiTranslator.translate("TalkEditorApp", "Load talks from RSS"))
        self.editorWidget.addButton.setText(self.uiTranslator.translate("TalkEditorApp", "Add"))
        self.editorWidget.removeButton.setText(self.uiTranslator.translate("TalkEditorApp", "Remove"))
        self.editorWidget.clearButton.setText(self.uiTranslator.translate("TalkEditorApp", "Clear"))
        self.editorWidget.closeButton.setText(self.uiTranslator.translate("TalkEditorApp", "Close"))
        # --- End EditorWidget
        
        self.aboutDialog.retranslate()
    
    def translate(self , action):
        '''
        When a language is selected from the language menu this function is called
        The language to be changed to is retrieved
        '''

        language = action.data().toString()
        
        logging.info("Switching language to: %s" % action.text())
        self.uiTranslator.load(":/languages/%s" % language)
        
        self.retranslate()
    
    def setupLanguageMenu(self):
        languages = QtCore.QDir(":/languages").entryList()
        
        if self.current_language is None:
            self.current_language = QtCore.QLocale.system().name()    #Retrieve Current Locale from the operating system
            logging.debug("Detected user's locale as %s" % self.current_language)
        
        for language in languages:
            translator = QtCore.QTranslator()   #Create a translator to translate Language Display Text
            translator.load(":/languages/%s" % language)
            language_display_text = translator.translate("Translation", "Language Display Text")
            
            languageAction = QtGui.QAction(self)
            languageAction.setCheckable(True)
            languageAction.setText(language_display_text)
            languageAction.setData(language)
            self.menuLanguage.addAction(languageAction)
            self.langActionGroup.addAction(languageAction)
            
            if self.current_language == str(language).strip("tr_").rstrip(".qm"):
                languageAction.setChecked(True)
        
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
                    self.confirmDBClearTitleString,
                    self.confirmDBClearQuestionString,
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

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = TalkEditorApp()
    main.show()
    sys.exit(app.exec_())
