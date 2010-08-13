#!/usr/bin/python


# freeseer - vga/presentation capture software
#
#  Copyright (C) 2010  Free and Open Source Software Learning Centre
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

from PyQt4 import QtGui, QtCore
from framework.db_connector import *
from framework.core import *
from framework.qt_area_selector import *
from freeseer_ui_qt import *
from freeseer_about import *

import framework.db_connector
import framework.presentation
import framework.rss_parser



__version__=u'1.9.7'

NAME=u'Freeseer'
DESCRIPTION=u'Freeseer is a video capture utility capable of capturing presentations. It captures video sources such as usb, firewire, or local desktop along with audio and mixes them together to produce a video.'
URL=u'http://github.com/fosslc/freeseer'
COPYRIGHT=u'Copyright (C) 2010 The Free and Open Source Software Learning Centre'
LICENSE_TEXT=u"Freeseer is licensed under the GPL version 3. This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software."
RECORD_BUTTON_ARTIST=u'Sekkyumu'
RECORD_BUTTON_LINK=u'http://sekkyumu.deviantart.com/'
HEADPHONES_ARTIST=u'Ben Fleming'
HEADPHONES_LINK=u'http://mediadesign.deviantart.com/'

ABOUT_INFO = u'<h1>'+NAME+u'</h1>' + \
u'<br><b>Version: ' + __version__ + u'</b>' + \
u'<p>' + DESCRIPTION + u'</p>' + \
u'<p>' + COPYRIGHT + u'</p>' + \
u'<p><a href="'+URL+u'">' + URL + u'</a></p>' \
u'<p>' + LICENSE_TEXT + u'</p>' \
u'<p>Record button graphics by: <a href="' + RECORD_BUTTON_LINK+ u'">' + RECORD_BUTTON_ARTIST + u'</a></p>' \
u'<p>Headphones graphics by: <a href="' + HEADPHONES_LINK+ u'">' + HEADPHONES_ARTIST + u'</a></p>'


class AboutDialog(QtGui.QDialog):
    '''
    About dialog class for displaying app information.
    '''
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_FreeseerAbout()
        self.ui.setupUi(self)
        self.ui.aboutInfo.setText(ABOUT_INFO)

