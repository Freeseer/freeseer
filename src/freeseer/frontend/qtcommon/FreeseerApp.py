#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2013  Free and Open Source Software Learning Centre
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

import logging

from PyQt4 import QtGui, QtCore

from freeseer import project_info
from freeseer.frontend.qtcommon.AboutDialog import AboutDialog
from freeseer.frontend.qtcommon.Resource import resource_rc

__version__= project_info.VERSION

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class FreeseerApp(QtGui.QMainWindow):
    
    def __init__(self):
        super(FreeseerApp, self).__init__()
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/freeseer/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)
        
        self.aboutDialog = AboutDialog()
        self.aboutDialog.setModal(True)
        
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
        self.menubar = self.menuBar()
        
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 50))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuLanguage = QtGui.QMenu(self.menubar)
        self.menuLanguage.setObjectName(_fromUtf8("menuLanguage"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        
        exitIcon = QtGui.QIcon.fromTheme("application-exit")
        self.actionExit = QtGui.QAction(self)
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionExit.setIcon(exitIcon)
        
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAbout.setIcon(self.icon)
        
        # Actions
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        self.setupLanguageMenu()
        # --- End Menubar
        
        self.connect(self.actionExit, QtCore.SIGNAL('triggered()'), self.close)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered()'), self.aboutDialog.show)
        
        self.retranslateFreeseerApp()
        self.aboutDialog.retranslate("en_US")
        
    def translate(self, action):
        """Translates the GUI via menu action.

        When a language is selected from the language menu, this function is
        called and the language to be changed to is retrieved.
        """
        self.current_language = str(action.data().toString()).strip("tr_").rstrip(".qm")
        
        logging.info("Switching language to: %s" % action.text())
        self.uiTranslator.load(":/languages/tr_%s.qm" % self.current_language)

        self.retranslateFreeseerApp()
        self.aboutDialog.retranslate(self.current_language)
        self.retranslate()
        
    def retranslate(self):
        """
        Reimplement this function to provide translations to your app.
        """
        pass
        
    def retranslateFreeseerApp(self):
        #
        # Menubar
        #
        self.menuFile.setTitle(self.uiTranslator.translate("FreeseerApp", "&File"))
        self.menuLanguage.setTitle(self.uiTranslator.translate("FreeseerApp", "&Language"))
        self.menuHelp.setTitle(self.uiTranslator.translate("FreeseerApp", "&Help"))
        
        self.actionExit.setText(self.uiTranslator.translate("FreeseerApp", "&Quit"))
        self.actionAbout.setText(self.uiTranslator.translate("FreeseerApp", "&About"))
        # --- Menubar
        
    def setupLanguageMenu(self):
        self.languages = QtCore.QDir(":/languages").entryList()
        
        if self.current_language is None:
            self.current_language = QtCore.QLocale.system().name()  # Retrieve Current Locale from the operating system.
            logging.debug("Detected user's locale as %s" % self.current_language)
        
        for language in self.languages:
            translator = QtCore.QTranslator()  # Create a translator to translate Language Display Text.
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
