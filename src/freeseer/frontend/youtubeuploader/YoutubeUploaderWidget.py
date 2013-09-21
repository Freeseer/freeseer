#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Alex Pilon (MadMub)
# description: a quick mock up of a simple Youtube upload widget

import sys
from PyQt4 import QtGui, QtCore

from lib.youtube_upload import youtube_upload

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

        # Timer for the animation
        self.timer = QtCore.QBasicTimer()

    # returns the file name via file picker
    def get_fname(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        if fname:
            self.chooseLabel.setText(fname)
        else:
            self.chooseLabel.setText('No file selected')

    # animation for progressbar
    def timerEvent(self, e):
        if youtube_upload.currentProgress >= 100:
            self.timer.stop()
            self.uploadBtn.setText('Finished')
            return
        self.pbar.setValue(youtube_upload.currentProgress)

    # handler for upload
    def upload(self):
        if self.timer.isActive():
            self.timer.stop()
            self.uploadBtn.setText('Start')
        else:
            self.timer.start(100, self)
            self.uploadBtn.setText('Stop')

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = YoutubeUploaderWidget()
    gui.show()
    app.exec_()