class MainApp(QtGui.QMainWindow):
    '''
    Freeseer main gui class
    '''
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_FreeseerMainWindow()
        self.ui.setupUi(self)
        self.ui.hardwareBox.hide()
        self.statusBar().showMessage('ready')
        self.aboutDialog = AboutDialog()    
        self.ui.editTable.setColumnHidden(3,True)
        
        self.talks_to_save = []
        self.talks_to_delete = []

        self.core = FreeseerCore(self)
        self.db_connection = DB_Connector(self.ui)

        # get supported video sources and enable the UI for supported devices.
        self.configure_supported_video_sources()

        # get available audio sources
        sndsrcs = self.core.get_audio_sources()
        for src in sndsrcs:
            self.ui.audioSourceList.addItem(src)

        self.load_talks()
        self.load_events()
        self.load_rooms()
        self.load_settings()

        # setup systray
        logo = QtGui.QPixmap(":/freeseer/freeseer_logo.png")
        sysIcon = QtGui.QIcon(logo)
        self.systray = QtGui.QSystemTrayIcon(sysIcon)
        self.systray.show()
        self.connect(self.systray, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self._icon_activated)

        # main tab connections
        self.connect(self.ui.eventList, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.filter_by_event)
        self.connect(self.ui.roomList, QtCore.SIGNAL('currentIndexChanged(const QString&)'),self.filter_by_room)
        self.connect(self.ui.recordButton, QtCore.SIGNAL('toggled(bool)'), self.capture)
        self.connect(self.ui.testButton, QtCore.SIGNAL('toggled(bool)'), self.test_sources)
        self.connect(self.ui.audioFeedbackCheckbox, QtCore.SIGNAL('stateChanged(int)'), self.toggle_audio_feedback)

        # configure tab connections
        self.connect(self.ui.videoConfigBox, QtCore.SIGNAL('toggled(bool)'), self.toggle_video_recording)
        self.connect(self.ui.soundConfigBox, QtCore.SIGNAL('toggled(bool)'), self.toggle_audio_recording)
        self.connect(self.ui.videoDeviceList, QtCore.SIGNAL('activated(int)'), self.change_video_device)
        self.connect(self.ui.audioSourceList, QtCore.SIGNAL('currentIndexChanged(int)'), self.change_audio_device)
        
        # connections for video source radio buttons
        self.connect(self.ui.localDesktopButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.recordLocalDesktopButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.recordLocalAreaButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.hardwareButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.usbsrcButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.firewiresrcButton, QtCore.SIGNAL('clicked()'), self.toggle_video_source)
        self.connect(self.ui.areaButton, QtCore.SIGNAL('clicked()'), self.area_select)
        self.connect(self.ui.resetSettingsButton, QtCore.SIGNAL('clicked()'), self.load_settings)
        self.connect(self.ui.applySettingsButton, QtCore.SIGNAL('clicked()'), self.save_settings)
        
        # connections for configure > File Locations
        self.connect(self.ui.videoDirectoryButton, QtCore.SIGNAL('clicked()'), self.browse_video_directory)
        self.connect(self.ui.talksFileButton, QtCore.SIGNAL('clicked()'), self.browse_talksfile)

        # edit talks tab connections
        self.connect(self.ui.addTalkButton, QtCore.SIGNAL('clicked()'), self.add_talk)
        self.connect(self.ui.rssButton, QtCore.SIGNAL('clicked()'), self.add_talk_from_rss)
        self.connect(self.ui.removeTalkButton, QtCore.SIGNAL('clicked()'), self.remove_talk)
        #self.connect(self.ui.saveButton, QtCore.SIGNAL('clicked()'), self.save_talks)
        self.connect(self.ui.resetButton, QtCore.SIGNAL('clicked()'), self.reset)

        # Main Window Connections
        self.connect(self.ui.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        
        # EditTable Connections
        
        self.connect(self.ui.editTable, QtCore.SIGNAL('cellChanged  (int,int)'), self.edit_talk)

        # setup video preview widget
        self.core.preview(True, self.ui.previewWidget.winId())

        # Setup default sources
        self.toggle_video_source()
        self.core.change_soundsrc(str(self.ui.audioSourceList.currentText()))

    def configure_supported_video_sources(self):
        vidsrcs = self.core.get_video_sources()
        for src in vidsrcs:
            if (src == 'desktop'): self.ui.localDesktopButton.setEnabled(True)
            elif (src == 'usb'):
                self.ui.hardwareButton.setEnabled(True)
                self.ui.usbsrcButton.setEnabled(True)
            elif (src == 'firewire'):
                self.ui.hardwareButton.setEnabled(True)
                self.ui.firewiresrcButton.setEnabled(True)
                
        self.videosrc = vidsrcs[0]
        if (self.videosrc == 'desktop'):
            self.ui.localDesktopButton.setChecked(True)
        elif (self.videosrc == 'usb'):
            self.ui.hardwareButton.setChecked(True)
            self.ui.usbsrcButton.setChecked(True)
        elif (self.videosrc == 'firewire'):
            self.ui.hardwareButton.setChecked(True)
            self.ui.firewiresrcButton.setChecked(True)

    def toggle_video_recording(self, state):
        '''
        Enables / Disables video recording depending on if the user has
        checked the video box in configuration mode.
        '''
        self.core.set_video_mode(state)

    def toggle_audio_recording(self, state):
        '''
        Enables / Disables audio recording depending on if the user has
        checked the audio box in configuration mode.
        '''
        self.core.set_audio_mode(state)

    def toggle_video_source(self):
        '''
        Updates the GUI when the user selects a different video source and
        configures core with new video source information
        '''
        # recording the local desktop
        if (self.ui.localDesktopButton.isChecked()): 
            if (self.ui.recordLocalDesktopButton.isChecked()):
                self.videosrc = 'desktop'
            elif (self.ui.recordLocalAreaButton.isChecked()):
                self.videosrc = 'desktop'
                self.core.set_record_area(True)

        # recording from hardware such as usb or fireware device
        elif (self.ui.hardwareButton.isChecked()):
            if (self.ui.usbsrcButton.isChecked()): self.videosrc = 'usb'
            elif (self.ui.firewiresrcButton.isChecked()): self.videosrc = 'firewire'
            else: return

            # add available video devices for selected source
            viddevs = self.core.get_video_devices(self.videosrc)
            self.ui.videoDeviceList.clear()
            for dev in viddevs:
                self.ui.videoDeviceList.addItem(dev)

        # invalid selection (this should never happen)
        else: return

        # finally load the changes into core
        videodev = str(self.ui.videoDeviceList.currentText())
        self.core.change_videosrc(self.videosrc, videodev)
        
    def load_settings(self):
        self.ui.videoDirectoryLineEdit.setText(self.core.config.videodir)
        self.ui.talksFileLineEdit.setText(self.core.config.talksfile)

        if self.core.config.resolution == '0x0':
            resolution = 0
        else:
            resolution = self.ui.resolutionComboBox.findText(self.core.config.resolution)
        if not (resolution < 0): self.ui.resolutionComboBox.setCurrentIndex(resolution)
        
    def save_settings(self):
        self.core.config.videodir = str(self.ui.videoDirectoryLineEdit.text())
        self.core.config.talksdir = str(self.ui.talksFileLineEdit.text())
        self.core.config.resolution = str(self.ui.resolutionComboBox.currentText())
        if self.core.config.resolution == 'NONE':
            self.core.config.resolution = '0x0'
        self.core.config.writeConfig()
        
        self.change_output_resolution()
        
    def browse_video_directory(self):
        directory = self.ui.videoDirectoryLineEdit.text()
        videodir = QtGui.QFileDialog.getExistingDirectory(self, 'Select Video Directory', directory) + '/'
        self.ui.videoDirectoryLineEdit.setText(videodir)
        
    def browse_talksfile(self):
        directory = str(self.ui.talksFileLineEdit.text()).rsplit('/', 1)[0]
        talksfile = QtGui.QFileDialog.getOpenFileName(self, 'Select Talks File', directory, 'Talks File (*.txt)')
        if talksfile:
            self.ui.talksFileLineEdit.setText(talksfile)

    def change_video_device(self):
        '''
        Function for changing video device
        eg. /dev/video1
        '''
        dev = str(self.ui.videoDeviceList.currentText())
        src = self.videosrc
        self.core.logger.log.debug('Changing video device to ' + dev)
        self.core.change_videosrc(src, dev)
        
    def change_output_resolution(self):
        res = str(self.ui.resolutionComboBox.currentText())
        if res == 'NONE':
            s = '0x0'.split('x')
        else:
            s = res.split('x')
        width = s[0]
        height = s[1]
        self.core.change_output_resolution(width, height)
        
    def area_select(self):
        self.area_selector = QtAreaSelector(self)
        self.area_selector.show()
        self.core.logger.log.info('Desktop area selector started.')
        self.hide()
    
    def desktopAreaEvent(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.core.set_recording_area(self.start_x, self.start_y, self.end_x, self.end_y)
        self.core.logger.log.debug('area selector start: %sx%s end: %sx%s' % (self.start_x, self.start_y, self.end_x, self.end_y))
        self.show()

    def change_audio_device(self):
        src = str(self.ui.audioSourceList.currentText())
        self.core.logger.log.debug('Changing audio device to ' + src)
        self.core.change_soundsrc(src)

    def toggle_audio_feedback(self):
        if (self.ui.audioFeedbackCheckbox.isChecked()):
            self.core.audioFeedback(True)
            return
        self.core.audioFeedback(False)

    def capture(self, state):
        '''
        Function for recording and stopping recording.
        '''
        if (state): # Start Recording.
            self.core.record(str(self.ui.talkList.currentText().toUtf8()))
            self.ui.recordButton.setText('Stop')
            self.statusBar().showMessage('recording...')
            
        else: # Stop Recording.
            self.core.stop()
            self.ui.recordButton.setText('Record')
            self.ui.audioFeedbackSlider.setValue(0)
            self.statusBar().showMessage('ready')
            

    def test_sources(self, state):
        # Test video and audio sources
        if (self.ui.audioFeedbackCheckbox.isChecked()):
            self.core.test_sources(state, True, True)
        # Test only video source
        else:
            self.core.test_sources(state, True, False)

    def add_talk(self):
        talk_title = self.ui.titleEdit.text()
        talk_room = self.ui.roomEdit.text()
        talk_speaker = self.ui.presenterEdit.text()
        talk_event = self.ui.eventEdit.text()
        talk_time = self.ui.dateTimeEdit   
                
        # Do not add talks if they are empty strings
        if (len(talk_title) == 0): return   
        
        presentation = framework.presentation.Presentation(str(talk_title),str(talk_speaker),"","",str(talk_event),str(talk_time),str(talk_room))
        
        event_list = self.db_connection.get_talk_events()
        room_list = self.db_connection.get_talk_rooms()
        
        if presentation.event not in event_list and len(presentation.event)>0:
            self.ui.eventList.addItem(presentation.event)
        
        if presentation.room not in room_list and len(presentation.room)>0:
            self.ui.roomList.addItem(presentation.room)
            
        presentation.save_to_db()   
        
        self.ui.editTable.insertRow(self.ui.editTable.rowCount())            
        self.ui.editTable.setItem(self.ui.editTable.rowCount()-1,0,QtGui.QTableWidgetItem(presentation.speaker))
        self.ui.editTable.setItem(self.ui.editTable.rowCount()-1,1,QtGui.QTableWidgetItem(presentation.title))
        self.ui.editTable.setItem(self.ui.editTable.rowCount()-1,2,QtGui.QTableWidgetItem(presentation.room))
        self.ui.editTable.setItem(self.ui.editTable.rowCount()-1,3,QtGui.QTableWidgetItem(self.db_connection.get_presentation_id(presentation)))
                    
        #clean up and add title boxes        
        self.ui.eventEdit.clear()
        self.ui.dateTimeEdit.clear()
        self.ui.roomEdit.clear()
        self.ui.presenterEdit.clear()
        self.ui.titleEdit.clear()

    def remove_talk(self):
        try:
            row_clicked = self.ui.editTable.selectionModel().selection().indexes()[0].row()
        except:
            return
        
        id = self.ui.editTable.item(row_clicked, 3).text() 
        self.db_connection.delete_talk(str(id))
        
        self.ui.editTable.setRowCount(0)
        self.ui.editTable.clearContents()
        
        
        self.load_talks()
        self.load_rooms()
        self.load_events()
        
        self.ui.editTable.resizeRowsToContents()
        
    def reset(self):
        self.db_connection.clear_database()
        self.load_events()
        self.load_rooms()
        self.load_talks()
                  
    def load_talks(self):
        '''
        This method updates the GUI with the available presentation titles.
        '''
        talklist = self.db_connection.get_talk_titles()
        self.ui.talkList.clear()
        self.ui.editTable.clearContents()
        self.ui.editTable.setRowCount(0)        
       
        for talk in talklist:          
            index = self.ui.editTable.rowCount()
            self.ui.editTable.insertRow(index)  
            self.ui.editTable.setRowHeight(index,20)                   
            for i in range(len(talk)):                
                self.ui.editTable.setItem(index,i,QtGui.QTableWidgetItem(unicode(talk[i])))                         
        
        
            item = "%s - %s - %s" % (talk[0],talk[1],talk[2])
            self.ui.talkList.addItem(item)
        self.ui.editTable.resizeRowsToContents()
            
    def load_events(self):
        '''
        This method updates the GUI with the available presentation events.
        '''
        event_list = self.db_connection.get_talk_events()
        self.ui.eventList.clear()
        self.ui.eventList.addItem("All")
        
        for event in event_list:
            if len(event)>0: self.ui.eventList.addItem(event)   
            
    def load_rooms(self):
        '''
        This method updates the GUI with the available presentation rooms.
        '''
        
        room_list = self.db_connection.get_talk_rooms()   
        self.ui.roomList.clear()
        self.ui.roomList.addItem("All")     
        for room in room_list:
            if len(room)>0:    self.ui.roomList.addItem(room)
        

            

    def save_talks(self):
        for item in self.talks_to_save:            
            item.save_to_db()
        
        for item in self.talks_to_delete:
            self.db_connection.delete_talk(item)
            
        del self.talks_to_delete[:]
        del self.talks_to_save[:]
        
        self.db_connection.aux()
        
        #reload filters
        self.load_talks()        
        self.load_events()
        self.load_rooms()

    def _icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.show()
            else: self.hide()

    def coreEvent(self, event_type, value):
        if event_type == 'audio_feedback':
            self.ui.audioFeedbackSlider.setValue(value)

    def closeEvent(self, event):
        self.core.logger.log.info('Exiting freeseer...')
        #self.core.stop()
        event.accept()

    def filter_by_room(self,roomName):
        if not self.db_connection.filter_by_room(roomName):
            self.load_talks()
            
    def filter_by_event(self,eventName):
        if not self.db_connection.filter_by_event(eventName):
            self.load_talks()
    
    def add_talk_from_rss(self):        
        entry = str(self.ui.rssEdit.text())
        a = framework.rss_parser.FeedParser(entry)
        
        if len(a.build_data_dictionary())==0:
            message = QtGui.QMessageBox()     
            message.setText("No data found")
            message.exec_()

        else: 
            for presentation in a.build_data_dictionary():
                talk = framework.presentation.Presentation(presentation["Title"],presentation["Speaker"],"",presentation["Level"],presentation["Event"],presentation["Time"],presentation["Room"])
                db_reference = framework.db_connector.DB_Connector(None)             

                if not db_reference.db_contains(talk):
                    talk.save_to_db()                   

            self.load_talks()
            self.load_events()
            self.load_rooms()
                   
    def edit_talk(self,row,cell):        
        try:
            new_speaker = self.ui.editTable.item(row, 0).text() 
        except:
            new_speaker = ""            
        try:
            new_title = self.ui.editTable.item(row, 1).text() 
        except:
            new_title = ""
        try:
            new_room = self.ui.editTable.item(row, 2).text() 
        except:
            new_room = ""            
        try:
            id = self.ui.editTable.item(row, 3).text() 
        except:
            id = ""             
        try:
            self.db_connection.update_talk(id, new_speaker, new_title, new_room)
        except:
            return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())
