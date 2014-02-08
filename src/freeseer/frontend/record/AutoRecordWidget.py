#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014  Free and Open Source Software Learning Centre
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

from PyQt4.QtGui import QFont
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QKeySequence
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import Qt


class AutoRecordWidget(QWidget):
    """Widget that displays the fullscreen countdown for Freeseer's automated recording mode"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.secs = None
        self.recording = False
        self.flashMillisecs = 1000
        self.flashTimes = [0, 250, 500, 750]

        self.resize(400, 400)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.talkInfoFont = QFont('Serif', 50, QFont.Light)
        self.countdownFont = QFont('Serif', 300, QFont.Light)

        self.talkInfoString = QLabel()
        self.mainLayout.addWidget(self.talkInfoString)
        self.talkInfoString.setFont(self.talkInfoFont)
        self.talkInfoString.setAlignment(Qt.AlignCenter)
        self.talkInfoString.setStyleSheet("QLabel { background-color : white; color : black; }")

        self.countdownString = QLabel()
        self.mainLayout.addWidget(self.countdownString)
        self.countdownString.setFont(self.countdownFont)
        self.countdownString.setAlignment(Qt.AlignCenter)
        self.countdownString.setStyleSheet("QLabel { background-color : white; color : black; }")

        self.countdownTimer = QTimer()
        self.countdownTimer.timeout.connect(self.timertick)

        self.flashTimer = QTimer()
        self.flashTimer.timeout.connect(self.flash_display_text)

        QShortcut(QKeySequence("Esc"), self, self.showNormal)

    def set_recording(self, recording):
        """Sets recording to true or false"""
        self.recording = recording

    def set_display_message(self, title="", speaker=""):
        """Sets the part of the display message on screen that is not related to countdown"""
        if self.recording:
            self.talkInfoString.setText("RECORDING\n\nTime remaining:")
        else:
            self.talkInfoString.setText("NEXT TALK\nTitle: %s\nSpeaker: %s\n\nTime until recording:" % (title, speaker))

    def start_timer(self, secs):
        """Sets how much time to count down and starts the timer"""
        self.secs = secs
        self.countdownTimer.start(1000)

    def start_flash_timer(self):
        """Sets how much time to flash the screen and starts the timer"""
        self.flashMillisecs = 1000
        self.flashTimer.start(50)

    def flash_display_text(self):
        """Sets the flashing talk info and countdown display, decrements flash countdown and stops timer"""
        if self.flashMillisecs in self.flashTimes:
            self.countdownString.setStyleSheet("QLabel { background-color : white; color : black; }")
            self.talkInfoString.setStyleSheet("QLabel { background-color : white; color : black; }")
        else:
            self.countdownString.setStyleSheet("QLabel { background-color : black; color : white; }")
            self.talkInfoString.setStyleSheet("QLabel { background-color : black; color : white; }")
        self.flashMillisecs -= 50
        if self.flashMillisecs < 0:
            self.flashTimer.stop()

    def timertick(self):
        """Sets the countdown display string, decrements countdown, plays alert and stops timer.

        Sets and displays the countdown until the start or end of recording of a talk using a countdown timer.
        The size of one unit of timer tick is one second. Before recording starts, plays an alert sound.
        """
        if self.secs > 120:
            self.countdownString.setText("%d min." % (self.secs / 60 + 1))  # e.g., 5 min
        else:
            self.countdownString.setText("%02d:%02d" % (self.secs / 60, self.secs % 60))  # e.g., 01:36

        # Flash the screen when there is 1 minute and when there is 30 seconds left
        if self.secs == 60 or self.secs == 30:
            self.start_flash_timer()

        # In the last 10 seconds, display countdown in red
        if self.secs <= 10:
            self.countdownString.setStyleSheet("QLabel { background-color : white; color : red; }")

        self.secs -= 1
        if self.secs < 0:
            self.stop_timer()
            self.countdownString.setStyleSheet("QLabel { background-color : white; color : black; }")

    def stop_timer(self):
        """Stops the countdown timer"""
        self.countdownTimer.stop()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = AutoRecordWidget()
    main.show()
    sys.exit(app.exec_())
