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
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QHeaderView
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QWidget

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer.framework.presentation import Presentation
from freeseer.frontend.qtcommon.FreeseerApp import FreeseerApp

from ReportEditorWidget import ReportEditorWidget

log = logging.getLogger(__name__)


class ReportEditorApp(FreeseerApp):
    '''
    Freeseer report editor main gui class
    '''

    def __init__(self, config, db):
        FreeseerApp.__init__(self)

        self.config = config
        self.db = db

        icon = QIcon()
        icon.addPixmap(QPixmap(_fromUtf8(":/freeseer/logo.png")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(960, 400)

        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.editorWidget = ReportEditorWidget()
        self.editorWidget.editor.setColumnHidden(5, True)

        self.mainLayout.addWidget(self.editorWidget)

        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        #
        # Setup Menubar
        #
        self.actionExportCsv = QAction(self)
        self.actionExportCsv.setObjectName(_fromUtf8("actionExportCsv"))

        # Actions
        self.menuFile.insertAction(self.actionExit, self.actionExportCsv)
        # --- End Menubar

        #
        # Report Editor Connections
        #

        # Editor Widget
        self.connect(self.editorWidget.removeButton, SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.editorWidget.clearButton, SIGNAL('clicked()'), self.confirm_reset)
        self.connect(self.editorWidget.closeButton, SIGNAL('clicked()'), self.close)

        # Main Window Connections
        self.connect(self.actionExportCsv, SIGNAL('triggered()'), self.export_reports_to_csv)
        self.connect(self.editorWidget.editor, SIGNAL('clicked (const QModelIndex&)'), self.editorSelectionChanged)

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
        self.setWindowTitle(self.app.translate("ReportEditorApp", "Freeseer Report Editor"))

        #
        # Reusable Strings
        #
        self.confirmDBClearTitleString = self.app.translate("ReportEditorApp", "Clear Database")
        self.confirmDBClearQuestionString = self.app.translate("ReportEditorApp", "Are you sure you want to clear the DB?")
        self.selectFileString = self.app.translate("ReportEditorApp", "Select File")
        # --- End Reusable Strings

        #
        # Menubar
        #
        self.actionExportCsv.setText(self.app.translate("ReportEditorApp", "&Export to CSV"))
        # --- End Menubar

        #
        # EditorWidget
        #
        self.editorWidget.removeButton.setText(self.app.translate("ReportEditorApp", "Remove"))
        self.editorWidget.clearButton.setText(self.app.translate("ReportEditorApp", "Clear"))
        self.editorWidget.closeButton.setText(self.app.translate("ReportEditorApp", "Close"))

        self.editorWidget.titleLabel.setText(self.app.translate("ReportEditorApp", "Title:"))
        self.editorWidget.speakerLabel.setText(self.app.translate("ReportEditorApp", "Speaker:"))
        self.editorWidget.descriptionLabel.setText(self.app.translate("ReportEditorApp", "Description:"))
        self.editorWidget.levelLabel.setText(self.app.translate("ReportEditorApp", "Level:"))
        self.editorWidget.eventLabel.setText(self.app.translate("ReportEditorApp", "Event:"))
        self.editorWidget.roomLabel.setText(self.app.translate("ReportEditorApp", "Room:"))
        self.editorWidget.timeLabel.setText(self.app.translate("ReportEditorApp", "Time:"))
        # --- End EditorWidget

    def load_failures_model(self):
        # Load Presentation Model
        self.failureModel = self.db.get_failures_model()
        editor = self.editorWidget.editor
        editor.setModel(self.failureModel)
        editor.horizontalHeader().setResizeMode(QHeaderView.Stretch)

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
                                    unicode(datetime.toString()))

        # Do not add talks if they are empty strings
        if (len(presentation.title) == 0):
            return

        self.db.insert_presentation(presentation)

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
        self.db.clear_report_db()
        self.failureModel.select()

    def confirm_reset(self):
        """
        Presents a confirmation dialog to ask the user if they are sure they
        wish to remove the report database.

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

    def closeEvent(self, event):
        log.info('Exiting report editor...')
        self.geometry = self.saveGeometry()
        event.accept()

    def editorSelectionChanged(self, index):
        talkId = self.failureModel.record(index.row()).value(0).toString()
        self.updatePresentationInfo(talkId)

    def updatePresentationInfo(self, talkId):
        p = self.db.get_presentation(talkId)
        if p is not None:
            self.editorWidget.titleLabel2.setText(p.title)
            self.editorWidget.speakerLabel2.setText(p.speaker)
            self.editorWidget.descriptionLabel2.setText(p.description)
            self.editorWidget.levelLabel2.setText(p.level)
            self.editorWidget.eventLabel2.setText(p.event)
            self.editorWidget.roomLabel2.setText(p.room)
            self.editorWidget.timeLabel2.setText(p.time)
        else:
            self.editorWidget.titleLabel2.setText("Talk not found")
            self.editorWidget.speakerLabel2.setText("Talk not found")
            self.editorWidget.descriptionLabel2.setText("Talk not found")
            self.editorWidget.levelLabel2.setText("Talk not found")
            self.editorWidget.eventLabel2.setText("Talk not found")
            self.editorWidget.roomLabel2.setText("Talk not found")
            self.editorWidget.timeLabel2.setText("Talk not found")

    def export_reports_to_csv(self):
        fname = QFileDialog.getSaveFileName(self, self.selectFileString, "", "*.csv")
        if fname:
            self.db.export_reports_to_csv(fname)
