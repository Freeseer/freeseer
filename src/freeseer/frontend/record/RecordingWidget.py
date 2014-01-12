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

"""
@author: Thanh Ha
"""

from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QSlider
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout

from freeseer.frontend.qtcommon import resource  # noqa


class RecordingWidget(QWidget):
    """Widget containing main recording UI for Freeseer"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/freeseer/logo.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(400, 400)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        boldFont = QFont()
        boldFont.setBold(True)

        # Control bar
        self.controlRow = QHBoxLayout()
        self.mainLayout.addLayout(self.controlRow)

        self.standbyIcon = QIcon.fromTheme("system-shutdown")
        recordFallbackIcon = QIcon(":/multimedia/record.png")
        self.recordIcon = QIcon.fromTheme("media-record", recordFallbackIcon)
        stopFallbackIcon = QIcon(":/multimedia/stop.png")
        self.stopIcon = QIcon.fromTheme("media-playback-stop", stopFallbackIcon)
        self.pauseIcon = QIcon.fromTheme("media-playback-pause")
        self.resumeIcon = QIcon.fromTheme("media-playback-start")
        self.headphoneIcon = QIcon()
        self.headphoneIcon.addPixmap(QPixmap(":/multimedia/headphones.png"), QIcon.Normal, QIcon.Off)

        self.standbyPushButton = QPushButton("Standby")
        self.standbyPushButton.setToolTip("Standby")
        self.standbyPushButton.setMinimumSize(QSize(0, 40))
        self.standbyPushButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.standbyPushButton.setIcon(self.standbyIcon)
        self.standbyPushButton.setCheckable(True)
        self.standbyPushButton.setObjectName("standbyButton")
        self.controlRow.addWidget(self.standbyPushButton)

        self.recordPushButton = QPushButton("Record")
        self.recordPushButton.setToolTip("Record")
        self.recordPushButton.setMinimumSize(QSize(0, 40))
        self.recordPushButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.recordPushButton.setIcon(self.recordIcon)
        self.recordPushButton.setHidden(True)
        self.recordPushButton.setEnabled(False)
        self.recordPushButton.setCheckable(True)
        self.recordPushButton.setObjectName("recordButton")
        self.controlRow.addWidget(self.recordPushButton)
        self.connect(self.recordPushButton, SIGNAL("toggled(bool)"), self.setRecordIcon)

        self.pauseToolButton = QToolButton()
        self.pauseToolButton.setText("Pause")
        self.pauseToolButton.setToolTip("Pause")
        self.pauseToolButton.setIcon(self.pauseIcon)
        self.pauseToolButton.setMinimumSize(QSize(40, 40))
        self.pauseToolButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.pauseToolButton.setHidden(True)
        self.pauseToolButton.setEnabled(False)
        self.pauseToolButton.setCheckable(True)
        self.controlRow.addWidget(self.pauseToolButton)
        self.connect(self.pauseToolButton, SIGNAL("toggled(bool)"), self.setPauseIcon)

        playbackIcon = QIcon.fromTheme("video-x-generic")
        self.playPushButton = QPushButton()
        self.playPushButton.setText("Play Video")
        self.playPushButton.setToolTip("Play last recorded Video")
        self.playPushButton.setIcon(playbackIcon)
        self.playPushButton.setMinimumSize(QSize(40, 40))
        self.playPushButton.setMaximumSize(QSize(120, 40))
        self.playPushButton.setHidden(True)
        self.playPushButton.setEnabled(False)
        self.playPushButton.setCheckable(True)
        self.controlRow.addWidget(self.playPushButton)

        # Filter bar
        self.filterBarLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.filterBarLayout)

        self.filterBarLayoutRow_1 = QHBoxLayout()
        self.filterBarLayout.addLayout(self.filterBarLayoutRow_1)
        self.eventLabel = QLabel("Event")
        self.eventLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.eventComboBox = QComboBox()
        self.eventLabel.setBuddy(self.eventComboBox)
        self.roomLabel = QLabel("Room")
        self.roomLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.roomComboBox = QComboBox()
        self.roomLabel.setBuddy(self.roomComboBox)
        self.dateLabel = QLabel("Date")
        self.dateLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.dateComboBox = QComboBox()
        self.dateLabel.setBuddy(self.dateComboBox)
        self.filterBarLayoutRow_1.addWidget(self.eventLabel)
        self.filterBarLayoutRow_1.addWidget(self.eventComboBox)
        self.filterBarLayoutRow_1.addWidget(self.roomLabel)
        self.filterBarLayoutRow_1.addWidget(self.roomComboBox)
        self.filterBarLayoutRow_1.addWidget(self.dateLabel)
        self.filterBarLayoutRow_1.addWidget(self.dateComboBox)

        self.filterBarLayoutRow_2 = QHBoxLayout()
        self.filterBarLayout.addLayout(self.filterBarLayoutRow_2)
        self.talkLabel = QLabel("Talk ")
        self.talkLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.talkComboBox = QComboBox()
        self.talkComboBox.setFont(boldFont)
        self.talkComboBox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.talkComboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.filterBarLayoutRow_2.addWidget(self.talkLabel)
        self.filterBarLayoutRow_2.addWidget(self.talkComboBox)

        # Preview Layout
        self.previewLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.previewLayout)

        self.previewWidget = QWidget()
        self.audioSlider = QSlider()
        self.audioSlider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.audioSlider.setEnabled(False)
        self.previewLayout.addWidget(self.previewWidget)
        self.previewLayout.addWidget(self.audioSlider)

        self.statusLabel = QLabel()
        self.mainLayout.addWidget(self.statusLabel)

        # Audio Feedback Checkbox
        self.audioFeedbackCheckbox = QCheckBox()
        self.audioFeedbackCheckbox.setLayoutDirection(Qt.RightToLeft)
        self.audioFeedbackCheckbox.setIcon(self.headphoneIcon)
        self.audioFeedbackCheckbox.setToolTip("Enable Audio Feedback")
        self.mainLayout.addWidget(self.audioFeedbackCheckbox)

    def setRecordIcon(self, state):
        if state:
            self.recordPushButton.setIcon(self.stopIcon)
        else:
            self.recordPushButton.setIcon(self.recordIcon)

    def setPauseIcon(self, state):
        if state:
            self.pauseToolButton.setIcon(self.resumeIcon)
        else:
            self.pauseToolButton.setIcon(self.pauseIcon)

if __name__ == "__main__":
    import sys
    from QtGui import QApplication
    app = QApplication(sys.argv)
    main = RecordingWidget()
    main.show()
    sys.exit(app.exec_())
