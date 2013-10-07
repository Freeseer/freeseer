#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Alex Pilon <apilo088@gmail.com>

'''
freeseer - vga/presentation capture software

Copyright (C) 2011  Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/Freeseer/freeseer/
'''

import sys
import shlex
import threading

import mutagen.oggvorbis

from PyQt4.QtGui import QMainWindow, QVBoxLayout, QLabel, QApplication, QLineEdit, QLabel, QPushButton, QProgressBar, QFileDialog, QWidget
from PyQt4.QtCore import SIGNAL, QBasicTimer


class UploadWidget(QWidget):

    def __init__(self):
        # create GUI
        QMainWindow.__init__(self)
        self.setWindowTitle('Upload to Youtube')
        # Set the window dimensions
        self.resize(300, 75)

        # vertical layout for widgets
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        # username label
        self.usernameLabel = QLabel('Username:')
        self.vbox.addWidget(self.usernameLabel)

        # username text input
        self.usernameInput = QLineEdit(self)
        self.vbox.addWidget(self.usernameInput)

        # password label
        self.passwordLabel = QLabel('Password:')
        self.vbox.addWidget(self.passwordLabel)

        # password input
        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.vbox.addWidget(self.passwordInput)

        # Choose file label
        self.chooseLabel = QLabel('No file selected')
        self.vbox.addWidget(self.chooseLabel)

        # Choose file button
        self.chooseBtn = QPushButton('Choose file', self)
        self.vbox.addWidget(self.chooseBtn)

        # connect button event to handler get_fname
        self.connect(
            self.chooseBtn, SIGNAL('clicked()'), self.get_fname)

        # Progress bar for uploading file
        self.pbar = QProgressBar(self)
        self.vbox.addWidget(self.pbar)

        # Upload button
        self.uploadBtn = QPushButton('Upload', self)
        self.vbox.addWidget(self.uploadBtn)

        # Connect clicked signal to mock upload animation handler
        #self.connect(self.uploadBtn, SIGNAL('clicked()'), self.upload)

        # Timer for the animation
        self.timer = QBasicTimer()

    # returns the file name via file picker
    def get_fname(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Select file')
        if self.fname:
            self.chooseLabel.setText(self.fname)
        else:
            self.chooseLabel.setText('No file selected')

    # animation for progressbar
    #def timerEvent(self, e):


    # handler for upload
    #def upload(self):


    def uploadToYouTube(self, vfile, email, password):
        # Get the title and description if video is an ogg file
        if vfile.lower().endswith(('.ogg', '.mpg')):
            if vfile.lower().endswith('.ogg'):
                metadata = mutagen.oggvorbis.Open(vfile)
                # print metadata.pprint()
                try:
                    title = metadata["title"][0]
                except KeyError:
                    title = vfile

                try:
                    description = metadata["description"][0]
                except KeyError:
                    description = ""
            else:
                title = vfile
                description = ""
        else:
            print vfile + " is not an ogg or mpg"
            return

        # Default category to education for now
        category = "Education"
        # Call 3rd parth library
        #threading.Thread(target = self.uploader.main, args=[shlex.split("-m" + email + " -p" + password + " -t" + escape(title) + " -c" + category + " " + escape(vfile))]).start()
        # self.uploader.main(shlex.split("-m" + email + " -p" + password +
         #                " -t" + escape(title) + " -c" + category + " " + escape(vfile)))


def escape(s):
    return "'" + s.replace("'", "'\\''") + "'"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = UploadWidget()
    gui.show()
    app.exec_()