#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011-2012  Free and Open Source Software Learning Centre
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
import time

from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer import project_info
from freeseer.framework.core import FreeseerCore
from freeseer.framework.failure import Failure
from freeseer.frontend.controller.Client import ClientDialog
from freeseer.frontend.record.ReportDialog import ReportDialog
from freeseer.frontend.record.RecordingWidget import RecordingWidget
from freeseer.frontend.qtcommon.AboutDialog import AboutDialog
from freeseer.frontend.qtcommon.Resource import resource_rc

__version__= project_info.VERSION

class RecordApp(QtGui.QMainWindow):
    """Freeseer's main GUI class."""
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(550, 450)
        
        self.aboutDialog = AboutDialog()
        self.aboutDialog.setModal(True)
        self.talks_to_save = []
        self.talks_to_delete = []
        
        self.mainWidget = RecordingWidget()
        self.setCentralWidget(self.mainWidget)
        self.reportWidget = ReportDialog()
        self.reportWidget.setModal(True)
        
        self.statusBar().addPermanentWidget(self.mainWidget.statusLabel)
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        # Initialize current_event , current_room
        self.current_event = None
        self.current_room = None

        self.core = FreeseerCore(self.mainWidget.previewWidget.winId(), self.audio_feedback)
        self.config = self.core.get_config()

        # ClientDialog needs to be loaded after core to get the config directory        
        self.clientWidget = ClientDialog(self.config.configdir, self.core.db)
        
        # Set timer for recording how much time elapsed during a recording
        self.reset_timer()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        
        #
        # Translator
        #
        self.current_language = None
        self.uiTranslator = QtCore.QTranslator()
        self.uiTranslator.load(":/languages/tr_en_US.qm")
        self.langActionGroup = QtGui.QActionGroup(self)
        self.langActionGroup.setExclusive(True)
        QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('utf-8'))
        self.connect(self.langActionGroup, QtCore.SIGNAL('triggered(QAction *)'), self.translate)
        # --- Translator
        
        #
        # Setup Menubar
        #
        self.menubar = QtGui.QMenuBar()
        self.setMenuBar(self.menubar)
        
        self.menubar.setGeometry(QtCore.QRect(0, 0, 566, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menuLanguage = QtGui.QMenu(self.menuOptions)
        self.menuLanguage.setObjectName(_fromUtf8("menuLanguage"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        
        folderIcon = QtGui.QIcon.fromTheme("folder")
        self.actionOpenVideoFolder = QtGui.QAction(self)
        self.actionOpenVideoFolder.setShortcut("Ctrl+O")
        self.actionOpenVideoFolder.setObjectName(_fromUtf8("actionOpenVideoFolder"))
        self.actionOpenVideoFolder.setIcon(folderIcon)
        
        exitIcon = QtGui.QIcon.fromTheme("application-exit")
        self.actionExit = QtGui.QAction(self)
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionExit.setIcon(exitIcon)
        
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAbout.setIcon(icon)
        
        self.actionReport = QtGui.QAction(self)
        self.actionReport.setObjectName(_fromUtf8("actionReport"))
        
        self.actionClient = QtGui.QAction(self)
        self.actionClient.setIcon(icon)
        # Actions
        self.menuFile.addAction(self.actionOpenVideoFolder)
        self.menuFile.addAction(self.actionClient)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionReport)
        self.menuOptions.addAction(self.menuLanguage.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        self.setupLanguageMenu()
        # --- End Menubar

        #
        # Systray Setup
        #
        self.systray = QtGui.QSystemTrayIcon(icon)
        self.systray.show()
        self.systray.menu = QtGui.QMenu()
        self.systray.setContextMenu(self.systray.menu)
        
        self.visibilityAction = QtGui.QAction(self)
        self.recordAction = QtGui.QAction(self)
        
        self.systray.menu.addAction(self.visibilityAction)
        self.systray.menu.addAction(self.recordAction)
        
        self.connect(self.visibilityAction, QtCore.SIGNAL('triggered()'), self.toggle_window_visibility)
        self.connect(self.recordAction, QtCore.SIGNAL('triggered()'), self.toggle_record_button)
        self.connect(self.systray, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self._icon_activated)
        # --- End Systray Setup

        # main tab connections
        self.connect(self.mainWidget.eventComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_rooms_from_event)
        self.connect(self.mainWidget.roomComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_dates_from_event_room)
        self.connect(self.mainWidget.dateComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_talks_from_date)
        self.connect(self.mainWidget.talkComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_talk_tooltip)
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.standby)
        self.connect(self.mainWidget.recordPushButton, QtCore.SIGNAL('toggled(bool)'), self.record)
        self.connect(self.mainWidget.pauseToolButton, QtCore.SIGNAL('toggled(bool)'), self.pause)
        self.connect(self.mainWidget.audioFeedbackCheckbox, QtCore.SIGNAL('toggled(bool)'), self.toggle_audio_feedback)

        # Main Window Connections
        self.connect(self.actionOpenVideoFolder, QtCore.SIGNAL('triggered()'), self.open_video_directory)
        self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        self.connect(self.actionReport, QtCore.SIGNAL('triggered()'), self.show_report_widget)
        self.connect(self.actionClient, QtCore.SIGNAL('triggered()'), self.show_client_widget)
        
        # GUI Disabling/Enabling Connections
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.standbyPushButton.setHidden)
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.recordPushButton.setVisible)
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.recordPushButton.setEnabled)
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.pauseToolButton.setVisible)
        self.connect(self.mainWidget.recordPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.pauseToolButton.setEnabled)
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.eventComboBox.setDisabled)
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.roomComboBox.setDisabled)
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.dateComboBox.setDisabled)
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.talkComboBox.setDisabled)
        self.connect(self.mainWidget.standbyPushButton, QtCore.SIGNAL("toggled(bool)"), self.mainWidget.audioFeedbackCheckbox.setDisabled)
        
        #Client Connections
        self.connect(self.clientWidget.socket, QtCore.SIGNAL('readyRead()'), self.getAction)
        
        #
        # ReportWidget Connections
        #
        self.connect(self.reportWidget.reportButton, QtCore.SIGNAL("clicked()"), self.report)

        self.load_settings()

        # Setup spacebar key.
        self.mainWidget.recordPushButton.setShortcut(QtCore.Qt.Key_Space)
        self.mainWidget.recordPushButton.setFocus()

    ###
    ### Translation Related
    ###
    def retranslate(self):
        self.setWindowTitle(self.uiTranslator.translate("RecordApp", "Freeseer - portable presentation recording station"))
        #
        # Reusable Strings
        #
        self.standbyString = self.uiTranslator.translate("RecordApp", "Standby")
        self.recordString = self.uiTranslator.translate("RecordApp", "Record")
        self.pauseString = self.uiTranslator.translate("RecordApp", "Pause")
        self.resumeString = self.uiTranslator.translate("RecordApp", "Resume")
        self.stopString = self.uiTranslator.translate("RecordApp", "Stop")
        self.hideWindowString = self.uiTranslator.translate("RecordApp", "Hide Main Window")
        self.showWindowString = self.uiTranslator.translate("RecordApp", "Show Main Window")
        
        # Status Bar messages
        self.idleString = self.uiTranslator.translate("RecordApp", "Idle.")
        self.readyString = self.uiTranslator.translate("RecordApp", "Ready.")
        self.recordingString = self.uiTranslator.translate("RecordApp", "Recording...")
        self.pausedString = self.uiTranslator.translate("RecordApp", "Recording Paused.")
        # --- End Reusable Strings
        
        if self.mainWidget.recordPushButton.isChecked() and self.mainWidget.pauseToolButton.isChecked():
            self.mainWidget.statusLabel.setText(self.pausedString)
        elif self.mainWidget.recordPushButton.isChecked() and (not self.mainWidget.pauseToolButton.isChecked()):
            self.mainWidget.statusLabel.setText(self.recordingString)
        elif self.mainWidget.standbyPushButton.isChecked():
            self.mainWidget.statusLabel.setText(self.readyString)
        else:
            self.mainWidget.statusLabel.setText(self.idleString)
        
        #
        # Menubar
        #
        self.menuFile.setTitle(self.uiTranslator.translate("RecordApp", "&File"))
        self.menuOptions.setTitle(self.uiTranslator.translate("RecordApp", "&Options"))
        self.menuLanguage.setTitle(self.uiTranslator.translate("RecordApp", "&Language"))
        self.menuHelp.setTitle(self.uiTranslator.translate("RecordApp", "&Help"))
        
        self.actionOpenVideoFolder.setText(self.uiTranslator.translate("RecordApp", "&Open Video Directory"))
        self.actionClient.setText(self.uiTranslator.translate("RecordApp", "&Connect to server"))
        self.actionExit.setText(self.uiTranslator.translate("RecordApp", "&Quit"))
        self.actionAbout.setText(self.uiTranslator.translate("RecordApp", "&About"))
        self.actionReport.setText(self.uiTranslator.translate("RecordApp", "&Report"))
        # --- End Menubar
        
        #
        # Systray
        #
        self.visibilityAction.setText(self.hideWindowString)
        self.recordAction.setText(self.recordString)
        # --- End Systray
        
        #
        # RecordingWidget
        #
        self.mainWidget.standbyPushButton.setText(self.standbyString)
        self.mainWidget.standbyPushButton.setToolTip(self.standbyString)
        if self.mainWidget.recordPushButton.isChecked():
            self.mainWidget.recordPushButton.setText(self.stopString)
            self.mainWidget.recordPushButton.setToolTip(self.stopString)
        else:
            self.mainWidget.recordPushButton.setText(self.recordString)
            self.mainWidget.recordPushButton.setToolTip(self.recordString)
        self.mainWidget.pauseToolButton.setText(self.pauseString)
        self.mainWidget.pauseToolButton.setToolTip(self.pauseString)
        self.mainWidget.eventLabel.setText(self.uiTranslator.translate("RecordApp", "Event"))
        self.mainWidget.roomLabel.setText(self.uiTranslator.translate("RecordApp", "Room"))
        self.mainWidget.dateLabel.setText(self.uiTranslator.translate("RecordApp", "Date"))
        self.mainWidget.talkLabel.setText(self.uiTranslator.translate("RecordApp", "Talk"))
        # --- End RecordingWidget
        
        #
        # ReportWidget
        #
        self.reportWidget.setWindowTitle(self.uiTranslator.translate("RecordApp", "Reporting Tool"))
        self.reportWidget.titleLabel.setText(self.uiTranslator.translate("RecordApp", "Title:"))
        self.reportWidget.speakerLabel.setText(self.uiTranslator.translate("RecordApp", "Speaker:"))
        self.reportWidget.eventLabel.setText(self.uiTranslator.translate("RecordApp", "Event:"))
        self.reportWidget.roomLabel.setText(self.uiTranslator.translate("RecordApp", "Room:"))
        self.reportWidget.timeLabel.setText(self.uiTranslator.translate("RecordApp", "Time:"))
        self.reportWidget.commentLabel.setText(self.uiTranslator.translate("RecordApp", "Comment"))
        self.reportWidget.releaseCheckBox.setText(self.uiTranslator.translate("RecordApp", "Release Received"))
        self.reportWidget.closeButton.setText(self.uiTranslator.translate("RecordApp", "Close"))
        self.reportWidget.reportButton.setText(self.uiTranslator.translate("RecordApp", "Report"))
        
        # Logic for translating the report options
        noissues = self.uiTranslator.translate("RecordApp", "No Issues")
        noaudio = self.uiTranslator.translate("RecordApp", "No Audio")
        novideo = self.uiTranslator.translate("RecordApp", "No Video")
        noaudiovideo = self.uiTranslator.translate("RecordApp", "No Audio/Video")
        self.reportWidget.options = [noissues, noaudio, novideo, noaudiovideo]
        self.reportWidget.reportCombo.clear()
        for i in self.reportWidget.options:
            self.reportWidget.reportCombo.addItem(i)
        # --- End ReportWidget
        
        self.aboutDialog.retranslate(self.current_language)
        
    def translate(self, action):
        """Translates the GUI.

        When a language is selected from the language menu, this function is
        called and the language to be changed to is retrieved.
        """
        self.current_language = str(action.data().toString()).strip("tr_").rstrip(".qm")
        
        logging.info("Switching language to: %s" % action.text())
        self.uiTranslator.load(":/languages/tr_%s.qm" % self.current_language)
        
        self.retranslate()
        self.clientWidget.retranslate()

    def setupLanguageMenu(self):
        languages = QtCore.QDir(":/languages").entryList()
        
        if self.current_language is None:
            self.current_language = QtCore.QLocale.system().name()  # Retrieve Current Locale from the operating system.
            logging.debug("Detected user's locale as %s" % self.current_language)
        
        for language in languages:
            translator = QtCore.QTranslator()  # Create a translator to translate Language Display Text.
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
            
    ###
    ### UI Logic
    ###    
    def load_settings(self): 
        logging.info('Loading settings...')
        
        # Load default language.
        actions = self.menuLanguage.actions()
        for action in actions:
            if action.data().toString() == self.config.default_language:
                action.setChecked(True)
                self.translate(action)
                break
        
        # Load Talks as a SQL Data Model.
        self.load_event_list()

    def current_presentation(self):
        """Creates a presentation object of the current presentation.
        
        Current presentation is the currently selected title on the GUI.
        """
        #i = self.mainWidget.talkComboBox.currentIndex()
        #p_id = self.mainWidget.talkComboBox.model().index(i, 1).data(QtCore.Qt.DisplayRole).toString()
        return self.core.db.get_presentation(self.current_presentation_id())
    
    def current_presentation_id(self):
        """Returns the current selected presentation ID."""
        i = self.mainWidget.talkComboBox.currentIndex()
        return self.mainWidget.talkComboBox.model().index(i, 1).data(QtCore.Qt.DisplayRole).toString()
    
    def standby(self, state):
        if (state): # Prepare the pipelines
            self.load_backend()
            self.core.pause()
            self.mainWidget.statusLabel.setText(self.readyString)

    def record(self, state):
        """The logic for recording and stopping recording."""

        if (state): # Start Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/logo_rec.png")
            sysIcon2 = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon2)
            self.systray.showMessage("Recording", "RECORDING")
            self.core.record()
            self.mainWidget.recordPushButton.setText(self.stopString)
            self.recordAction.setText(self.stopString)

            # Hide if auto-hide is set.
            if(self.core.config.auto_hide == True):
                self.hide_window()
                self.visibilityAction.setText(self.showWindowString)
                
            if (self.core.config.delay_recording>0):
                time.sleep(float(self.core.config.delay_recording))

            self.mainWidget.statusLabel.setText(self.recordingString)
            
            # Start timer.
            self.timer.start(1000)
            
        else: # Stop Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/logo.png")
            sysIcon = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon)
            self.core.stop()
            self.mainWidget.pauseToolButton.setChecked(False)
            self.mainWidget.recordPushButton.setText(self.recordString)
            self.recordAction.setText(self.recordString)
            self.mainWidget.audioSlider.setValue(0)
            
            # Finally set the standby button back to unchecked position.
            self.mainWidget.standbyPushButton.setChecked(False)
            
            # Stop and reset timer.
            self.timer.stop()
            self.reset_timer()
            
            # Select next talk if there is one within 15 minutes.
            starttime = QtCore.QDateTime().currentDateTime()
            stoptime = starttime.addSecs(900)
            if self.current_event is not None or self.current_room is not None:
                talkid = self.core.db.get_talk_between_time(self.current_event, self.current_room,
                                                            starttime.toString(), stoptime.toString())
                if talkid is not None:
                    for i in range(self.mainWidget.talkComboBox.count()):
                        if talkid == self.mainWidget.talkComboBox.model().index(i, 1).data(QtCore.Qt.DisplayRole).toString():
                            self.mainWidget.talkComboBox.setCurrentIndex(i)

    def pause(self, state):
        if (state): # Pause Recording.
            self.core.pause()
            logging.info("Recording paused.")
            self.mainWidget.pauseToolButton.setToolTip(self.resumeString)
            self.mainWidget.statusLabel.setText(self.pausedString)
            self.timer.stop()
        elif self.mainWidget.recordPushButton.isChecked():
            self.core.record()
            logging.info("Recording unpaused.")
            self.mainWidget.pauseToolButton.setToolTip(self.pauseString)
            self.mainWidget.statusLabel.setText(self.recordingString)
            self.timer.start(1000)
            
    def load_backend(self, talk=None):
        if talk is not None: self.core.stop()
        
        self.core.load_backend(self.current_presentation())
        
    def update_timer(self):
        """Updates the Elapsed Time displayed.
        
        Uses the statusLabel for the display.
        """
        time = "%d:%02d" % (self.time_minutes, self.time_seconds)
        self.time_seconds += 1
        if self.time_seconds == 60:
            self.time_seconds = 0
            self.time_minutes += 1
            
        self.mainWidget.statusLabel.setText("Elapsed Time: " + time)
        
    def reset_timer(self):
        """Resets the Elapsed Time."""
        self.time_minutes = 0
        self.time_seconds = 0
        
    def toggle_audio_feedback(self, enabled):
        self.config.audio_feedback = enabled

    ###
    ### Talk Related
    ###
    
    def set_talk_tooltip(self, talk):
        self.mainWidget.talkComboBox.setToolTip(talk)
    
    def load_event_list(self):
        model = self.core.db.get_events_model()
        self.mainWidget.eventComboBox.setModel(model)

    def load_rooms_from_event(self, event):
        #self.disconnect(self.mainWidget.roomComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_talks_from_room)
        
        self.current_event = event

        model = self.core.db.get_rooms_model(self.current_event)
        self.mainWidget.roomComboBox.setModel(model)
        
        #self.connect(self.mainWidget.roomComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_talks_from_room)
        
    def load_dates_from_event_room(self, change):
        event = str(self.mainWidget.eventComboBox.currentText())
        room = str(self.mainWidget.roomComboBox.currentText())
        model = self.core.db.get_dates_from_event_room_model(event, room)
        self.mainWidget.dateComboBox.setModel(model)

    def load_talks_from_date(self, date):
        self.current_room = str(self.mainWidget.roomComboBox.currentText())
        self.current_date = date
        
        model = self.core.db.get_talks_model(self.current_event, self.current_room, self.current_date)
        self.mainWidget.talkComboBox.setModel(model)
        
    ###
    ### Report Failure
    ###
    def show_report_widget(self):
        p = self.current_presentation()
        self.reportWidget.titleLabel2.setText(p.title)
        self.reportWidget.speakerLabel2.setText(p.speaker)
        self.reportWidget.eventLabel2.setText(p.event)
        self.reportWidget.roomLabel2.setText(p.room)
        self.reportWidget.timeLabel2.setText(p.time)
        
        # Get existing report if there is one.
        talk_id = self.current_presentation_id()
        f = self.core.db.get_report(talk_id)
        if f is not None:
            self.reportWidget.commentEdit.setText(f.comment)
            i = self.reportWidget.reportCombo.findText(f.indicator)
            self.reportWidget.reportCombo.setCurrentIndex(i)
            self.reportWidget.releaseCheckBox.setChecked(f.release)
        else:
            self.reportWidget.commentEdit.setText("")
            self.reportWidget.reportCombo.setCurrentIndex(0)
            self.reportWidget.releaseCheckBox.setChecked(False)
        
        self.reportWidget.show()
    
    def report(self):
        talk_id = self.current_presentation_id()
        presentation = self.current_presentation()
        i = self.reportWidget.reportCombo.currentIndex()
        
        failure = Failure(talk_id, self.reportWidget.commentEdit.text(), self.reportWidget.options[i], self.reportWidget.releaseCheckBox.isChecked())
        logging.info("Report Failure: %s, %s, %s, release form? %s" % (talk_id,
                                                                       self.reportWidget.commentEdit.text(),
                                                                       self.reportWidget.options[i],
                                                                       self.reportWidget.releaseCheckBox.isChecked()))
        
        self.core.db.insert_failure(failure)
        self.reportWidget.close()
    
    ###
    ### Misc.
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
            self.visibilityAction.setText(self.showWindowString)
            
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
        """Toggles the visibility of the Recording Main Window."""
        if self.isHidden():
            self.show_window()
            self.visibilityAction.setText(self.hideWindowString)
        else:
            self.hide_window()
            self.visibilityAction.setText(self.showWindowString)

    def toggle_record_button(self):
        self.mainWidget.recordPushButton.toggle()

    def audio_feedback(self, value):
        self.mainWidget.audioSlider.setValue(value)
        
    def open_video_directory(self):
        if sys.platform.startswith("linux"):
            os.system("xdg-open %s" % self.core.config.videodir)
        elif sys.platform.startswith("win32"):
            os.system("explorer %s" % self.core.config.videodir)
        else:
            logging.info("Error: This command is not supported on the current OS.")
    
    def closeEvent(self, event):
        logging.info('Exiting freeseer...')
        event.accept()
        
    def keyPressEvent(self, event):
        logging.debug("Keypressed: %s" % event.key())
        self.core.backend.keyboard_event(event.key())
    
    '''
    Client functions
    '''
    def show_client_widget(self):
        self.current_presentation()
        self.clientWidget.show()
    
    '''
    This function is for handling commands sent from the server to the client
    '''
    def getAction(self):
        message = self.clientWidget.socket.read(self.clientWidget.socket.bytesAvailable())
        if message == 'Record':
            self.mainWidget.standbyPushButton.toggle()
            self.mainWidget.recordPushButton.toggle()
            self.clientWidget.sendMessage('Started recording')
            logging.info("Started recording by server's request")
        elif message == 'Stop':
            self.mainWidget.recordPushButton.toggle()
            logging.info("Stopping recording by server's request")
        elif message == 'Pause' or 'Resume':
            self.mainWidget.pauseToolButton.toggle()
            if message == 'Pause':
                logging.info("Paused recording by server's request")
            elif message == 'Resume':
                logging.info("Resumed recording by server's request")
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = RecordApp()
    main.show()
    sys.exit(app.exec_())
