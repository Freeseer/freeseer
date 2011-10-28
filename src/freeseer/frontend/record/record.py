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
import time

from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer import project_info
from freeseer.framework.core import FreeseerCore
from freeseer.frontend.qtcommon.AboutDialog import AboutDialog
from freeseer.frontend.qtcommon.Resource import resource_rc

from RecordingWidget import RecordingWidget

__version__= project_info.VERSION

class RecordApp(QtGui.QMainWindow):
    '''
    Freeseer main gui class
    '''

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(550, 450)
        
        self.aboutDialog = AboutDialog()
        self.talks_to_save = []
        self.talks_to_delete = []
        
        self.mainWidget = RecordingWidget()
        self.setCentralWidget(self.mainWidget)
        
        self.statusBar().addPermanentWidget(self.mainWidget.statusLabel)
        
        # Initialize geometry, to be used for restoring window positioning.
        self.geometry = None

        self.core = FreeseerCore(self.mainWidget.previewWidget.winId(), self.audio_feedback)
        self.config = self.core.get_config()
        
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
        
        # Actions
        self.menuFile.addAction(self.actionOpenVideoFolder)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
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

        # Main Window Connections
        self.connect(self.actionOpenVideoFolder, QtCore.SIGNAL('triggered()'), self.open_video_directory)
        self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        
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

        self.load_settings()

        # setup spacebar key
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
        self.stopString = self.uiTranslator.translate("RecordApp", "Stop")
        self.hideWindowString = self.uiTranslator.translate("RecordApp", "Hide Main Window")
        self.showWindowString = self.uiTranslator.translate("RecordApp", "Show Main Window")
        
        # Status Bar messages
        self.readyString = self.uiTranslator.translate("RecordApp", "Ready.")
        self.recordingString = self.uiTranslator.translate("RecordApp", "Recording...")
        self.pausedString = self.uiTranslator.translate("RecordApp", "Recording Paused.")
        # --- End Reusable Strings
        
        if self.mainWidget.recordPushButton.isChecked() and self.mainWidget.pauseToolButton.isChecked():
            self.mainWidget.statusLabel.setText(self.pausedString)
        elif self.mainWidget.recordPushButton.isChecked() and (not self.mainWidget.pauseToolButton.isChecked()):
            self.mainWidget.statusLabel.setText(self.recordingString)
        else:
            self.mainWidget.statusLabel.setText(self.readyString)
        
        #
        # Menubar
        #
        self.menuFile.setTitle(self.uiTranslator.translate("RecordApp", "&File"))
        self.menuOptions.setTitle(self.uiTranslator.translate("RecordApp", "&Options"))
        self.menuLanguage.setTitle(self.uiTranslator.translate("RecordApp", "&Language"))
        self.menuHelp.setTitle(self.uiTranslator.translate("RecordApp", "&Help"))
        
        self.actionOpenVideoFolder.setText(self.uiTranslator.translate("RecordApp", "&Open Video Directory"))
        self.actionExit.setText(self.uiTranslator.translate("RecordApp", "&Quit"))
        self.actionAbout.setText(self.uiTranslator.translate("RecordApp", "&About"))
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
        
        self.aboutDialog.retranslate(self.current_language)
        
    def translate(self, action):
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
            
    ###
    ### UI Logic
    ###    
    def load_settings(self): 
        logging.info('Loading settings...')
        
        # Load default language
        actions = self.menuLanguage.actions()
        for action in actions:
            if action.data().toString() == self.config.default_language:
                action.setChecked(True)
                self.translate(action)
                break
        
        # Load Talks as a SQL Data Model
        self.load_event_list()

    def current_presentation(self):
        '''
        Creates a presentation object from the currently selected title on the GUI
        '''
        i = self.mainWidget.talkComboBox.currentIndex()
        p_id = self.mainWidget.talkComboBox.model().index(i, 1).data(QtCore.Qt.DisplayRole).toString()
        return self.core.db.get_presentation(p_id)

    def standby(self, state):
        if (state): # Prepare the pipelines
            self.load_backend()
            self.core.pause()

    def record(self, state):
        '''
        Function for recording and stopping recording.
        '''

        if (state): # Start Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/logo_rec.png")
            sysIcon2 = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon2)
            
            self.core.record()
            self.mainWidget.recordPushButton.setText(self.stopString)
            self.recordAction.setText(self.stopString)
            # check if auto-hide is set and if so hide
            if(self.core.config.auto_hide == True):
                self.hide_window()

            if (self.core.config.delay_recording>0):
                time.sleep(float(self.core.config.delay_recording))

            self.mainWidget.statusLabel.setText(self.recordingString)
            
        else: # Stop Recording.
            logo_rec = QtGui.QPixmap(":/freeseer/logo.png")
            sysIcon = QtGui.QIcon(logo_rec)
            self.systray.setIcon(sysIcon)
            self.core.stop()
            self.mainWidget.pauseToolButton.setChecked(False)
            self.mainWidget.recordPushButton.setText(self.recordString)
            self.recordAction.setText(self.recordString)
            self.mainWidget.audioSlider.setValue(0)
            self.mainWidget.statusLabel.setText(self.readyString)
            
            # Finally set the standby button back to unchecked position.
            self.mainWidget.standbyPushButton.setChecked(False)
            
    def pause(self, state):
        if (state): # Pause Recording.
            self.core.pause()
            logging.info("Recording paused.")
            self.mainWidget.statusLabel.setText(self.pausedString)
        else:
            if self.mainWidget.recordPushButton.isChecked():
                self.core.record()
                logging.info("Recording unpaused.")
                self.mainWidget.statusLabel.setText(self.recordingString)
            
    def load_backend(self, talk=None):
        if talk is not None: self.core.stop()
        
        self.core.load_backend(self.current_presentation())

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
    ### Misc
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
        """
        This function is used to toggle the visibility of the Recording
        Main Window.
        """
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
        else:
            logging.INFO("Error: This command is not supported on the current OS.")

    def closeEvent(self, event):
        logging.info('Exiting freeseer...')
        event.accept()
        
    def keyPressEvent(self, event):
        logging.debug("Keypressed: %s" % event.key())
        self.core.backend.keyboard_event(event.key())

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = RecordApp()
    main.show()
    sys.exit(app.exec_())
