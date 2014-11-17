#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
freeseer - vga/presentation capture software

 Copyright (C) 2014  Free and Open Source Software Learning Centre
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

@author: Faraz Sherwani
'''

import functools
import logging

from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QSlider
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QStandardItem
from PyQt4.QtGui import QStandardItemModel
from PyQt4.QtGui import QTableView
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

from freeseer.frontend.qtcommon.widgets import ClickableLabel
from freeseer.frontend.qtcommon import resource  # noqa


class LogDialog(QDialog):
    """LogDialog for the Freeseer project.

    It is the dialog window for the log.
    There is an instance for every FreeseerApp.
    It has a LogHandler which calls LogDialog's
    message() method when a new log message is received.
    The call to message() causes a call to add_entry()
    which adds the information to a new row in the table.
    """

    def __init__(self, parent=None):
        super(LogDialog, self).__init__(parent)

        self.resize(800, 500)

        self.app = QApplication.instance()

        icon = QIcon()
        icon.addPixmap(QPixmap(_fromUtf8(":/freeseer/logo.png")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.level = 0
        self.handler = LogHandler()

        self.table_model = QStandardItemModel(0, 5)
        header_names = ["Date", "Level", "Module", "Message", "LevelNo"]
        date_column = header_names.index("Date")
        level_column = header_names.index("Level")
        module_column = header_names.index("Module")
        self.level_num_column = header_names.index("LevelNo")
        self.table_model.setHorizontalHeaderLabels(header_names)

        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setColumnWidth(date_column, 125)
        self.table_view.setColumnWidth(level_column, 60)
        self.table_view.setColumnWidth(module_column, 250)
        self.table_view.setColumnHidden(self.level_num_column, True)
        self.table_view.setShowGrid(False)
        self.table_view.horizontalHeader().setClickable(False)
        self.table_view.verticalHeader().hide()
        self.table_view.setStyleSheet("""Qtable_view::item {
            border-bottom: 1px solid lightgrey;
            selection-background-color: white;
            selection-color: black;
            }""")

        top_panel = QHBoxLayout()
        self.log_levels = ["Debug", "Info", "Warning", "Error"]
        self.level_colors = ["#3E4C85", "#269629", "#B0AB21", "#B32020"]

        self.levels_label = QLabel("Filter Level: ")
        self.levels_label.setStyleSheet("QLabel { font-weight: bold }")
        self.current_level_label = QLabel(self.log_levels[0])
        self.current_level_label.setStyleSheet("QLabel {{ color: {} }}".format(self.level_colors[0]))
        self.clear_button = QPushButton("Clear Log")
        self.levels_slider = QSlider(Qt.Horizontal)
        self.levels_slider.setStyleSheet("""
        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #FFFFFF, stop:1 #E3E3E3);
            border: 1px solid #707070;
            width: 10px;
            margin-top: -4px;
            margin-bottom: -4px;
            border-radius: 4px;
        }

        QSlider::handle:horizontal:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #DEDEDE, stop:1 #C9C9C9);
            border: 1px solid #4F4F4F;
            border-radius: 4px;
        }

        QSlider::sub-page:horizontal {
            background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
                stop: 0 #BFBFBF, stop: 1 #9E9E9E);
            background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
                stop: 0 #9E9E9E, stop: 1 #858585);
            border: 1px solid #777;
            height: 10px;
            border-radius: 4px;
        }

        QSlider::add-page:horizontal {
            background: #fff;
            border: 1px solid #707070;
            height: 10px;
            border-radius: 4px;
        }""")
        self.levels_slider.setRange(0, len(self.log_levels) - 1)
        self.levels_slider.setTickPosition(QSlider.TicksBelow)
        self.levels_slider.setTickInterval(1)

        top_panel.addSpacerItem(QSpacerItem(10, 0))
        top_panel.addWidget(self.levels_label, 3)
        top_panel.addWidget(self.current_level_label, 2)
        top_panel.addWidget(self.levels_slider, 8)
        top_panel.addSpacerItem(QSpacerItem(25, 0))
        top_panel.addWidget(self.clear_button, 10)

        layout.addLayout(top_panel)
        layout.addWidget(self.table_view)

        self.connect(self.clear_button, SIGNAL('clicked()'), functools.partial(self.table_model.setRowCount, 0))
        self.connect(self.levels_slider, SIGNAL('valueChanged(int)'), self.slider_set_level)

        self.setWindowTitle("Log")
        self.handler.add_listener(self)

    def __del__(self):
        self.handler.remove_listener(self)

    def retranslate(self):
        self.setWindowTitle(self.app.translate("LogDialog", "Log"))
        self.clear_button.setText(self.app.translate("LogDialog", "Clear Log"))
        self.levels_label.setText("{}: ".format(self.app.translate("LogDialog", "Filter Level")))

    def message(self, message):
        """Passes the log fields to add_entry()

        It is called by LogHandler when a log message is received"""
        self.add_entry(message["time"], message["level"], message["full_module_name"], message["message"], str(message["levelno"]))

    def add_entry(self, date, level, module, message, levelno):
        """Adds the given fields to a new row in the log table

        It is called by message() when a log message is received"""
        items = [QStandardItem(date), QStandardItem(level), QStandardItem(module), QStandardItem(message), QStandardItem(levelno)]
        for item in items:
            item.setEditable(False)
        self.table_model.appendRow(items)

    def slider_set_level(self, level):
        self.current_level_label.setText(self.log_levels[level])
        self.current_level_label.setStyleSheet("QLabel {{ color: {} }}".format(self.level_colors[level]))
        self.set_level(level + 1)

    def set_level(self, level):
        """Sets the current level of the LogDialog.

        Level is based on the selection made in the levels_combo_box.
        It hides all messages with a lower level."""
        self.level = level * 10
        for i in range(self.table_model.rowCount()):
            if int(str(self.table_model.item(i, self.level_num_column).text())) < self.level:
                self.table_view.setRowHidden(i, True)
            else:
                self.table_view.setRowHidden(i, False)


class LogHandler(logging.Handler):
    """Handler to receive LogRecord from the logger.

    When a message is received, emit is called and the message()
    method of all listeners is called with a dictionary containing
    the various log message fields (message, level, levelno, time, module, full_module_name).
    """

    def __init__(self, listener=None):
        super(LogHandler, self).__init__()
        self.listeners = []
        if listener is not None:
            self.listeners.append(listener)

        self.setFormatter(logging.Formatter("%(message)s, %(asctime)s, %(levelno)s", "%Y-%m-%d %H:%M:%S"))
        logging.getLogger().addHandler(self)

    def __del__(self):
        logging.getLogger().removeHandler(self)

    def add_listener(self, listener):
        """Add a listener to be notified when a message is received.

        The listener's message() method will be called"""
        self.listeners.append(listener)

    def remove_listener(self, listener):
        """Remove a listener from the list of listeners.

        Do not notify it of any further log messages."""
        self.listeners.remove(listener)

    def emit(self, record):
        """Send received log message to all listeners.

        Create a dictionary containing all the log message fields
        and Send it to all listeners by calling their message() method"""
        self.format(record)
        message = {
            "message": record.msg % record.args,
            "level": record.levelname,
            "levelno": record.levelno,
            "time": record.asctime,
            "module": record.module,
            "full_module_name": record.name,
        }
        for listener in self.listeners:
            listener.message(message)


class LogStatusWidget(QWidget):
    """Widget to display latest log message and icon.

    This widget is used by RecordApp to show the latest
    log message in it's status bar. It opens the LogDialog
    it was created with, when it is double-clicked."""

    def __init__(self, log_dialog, parent=None):
        super(LogStatusWidget, self).__init__(parent)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.app = QApplication.instance()

        self.last_message_level = logging.INFO
        self.handler = log_dialog.handler

        self.label = ClickableLabel()

        self.okay_pixmap = QPixmap(":/freeseer/state_okay.png").scaledToHeight(19)
        self.warning_pixmap = QPixmap(":/freeseer/state_warning.png").scaledToHeight(19)
        self.error_pixmap = QPixmap(":/freeseer/state_error.png").scaledToHeight(19)
        self.icon = ClickableLabel()
        self.icon.setPixmap(self.okay_pixmap)
        self.icon.setToolTip("Okay")

        main_layout.addWidget(self.icon)
        main_layout.addWidget(self.label, Qt.AlignLeft)

        self.connect(self.label, SIGNAL('double_clicked()'), log_dialog.show)
        self.connect(self.icon, SIGNAL('double_clicked()'), log_dialog.show)

        self.message_timer = QTimer()
        self.connect(self.message_timer, SIGNAL("timeout()"), functools.partial(self.label.setText, ""))

        self.handler.add_listener(self)

    def __del__(self):
        self.handler.remove_listener(self)

    def message(self, message):
        """Shows latest high priority log message in status bar.

        This method is called by the LogHandler when a new log message is received.
        LogStatusWidget is added as a listener to a LogHandler on init.
        """
        level = message["levelno"]
        if level >= self.last_message_level and level >= logging.INFO:
            if self.message_timer.isActive():
                self.message_timer.stop()

            if level == logging.INFO:
                self.message_timer.start(3000)

            if level != self.last_message_level:
                if level == logging.INFO:
                    self.icon.setPixmap(self.okay_pixmap)
                    self.icon.setToolTip(self.okay_string)
                elif level == logging.WARNING:
                    self.icon.setPixmap(self.warning_pixmap)
                    self.icon.setToolTip(self.warning_string)
                else:
                    self.icon.setPixmap(self.error_pixmap)
                    self.icon.setToolTip(self.error_string)

            self.label.setText(message["message"])
            self.last_message_level = level

    def retranslate(self):
        self.okay_string = self.app.translate("LogStatusWidget", "Okay")
        self.warning_string = self.app.translate("LogStatusWidget", "Warning.")
        self.error_string = self.app.translate("LogStatusWidget", "Error!")
        self.label.setToolTip(self.app.translate("LogStatusWidget", "Double-click to open log window"))
        if self.last_message_level == logging.INFO:
            self.icon.setToolTip(self.okay_string)
        elif self.last_message_level == logging.WARNING:
            self.icon.setToolTip(self.warning_string)
        else:
            self.icon.setToolTip(self.error_string)
