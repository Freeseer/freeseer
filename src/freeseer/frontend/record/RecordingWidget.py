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
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QSlider
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout

from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QPushButtonWithDpi
from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QToolButtonWithDpi
from freeseer.frontend.qtcommon.dpi_adapt_qtgui import QWidgetWithDpi
from freeseer.frontend.qtcommon import resource  # noqa


class RecordingWidget(QWidgetWithDpi):
    """Widget containing main recording UI for Freeseer"""

    def __init__(self, parent=None):
        super(RecordingWidget, self).__init__(parent)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/freeseer/logo.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.resize(400, 400)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.setStyleSheet("""
            QToolButton {
                background-color: #D1D1D1;
                border-style: solid;
                border-width: 1px;
                border-radius: 10px;
                border-color: #969696;
                padding: 6px;
            }

            QToolButton:pressed {
                background-color: #A3A2A2;
                border-width: 2px;
                border-color: #707070;
            }

            QToolButton:checked {
                background-color: #A3A2A2;
                border-width: 2px;
                border-color: #707070;
            }

            QToolButton:disabled {
                background-color: #EDEDED;
                border-color: #BFBDBD;
            }

            QToolButton:hover {
                border-width: 2px;
            }
        """)

        boldFont = QFont()
        boldFont.setBold(True)

        fontSize = self.font().pixelSize()
        fontUnit = "px"
        if fontSize == -1:  # Font is set as points, not pixels.
            fontUnit = "pt"
            fontSize = self.font().pointSize()

        # Control bar
        self.controlRow = QHBoxLayout()
        self.mainLayout.addLayout(self.controlRow)

        self.recordIcon = QIcon(":/multimedia/record.png")
        self.stopIcon = QIcon(":/multimedia/stop.png")
        pauseIcon = QIcon(":/multimedia/pause.png")
        playIcon = QIcon(":/multimedia/play.png")
        self.headphoneIcon = QIcon()
        self.headphoneIcon.addPixmap(QPixmap(":/multimedia/headphones.png"), QIcon.Normal, QIcon.Off)

        self.is_recording = False
        self.recordButton = QToolButtonWithDpi()
        self.recordButton.setToolTip("Record")
        self.recordButton.setFixedSize(QSize(60, 40))
        self.recordButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.recordButton.setIcon(self.recordIcon)
        self.recordButton.setEnabled(False)
        self.recordButton.setObjectName("recordButton")
        self.controlRow.addWidget(self.recordButton, 0, Qt.AlignLeft)
        self.connect(self.recordButton, SIGNAL("clicked()"), self.setRecordIcon)

        self.playButton = QToolButtonWithDpi()
        self.playButton.setToolTip("Play last recorded Video")
        self.playButton.setFixedSize(QSize(60, 40))
        self.playButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.playButton.setIcon(playIcon)
        self.playButton.setEnabled(False)
        self.controlRow.addWidget(self.playButton, 0, Qt.AlignLeft)

        self.pauseButton = QToolButtonWithDpi()
        self.pauseButton.setToolTip("Pause")
        self.pauseButton.setIcon(pauseIcon)
        self.pauseButton.setFixedSize(QSize(60, 40))
        self.pauseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pauseButton.setEnabled(False)
        self.pauseButton.setCheckable(True)
        self.controlRow.addWidget(self.pauseButton, 0, Qt.AlignLeft)

        self.controlRow.addSpacerItem(self.qspacer_item_with_dpi(30, 40))
        self.controlRow.addStretch(1)

        self.standbyButton = QPushButtonWithDpi("Standby")
        self.standbyButton.setStyleSheet("""
            QPushButton {{
                color: white;
                background-color: #47a447;
                border-style: solid;
                border-width: 0px;
                border-radius: 10px;
                border-color: #398439;
                font: bold {}{};
                padding: 6px;
            }}

            QPushButton:pressed {{
                background-color: #3E8A3E;
                border-color: #327532;
            }}

            QPushButton:hover {{
                border-width: 2px;
            }}
        """.format(fontSize + 3, fontUnit))
        self.standbyButton.setToolTip("Standby")
        self.standbyButton.setFixedSize(QSize(180, 40))
        self.standbyButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.standbyButton.setCheckable(True)
        self.standbyButton.setObjectName("standbyButton")
        self.controlRow.addWidget(self.standbyButton)

        self.disengageButton = QPushButtonWithDpi("Leave record-mode")
        self.disengageButton.setStyleSheet("""
            QPushButton {{
                color: white;
                background-color: #D14343;
                border-style: solid;
                border-width: 0px;
                border-radius: 10px;
                border-color: #B02C2C;
                font: bold {}{};
                padding: 6px;
            }}

            QPushButton:pressed {{
                background-color: #AD2B2B;
                border-color: #8C2929;
            }}

            QPushButton:hover {{
                border-width: 2px;
            }}

            QPushButton:disabled {{
                background-color: #B89E9E;
        }}
        """.format(fontSize + 3, fontUnit))
        self.disengageButton.setToolTip("Leave record-mode")
        self.disengageButton.setFixedSize(QSize(180, 40))
        self.disengageButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.disengageButton.setHidden(True)
        self.disengageButton.setObjectName("disengageButton")
        self.controlRow.addWidget(self.disengageButton)

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

    def setRecordIcon(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.recordButton.setIcon(self.stopIcon)
        else:
            self.recordButton.setIcon(self.recordIcon)

if __name__ == "__main__":
    import sys
    from QtGui import QApplication
    app = QApplication(sys.argv)
    main = RecordingWidget()
    main.show()
    sys.exit(app.exec_())
