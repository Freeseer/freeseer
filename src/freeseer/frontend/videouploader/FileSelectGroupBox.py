'''
Created on Oct 15, 2011

@author: jord
'''

from PyQt4 import QtCore, QtGui

class FileSelectGroupBox(QtGui.QGroupBox):
    '''
    classdocs
    '''
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QGroupBox.__init__(self, parent)
        
        self.setObjectName("groupBox_fileselect")
        self.verticalLayout_fileselectgbox = QtGui.QVBoxLayout(self)
        self.verticalLayout_fileselectgbox.setObjectName("verticalLayout_fileselectgbox")
        
        self.horizontalLayout_filepathbuttons = QtGui.QHBoxLayout()
        self.horizontalLayout_filepathbuttons.setObjectName("horizontalLayout_filepathbuttons")
        
        # directory select button #
        self.toolButton_directorydropdown = QtGui.QToolButton(self)
        self.toolButton_directorydropdown.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
#        self.toolButton_directorydropdown.setArrowType(QtCore.Qt.DownArrow)
        self.toolButton_directorydropdown.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.toolButton_directorydropdown.setObjectName("toolButton_directorydropdown")
        self.horizontalLayout_filepathbuttons.addWidget(self.toolButton_directorydropdown)
        
        # directory dropdown menu #
        self.menu_directorydropdown = QtGui.QMenu(self.toolButton_directorydropdown)
        self.actionNavFreeseerVideoDir = QtGui.QAction(self)
        self.actionNavFreeseerVideoDir.setObjectName("actionNavFreeseerVideoDir")
        self.actionNavHomeDir = QtGui.QAction(self)
        self.actionNavHomeDir.setObjectName("actionNavHomeDir")
        self.actionAddFavourite = QtGui.QAction(self)
        self.actionAddFavourite.setObjectName("actionAddFavourite")
        
        self.menu_directorydropdown.addAction(self.actionNavFreeseerVideoDir)
        self.menu_directorydropdown.addAction(self.actionNavHomeDir)
        self.menu_directorydropdown.addSeparator()
        self.menu_directorydropdown.addAction(self.actionAddFavourite)
        self.toolButton_directorydropdown.setMenu(self.menu_directorydropdown)
        
        # file path input #
        self.lineEdit_filepath = QtGui.QLineEdit(self)
        self.lineEdit_filepath.setObjectName("lineEdit_filepath")
        self.horizontalLayout_filepathbuttons.addWidget(self.lineEdit_filepath)
        self.toolButton_filepathgo = QtGui.QToolButton(self)
        self.toolButton_filepathgo.setObjectName("toolButton_filepathgo")
        self.horizontalLayout_filepathbuttons.addWidget(self.toolButton_filepathgo)
        self.line_filepathspacer = QtGui.QFrame(self)
        self.line_filepathspacer.setFrameShape(QtGui.QFrame.VLine)
        self.line_filepathspacer.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_filepathspacer.setObjectName("line_filepathspacer")
        self.horizontalLayout_filepathbuttons.addWidget(self.line_filepathspacer)
        self.pushButton_filepathbrowse = QtGui.QPushButton(self)
        self.pushButton_filepathbrowse.setObjectName("pushButton_filepathbrowse")
        self.horizontalLayout_filepathbuttons.addWidget(self.pushButton_filepathbrowse)
        self.verticalLayout_fileselectgbox.addLayout(self.horizontalLayout_filepathbuttons)
        self.listView_filelist = QtGui.QListView(self)
        self.listView_filelist.setObjectName("listView_filelist")
        self.verticalLayout_fileselectgbox.addWidget(self.listView_filelist)
        
        ## file selection modification buttons ##
        self.horizontalLayout_fileselectbuttons = QtGui.QHBoxLayout()
        self.horizontalLayout_fileselectbuttons.setObjectName("horizontalLayout_fileselectbuttons")
        
        # all #
        self.toolButton_selectall = QtGui.QToolButton(self)
        self.toolButton_selectall.setObjectName("toolButton_selectall")
        self.horizontalLayout_fileselectbuttons.addWidget(self.toolButton_selectall)
        
        # none #
        self.toolButton_selectnone = QtGui.QToolButton(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.toolButton_selectnone.setObjectName("toolButton_selectnone")
        self.horizontalLayout_fileselectbuttons.addWidget(self.toolButton_selectnone)
        
        # invert #
        self.toolButton_selectinvert = QtGui.QToolButton(self)
        self.toolButton_selectinvert.setObjectName("toolButton_selectinvert")
        self.horizontalLayout_fileselectbuttons.addWidget(self.toolButton_selectinvert)
        
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_fileselectbuttons.addItem(spacerItem1)
        
        # filter #
        self.toolButton_selectfilter = QtGui.QToolButton(self)
        self.toolButton_selectfilter.setObjectName("toolButton_selectfilter")
        self.horizontalLayout_fileselectbuttons.addWidget(self.toolButton_selectfilter)
        
        self.verticalLayout_fileselectgbox.addLayout(self.horizontalLayout_fileselectbuttons)
        
        self.retranslateUi()
        
    def retranslateUi(self):
        self.setTitle(self.tr("File Selection"))
        self.toolButton_directorydropdown.setText(self.tr("Directory "))
        self.actionNavFreeseerVideoDir.setText(self.tr("Freeseer Video Directory"))
        self.actionNavHomeDir.setText(self.tr("Home"))
        self.actionAddFavourite.setText(self.tr("Add favourite..."))
        
        self.lineEdit_filepath.setText(self.tr("~/Videos"))
        self.toolButton_filepathgo.setText(self.tr("Go"))
        self.pushButton_filepathbrowse.setText(self.tr("Browse..."))
        self.toolButton_selectall.setText(self.tr("All"))
        self.toolButton_selectnone.setText(self.tr("None"))
        self.toolButton_selectinvert.setText(self.tr("Invert"))
        self.toolButton_selectfilter.setText(self.tr("Filter..."))
        
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = FileSelectGroupBox()
    main.show()
    sys.exit(app.exec_())