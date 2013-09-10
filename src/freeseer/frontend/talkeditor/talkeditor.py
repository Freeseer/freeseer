#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2013  Free and Open Source Software Learning Centre
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

from PyQt4.QtCore import QDateTime
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QWidget

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


from freeseer import settings
from freeseer.framework.config import Config
from freeseer.framework.database import QtDBConnector
from freeseer.framework.presentation import Presentation
from freeseer.frontend.qtcommon.FreeseerApp import FreeseerApp
from freeseer.frontend.qtcommon.Resource import resource_rc

from EditorWidget import EditorWidget
from AddTalkWidget import AddTalkWidget

log = logging.getLogger(__name__)


class TalkEditorApp(FreeseerApp):
    '''
    Freeseer talk database editor main gui class
    '''
    def __init__(self, recordapp=None):
        FreeseerApp.__init__(self)

        self.recordapp = recordapp

        icon = QIcon()
        icon.addPixmap(QPixmap(_fromUtf8(":/freeseer/logo.png")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(960, 400)

        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.editorWidget = EditorWidget()
        self.editorWidget.editor.setColumnHidden(5, True)
        self.addTalkWidget = AddTalkWidget()

        self.mainLayout.addWidget(self.editorWidget)
        self.mainLayout.addWidget(self.addTalkWidget)

        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        self.config = Config(settings.configdir)
        self.db = QtDBConnector(settings.configdir)

        #
        # Setup Menubar
        #
        self.actionExportCsv = QAction(self)
        self.actionExportCsv.setObjectName(_fromUtf8("actionExportCsv"))

        # Actions
        self.menuFile.insertAction(self.actionExit, self.actionExportCsv)
        # --- End Menubar

        #
        # Talk Editor Connections
        #
        # Add Talk Widget
        self.connect(self.addTalkWidget.addButton, SIGNAL('clicked()'), self.add_talk)
        self.connect(self.addTalkWidget.cancelButton, SIGNAL('clicked()'), self.hide_add_talk_widget)
        self.addTalkWidget.setHidden(True)

        # Editor Widget
        self.connect(self.editorWidget.rssLineEdit, SIGNAL('returnPressed()'), self.editorWidget.rssPushButton.click)
        self.connect(self.editorWidget.rssPushButton, SIGNAL('clicked()'), self.add_talks_from_rss)
        self.connect(self.editorWidget.addButton, SIGNAL('clicked()'), self.show_add_talk_widget)
        self.connect(self.editorWidget.removeButton, SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.editorWidget.clearButton, SIGNAL('clicked()'), self.confirm_reset)
        self.connect(self.editorWidget.closeButton, SIGNAL('clicked()'), self.close)

        # CSV Widget
        self.connect(self.editorWidget.csvLineEdit, SIGNAL('returnPressed()'), self.editorWidget.csvPushButton.click)
        self.connect(self.editorWidget.csvFileSelectButton, SIGNAL('clicked()'), self.csv_file_select)
        self.connect(self.editorWidget.csvPushButton, SIGNAL('clicked()'), self.add_talks_from_csv)
        self.connect(self.actionExportCsv, SIGNAL('triggered()'), self.export_talks_to_csv)

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
        self.setWindowTitle(self.app.translate("TalkEditorApp", "Freeseer Talk Editor"))

        #
        # Reusable Strings
        #
        self.confirmDBClearTitleString = self.app.translate("TalkEditorApp", "Clear Database")
        self.confirmDBClearQuestionString = self.app.translate("TalkEditorApp", "Are you sure you want to clear the DB?")
        # --- End Reusable Strings

        #
        # Menubar
        #
        self.actionExportCsv.setText(self.app.translate("TalkEditorApp", "&Export to CSV"))
        # --- End Menubar

        #
        # AddTalkWidget
        #
        self.addTalkWidget.addTalkGroupBox.setTitle(self.app.translate("TalkEditorApp", "Add Talk"))
        self.addTalkWidget.titleLabel.setText(self.app.translate("TalkEditorApp", "Title"))
        self.addTalkWidget.presenterLabel.setText(self.app.translate("TalkEditorApp", "Presenter"))
        self.addTalkWidget.eventLabel.setText(self.app.translate("TalkEditorApp", "Event"))
        self.addTalkWidget.roomLabel.setText(self.app.translate("TalkEditorApp", "Room"))
        self.addTalkWidget.dateLabel.setText(self.app.translate("TalkEditorApp", "Date"))
        self.addTalkWidget.timeLabel.setText(self.app.translate("TalkEditorApp", "Time"))
        self.addTalkWidget.addButton.setText(self.app.translate("TalkEditorApp", "Add"))
        self.addTalkWidget.cancelButton.setText(self.app.translate("TalkEditorApp", "Cancel"))
        # --- End AddTalkWidget

        #
        # EditorWidget
        #
        self.editorWidget.rssLabel.setText(self.app.translate("TalkEditorApp", "URL"))
        self.editorWidget.rssPushButton.setText(self.app.translate("TalkEditorApp", "Load talks from RSS"))
        self.editorWidget.csvLabel.setText(self.app.translate("TalkEditorApp", "File"))
        self.editorWidget.csvPushButton.setText(self.app.translate("TalkEditorApp", "Load talks from CSV"))
        self.editorWidget.addButton.setText(self.app.translate("TalkEditorApp", "Add"))
        self.editorWidget.removeButton.setText(self.app.translate("TalkEditorApp", "Remove"))
        self.editorWidget.clearButton.setText(self.app.translate("TalkEditorApp", "Clear"))
        self.editorWidget.closeButton.setText(self.app.translate("TalkEditorApp", "Close"))
        # --- End EditorWidget

    def load_presentations_model(self):
        # Load Presentation Model
        self.presentationModel = self.db.get_presentations_model()
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
        datetime = QDateTime(date, time)
        presentation = Presentation(unicode(self.addTalkWidget.titleLineEdit.text()),
                                    unicode(self.addTalkWidget.presenterLineEdit.text()),
                                    "",  # description
                                    "",  # level
                                    unicode(self.addTalkWidget.eventLineEdit.text()),
                                    unicode(self.addTalkWidget.roomLineEdit.text()),
                                    unicode(datetime.toString(Qt.ISODate)))

        # Do not add talks if they are empty strings
        if (len(presentation.title) == 0):
            return

        self.db.insert_presentation(presentation)

        # cleanup
        self.addTalkWidget.titleLineEdit.clear()
        self.addTalkWidget.presenterLineEdit.clear()

        self.presentationModel.select()

        self.hide_add_talk_widget()

        # If this is launched from the recording app
        # refresh the talk list
        if self.recordapp:
            self.recordapp.load_event_list()

    def remove_talk(self):
        try:
            row_clicked = self.editorWidget.editor.currentIndex().row()
        except:
            return

        self.presentationModel.removeRow(row_clicked)
        self.presentationModel.select()

    def reset(self):
        self.db.clear_database()
        self.presentationModel.select()

    def confirm_reset(self):
        """
        Presents a confirmation dialog to ask the user if they are sure they
        wish to remove the talk database.

        If Yes call the reset() function.
        """
        confirm = QMessageBox.question(self,
                    self.confirmDBClearTitleString,
                    self.confirmDBClearQuestionString,
                    QMessageBox.Yes |
                    QMessageBox.No,
                    QMessageBox.No)

        if confirm == QMessageBox.Yes:
            self.reset()

    def add_talks_from_rss(self):
        rss_url = unicode(self.editorWidget.rssLineEdit.text())
        self.db.add_talks_from_rss(rss_url)
        self.presentationModel.select()

    def closeEvent(self, event):
        log.info('Exiting talk database editor...')
        self.geometry = self.saveGeometry()
        event.accept()

    def csv_file_select(self):
        dirpath = str(self.editorWidget.csvLineEdit.text())
        fname = QFileDialog.getOpenFileName(self, 'Select file', "", "*.csv")
        if fname:
            self.editorWidget.csvLineEdit.setText(fname)

    def add_talks_from_csv(self):
        fname = self.editorWidget.csvLineEdit.text()

        if fname:
            self.db.add_talks_from_csv(fname)
            self.presentationModel.select()

    def export_talks_to_csv(self):
        dirpath = str(self.editorWidget.csvLineEdit.text())
        fname = QFileDialog.getSaveFileName(self, 'Select file', "", "*.csv")
        if fname:
            self.db.export_talks_to_csv(fname)
