#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011, 2014  Free and Open Source Software Learning Centre
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

# PyQt modules
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QPersistentModelIndex
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QDataWidgetMapper
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QHeaderView
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QSortFilterProxyModel
from PyQt4.QtGui import QTableView
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget

# Freeseer modules
from freeseer.framework.presentation import Presentation
from freeseer.frontend.qtcommon.FreeseerApp import FreeseerApp

# TalkEditor modules
from freeseer.frontend.talkeditor.CommandButtons import CommandButtons
from freeseer.frontend.talkeditor.TalkDetailsWidget import TalkDetailsWidget
from freeseer.frontend.talkeditor.NewTalkWidget import NewTalkWidget
from freeseer.frontend.talkeditor.ImportTalksWidget import ImportTalksWidget

log = logging.getLogger(__name__)


class TalkEditorApp(FreeseerApp):
    '''Freeseer talk database editor main gui class'''
    def __init__(self, config, db):
        super(TalkEditorApp, self).__init__(config)

        self.db = db

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
        self.mainLayout.setAlignment(Qt.AlignTop)

        # Add custom widgets
        self.commandButtons = CommandButtons()
        self.tableView = QTableView()
        self.tableView.setSortingEnabled(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.talkDetailsWidget = TalkDetailsWidget()
        self.importTalksWidget = ImportTalksWidget()
        self.newTalkWidget = NewTalkWidget()
        self.mainLayout.addWidget(self.importTalksWidget)
        #self.mainLayout.addLayout(self.titleLayout)
        self.mainLayout.addWidget(self.commandButtons)
        self.mainLayout.addWidget(self.tableView)
        self.mainLayout.addWidget(self.talkDetailsWidget)
        self.mainLayout.addWidget(self.importTalksWidget)
        # --- End Layout

        # Keep track of index of the most recently selected talk
        self.currentTalkIndex = QPersistentModelIndex()

        # Prompt user to "Continue Editing", "Discard Changes" or "Save Changes"
        self.savePromptBox = QMessageBox()
        self.savePromptBox.setWindowTitle("Unsaved Changes Exist")
        self.savePromptBox.setIcon(QMessageBox.Information)
        self.savePromptBox.setText("The talk you were editing has unsaved changes.")
        self.continueButton = self.savePromptBox.addButton("Continue Editing", QMessageBox.RejectRole)
        self.discardButton = self.savePromptBox.addButton("Discard Changes", QMessageBox.DestructiveRole)
        self.saveButton = self.savePromptBox.addButton("Save Changes", QMessageBox.AcceptRole)
        self.savePromptBox.setDefaultButton(self.saveButton)

        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

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
        self.connect(self.tableView, SIGNAL('activated(const QModelIndex)'), self.click_talk)
        self.connect(self.tableView, SIGNAL('selected(const QModelIndex)'), self.click_talk)
        self.connect(self.tableView, SIGNAL('clicked(const QModelIndex)'), self.click_talk)

        # Import Widget
        self.connect(self.importTalksWidget.csvRadioButton, SIGNAL('toggled(bool)'), self.toggle_import)
        self.connect(self.importTalksWidget.importButton, SIGNAL('clicked()'), self.import_talks)
        self.connect(self.importTalksWidget.cancelButton, SIGNAL('clicked()'), self.hide_import_talks_widget)
        self.importTalksWidget.setHidden(True)
        self.connect(self.importTalksWidget.csvFileSelectButton, SIGNAL('clicked()'), self.csv_file_select)
        self.connect(self.importTalksWidget.csvLineEdit, SIGNAL('returnPressed()'),
            self.importTalksWidget.importButton.click)
        self.connect(self.importTalksWidget.rssLineEdit, SIGNAL('returnPressed()'),
            self.importTalksWidget.importButton.click)
        self.connect(self.actionExportCsv, SIGNAL('triggered()'), self.export_talks_to_csv)
        self.connect(self.actionRemoveAll, SIGNAL('triggered()'), self.confirm_reset)

        # Command Buttons
        self.connect(self.commandButtons.addButton, SIGNAL('clicked()'), self.click_add_button)
        self.connect(self.commandButtons.removeButton, SIGNAL('clicked()'), self.remove_talk)
        self.connect(self.commandButtons.removeAllButton, SIGNAL('clicked()'), self.confirm_reset)
        self.connect(self.commandButtons.importButton, SIGNAL('clicked()'), self.show_import_talks_widget)
        self.connect(self.commandButtons.exportButton, SIGNAL('clicked()'), self.export_talks_to_csv)
        self.connect(self.commandButtons.searchButton, SIGNAL('clicked()'), self.search_talks)
        self.connect(self.commandButtons.searchLineEdit, SIGNAL('textEdited(QString)'), self.search_talks)
        self.connect(self.commandButtons.searchLineEdit, SIGNAL('returnPressed()'), self.search_talks)

        # Talk Details Buttons
        self.connect(self.talkDetailsWidget.saveButton, SIGNAL('clicked()'), self.update_talk)

        # Talk Details Widget
        self.connect(self.talkDetailsWidget.titleLineEdit, SIGNAL('textEdited(const QString)'), self.enable_save)
        self.connect(self.talkDetailsWidget.presenterLineEdit, SIGNAL('textEdited(const QString)'), self.enable_save)
        self.connect(self.talkDetailsWidget.categoryLineEdit, SIGNAL('textEdited(const QString)'), self.enable_save)
        self.connect(self.talkDetailsWidget.eventLineEdit, SIGNAL('textEdited(const QString)'), self.enable_save)
        self.connect(self.talkDetailsWidget.roomLineEdit, SIGNAL('textEdited(const QString)'), self.enable_save)
        self.connect(self.talkDetailsWidget.descriptionTextEdit, SIGNAL('modificationChanged(bool)'), self.enable_save)
        self.connect(self.talkDetailsWidget.dateEdit, SIGNAL('dateChanged(const QDate)'), self.enable_save)
        self.connect(self.talkDetailsWidget.startTimeEdit, SIGNAL('timeChanged(const QTime)'), self.enable_save)
        self.connect(self.talkDetailsWidget.endTimeEdit, SIGNAL('timeChanged(const QTime)'), self.enable_save)

        # New Talk Widget
        self.newTalkWidget.connect(self.newTalkWidget.addButton, SIGNAL('clicked()'), self.add_talk)
        self.newTalkWidget.connect(self.newTalkWidget.cancelButton, SIGNAL('clicked()'), self.newTalkWidget.reject)

        # Load default language
        actions = self.menuLanguage.actions()
        for action in actions:
            if action.data().toString() == self.config.default_language:
                action.setChecked(True)
                self.translate(action)
                break

        # Load Talk Database
        self.load_presentations_model()

        # Setup Autocompletion
        self.update_autocomplete_fields()

        self.talkDetailsWidget.saveButton.setEnabled(False)

        # Select first item
        #self.tableView.setCurrentIndex(self.proxy.index(0,0))
        #self.talk_selected(self.proxy.index(0,0))

    #
    # Translation
    #
    def retranslate(self):
        self.setWindowTitle(self.app.translate("TalkEditorApp", "Freeseer Talk Editor"))

        #
        # Reusable Strings
        #
        self.confirmDBClearTitleString = self.app.translate("TalkEditorApp", "Remove All Talks from Database")
        self.confirmDBClearQuestionString = self.app.translate("TalkEditorApp",
                                                               "Are you sure you want to clear the DB?")
        self.confirmTalkDetailsClearTitleString = self.app.translate("TalkEditorApp", "Unsaved Data")
        self.confirmTalkDetailsClearQuestionString = self.app.translate("TalkEditorApp",
                                                                        "Unsaved talk details will be lost. Continue?")
        # --- End Reusable Strings

        #
        # Menubar
        #
        self.actionExportCsv.setText(self.app.translate("TalkEditorApp", "&Export to CSV"))
        self.actionRemoveAll.setText(self.app.translate("TalkEditorApp", "&Remove All Talks"))

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
        self.talkDetailsWidget.startTimeLabel.setText(self.app.translate("TalkEditorApp", "Start Time"))
        self.talkDetailsWidget.endTimeLabel.setText(self.app.translate("TalkEditorApp", "End Time"))
        # --- End TalkDetailsWidget

        #
        # Import Talks Widget Translations
        #
        self.importTalksWidget.rssRadioButton.setText(self.app.translate("TalkEditorApp", "RSS URL"))
        self.importTalksWidget.csvRadioButton.setText(self.app.translate("TalkEditorApp", "CSV File"))
        self.importTalksWidget.importButton.setText(self.app.translate("TalkEditorApp", "Import"))
        # --- End Talks Widget Translations

        #
        # Command Button Translations\
        #
        self.commandButtons.importButton.setText(self.app.translate("TalkEditorApp", "Import"))
        self.commandButtons.exportButton.setText(self.app.translate("TalkEditorApp", "Export"))
        self.commandButtons.addButton.setText(self.app.translate("TalkEditorApp", "Add New Talk"))
        self.commandButtons.removeButton.setText(self.app.translate("TalkEditorApp", "Remove"))
        self.commandButtons.removeAllButton.setText(self.app.translate("TalkEditorApp", "Remove All"))
        # --- End Command Butotn Translations

        #
        # Search Widget Translations
        #
        self.commandButtons.searchButton.setText(self.app.translate("TalkEditorApp", "Search"))
        # --- End Command Button Translations

    def load_presentations_model(self):
        # Load Presentation Model
        # FIXME: The raw databse values are being loaded into the view. This means the date, startTime, and
        # endTime are showing the raw QDate(Time) values. There should be a layer that converts between the
        # frontend values and the backend.
        self.presentationModel = self.db.get_presentations_model()
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.presentationModel)
        self.tableView.setModel(self.proxy)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # Fill table whitespace.
        self.tableView.horizontalHeader().setStretchLastSection(False)
        for i in range(2, self.tableView.horizontalHeader().count() + 1):
            self.tableView.horizontalHeader().resizeSection(i, self.set_width_with_dpi(80))
        self.tableView.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)

        # Hide the ID field
        self.tableView.setColumnHidden(0, True)

        # Map data to widgets
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.proxy)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.addMapping(self.talkDetailsWidget.titleLineEdit, 1)
        self.mapper.addMapping(self.talkDetailsWidget.presenterLineEdit, 2)
        self.mapper.addMapping(self.talkDetailsWidget.categoryLineEdit, 4)
        self.mapper.addMapping(self.talkDetailsWidget.eventLineEdit, 5)
        self.mapper.addMapping(self.talkDetailsWidget.roomLineEdit, 6)
        self.mapper.addMapping(self.talkDetailsWidget.descriptionTextEdit, 3)
        self.mapper.addMapping(self.talkDetailsWidget.dateEdit, 7)
        self.mapper.addMapping(self.talkDetailsWidget.startTimeEdit, 8)
        self.mapper.addMapping(self.talkDetailsWidget.endTimeEdit, 9)

        # Load StringLists
        self.titleList = QStringList(self.db.get_string_list("Title"))
        #self.speakerList = QStringList(self.db.get_speaker_list())
        #self.categoryList = QStringList(self.db.get_category_list())
        #self.eventList = QStringList(self.db.get_event_list())
        #self.roomList = QStringList(self.db.get_room_list())

        #Disble input
        self.talkDetailsWidget.disable_input_fields()

    def search_talks(self):
        # The default value is 0. If the value is -1, the keys will be read from all columns.
        self.proxy.setFilterKeyColumn(-1)
        self.proxy.setFilterFixedString(self.commandButtons.searchLineEdit.text())

    def show_save_prompt(self):
        """Prompts the user to save or discard changes, or continue editing."""
        self.savePromptBox.exec_()
        self.savePromptBox.setDefaultButton(self.saveButton)
        return self.savePromptBox.clickedButton()

    def click_talk(self, model):
        """Warns user if there are unsaved changes, and selects talk clicked by the user."""
        log.info("Selecting row %d", model.row())
        modelRow = model.row()
        if self.unsaved_details_exist():
            log.info("Unsaved changes exist in row %d", self.currentTalkIndex.row())
            confirm = self.show_save_prompt()
            if confirm == self.saveButton:
                log.info("Saving changes in row %d...", self.currentTalkIndex.row())
                self.tableView.selectRow(self.currentTalkIndex.row())
                self.update_talk()
                newModel = self.tableView.currentIndex().sibling(modelRow, 0)
                self.select_talk(newModel)
            elif confirm == self.discardButton:
                log.info("Discarding changes in row %d...", self.currentTalkIndex.row())
                self.talk_selected(model)
            else:
                log.info("Continue editing row %d", self.currentTalkIndex.row())
                self.tableView.selectRow(self.currentTalkIndex.row())
        else:
            self.talk_selected(model)

    def click_add_button(self):
        """Warns user if there are unsaved changes, and shows the New Talk window."""
        if self.unsaved_details_exist():
            log.info("Unsaved changes exist in row %d", self.currentTalkIndex.row())
            confirm = self.show_save_prompt()
            if confirm == self.saveButton:
                log.info("Saving changes in row %d...", self.currentTalkIndex.row())
                self.update_talk()
                self.show_new_talk_popup()
            elif confirm == self.discardButton:
                log.info("Discarding changes in row %d...", self.currentTalkIndex.row())
                # Ensure that changes are discarded
                self.talk_selected(self.currentTalkIndex)
                self.show_new_talk_popup()
            else:
                log.info("Continue editing row %d", self.currentTalkIndex.row())
        else:
            self.show_new_talk_popup()

    def talk_selected(self, model):
        self.mapper.setCurrentIndex(model.row())
        self.talkDetailsWidget.enable_input_fields()
        self.talkDetailsWidget.saveButton.setEnabled(False)
        self.currentTalkIndex = QPersistentModelIndex(model)

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
        """Adds a new talk to the database using data from the NewTalkWidget input fields"""
        presentation = self.create_presentation(self.newTalkWidget.talkDetailsWidget)

        if presentation:
            self.db.insert_presentation(presentation)
            self.newTalkWidget.accept()  # Close the dialog

    def update_talk(self):
        """Updates the currently selected talk using data from the TalkEditorApp input fields"""
        selected_talk = self.tableView.currentIndex()
        if selected_talk.row() >= 0:  # The tableView index begins at 0 and is -1 by default
            talk_id = selected_talk.sibling(selected_talk.row(), 0).data().toString()
            presentation = self.create_presentation(self.talkDetailsWidget)

            if presentation:
                self.db.update_presentation(talk_id, presentation)
                self.apply_changes(selected_talk)
                self.talkDetailsWidget.saveButton.setEnabled(False)

    def create_presentation(self, talkDetailsWidget):
        """Creates and returns an instance of Presentation using data from the input fields"""

        title = unicode(talkDetailsWidget.titleLineEdit.text()).strip()
        if title:
            return Presentation(
                unicode(talkDetailsWidget.titleLineEdit.text()).strip(),
                unicode(talkDetailsWidget.presenterLineEdit.text()).strip(),
                unicode(talkDetailsWidget.descriptionTextEdit.toPlainText()).strip(),
                unicode(talkDetailsWidget.categoryLineEdit.text()).strip(),
                unicode(talkDetailsWidget.eventLineEdit.text()).strip(),
                unicode(talkDetailsWidget.roomLineEdit.text()).strip(),
                talkDetailsWidget.dateEdit.date(),
                talkDetailsWidget.startTimeEdit.time().toString('hh:mm ap'),
                talkDetailsWidget.endTimeEdit.time().toString('hh:mm ap'))

    def show_new_talk_popup(self):
        """Displays a modal dialog with a talk details view

        When Add is selected, a new talk is added to the database using the input field data.
        When Cancel is selected, no talk is added.
        """
        log.info('Opening Add Talk window...')
        self.clear_new_talk_fields()
        self.remove_new_talk_placeholder_text()
        self.newTalkWidget.talkDetailsWidget.titleLineEdit.setFocus()
        if self.newTalkWidget.exec_() == 1:
            self.apply_changes()
            self.talkDetailsWidget.disable_input_fields()
        else:
            log.info('No talk added...')

    def apply_changes(self, updated_talk=None):
        """Repopulates the model to display the effective changes

        Updates the autocomplete fields.
        Displays the updated model in the table view, and selects the newly updated/added talk.
        """
        self.presentationModel.select()
        self.select_talk(updated_talk)
        self.update_autocomplete_fields()

    def select_talk(self, talk=None):
        """Selects the given talk in the table view

        If no talk is given, the last row in the table view is selected.
        """
        if talk:
            row = talk.row()
            column = talk.column()
        else:
            row = self.presentationModel.rowCount() - 1  # Select last row
            column = 0

        self.tableView.selectRow(row)
        self.tableView.setCurrentIndex(self.proxy.index(row, column))
        self.talk_selected(self.proxy.index(row, column))

    def remove_talk(self):
        try:
            rows_selected = self.tableView.selectionModel().selectedRows()
        except:
            return

        # Reversed because rows in list change position once row is removed
        for row in reversed(rows_selected):
            self.presentationModel.removeRow(row.row())
        self.talkDetailsWidget.clear_input_fields()
        self.talkDetailsWidget.disable_input_fields()

    def load_talk(self):
        try:
            self.tableView.currentIndex().row()
        except:
            return

        self.mapper.addMapping(self.talkDetailsWidget.roomLineEdit, 6)
        self.presentationModel.select()

    def reset(self):
        self.db.clear_database()
        self.presentationModel.select()
        self.talkDetailsWidget.clear_input_fields()
        self.talkDetailsWidget.disable_input_fields()

    def confirm_reset(self):
        """Presents a confirmation dialog to ask the user if they are sure they wish to remove the talk database.
        If Yes call the reset() function"""
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
        if self.unsaved_details_exist():
            log.info("Unsaved changes exist in row %d", self.currentTalkIndex.row())
            confirm = self.show_save_prompt()
            if confirm == self.saveButton:
                log.info("Saving changes in row %d...", self.currentTalkIndex.row())
                self.update_talk()
                log.info('Exiting talk database editor...')
                self.geometry = self.saveGeometry()
                event.accept()
            elif confirm == self.discardButton:
                log.info("Discarding changes in row %d...", self.currentTalkIndex.row())
                # Ensure that changes are discarded
                self.talk_selected(self.currentTalkIndex)
                log.info('Exiting talk database editor...')
                self.geometry = self.saveGeometry()
                event.accept()
            else:
                log.info("Continue editing row %d", self.currentTalkIndex.row())
                event.ignore()
        else:
            log.info('Exiting talk database editor...')
            self.geometry = self.saveGeometry()
            event.accept()

    def csv_file_select(self):
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

        self.update_autocomplete_fields()

    def export_talks_to_csv(self):
        fname = QFileDialog.getSaveFileName(self, 'Select file', "", "*.csv")
        if fname:
            self.db.export_talks_to_csv(fname)

    def update_autocomplete_fields(self):
        self.titleList = QStringList(self.db.get_string_list("Title"))
        self.speakerList = QStringList(self.db.get_string_list("Speaker"))
        self.categoryList = QStringList(self.db.get_string_list("Category"))
        self.eventList = QStringList(self.db.get_string_list("Event"))
        self.roomList = QStringList(self.db.get_string_list("Room"))

        self.titleCompleter = QCompleter(self.titleList)
        self.titleCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.speakerCompleter = QCompleter(self.speakerList)
        self.speakerCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.categoryCompleter = QCompleter(self.categoryList)
        self.categoryCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.eventCompleter = QCompleter(self.eventList)
        self.eventCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.roomCompleter = QCompleter(self.roomList)
        self.roomCompleter.setCaseSensitivity(Qt.CaseInsensitive)

        self.talkDetailsWidget.titleLineEdit.setCompleter(self.titleCompleter)
        self.talkDetailsWidget.presenterLineEdit.setCompleter(self.speakerCompleter)
        self.talkDetailsWidget.categoryLineEdit.setCompleter(self.categoryCompleter)
        self.talkDetailsWidget.eventLineEdit.setCompleter(self.eventCompleter)
        self.talkDetailsWidget.roomLineEdit.setCompleter(self.roomCompleter)

    def are_fields_enabled(self):
        return (self.talkDetailsWidget.titleLineEdit.isEnabled() and
                self.talkDetailsWidget.presenterLineEdit.isEnabled() and
                self.talkDetailsWidget.categoryLineEdit.isEnabled() and
                self.talkDetailsWidget.eventLineEdit.isEnabled() and
                self.talkDetailsWidget.roomLineEdit.isEnabled() and
                self.talkDetailsWidget.dateEdit.isEnabled() and
                self.talkDetailsWidget.startTimeEdit.isEnabled() and
                self.talkDetailsWidget.endTimeEdit.isEnabled())

    def unsaved_details_exist(self):
        """Checks if changes have been made to new/existing talk details

        Looks for text in the input fields and check the enabled state of the Save Talk button
        If the Save Talk button is enabled, the input fields contain modified values
        """
        return (self.talkDetailsWidget.saveButton.isEnabled() and
                (self.talkDetailsWidget.titleLineEdit.text() or
                self.talkDetailsWidget.presenterLineEdit.text() or
                self.talkDetailsWidget.categoryLineEdit.text() or
                self.talkDetailsWidget.descriptionTextEdit.toPlainText()))

    def enable_save(self):
        self.talkDetailsWidget.saveButton.setEnabled(True)

    def clear_new_talk_fields(self):
        """Removes existing data from all NewTalkWidget fields except event, room, date and time"""
        self.newTalkWidget.talkDetailsWidget.titleLineEdit.clear()
        self.newTalkWidget.talkDetailsWidget.presenterLineEdit.clear()
        self.newTalkWidget.talkDetailsWidget.descriptionTextEdit.clear()
        self.newTalkWidget.talkDetailsWidget.categoryLineEdit.clear()

    def remove_new_talk_placeholder_text(self):
        """Removes placeholder text in NewTalkWidget originally set by TalkDetailsWidget"""
        self.newTalkWidget.talkDetailsWidget.titleLineEdit.setPlaceholderText("")
        self.newTalkWidget.talkDetailsWidget.presenterLineEdit.setPlaceholderText("")
        self.newTalkWidget.talkDetailsWidget.categoryLineEdit.setPlaceholderText("")
        self.newTalkWidget.talkDetailsWidget.eventLineEdit.setPlaceholderText("")
        self.newTalkWidget.talkDetailsWidget.roomLineEdit.setPlaceholderText("")
