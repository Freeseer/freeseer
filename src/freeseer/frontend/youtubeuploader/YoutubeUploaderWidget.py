#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Alex Pilon (MadMub)
# description: Youtube uploader gui

import sys
import shlex
import threading

import mutagen.oggvorbis


from PyQt4 import QtGui, QtCore


class YoutubeUploaderWidget(QtGui.QWidget):

    def __init__(self):
        # create GUI
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Upload to Youtube')
        # Set the window dimensions
        self.resize(300, 75)

        # vertical layout for widgets
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        # username label
        self.usernameLabel = QtGui.QLabel('Username:')
        self.vbox.addWidget(self.usernameLabel)

        # username text input
        self.usernameInput = QtGui.QLineEdit(self)
        self.vbox.addWidget(self.usernameInput)

        # password label
        self.passwordLabel = QtGui.QLabel('Password:')
        self.vbox.addWidget(self.passwordLabel)

        # password input
        self.passwordInput = QtGui.QLineEdit(self)
        self.passwordInput.setEchoMode(QtGui.QLineEdit.Password)
        self.vbox.addWidget(self.passwordInput)

        # Choose file label
        self.chooseLabel = QtGui.QLabel('No file selected')
        self.vbox.addWidget(self.chooseLabel)

        # Choose file button
        self.chooseBtn = QtGui.QPushButton('Choose file', self)
        self.vbox.addWidget(self.chooseBtn)

        # connect button event to handler get_fname
        self.connect(
            self.chooseBtn, QtCore.SIGNAL('clicked()'), self.get_fname)

        # Progress bar for uploading file
        self.pbar = QtGui.QProgressBar(self)
        self.vbox.addWidget(self.pbar)

        # Upload button
        self.uploadBtn = QtGui.QPushButton('Upload', self)
        self.vbox.addWidget(self.uploadBtn)

        # Connect clicked signal to mock upload animation handler
        self.connect(self.uploadBtn, QtCore.SIGNAL('clicked()'), self.upload)

        self.uploader = youtube_upload

        # Timer for the animation
        self.timer = QtCore.QBasicTimer()

    # returns the file name via file picker
    def get_fname(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        if self.fname:
            self.chooseLabel.setText(self.fname)
        else:
            self.chooseLabel.setText('No file selected')

    # animation for progressbar
    def timerEvent(self, e):
        print "hello"
        if self.uploader.currentProgress[0] >= 100:
            self.timer.stop()
            self.uploadBtn.setText('Finished')
            return
        self.pbar.setValue(self.uploader.currentProgress[0])

    # handler for upload
    def upload(self):
        self.uploadToYouTube(
            str(self.fname), str(self.usernameInput.text()), str(self.passwordInput.text()))
        if self.timer.isActive():
            self.timer.stop()
            self.uploadBtn.setText('Start')
        else:
            self.timer.start(100, self)
            self.uploadBtn.setText('Stop')

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
    app = QtGui.QApplication(sys.argv)
    gui = YoutubeUploaderWidget()
    gui.show()
    app.exec_()