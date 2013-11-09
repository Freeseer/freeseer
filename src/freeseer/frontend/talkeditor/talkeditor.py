#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011-2013  Free and Open Source Software Learning Centre
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

# python-libs
import logging
import sys

# PyQt modules
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QDataWidgetMapper
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTableView
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QItemSelectionModel

# Freeseer modules
from freeseer import settings, __version__
from freeseer.framework.config import Config
from freeseer.framework.database import QtDBConnector
from freeseer.framework.presentation import Presentation
from freeseer.frontend.qtcommon.FreeseerApp import FreeseerApp
from freeseer.frontend.qtcommon.Resource import resource_rc

# TalkEditor modules
from CommandButtons import CommandButtons
from TalkDetailsWidget import TalkDetailsWidget
from ImportTalksWidget import ImportTalksWidget
from AddTalkWidget import AddTalkWidget

log = logging.getLogger(__name__)


class TalkEditorApp(FreeseerApp):

    '''
    Freeseer talk database editor main gui class
    '''

    def __init__(self, backButton=False):
        FreeseerApp.__init__(self)

        icon = QIcon()
        icon.addPixmap(QPixmap(':/freeseer/logo.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(960, 600)

        #
        # Setup Layout
        #
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)

        # Add the Title Row (Use BOLD / Big Font)
        self.titleLayout = QHBoxLayout()
        self.talkEditorLabel = QLabel('Talk Editor')
        font = QFont('Helvetica', 24, QFont.Bold)
        self.talkEditorLabel.setFont(font)
        self.titleLayout.addWidget(self.talkEditorLabel)
        self.backButton = QPushButton('Back to Recorder')
        if backButton:  # Only show the back button if requested by caller
            self.titleLayout.addWidget(self.backButton)
        self.titleLayout.addStretch()

        # Add custom widgets
        self.commandButtons = CommandButtons()
        self.tableView = QTableView()
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.talkDetailsWidget = TalkDetailsWidget()
        self.importTalksWidget = ImportTalksWidget()
        self.mainLayout.addWidget(self.importTalksWidget)
        self.mainLayout.addLayout(self.titleLayout)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addWidget(self.commandButtons)
        self.mainLayout.addWidget(self.tableView)
        self.mainLayout.addWidget(self.talkDetailsWidget)
        self.mainLayout.addWidget(self.importTalksWidget)
        # --- End Layout

        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        # Load backends
        self.config = Config(settings.configdir)
        self.db = QtDBConnector(settings.configdir)

        #
        # Setup Menubar
        #
        self.actionExportCsv = QAction(self)
        self.actionExportCsv.setObjectName('actionExportCsv')
        self.actionRemoveAll = QAction(self)
        self.actionRemoveAll.setObjectName('actionRemoveAll')

        # Actions
        self.menuFile.insertAction(self.actionExit, self.actionExportCsv)
        self.menuFile.insertAction(self.actionExit, self.actionRemoveAll)
        # --- End Menubar

        #
        # TableView Connections
        #
        self.connect(self.tableView, SIGNAL(
            'activated(const QModelIndex)'), self.talk_selected)
        self.connect(self.tableView, SIGNAL(
            'selected(const QModelIndex)'), self.talk_selected)
        self.connect(self.tableView, SIGNAL(
            'clicked(const QModelIndex)'), self.talk_selected)

        # Import Widget
        self.connect(self.importTalksWidget.csvRadioButton,
                     SIGNAL('toggled(bool)'), self.toggle_import)
        self.connect(self.importTalksWidget.importButton,
                     SIGNAL('clicked()'), self.import_talks)
        self.connect(self.importTalksWidget.cancelButton,
                     SIGNAL('clicked()'), self.hide_import_talks_widget)
        self.importTalksWidget.setHidden(True)
        self.connect(self.importTalksWidget.csvFileSelectButton,
                     QtCore.SIGNAL('clicked()'), self.csv_file_select)
        self.connect(self.importTalksWidget.csvLineEdit, QtCore.SIGNAL(
            'returnPressed()'), self.importTalksWidget.importButton.click)
        self.connect(self.importTalksWidget.rssLineEdit, QtCore.SIGNAL(
            'returnPressed()'), self.importTalksWidget.importButton.click)
        self.connect(self.actionExportCsv, QtCore.SIGNAL(
            'triggered()'), self.export_talks_to_csv)
        self.connect(self.actionRemoveAll, QtCore.SIGNAL(
            'triggered()'), self.confirm_reset)

        # Command Buttons
        self.connect(self.commandButtons.addButton,
                     SIGNAL('clicked()'), self.add_talk)
        self.connect(self.commandButtons.removeButton,
                     SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.commandButtons.removeAllButton,
                     SIGNAL('clicked()'), self.confirm_reset)
        self.connect(self.commandButtons.importButton,
                     SIGNAL('clicked()'), self.show_import_talks_widget)
        self.connect(self.commandButtons.exportButton,
                     SIGNAL('clicked()'), self.export_talks_to_csv)

        # Load default language
        actions = self.menuLanguage.actions()
        for action in actions:
            if action.data().toString() == self.config.default_language:
                action.setChecked(True)
                self.translate(action)
                break

        # Load Talk Database
        self.load_presentations_model()

    #
    # Translation
    #
    def retranslate(self):
        self.setWindowTitle(
            self.app.translate("TalkEditorApp", "Freeseer Talk Editor"))

        #
        # Reusable Strings
        #
        self.confirmDBClearTitleString = self.app.translate(
            "TalkEditorApp", "Remove All Talks from Database")
        self.confirmDBClearQuestionString = self.app.translate(
            "TalkEditorApp", "Are you sure you want to clear the DB?")
        # --- End Reusable Strings

        #
        # Menubar
        #
        self.actionExportCsv.setText(
            self.app.translate("TalkEditorApp", "&Export to CSV"))
        self.actionRemoveAll.setText(
            self.app.translate("TalkEditorApp", "&Remove All Talks"))

        # --- End Menubar

        #
        # TalkDetailsWidget
        #
        self.talkDetailsWidget.titleLabel.setText(self.app.translate("TalkEditorApp", "Title"))
        self.talkDetailsWidget.presenterLabel.setText(self.app.translate("TalkEditorApp", "Presenter"))
        self.talkDetailsWidget.categoryLabel.setText(self.app.translate("TalkEditorApp", "Category"))
        self.talkDetailsWidget.eventLabel.setText(self.app.translate("TalkEditorApp", "Event"))
        self.talkDetailsWidget.roomLabel.setText(self.app.translate("TalkEditorApp", "Room"))
        self.talkDetailsWidget.dateLabel.setText(self.app.translate("TalkEditorApp", "Date"))
        self.talkDetailsWidget.timeLabel.setText(self.app.translate("TalkEditorApp", "Time"))
        # --- End TalkDetailsWidget

        #
        # Import Talks Widget Translations
        #
        self.importTalksWidget.rssRadioButton.setText(
           self.app.translate("TalkEditorApp", "RSS URL"))
        self.importTalksWidget.csvRadioButton.setText(
           self.app.translate("TalkEditorApp", "CSV File"))
        self.importTalksWidget.importButton.setText(
           self.app.translate("TalkEditorApp", "Import"))
        # --- End Talks Widget Translations

        #
        # Command Button Translations
        #
        self.commandButtons.addButton.setText(
           self.app.translate("TalkEditorApp", "Add"))
        self.commandButtons.duplicateButton.setText(
           self.app.translate("TalkEditorApp", "Duplicate"))
        self.commandButtons.importButton.setText(
           self.app.translate("TalkEditorApp", "Import"))
        self.commandButtons.exportButton.setText(
           self.app.translate("TalkEditorApp", "Export"))
        self.commandButtons.removeButton.setText(
           self.app.translate("TalkEditorApp", "Remove"))
        self.commandButtons.removeAllButton.setText(
           self.app.translate("TalkEditorApp", "Remove All"))
        # --- End Command Butotn Translations

    def load_presentations_model(self):
        # Load Presentation Model
        self.presentationModel = self.db.get_presentations_model()
        self.tableView.setModel(self.presentationModel)

        # Fill table whitespace.
        self.tableView.horizontalHeader().setStretchLastSection(True)

        # Hide the ID field
        self.tableView.setColumnHidden(0, True)

        # Map data to widgets
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.presentationModel)
        self.mapper.addMapping(self.talkDetailsWidget.titleLineEdit, 1)
        self.mapper.addMapping(self.talkDetailsWidget.presenterLineEdit, 2)
        self.mapper.addMapping(self.talkDetailsWidget.categoryLineEdit, 4)
        self.mapper.addMapping(self.talkDetailsWidget.eventLineEdit, 5)
        self.mapper.addMapping(self.talkDetailsWidget.roomLineEdit, 6)
        self.mapper.addMapping(self.talkDetailsWidget.descriptionTextEdit, 3)
        self.mapper.addMapping(self.talkDetailsWidget.dateEdit, 7)
        self.mapper.addMapping(self.talkDetailsWidget.timeEdit, 8)

    def talk_selected(self, model):
        print "selected " + str(model.row())
        self.mapper.setCurrentIndex(model.row())

    def toggle_import(self):
        if self.importTalksWidget.csvRadioButton.isChecked():
            self.importTalksWidget.csvLineEdit.setEnabled(True)
            self.importTalksWidget.csvFileSelectButton.setEnabled(True)
            self.importTalksWidget.rssLineEdit.setEnabled(False)
        else:
            self.importTalksWidget.csvLineEdit.setEnabled(False)
            self.importTalksWidget.csvFileSelectButton.setEnabled(False)
            self.importTalksWidget.rssLineEdit.setEnabled(True)

    def show_import_talks_widget(self):
        self.commandButtons.setHidden(True)
        self.tableView.setHidden(True)
        self.talkDetailsWidget.setHidden(True)
        self.importTalksWidget.setHidden(False)

    def hide_import_talks_widget(self):
        self.commandButtons.setHidden(False)
        self.tableView.setHidden(False)
        self.talkDetailsWidget.setHidden(False)
        self.importTalksWidget.setHidden(True)

    def add_talk(self):
        date = self.talkDetailsWidget.dateEdit.date()
        time = self.talkDetailsWidget.timeEdit.time()
        #datetime = QtCore.QDateTime(date, time)
        presentation = Presentation(
            unicode(self.talkDetailsWidget.titleLineEdit.text()),
            unicode(
                self.talkDetailsWidget.presenterLineEdit.text(
                )),
            unicode(
                self.talkDetailsWidget.descriptionTextEdit.toPlainText(
                )),
            unicode(
                self.talkDetailsWidget.categoryLineEdit.text(
                )),
            unicode(
                self.talkDetailsWidget.eventLineEdit.text(
                )),
            unicode(
                self.talkDetailsWidget.roomLineEdit.text(
                )),
            unicode(date.toString(QtCore.Qt.ISODate
                )),
            unicode(time.toString(QtCore.Qt.ISODate)))


        # Do not add talks if they are empty strings
        if (len(presentation.title) == 0):
            return

        self.db.insert_presentation(presentation)

        # cleanup
        self.talkDetailsWidget.titleLineEdit.clear()
        self.talkDetailsWidget.presenterLineEdit.clear()
        self.talkDetailsWidget.descriptionTextEdit.clear()
        self.talkDetailsWidget.categoryLineEdit.clear()
        self.talkDetailsWidget.eventLineEdit.clear()
        self.talkDetailsWidget.roomLineEdit.clear()

        # Update Model, Refreshes TableView
        self.presentationModel.select()

        # Select Last Row
        self.tableView.selectRow(self.presentationModel.rowCount() - 1)

    def remove_talk(self):
        try:
            row_clicked = self.tableView.currentIndex().row()
        except:
            return
        try:
            rows_selected = self.tableView.selectionModel().selectedRows()
        except:
            return
        print rows_selected
        print row_clicked
        for row in reversed(rows_selected):
            print row.row()
            self.presentationModel.removeRow(row.row())
        self.presentationModel.select()

    def load_talk(self):
        try:
            row_clicked = self.tableView.currentIndex().row()
        except:
            return

        self.mapper.addMapping(self.talkDetailsWidget.roomLineEdit, 6)

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
        rss_url = unicode(self.importTalksWidget.rssLineEdit.text())
        if rss_url:
            self.db.add_talks_from_rss(rss_url)
            self.presentationModel.select()
            self.hide_import_talks_widget()
        else:
            error = QMessageBox()
            error.setText("Please enter a RSS URL")
            error.exec_()

    def closeEvent(self, event):
        log.info('Exiting talk database editor...')
        self.geometry = self.saveGeometry()
        event.accept()

    def csv_file_select(self):
        dirpath = str(self.importTalksWidget.csvLineEdit.text())
        fname = QFileDialog.getOpenFileName(
            self, 'Select file', "", "*.csv")
        if fname:
            self.importTalksWidget.csvLineEdit.setText(fname)

    def add_talks_from_csv(self):
        fname = self.importTalksWidget.csvLineEdit.text()

        if fname:
            self.db.add_talks_from_csv(fname)
            self.presentationModel.select()
            self.hide_import_talks_widget()
        else:
            error = QMessageBox()
            error.setText("Please select a file")
            error.exec_()

    def import_talks(self):
        if self.importTalksWidget.csvRadioButton.isChecked():
            self.add_talks_from_csv()
        else:
            self.add_talks_from_rss()

    def export_talks_to_csv(self):
        dirpath = str(self.importTalksWidget.csvLineEdit.text())
        fname = QFileDialog.getSaveFileName(self, 'Select file', "", "*.csv")
        if fname:
            self.db.export_talks_to_csv(fname)
