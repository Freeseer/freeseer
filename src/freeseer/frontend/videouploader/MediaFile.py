'''
Created on Nov 11, 2011

@author: jord
'''
import os
import mimetypes

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from freeseer.framework.presentation import PresentationFile
from freeseer.framework import uploader
from freeseer.framework.metadata import FreeseerMetadataLoader

# TODO: (junior task) separate this class between the checkbox column functions
# and the rest of the essential functions
class MediaFileView(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent)
        
        self.verticalHeader().hide()
        hheader = self.horizontalHeader()
        assert isinstance(hheader, QtGui.QHeaderView)
        hheader.setHighlightSections(False)
#        self.lastSort = (-1, Qt.DescendingOrder)
        hheader.sortIndicatorChanged.connect(self.cancelFirstColumnSort)
        
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setSortingEnabled(True) # TODO: sorting.
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.realmodel = None
        self.sortmodel = DisabledColumnSortFilterProxyModel(self)
        self.sortmodel.setSortCaseSensitivity(Qt.CaseInsensitive)
        QtGui.QTableView.setModel(self, self.sortmodel)
    
    def setModel(self, model):
        self.onModelReset()
        if self.realmodel:
            self.realmodel.modelReset.disconnect(self.onModelReset)
            self.realmodel.headersReset.disconnect(self.onHeadersReset)
            self.realmodel.columnHidden.disconnect(self.setColumnHidden)
            if isinstance(self.model(), CheckableRowTableModel):
                self.setItemDelegateForColumn(self.model().CHECK_COL, self.itemDelegate())
        self.realmodel = model
        self.sortmodel.check_col = model.CHECK_COL
        self.sortmodel.setSourceModel(model)
#        QtGui.QTableView.setModel(self, model)
        
        if isinstance(model, CheckableRowTableModel):
            self.setItemDelegateForColumn(model.CHECK_COL, CheckBoxDelegate(self))
        
        assert isinstance(model, MediaFileModel)
        model.modelReset.connect(self.onModelReset)
        model.headersReset.connect(self.onHeadersReset)
        model.columnHidden.connect(self.setColumnHidden)
    
    def onModelReset(self):
        pass
    
    def onHeadersReset(self):
        hheader = self.horizontalHeader()
        assert isinstance(hheader, QtGui.QHeaderView)
#        model = self.model()
        model = self.realmodel
        if model == None:
            return
        assert isinstance(model, MediaFileModel)
        
        hheader.resizeSection(model.CHECK_COL,25)
        hheader.setResizeMode(model.CHECK_COL, QtGui.QHeaderView.Fixed)
        
        hheader.setStretchLastSection(True)
        if model.header_keyindex.has_key("FileName.name"):
            hheader.resizeSection(model.header_keyindex["FileName.name"], 300)
        
        for index in model.iterHiddenColumnIndicies():
            self.setColumnHidden(index, True)
    
    
    @QtCore.pyqtSlot(int, Qt.SortOrder)
    def cancelFirstColumnSort(self, column, order):
#        if column == 0:
#            column, order = self.lastSort
#            self.horizontalHeader().setSortIndicator(column, order)
#        else:
#            self.lastSort = (column, order)
        # instead of canceling, lets just revert to the natural sort
        if column == 0:
            self.horizontalHeader().setSortIndicator(-1, Qt.DescendingOrder)
            
    def sortByColumn(self, column, order):
        print(column, order)

