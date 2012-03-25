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
# http://wiki.github.com/Freeseer/freeseer/

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
from freeseer.frontend.qtcommon.Resource import resource_rc

from ReportEditorWidget import ReportEditorWidget

__version__ = project_info.VERSION
        
class ReportEditorApp(QtGui.QMainWindow):
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
        
        self.editorWidget = ReportEditorWidget()
        self.editorWidget.editor.setColumnHidden(5, True)
        self.aboutDialog = AboutDialog()
        
        self.mainLayout.addWidget(self.editorWidget)
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        # Only instantiate a new Core if we need to
        if core is not None:
            self.core = core
        else:
            self.core = FreeseerCore(self)
            
        self.config = self.core.get_config()
        
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
        
        exitIcon = QtGui.QIcon.fromTheme("application-exit")
        self.actionExit = QtGui.QAction(self)
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionExit.setIcon(exitIcon)
        
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAbout.setIcon(icon)
        
        self.actionExportCsv = QtGui.QAction(self)
        self.actionExportCsv.setObjectName(_fromUtf8("actionExportCsv"))
        
        # Actions
        self.menuFile.addAction(self.actionExportCsv)
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.menuLanguage.menuAction())
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        self.setupLanguageMenu()
        # --- End Menubar
        
        #
        # Report Editor Connections
        #
        
        # Editor Widget
        self.connect(self.editorWidget.removeButton, QtCore.SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.editorWidget.clearButton, QtCore.SIGNAL('clicked()'), self.confirm_reset)
        self.connect(self.editorWidget.closeButton, QtCore.SIGNAL('clicked()'), self.close)
        
        # Main Window Connections
        self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        self.connect(self.actionExportCsv, QtCore.SIGNAL('triggered()'), self.export_reports_to_csv)
        self.connect(self.editorWidget.editor, QtCore.SIGNAL('clicked (const QModelIndex&)'), self.editorSelectionChanged)

        # Load default language
        actions = self.menuLanguage.actions()
        for action in actions:
            if action.data().toString() == self.config.default_language:
                action.setChecked(True)
                self.translate(action)
                break
            
            
        self.load_failures_model()
        self.editorWidget.editor.resizeColumnsToContents()
        self.editorWidget.editor.resizeRowsToContents()

    ###
    ### Translation
    ###
    def retranslate(self):
        self.setWindowTitle(self.uiTranslator.translate("ReportEditorApp", "Freeseer Report Editor"))
        
        #
        # Reusable Strings
        #
        self.confirmDBClearTitleString = self.uiTranslator.translate("ReportEditorApp", "Clear Database")
        self.confirmDBClearQuestionString = self.uiTranslator.translate("ReportEditorApp", "Are you sure you want to clear the DB?")
        # --- End Reusable Strings
        
        #
        # Menubar
        #
        self.menuFile.setTitle(self.uiTranslator.translate("ReportEditorApp", "&File"))
        self.menuOptions.setTitle(self.uiTranslator.translate("ReportEditorApp", "&Options"))
        self.menuLanguage.setTitle(self.uiTranslator.translate("ReportEditorApp", "&Language"))
        self.menuHelp.setTitle(self.uiTranslator.translate("ReportEditorApp", "&Help"))
        self.actionExportCsv.setText(self.uiTranslator.translate("ReportEditorApp", "&Export to CSV"))
        self.actionExit.setText(self.uiTranslator.translate("ReportEditorApp", "&Quit"))
        self.actionAbout.setText(self.uiTranslator.translate("ReportEditorApp", "&About"))
        # --- End Menubar
        
        #
        # EditorWidget
        #
        self.editorWidget.removeButton.setText(self.uiTranslator.translate("ReportEditorApp", "Remove"))
        self.editorWidget.clearButton.setText(self.uiTranslator.translate("ReportEditorApp", "Clear"))
        self.editorWidget.closeButton.setText(self.uiTranslator.translate("ReportEditorApp", "Close"))
        
        self.editorWidget.titleLabel.setText(self.uiTranslator.translate("ReportEditorApp", "Title:"))
        self.editorWidget.speakerLabel.setText(self.uiTranslator.translate("ReportEditorApp", "Speaker:"))
        self.editorWidget.descriptionLabel.setText(self.uiTranslator.translate("ReportEditorApp", "Description:"))
        self.editorWidget.levelLabel.setText(self.uiTranslator.translate("ReportEditorApp", "Level:"))
        self.editorWidget.eventLabel.setText(self.uiTranslator.translate("ReportEditorApp", "Event:"))
        self.editorWidget.roomLabel.setText(self.uiTranslator.translate("ReportEditorApp", "Room:"))
        self.editorWidget.timeLabel.setText(self.uiTranslator.translate("ReportEditorApp", "Time:"))
        # --- End EditorWidget
        
        self.aboutDialog.retranslate(self.current_language)
    
    def translate(self , action):
        '''
        When a language is selected from the language menu this function is called
        The language to be changed to is retrieved
        '''

        self.current_language = str(action.data().toString()).strip("tr_").rstrip(".qm")
        
        logging.info("Switching language to: %s" % action.text())
        self.uiTranslator.load(":/languages/tr_%s.qm" % self.current_language)
        
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
        
    def load_failures_model(self):
        # Load Presentation Model
        self.failureModel = self.core.db.get_failures_model()
        editor = self.editorWidget.editor
        editor.setModel(self.failureModel)
        editor.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        
    
        
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

        self.failureModel.select()
        
        self.hide_add_talk_widget()

    def remove_talk(self):
        try:
            row_clicked = self.editorWidget.editor.currentIndex().row()
        except:
            return
        
        self.failureModel.removeRow(row_clicked)
        self.failureModel.select()
        
    def reset(self):
        self.core.db.clear_database()
        self.failureModel.select()
        
    def confirm_reset(self):
        """
        Presents a confirmation dialog to ask the user if they are sure they
        wish to remove the report database.
        
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

    def closeEvent(self, event):
        logging.info('Exiting report editor...')
        self.geometry = self.saveGeometry()
        event.accept()
    
    def editorSelectionChanged(self, index):
        talkId = self.failureModel.record(index.row()).value(0).toString()
        self.updatePresentationInfo(talkId)
        
    def updatePresentationInfo(self, talkId):
        p = self.core.db.get_presentation(talkId)
        self.editorWidget.titleLabel2.setText(p.title)
        self.editorWidget.speakerLabel2.setText(p.speaker)
        self.editorWidget.descriptionLabel2.setText(p.description)
        self.editorWidget.levelLabel2.setText(p.level)
        self.editorWidget.eventLabel2.setText(p.event)
        self.editorWidget.roomLabel2.setText(p.room)
        self.editorWidget.timeLabel2.setText(p.time)
        
    def export_reports_to_csv(self):
        fname = QtGui.QFileDialog.getSaveFileName(self,'Select file')
        if fname:
            self.core.export_reports_to_csv(fname)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = ReportEditorApp()
    main.show()
    sys.exit(app.exec_())
