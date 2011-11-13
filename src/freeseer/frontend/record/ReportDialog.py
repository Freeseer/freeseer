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

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

import logging

from freeseer import project_info
from freeseer.frontend.qtcommon.Resource import resource_rc
from freeseer.framework.core import FreeseerCore
from freeseer.framework.failure import *
__version__= project_info.VERSION


class ReportDialog(QtGui.QWidget):
    """
    Failure report Dialog for the Freeseer Project. 

    """
    def __init__(self, presentation, talk_ID, core, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.current_language = "tr_en_US.qm"
        self.uiTranslator = QtCore.QTranslator()
        self.uiTranslator.load(":/languages/tr_en_US.qm")
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        self.core = core
        self.talk_ID = talk_ID
        self.mainWidget = QtGui.QWidget()
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.infoLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(self.infoLayout)
        self.reportLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.reportLayout)
        self.buttonLayout = QtGui.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)
        
        # Talk infomation
        self.titleLabel = QtGui.QLabel("Title: %s" % presentation.title)
        self.speakerLabel = QtGui.QLabel("Speaker: %s" % presentation.speaker)
        self.eventLabel = QtGui.QLabel("Event: %s" % presentation.event)
        self.roomLabel = QtGui.QLabel("Room: %s" % presentation.room)
        self.timeLabel = QtGui.QLabel("Time: %s" % presentation.time)
        self.infoLayout.addWidget(self.titleLabel)
        self.infoLayout.addWidget(self.speakerLabel)
        self.infoLayout.addWidget(self.eventLabel)
        self.infoLayout.addWidget(self.roomLabel)
        self.infoLayout.addWidget(self.timeLabel)
        
        #Report
        self.commentLabel = QtGui.QLabel("Comment")
        self.commentEdit = QtGui.QLineEdit()
        
        self.reportCombo = QtGui.QComboBox()
        self.options = ['No Audio', 'No Video', 'No Audio/Video']
        for i in self.options:
            self.reportCombo.addItem(i)
        
        self.reportLayout.addWidget(self.commentLabel)
        self.reportLayout.addWidget(self.commentEdit)
        self.reportLayout.addWidget(self.reportCombo)
        
        #Buttons
        self.reportButton = QtGui.QPushButton("Report")
        self.closeButton = QtGui.QPushButton("Close")
        
        self.buttonLayout.addWidget(self.closeButton)
        self.buttonLayout.addWidget(self.reportButton)
        self.connect(self.closeButton, QtCore.SIGNAL("clicked()"), self.close)
        self.connect(self.reportButton, QtCore.SIGNAL("clicked()"), self.report)
        #self.retranslate()
    
    def report(self):
        i = self.reportCombo.currentIndex()
        print self.talk_ID
        print self.commentEdit.text()
        print self.options[i]
        failure = Failure(self.talk_ID, self.commentEdit.text(), self.options[i])
        logging.info("Report failure %s %s %s" % (self.talk_ID, self.commentEdit.text(), self.options[i]))
        self.core.db.insert_failure(failure)
        self.close()
   
    def retranslate(self, language=None):
        if language is not None:
            self.current_language = language
        
        self.uiTranslator.load(":/languages/tr_%s.qm" % self.current_language)