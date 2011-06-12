# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms/configtoolui.ui'
#
# Created by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ConfigTool(object):
    def setupUi(self, ConfigTool):
        ConfigTool.setObjectName(_fromUtf8("ConfigTool"))
        ConfigTool.resize(592, 526)
        self.optionsWidget = QtGui.QTreeWidget(ConfigTool)
        self.optionsWidget.setGeometry(QtCore.QRect(20, 20, 171, 491))
        self.optionsWidget.setHeaderHidden(True)
        self.optionsWidget.setObjectName(_fromUtf8("optionsWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.optionsWidget)
        item_0 = QtGui.QTreeWidgetItem(self.optionsWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.mainWidget = QtGui.QWidget(ConfigTool)
        self.mainWidget.setGeometry(QtCore.QRect(210, 20, 361, 491))
        self.mainWidget.setObjectName(_fromUtf8("mainWidget"))

        self.retranslateUi(ConfigTool)
        QtCore.QMetaObject.connectSlotsByName(ConfigTool)

    def retranslateUi(self, ConfigTool):
        ConfigTool.setWindowTitle(QtGui.QApplication.translate("ConfigTool", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsWidget.headerItem().setText(0, QtGui.QApplication.translate("ConfigTool", "1", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.optionsWidget.isSortingEnabled()
        self.optionsWidget.setSortingEnabled(False)
        self.optionsWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("ConfigTool", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsWidget.topLevelItem(1).setText(0, QtGui.QApplication.translate("ConfigTool", "Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsWidget.topLevelItem(1).child(0).setText(0, QtGui.QApplication.translate("ConfigTool", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsWidget.topLevelItem(1).child(1).setText(0, QtGui.QApplication.translate("ConfigTool", "Mixer", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsWidget.topLevelItem(1).child(2).setText(0, QtGui.QApplication.translate("ConfigTool", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsWidget.setSortingEnabled(__sortingEnabled)

