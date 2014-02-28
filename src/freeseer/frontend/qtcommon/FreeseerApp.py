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

from PyQt4.QtCore import QDir
from PyQt4.QtCore import QLocale
from PyQt4.QtCore import QRect
from PyQt4.QtCore import QString
from PyQt4.QtCore import QTextCodec
from PyQt4.QtCore import QTranslator
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QActionGroup
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QPixmap

from freeseer.frontend.qtcommon.AboutDialog import AboutDialog
from freeseer.frontend.qtcommon import resource  # noqa

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

log = logging.getLogger(__name__)


class FreeseerApp(QMainWindow):

    def __init__(self):
        super(FreeseerApp, self).__init__()
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(_fromUtf8(":/freeseer/logo.png")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(self.icon)

        self.aboutDialog = AboutDialog()
        self.aboutDialog.setModal(True)

        #
        # Translator
        #
        self.app = QApplication.instance()
        self.current_language = None
        self.uiTranslator = QTranslator()
        self.uiTranslator.load(":/languages/tr_en_US.qm")
        self.app.installTranslator(self.uiTranslator)
        self.langActionGroup = QActionGroup(self)
        self.langActionGroup.setExclusive(True)
        QTextCodec.setCodecForTr(QTextCodec.codecForName('utf-8'))
        self.connect(self.langActionGroup, SIGNAL('triggered(QAction *)'), self.translate)
        # --- Translator

        #
        # Setup Menubar
        #
        self.menubar = self.menuBar()

        self.menubar.setGeometry(QRect(0, 0, 500, 50))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuLanguage = QMenu(self.menubar)
        self.menuLanguage.setObjectName(_fromUtf8("menuLanguage"))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))

        exitIcon = QIcon.fromTheme("application-exit")
        self.actionExit = QAction(self)
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionExit.setIcon(exitIcon)

        helpIcon = QIcon.fromTheme("help-contents")
        self.actionOnlineHelp = QAction(self)
        self.actionOnlineHelp.setObjectName(_fromUtf8("actionOnlineHelp"))
        self.actionOnlineHelp.setIcon(helpIcon)

        self.actionAbout = QAction(self)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAbout.setIcon(self.icon)

        # Actions
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionOnlineHelp)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.setupLanguageMenu()
        # --- End Menubar

        self.connect(self.actionExit, SIGNAL('triggered()'), self.close)
        self.connect(self.actionAbout, SIGNAL('triggered()'), self.aboutDialog.show)
        self.connect(self.actionOnlineHelp, SIGNAL('triggered()'), self.openOnlineHelp)

        self.retranslateFreeseerApp()
        self.aboutDialog.aboutWidget.retranslate("en_US")

    def openOnlineHelp(self):
        """Opens a link to the Freeseer Online Help"""
        url = QUrl("http://freeseer.readthedocs.org")
        QDesktopServices.openUrl(url)

    def translate(self, action):
        """Translates the GUI via menu action.

        When a language is selected from the language menu, this function is
        called and the language to be changed to is retrieved.
        """
        self.current_language = str(action.data().toString()).strip("tr_").rstrip(".qm")

        log.info("Switching language to: %s" % action.text())
        self.uiTranslator.load(":/languages/tr_%s.qm" % self.current_language)
        self.app.installTranslator(self.uiTranslator)

        self.retranslateFreeseerApp()
        self.aboutDialog.aboutWidget.retranslate(self.current_language)
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
        self.menuFile.setTitle(self.app.translate("FreeseerApp", "&File"))
        self.menuLanguage.setTitle(self.app.translate("FreeseerApp", "&Language"))
        self.menuHelp.setTitle(self.app.translate("FreeseerApp", "&Help"))

        self.actionExit.setText(self.app.translate("FreeseerApp", "&Quit"))
        self.actionAbout.setText(self.app.translate("FreeseerApp", "&About"))
        self.actionOnlineHelp.setText(self.app.translate("FreeseerApp", "Online Documentation"))
        # --- Menubar

    def setupLanguageMenu(self):
        self.languages = QDir(":/languages").entryList()

        if self.current_language is None:
            self.current_language = QLocale.system().name()  # Retrieve Current Locale from the operating system.
            log.debug("Detected user's locale as %s" % self.current_language)

        for language in self.languages:
            translator = QTranslator()  # Create a translator to translate Language Display Text.
            translator.load(":/languages/%s" % language)
            language_display_text = translator.translate("Translation", "Language Display Text")

            languageAction = QAction(self)
            languageAction.setCheckable(True)
            languageAction.setText(language_display_text)
            languageAction.setData(language)
            self.menuLanguage.addAction(languageAction)
            self.langActionGroup.addAction(languageAction)

            if self.current_language == str(language).strip("tr_").rstrip(".qm"):
                languageAction.setChecked(True)
