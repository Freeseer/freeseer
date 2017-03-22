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

import logging
import os
import subprocess
import sys
import functools

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QCursor

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer.framework.failure import Failure
from freeseer.framework.util import get_free_space
from freeseer.frontend.qtcommon.FreeseerApp import FreeseerApp
from freeseer.frontend.qtcommon.log import LogStatusWidget
from freeseer.frontend.configtool.configtool import ConfigToolApp
from freeseer.frontend.record.RecordingController import RecordingController
from freeseer.frontend.record.RecordingWidget import RecordingWidget
from freeseer.frontend.record.AutoRecordWidget import AutoRecordWidget
from freeseer.frontend.record.ReportDialog import ReportDialog
from freeseer.frontend.talkeditor.talkeditor import TalkEditorApp

log = logging.getLogger(__name__)


class RecordApp(FreeseerApp):
    """Freeseer's main GUI class."""

    def __init__(self, profile, config):
        super(RecordApp, self).__init__(config)

        self.db = profile.get_database()
        self.controller = RecordingController(profile, self.db, self.config)

        self.recently_recorded_video = None

        self.resize(550, 450)

        # Setup custom widgets
        self.mainWidget = RecordingWidget()
        self.setCentralWidget(self.mainWidget)
        self.reportWidget = ReportDialog()
        self.reportWidget.setModal(True)
        self.autoRecordWidget = AutoRecordWidget()
        self.configToolApp = ConfigToolApp(profile, config)
        self.configToolApp.setWindowModality(QtCore.Qt.ApplicationModal)
        self.configToolApp.setWindowFlags(QtCore.Qt.Dialog)
        self.talkEditorApp = TalkEditorApp(self.config, self.db)
        self.talkEditorApp.setWindowModality(QtCore.Qt.ApplicationModal)
        self.talkEditorApp.setWindowFlags(QtCore.Qt.Dialog)

        self.logStatusWidget = LogStatusWidget(self.logDialog)
        self.statusBar().addPermanentWidget(self.logStatusWidget, 1)
        self.statusBar().addPermanentWidget(self.mainWidget.statusLabel)

        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None
        self.current_event = None
        self.current_room = None
        self.controller.set_window_id(self.mainWidget.previewWidget.winId())
        self.controller.set_audio_feedback_handler(self.audio_feedback)

        # Set timer for recording how much time elapsed during a recording
        self.reset_timer()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # Initialize variables for auto-recording
        self.singleID = None
        self.timeUntilStart = None
        self.timeUntilEnd = None
        self.autoTalks = None
        self.recorded = False
        self.beforeStartTimer = QtCore.QTimer(self)
        self.beforeStartTimer.timeout.connect(self.start_single_record)
        self.beforeEndTimer = QtCore.QTimer(self)
        self.beforeEndTimer.timeout.connect(self.single_auto_record)

        #
        # Setup Menubar
        #

        # Build the options Menu, TalkEditor and ConfigTool
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menubar.insertMenu(self.menuHelp.menuAction(), self.menuOptions)
        self.actionConfigTool = QtGui.QAction(self)
        self.actionConfigTool.setShortcut("Ctrl+C")
        self.actionConfigTool.setObjectName(_fromUtf8("actionConfigTool"))
        self.actionTalkEditor = QtGui.QAction(self)
        self.actionTalkEditor.setShortcut("Ctrl+E")
        self.actionTalkEditor.setObjectName(_fromUtf8("actionTalkEditor"))
        self.actionAutoRecord = QtGui.QAction(self)
        leaveButtonShortcut = "Ctrl+R"
        self.actionAutoRecord.setShortcut(leaveButtonShortcut)
        self.actionAutoRecord.setCheckable(True)
        self.actionAutoRecord.setObjectName(_fromUtf8("actionAutoRecord"))
        self.menuOptions.addAction(self.actionConfigTool)
        self.menuOptions.addAction(self.actionTalkEditor)
        self.menuOptions.addAction(self.actionAutoRecord)

        folderIcon = QtGui.QIcon.fromTheme("folder")
        self.actionOpenVideoFolder = QtGui.QAction(self)
        self.actionOpenVideoFolder.setShortcut("Ctrl+O")
        self.actionOpenVideoFolder.setObjectName(_fromUtf8("actionOpenVideoFolder"))
        self.actionOpenVideoFolder.setIcon(folderIcon)

        self.actionReport = QtGui.QAction(self)
        self.actionReport.setObjectName(_fromUtf8("actionReport"))

        # Actions
        self.menuFile.insertAction(self.actionExit, self.actionOpenVideoFolder)
        self.menuHelp.addAction(self.actionReport)
        # --- End Menubar

        #
        # Systray Setup
        #
        self.systray = QtGui.QSystemTrayIcon(self.icon)
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
        self.connect(self.mainWidget.standbyButton, QtCore.SIGNAL("toggled(bool)"), self.standby)
        self.connect(self.mainWidget.disengageButton, QtCore.SIGNAL("clicked()"), functools.partial(self.standby, state=False))
        self.connect(self.mainWidget.recordButton, QtCore.SIGNAL('clicked()'), self.record)
        self.connect(self.mainWidget.pauseButton, QtCore.SIGNAL('toggled(bool)'), self.pause)
        self.connect(self.mainWidget.audioFeedbackCheckbox, QtCore.SIGNAL('toggled(bool)'), self.toggle_audio_feedback)
        self.connect(self.mainWidget.playButton, QtCore.SIGNAL('clicked()'), self.play_video)

        self.connect(self.autoRecordWidget.leaveButton, QtCore.SIGNAL('clicked()'), functools.partial(self.auto_record, state=False))
        self.autoRecordWidget.leaveButton.setShortcut(leaveButtonShortcut)

        # Main Window Connections
        self.connect(self.actionConfigTool, QtCore.SIGNAL('triggered()'), self.open_configtool)
        self.connect(self.actionTalkEditor, QtCore.SIGNAL('triggered()'), self.open_talkeditor)
        self.connect(self.actionAutoRecord, QtCore.SIGNAL('toggled(bool)'), self.auto_record)
        self.connect(self.actionOpenVideoFolder, QtCore.SIGNAL('triggered()'), self.open_video_directory)
        self.connect(self.actionReport, QtCore.SIGNAL('triggered()'), self.show_report_widget)

        #
        # ReportWidget Connections
        #
        self.connect(self.reportWidget.reportButton, QtCore.SIGNAL("clicked()"), self.report)

        self.load_settings()

        # Setup spacebar key.
        self.mainWidget.pauseButton.setShortcut(QtCore.Qt.Key_Space)
        self.mainWidget.pauseButton.setFocus()

        self.retranslate()

    ###
    ### Translation Related
    ###
    def retranslate(self):
        self.setWindowTitle(self.app.translate("RecordApp", "Freeseer - portable presentation recording station"))
        #
        # Reusable Strings
        #
        self.standbyString = self.app.translate("RecordApp", "Standby")
        self.disengageString = self.app.translate("RecordApp", "Leave record-mode")
        self.standbyTooltipString = self.app.translate("RecordApp", "Sets up the system for recording")
        self.disengageTooltipString = self.app.translate("RecordApp", "Go back to edit talk information or select a different talk")
        self.autoRecordString = self.app.translate("RecordApp", "Auto Record")
        self.recordString = self.app.translate("RecordApp", "Record")
        self.pauseString = self.app.translate("RecordApp", "Pause")
        self.resumeString = self.app.translate("RecordApp", "Resume")
        self.stopString = self.app.translate("RecordApp", "Stop")
        self.stopAutoString = self.app.translate("RecordApp", "Stop Auto Record")
        self.hideWindowString = self.app.translate("RecordApp", "Hide Main Window")
        self.showWindowString = self.app.translate("RecordApp", "Show Main Window")
        self.playVideoString = self.app.translate("RecordApp", "Play")

        # Status Bar messages
        self.idleString = self.app.translate("RecordApp", "Idle.")
        self.readyString = self.app.translate("RecordApp", "Ready.")
        self.recordingString = self.app.translate("RecordApp", "Recording")
        self.pausedString = self.app.translate("RecordApp", "Recording Paused.")
        self.freeSpaceString = self.app.translate("RecordApp", "Free Space:")
        self.elapsedTimeString = self.app.translate("RecordApp", "Elapsed Time:")
        # --- End Reusable Strings

        if self.mainWidget.is_recording and self.mainWidget.pauseButton.isChecked():
            self.mainWidget.statusLabel.setText(self.pausedString)
        elif self.mainWidget.is_recording and (not self.mainWidget.pauseButton.isChecked()):
            self.mainWidget.statusLabel.setText(self.recordingString)
        elif self.mainWidget.standbyButton.isChecked():
            self.mainWidget.statusLabel.setText(self.readyString)
        elif self.actionAutoRecord.isChecked():
            self.mainWidget.statusLabel.setText(self.autoRecordString)
        else:
            self.mainWidget.statusLabel.setText(u"{} {} --- {} ".format(self.freeSpaceString,
                                                                        get_free_space(self.config.videodir),
                                                                        self.idleString))

        #
        # Menubar
        #
        self.menuOptions.setTitle(self.app.translate("RecordApp", "&Options"))
        self.actionConfigTool.setText(self.app.translate("RecordApp", "&Configuration"))
        self.actionTalkEditor.setText(self.app.translate("RecordApp", "&Edit Talks"))
        self.actionAutoRecord.setText(self.autoRecordString)
        self.actionOpenVideoFolder.setText(self.app.translate("RecordApp", "&Open Video Directory"))
        self.actionReport.setText(self.app.translate("RecordApp", "&Report"))
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
        self.mainWidget.disengageButton.setText(self.disengageString)
        self.mainWidget.standbyButton.setText(self.standbyString)
        self.mainWidget.standbyButton.setToolTip(self.standbyTooltipString)
        self.mainWidget.disengageButton.setToolTip(self.disengageTooltipString)
        if self.mainWidget.is_recording:
            self.mainWidget.recordButton.setToolTip(self.stopString)
        else:
            self.mainWidget.recordButton.setToolTip(self.recordString)
        self.mainWidget.pauseButton.setText(self.pauseString)
        self.mainWidget.pauseButton.setToolTip(self.pauseString)
        self.mainWidget.eventLabel.setText(self.app.translate("RecordApp", "Event"))
        self.mainWidget.roomLabel.setText(self.app.translate("RecordApp", "Room"))
        self.mainWidget.dateLabel.setText(self.app.translate("RecordApp", "Date"))
        self.mainWidget.talkLabel.setText(self.app.translate("RecordApp", "Talk"))
        # --- End RecordingWidget

        #
        # ReportWidget
        #
        self.reportWidget.setWindowTitle(self.app.translate("RecordApp", "Reporting Tool"))
        self.reportWidget.titleLabel.setText(self.app.translate("RecordApp", "Title:"))
        self.reportWidget.speakerLabel.setText(self.app.translate("RecordApp", "Speaker:"))
        self.reportWidget.eventLabel.setText(self.app.translate("RecordApp", "Event:"))
        self.reportWidget.roomLabel.setText(self.app.translate("RecordApp", "Room:"))
        self.reportWidget.startTimeLabel.setText(self.app.translate("RecordApp", "Start Time:"))
        self.reportWidget.endTimeLabel.setText(self.app.translate("RecordApp", "End Time:"))
        self.reportWidget.commentLabel.setText(self.app.translate("RecordApp", "Comment"))
        self.reportWidget.releaseCheckBox.setText(self.app.translate("RecordApp", "Release Received"))
        self.reportWidget.closeButton.setText(self.app.translate("RecordApp", "Close"))
        self.reportWidget.reportButton.setText(self.app.translate("RecordApp", "Report"))

        # Logic for translating the report options
        noissues = self.app.translate("RecordApp", "No Issues")
        noaudio = self.app.translate("RecordApp", "No Audio")
        novideo = self.app.translate("RecordApp", "No Video")
        noaudiovideo = self.app.translate("RecordApp", "No Audio/Video")
        self.reportWidget.options = [noissues, noaudio, novideo, noaudiovideo]
        self.reportWidget.reportCombo.clear()
        for i in self.reportWidget.options:
            self.reportWidget.reportCombo.addItem(i)
        # --- End ReportWidget

        self.logStatusWidget.retranslate()

    ###
    ### UI Logic
    ###

    def load_settings(self):
        """Load settings for Freeseer"""
        log.info('Loading settings...')

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
        return self.db.get_presentation(self.current_presentation_id())

    def current_presentation_id(self):
        """Returns the current selected presentation ID."""
        i = self.mainWidget.talkComboBox.currentIndex()
        return self.mainWidget.talkComboBox.model().index(i, 1).data(QtCore.Qt.DisplayRole).toString()

    def standby(self, state):
        """Prepares the GStreamer pipelines for recording

        Sets the pipeline to paused state so that initiating a recording
        does not have a delay due to GStreamer initialization.
        """
        def toggle_gui(state):
            """Toggles GUI components when standby is pressed"""
            if state:
                self.mainWidget.standbyButton.setHidden(state)
                self.mainWidget.disengageButton.setVisible(state)
            else:
                self.mainWidget.disengageButton.setVisible(state)
                self.mainWidget.standbyButton.setHidden(state)

            self.mainWidget.recordButton.setEnabled(state)
            self.mainWidget.eventComboBox.setDisabled(state)
            self.mainWidget.roomComboBox.setDisabled(state)
            self.mainWidget.dateComboBox.setDisabled(state)
            self.mainWidget.talkComboBox.setDisabled(state)
            self.mainWidget.audioFeedbackCheckbox.setDisabled(state)

        if state:  # Prepare the pipelines
            if self.load_backend():
                toggle_gui(True)
                self.controller.pause()
                self.mainWidget.statusLabel.setText(u"{} {} --- {} ".format(self.freeSpaceString,
                                                                            get_free_space(self.config.videodir),
                                                                            self.readyString))
            else:
                toggle_gui(False)
                self.mainWidget.standbyButton.setChecked(False)
        else:
            toggle_gui(False)
            self.controller.stop()
            self.mainWidget.standbyButton.setChecked(False)

        self.mainWidget.playButton.setEnabled(False)

    def record(self):
        """The logic for recording and stopping recording."""

        if self.mainWidget.is_recording:  # Start Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/logo_rec.png")
            sysIcon2 = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon2)
            self.controller.record()
            self.mainWidget.recordButton.setToolTip(self.stopString)
            self.mainWidget.disengageButton.setEnabled(False)
            self.mainWidget.pauseButton.setEnabled(True)
            self.recordAction.setText(self.stopString)

            # Hide if auto-hide is set.
            if self.config.auto_hide:
                self.hide_window()
                self.visibilityAction.setText(self.showWindowString)
                log.debug('auto-hide is enabled, main window is now hidden in systray.')

            # Start timer.
            self.timer.start(1000)

        else:  # Stop Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/logo.png")
            sysIcon = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon)
            self.controller.stop()
            self.mainWidget.pauseButton.setChecked(False)
            self.mainWidget.recordButton.setToolTip(self.recordString)
            self.mainWidget.disengageButton.setEnabled(True)
            self.mainWidget.pauseButton.setEnabled(False)
            self.recordAction.setText(self.recordString)
            self.mainWidget.audioSlider.setValue(0)
            self.mainWidget.statusLabel.setText(u"{} {} --- {} ".format(self.freeSpaceString,
                                                                        get_free_space(self.config.videodir),
                                                                        self.idleString))

            # Finally set the standby button back to unchecked position.
            self.standby(False)

            # Stop and reset timer.
            self.timer.stop()
            self.reset_timer()

            #Show playback button
            self.mainWidget.playButton.setVisible(True)
            self.mainWidget.playButton.setEnabled(True)

            # Select next talk if there is one within 15 minutes.
            if self.current_event and self.current_room:
                starttime = QtCore.QDateTime().currentDateTime()
                stoptime = starttime.addSecs(900)
                talkid = self.db.get_talk_between_time(self.current_event, self.current_room,
                                                       starttime.toString(), stoptime.toString())

                if talkid is not None:
                    for i in range(self.mainWidget.talkComboBox.count()):
                        if talkid == self.mainWidget.talkComboBox.model().index(i, 1).data(QtCore.Qt.DisplayRole).toString():
                            self.mainWidget.talkComboBox.setCurrentIndex(i)

    def _enable_disable_gui(self, state):
        """Disables GUI components when Auto Record is pressed, and enables them when Auto Record is released"""
        self.mainWidget.standbyButton.setDisabled(state)
        self.mainWidget.eventComboBox.setDisabled(state)
        self.mainWidget.roomComboBox.setDisabled(state)
        self.mainWidget.dateComboBox.setDisabled(state)
        self.mainWidget.talkComboBox.setDisabled(state)
        self.mainWidget.audioFeedbackCheckbox.setDisabled(state)

    def stop_auto_record_gui(self):
        """Sets the gui for stopping the auto record"""
        self.autoRecordWidget.stop_timer()
        self.autoRecordWidget.close()
        self._enable_disable_gui(False)
        self.recorded = False
        self.actionAutoRecord.setChecked(False)

    def auto_record(self, state):
        """Starts automated recording"""
        if state:
            # If there is a room selected, then it's possible to auto-record
            if self.current_room:
                self.autoTalks = self.db.get_talks_by_room_and_time(self.current_room)
                # Start recording if there are talks in database that can be auto-recorded
                if self.autoTalks.next():
                    # Set the cursor back to before the first record so that single_auto_record works properly
                    self.autoTalks.previous()
                    self._enable_disable_gui(True)
                    self.single_auto_record()
                else:
                    # Dialog for no talks to auto-record
                    QtGui.QMessageBox.information(self, 'No Talks to Record',
                        'There are no upcoming talks to auto-record in this room', QtGui.QMessageBox.Ok)
                    self.actionAutoRecord.setChecked(False)

            else:
                # Dialog that pops up when no room is selected
                QtGui.QMessageBox.information(self, 'No Room Selected',
                    'Please select a room to auto-record', QtGui.QMessageBox.Ok)
                self.actionAutoRecord.setChecked(False)
        else:
            self.beforeStartTimer.stop()
            self.beforeEndTimer.stop()
            self.controller.stop()
            self.stop_auto_record_gui()

        self.mainWidget.playButton.setEnabled(False)

    def single_auto_record(self):
        """Completes one display and record cycle of the auto-record feature.

        Stops the recording of the last talk if it exists, displays the countdown until the start of
        the next talk, and when the talk begins, records the talk while displaying the countdown until
        the end of the talk.
        """
        if self.recorded:
            self.controller.stop()
            self.recorded = False
            log.debug("Auto-recording for the current talk stopped.")

        if self.autoTalks.next():
            starttime = QtCore.QTime.fromString(self.autoTalks.value(8).toString())
            endtime = QtCore.QTime.fromString(self.autoTalks.value(9).toString())
            currenttime = QtCore.QTime.currentTime()

            if currenttime <= starttime:
                self.singleID = self.autoTalks.value(0).toString()
                title = self.autoTalks.value(1).toString()
                speaker = self.autoTalks.value(2).toString()

                # Time (in seconds) until recording for the talk starts
                self.timeUntilStart = currenttime.secsTo(starttime)
                # Time (in seconds) from the starttime to endtime of this talk
                self.timeUntilEnd = starttime.secsTo(endtime)

                # Display fullscreen countdown and talk info until talk starts
                self.autoRecordWidget.set_recording(False)
                self.autoRecordWidget.set_display_message(title, speaker)
                self.autoRecordWidget.start_timer(self.timeUntilStart)
                self.autoRecordWidget.showFullScreen()

                # Wait for talk to start, then change display and start recording
                self.beforeStartTimer.setInterval((self.timeUntilStart + 1) * 1000)
                self.beforeStartTimer.setSingleShot(True)
                self.beforeStartTimer.start()
            else:
                # Start time has already passed, so move on to next talk
                self.single_auto_record()
        else:
            self.stop_auto_record_gui()

    def start_single_record(self):
        """Begins the auto-recording of a single talk while displaying the countdown on screen"""
        self.autoRecordWidget.set_recording(True)
        self.autoRecordWidget.set_display_message()
        self.autoRecordWidget.start_timer(self.timeUntilEnd)
        if self.controller.record_talk_id(self.singleID):
            log.debug("Auto-recording for the current talk started.")
            self.recorded = True
        self.beforeEndTimer.setInterval((self.timeUntilEnd + 1) * 1000)
        self.beforeEndTimer.setSingleShot(True)
        self.beforeEndTimer.start()

    def pause(self, state):
        """Pause the recording"""
        if state:  # Pause Recording.
            self.controller.pause()
            log.info("Recording paused.")
            self.mainWidget.pauseButton.setToolTip(self.resumeString)
            self.mainWidget.statusLabel.setText(self.pausedString)
            self.timer.stop()
        elif self.mainWidget.is_recording:
            self.controller.record()
            log.info("Recording unpaused.")
            self.mainWidget.pauseButton.setToolTip(self.pauseString)
            self.timer.start(1000)

    def load_backend(self):
        """Prepares the backend for recording"""
        if self.current_presentation():
            self.mainWidget.recordPushButton.setEnabled(True)
            self.mainWidget.standbyPushButton.setToolTip(self.standbyString)
            presentation = self.current_presentation()
            self.recently_recorded_video = self.controller.load_backend_with_presentation(presentation)

        # If current presentation is non-existent (empty talk database)
        # disable Record button and set tooltip
        else:
            self.mainWidget.recordPushButton.setEnabled(False)
            self.mainWidget.standbyPushButton.setToolTip('No presentations available')
            return False

        if self.recently_recorded_video:
            return True
        else:
            return False  # Error something failed while loading the backend

    def update_timer(self):
        """Updates the Elapsed Time displayed.

        Uses the statusLabel for the display.
        """
        frmt_time = "%d:%02d" % (self.time_minutes, self.time_seconds)
        self.time_seconds += 1
        if self.time_seconds == 60:
            self.time_seconds = 0
            self.time_minutes += 1

        self.mainWidget.statusLabel.setText(u"{} {} --- {} {} --- {}".format(self.elapsedTimeString,
                                                                             frmt_time,
                                                                             self.freeSpaceString,
                                                                             get_free_space(self.config.videodir),
                                                                             self.recordingString))

    def reset_timer(self):
        """Resets the Elapsed Time."""
        self.time_minutes = 0
        self.time_seconds = 0

    def toggle_audio_feedback(self, enabled):
        """Enables or disables audio feedback according to checkbox state"""
        self.config.audio_feedback = enabled

    ###
    ### Talk Related
    ###

    def set_talk_tooltip(self, talk):
        self.mainWidget.talkComboBox.setToolTip(talk)

    def load_event_list(self):
        model = self.db.get_events_model()
        self.mainWidget.eventComboBox.setModel(model)

    def load_rooms_from_event(self, event):
        #self.disconnect(self.mainWidget.roomComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_talks_from_room)

        self.current_event = event

        model = self.db.get_rooms_model(self.current_event)
        self.mainWidget.roomComboBox.setModel(model)

        #self.connect(self.mainWidget.roomComboBox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.load_talks_from_room)

    def load_dates_from_event_room(self, change):
        event = str(self.mainWidget.eventComboBox.currentText())
        room = str(self.mainWidget.roomComboBox.currentText())
        model = self.db.get_dates_from_event_room_model(event, room)
        self.mainWidget.dateComboBox.setModel(model)

    def load_talks_from_date(self, date):
        self.current_room = str(self.mainWidget.roomComboBox.currentText())
        self.current_date = date

        model = self.db.get_talks_model(self.current_event, self.current_room, self.current_date)
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
        self.reportWidget.startTimeLabel2.setText(p.startTime)
        self.reportWidget.endTimeLabel2.setText(p.endTime)

        # Get existing report if there is one.
        talk_id = self.current_presentation_id()
        f = self.db.get_report(talk_id)
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
        i = self.reportWidget.reportCombo.currentIndex()

        failure = Failure(talk_id, self.reportWidget.commentEdit.text(), self.reportWidget.options[i], self.reportWidget.releaseCheckBox.isChecked())
        log.info("Report Failure: %s, %s, %s, release form? %s" % (talk_id,
                                                                   self.reportWidget.commentEdit.text(),
                                                                   self.reportWidget.options[i],
                                                                   self.reportWidget.releaseCheckBox.isChecked()))

        self.db.insert_failure(failure)
        self.reportWidget.close()

    ###
    ### Misc.
    ###
    def _icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.systray.menu.popup(QCursor.pos())
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.toggle_record_button()

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
        self.mainWidget.standbyButton.toggle()
        self.mainWidget.recordButton.toggle()

    def audio_feedback(self, value):
        self.mainWidget.audioSlider.setValue(value)

    def open_video_directory(self):
        if sys.platform.startswith("linux"):
            os.system("xdg-open %s" % self.config.videodir)
        elif sys.platform.startswith("win32"):
            os.system("explorer %s" % self.config.videodir)
        else:
            log.info("Error: This command is not supported on the current OS.")

    def closeEvent(self, event):
        log.info('Exiting freeseer...')
        event.accept()

    '''
    This function plays the most recently recorded video
    '''
    def play_video(self):
        if sys.platform.startswith("linux"):
            subprocess.call(["xdg-open", "{}/{}".format(self.config.videodir, self.recently_recorded_video)])
        if sys.platform.startswith("win32"):
            os.system("start {}".format(os.path.join(self.config.videodir, self.recently_recorded_video)))

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
            self.mainWidget.standbyButton.toggle()
            self.mainWidget.recordButton.toggle()
            self.clientWidget.sendMessage('Started recording')
            log.info("Started recording by server's request")
        elif message == 'Stop':
            self.mainWidget.recordButton.toggle()
            log.info("Stopping recording by server's request")
        elif message == 'Pause' or 'Resume':
            self.mainWidget.pauseButton.toggle()
            if message == 'Pause':
                log.info("Paused recording by server's request")
            elif message == 'Resume':
                log.info("Resumed recording by server's request")

    ###
    ### Utility
    ###
    def open_configtool(self):
        self.configToolApp.show()

    def open_talkeditor(self):
        self.talkEditorApp.show()
        self.load_event_list()
