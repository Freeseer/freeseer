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
from freeseer.frontend.qtcommon.FreeseerApp import FreeseerApp
from freeseer.frontend.qtcommon.Resource import resource_rc

from EditorWidget import EditorWidget
from AddTalkWidget import AddTalkWidget

__version__ = project_info.VERSION
        
class TalkEditorApp(FreeseerApp):
    '''
    Freeseer talk database editor main gui class
    '''
    def __init__(self, core=None):
        FreeseerApp.__init__(self)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(960, 400)
        
        self.mainWidget = QtGui.QWidget()
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        
        self.editorWidget = EditorWidget()
        self.editorWidget.editor.setColumnHidden(5, True)
        self.addTalkWidget = AddTalkWidget()
        
        self.mainLayout.addWidget(self.editorWidget)
        self.mainLayout.addWidget(self.addTalkWidget)
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        # Only instantiate a new Core if we need to
        if core is not None:
            self.core = core
        else:
            self.core = FreeseerCore(self)
            
        self.config = self.core.get_config()
        
        #
        # Setup Menubar
        #
        self.actionExportCsv = QtGui.QAction(self)
        self.actionExportCsv.setObjectName(_fromUtf8("actionExportCsv"))
        
        # Actions
        self.menuFile.insertAction(self.actionExit, self.actionExportCsv)
        # --- End Menubar
        
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
        
        # CSV Widget
        self.connect(self.editorWidget.csvFileSelectButton, QtCore.SIGNAL('clicked()'), self.csv_file_select)
        self.connect(self.editorWidget.csvPushButton, QtCore.SIGNAL('clicked()'), self.add_talks_from_csv)
        self.connect(self.actionExportCsv, QtCore.SIGNAL('triggered()'), self.export_talks_to_csv)

        # Load default language
        actions = self.menuLanguage.actions()
        for action in actions:
            if action.data().toString() == self.config.default_language:
                action.setChecked(True)
                self.translate(action)
                break
        self.load_presentations_model()

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
        self.editorWidget.csvLabel.setText(self.uiTranslator.translate("TalkEditorApp", "File"))
        self.editorWidget.csvPushButton.setText(self.uiTranslator.translate("TalkEditorApp", "Load talks from CSV"))
        self.editorWidget.addButton.setText(self.uiTranslator.translate("TalkEditorApp", "Add"))
        self.editorWidget.removeButton.setText(self.uiTranslator.translate("TalkEditorApp", "Remove"))
        self.editorWidget.clearButton.setText(self.uiTranslator.translate("TalkEditorApp", "Clear"))
        self.editorWidget.closeButton.setText(self.uiTranslator.translate("TalkEditorApp", "Close"))
        # --- End EditorWidget
    
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
            row_clicked = self.editorWidget.editor.currentIndex().row()
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
    
    def csv_file_select(self):
        dirpath = str(self.editorWidget.csvLineEdit.text())
        fname = QtGui.QFileDialog.getOpenFileName(self,'Select file',
                                dirpath[0:dirpath.rfind(os.path.sep)])
        if fname:
            self.editorWidget.csvLineEdit.setText(fname)    
    
    def add_talks_from_csv(self):
        fname = self.editorWidget.csvLineEdit.text()
        
        if fname:
            self.core.add_talks_from_csv(fname)
            self.presentationModel.select()
    
    def export_talks_to_csv(self):
        dirpath = str(self.editorWidget.csvLineEdit.text())
        fname = QtGui.QFileDialog.getSaveFileName(self,'Select file',
                                dirpath[0:dirpath.rfind(os.path.sep)])
        if fname:
            self.core.export_talks_to_csv(fname)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = TalkEditorApp()
    main.show()
    sys.exit(app.exec_())