# http://stackoverflow.com/questions/3363190/
#  qt-qtableview-how-to-have-a-checkbox-only-column/7392432#7392432
# pylint: disable-msg=W0613
class CheckBoxDelegate(QtGui.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return None
    def paint(self, painter, option, index):
        data = index.model().data(index, Qt.DisplayRole)
        checked = (data.toBool() if isinstance(data, QtCore.QVariant) else
                   bool(data))
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
        data = index.model().data(index, Qt.DisplayRole)
        newValue = not (data.toBool() if isinstance(data, QtCore.QVariant) else
                        bool(data))
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

class DisabledColumnSortFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QtGui.QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.check_col = -1
    def sort(self, column, order):
        if column == self.check_col:
            # remove the following line to just disable sorting of the column
            QtGui.QSortFilterProxyModel.sort(self, -1, Qt.DescendingOrder)
            return
        QtGui.QSortFilterProxyModel.sort(self, column, order)

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
                if isinstance(value, QtCore.QVariant):
                    self.checked[index.row()] = value.toBool()
                else:
                    self.checked[index.row()] = value
                self.dataChanged.emit(index, index)
            return True
        return False
    
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
    headersReset = QtCore.pyqtSignal()
    columnHidden = QtCore.pyqtSignal(int, bool)

    class emptyloader(FreeseerMetadataLoader):
        def __init__(self):
            FreeseerMetadataLoader.__init__(self, None)
        def get_fields(self):
            return {}
    
    def __init__(self, parent=None, loader=None):
        CheckableRowTableModel.__init__(self, parent)
        self.loader = None
        self.setMetadataLoader(loader)
        
        self.filedata = [] # [{field_id: data}]
        self.header_data = {} # {field_id: IMetadataReader.header}
        self.header_indexkey = {} # {int: field_id}
        self.header_keyindex = {} # {field_id: int}
        
    def setDirectory(self, directory):
        self.beginResetModel()
        self.filedata = []
        self.endResetModel()
        
        listabsdir = lambda d: (os.path.join(str(d), f) for f in os.listdir(str(d)))
        isAVmimetype = lambda t: t[0] != None and (t[0].find("video") >= 0 or
                                                   t[0].find("audio") >= 0)
        
        # using qt libraries
#        qdir = QtCore.QDir(directory)
#        print [entry.absoluteFilePath() for entry in qdir.entryInfoList()]
        for f in [f for f in listabsdir(directory) 
                  if isAVmimetype(mimetypes.guess_type(f, False))]:
            self.beginInsertRows(QtCore.QModelIndex(), 
                                 len(self.filedata), len(self.filedata))
            item = self.loader.retrieve_metadata(f)
#            print item
            
            self.filedata.append(item)
            self.endInsertRows()
    
    def setMetadataLoader(self, loader):
        if self.loader != None:
            self.loader.field_visibility_changed.disconnect(self.onFieldVisiblityChange)
            self.loader.fields_changed.disconnect(self.refreshHeaders)
        if loader == None:
            loader = self.emptyloader()
        self.loader = loader
        self.refreshHeaders()
#        assert isinstance(loader, FreeseerMetadataLoader)
        loader.field_visibility_changed.connect(self.onFieldVisiblityChange)
        loader.fields_changed.connect(self.refreshHeaders)
        
    def refreshHeaders(self):
        self.beginResetModel()
        self.header_indexkey = {}
        self.header_keyindex = {}
        
        self.header_data = self.loader.get_fields()
        
        count = 1
#        for key, _ in sorted(self.header_data.iteritems(), key=lambda (k,v): v.position):
        for key, _ in self.loader.get_fields_sorted():
            self.header_indexkey[count] = key
            self.header_keyindex[key] = count
            count = count + 1
        
        self.endResetModel()
        self.headersReset.emit()
    
    # pylint: disable-msg=W0613
    ## Mandatory implemented abstract methods ##
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.filedata)
    
    def columnCount(self, parent=QtCore.QModelIndex()):
#        return MediaFileModel.NUM_FIELDS
        return len(self.loader.get_fields())+1
    # pylint: enable-msg=W0613
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        assert isinstance(index, QtCore.QModelIndex)
        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if self.header_indexkey.has_key(index.column()):
                return self.filedata[index.row()].get(self.header_indexkey[index.column()])
        return CheckableRowTableModel.data(self, index, role)
    
    ## Optionally implemented abstract methods ##
#    def index(self, row, column, parent=QtCore.QModelIndex()):
#        return CheckableRowTableModel.index(row, column, parent)
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
#                print section
                try:
                    return self.header_data[self.header_indexkey[section]].name
                except KeyError: 
                    pass
        return CheckableRowTableModel.headerData(self, section, orientation, role)
    
#    def sort(self, column, order):
#        
#        
#        if order == Qt.DescendingOrder:
#            [].reverse()
    
    def onFieldVisiblityChange(self, field_id, value):
        self.columnHidden.emit(self.header_keyindex[str(field_id)], not value)
    
    def iterHiddenColumnIndicies(self):
        return (self.header_keyindex[k] 
                for k, v in self.header_data.iteritems() 
                if not v.visible)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
    filelist = MediaFileView()
    filelist.resize(QtCore.QSize(320,320))
    
    filemodel = MediaFileModel(filelist)
    filelist.setModel(filemodel)
    
    filelist.show()
    sys.exit(app.exec_())