#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Alex Pilon (MadMub)
# description: a quick mock up of a simple Youtube upload widget

import sys
from PyQt4 import QtGui, QtCore

class YoutubeUploaderWidget(QtGui.QWidget):

    def __init__(self):
        # create GUI
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Upload to Youtube')
        # Set the window dimensions
        self.resize(300,75)
        
        # vertical layout for widgets
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        # Choose file label
        self.lbl = QtGui.QLabel('No file selected')
        self.vbox.addWidget(self.lbl)

        # Choose file button
        self.chooseBtn = QtGui.QPushButton('Choose file', self)
        self.vbox.addWidget(self.chooseBtn)
        
        # connect button event to handler get_fname
        self.connect(self.chooseBtn, QtCore.SIGNAL('clicked()'), self.get_fname)

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
        self.step = 0

    def get_fname(self):
        # returns the file name via file picker
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        if fname:
            self.lbl.setText(fname)
        else:
            self.lbl.setText('No file selected')

    def timerEvent(self, e):
        #animation for progressbar
        if self.step >= 100:
            self.timer.stop()
            self.uploadBtn.setText('Finished')
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def upload(self):
        # handler for upload
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