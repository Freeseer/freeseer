'''
Created on Nov 11, 2011

@author: jord
'''

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

class MediaFileView(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent)
        
        self.verticalHeader().hide()
        hheader = self.horizontalHeader()
        assert isinstance(hheader, QtGui.QHeaderView)
        hheader.setHighlightSections(False)
        self.lastSort = (1, Qt.DescendingOrder)
        hheader.sortIndicatorChanged.connect(self.cancelFirstColumnSort)
        
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self.setItemDelegateForColumn(0, CheckBoxDelegate(self))
    
    def setModel(self, model):
        QtGui.QTableView.setModel(self, model)
        hheader = self.horizontalHeader()
        assert isinstance(hheader, QtGui.QHeaderView)
        
        hheader.resizeSection(0,25)
        hheader.setResizeMode(0, QtGui.QHeaderView.Fixed)
        hheader.setStretchLastSection(True)
        
    @QtCore.pyqtSlot(int, Qt.SortOrder)
    def cancelFirstColumnSort(self, column, order):
        if column == 0:
            column, order = self.lastSort
            self.horizontalHeader().setSortIndicator(column, order)
        else:
            self.lastSort = (column, order)

# http://stackoverflow.com/questions/3363190/qt-qtableview-how-to-have-a-checkbox-only-column/7392432#7392432
# pylint: disable-msg=W0613
class CheckBoxDelegate(QtGui.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return None
    def paint(self, painter, option, index):
        checked = bool(index.model().data(index, Qt.DisplayRole))
        check_box_style_option = QtGui.QStyleOptionButton()
    
        if index.flags() & Qt.ItemIsEditable:
            check_box_style_option.state |= QtGui.QStyle.State_Enabled
        else:
            check_box_style_option.state |= QtGui.QStyle.State_ReadOnly
    
        if checked:
            check_box_style_option.state |= QtGui.QStyle.State_On
        else:
            check_box_style_option.state |= QtGui.QStyle.State_Off
    
        check_box_style_option.rect = self.getCheckBoxRect(option)
        
#        if not index.model().hasFlag(index, Qt.ItemIsEditable):
        if not index.flags() & Qt.ItemIsEditable:
            check_box_style_option.state |= QtGui.QStyle.State_ReadOnly
    
        QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_CheckBox, 
                                               check_box_style_option, painter)
    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.
        '''
        if not index.flags() & Qt.ItemIsEditable:
            return False
    
        # Do not change the checkbox-state
        if (event.type() == QtCore.QEvent.MouseButtonRelease or 
            event.type() == QtCore.QEvent.MouseButtonDblClick):
            if (event.button() != Qt.LeftButton or 
                not self.getCheckBoxRect(option).contains(event.pos())):
                return False
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() != Qt.Key_Space and event.key() != Qt.Key_Select:
                return False
        else:
            return False
    
        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True
    def setModelData (self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        newValue = not bool(index.model().data(index, Qt.DisplayRole))
        model.setData(index, newValue, Qt.EditRole)
    def getCheckBoxRect(self, option):
        check_box_style_option = QtGui.QStyleOptionButton()
        check_box_rect = QtGui.QApplication.style().subElementRect(
                QtGui.QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QtCore.QPoint (option.rect.x() +
                             option.rect.width() / 2 -
                             check_box_rect.width() / 2,
                             option.rect.y() +
                             option.rect.height() / 2 -
                             check_box_rect.height() / 2)
        return QtCore.QRect(check_box_point, check_box_rect.size())
# pylint: enable-msg=W0613

class CheckableRowTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.CHECK_COL = 0
        self.checked = {}
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == self.CHECK_COL:
                    return ""
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        assert isinstance(index, QtCore.QModelIndex)
        if index.column() == self.CHECK_COL:   
            if role == Qt.DisplayRole:
                return self.checked.get(index.row(), False)
            if role == Qt.CheckStateRole:
                return Qt.Unchecked
        return None
    
    def setData(self, index, value, role=Qt.EditRole):
        assert isinstance(index, QtCore.QModelIndex)
        if index.column() == self.CHECK_COL:
            if role == Qt.EditRole:
                self.checked[index.row()] = value
                self.dataChanged.emit(index, index)
    
    def flags(self, index):
        assert isinstance(index, QtCore.QModelIndex)
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
#        if True:
#            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable
        return QtCore.QAbstractTableModel.flags(self, index)
    
    # selection modification tools #
    def checkAll(self):
        for index in self._iterCheckIndicies():
            self.setData(index, True, Qt.EditRole)
    def checkNone(self):
        for index in self._iterCheckIndicies():
            self.setData(index, False, Qt.EditRole)
    def checkInvert(self):
        for index in self._iterCheckIndicies():
            self.setData(index, not self.data(index, Qt.DisplayRole), Qt.EditRole)
    
    def _iterCheckIndicies(self):
        for row in range(0, self.rowCount()):
            yield self.index(row, self.CHECK_COL)
    
class MediaFileModel(CheckableRowTableModel):
    def __init__(self, parent=None):
        CheckableRowTableModel.__init__(self, parent)
        
    def setDirectory(self, directory):
        # TODO: look at QtGui.QFileSystemModel
        pass
    
    # pylint: disable-msg=W0613
    ## Mandatory implemented abstract methods ##
    def rowCount(self, parent=QtCore.QModelIndex()):
        return 4
    
    def columnCount(self, parent=QtCore.QModelIndex()):
        return 5
    # pylint: enable-msg=W0613
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        assert isinstance(index, QtCore.QModelIndex)
        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            return {1: self.tr("fname"),
                    2: self.tr("title"),
                    3: self.tr("artist"),
                    4: self.tr("blah")
                    }.get(index.column(),
                          CheckableRowTableModel.data(self, index, 
                                                            role))
        
        return CheckableRowTableModel.data(self, index, role)
    
    ## Optionally implemented abstract methods ##
#    def index(self, row, column, parent=QtCore.QModelIndex()):
#        return CheckableRowTableModel.index(row, column, parent)
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
#                print section
                return {1: self.tr("File Name"),
                        2: self.tr("Title"),
                        3: self.tr("Speaker"),
                        4: self.tr("Description")
                        }.get(section,
                          CheckableRowTableModel.headerData(self, section, 
                                                            orientation, 
                                                            role))
        # else
        return CheckableRowTableModel.headerData(self, section, orientation, role)

class MediaFileItem(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(parent)
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    filelist = MediaFileView()
    filelist.resize(QtCore.QSize(320,320))
    
    filemodel = MediaFileModel(filelist)
#    filemodel.in
    filelist.setModel(filemodel)
#    filelist.horizontalHeader().resizeSections(QtGui.QHeaderView.ResizeToContents)
#    filelist.horizontalHeader().resizeSection(0,25)
    
#    filelist_model = QtGui.QFileSystemModel()
#    filelist_model.setRootPath("file:///home/")
#    filelist_model = QtGui.QStandardItemModel()
#    filelist_model.setColumnCount(3)
#    
#    from random import randint
#    for _ in range(10):
#        item = QtGui.QStandardItem('Item %s' % randint(1, 100))
#        check = QtCore.Qt.Checked if randint(0, 1) == 1 else QtCore.Qt.Unchecked
#        item.setColumnCount(3)
#        item.setCheckState(check)
#        item.setCheckable(True)
#        item.setEditable(False)
#        filelist_model.appendRow(item)
#    filelist.setModel(filelist_model)
    
    
    filelist.show()
    sys.exit(app.exec_())