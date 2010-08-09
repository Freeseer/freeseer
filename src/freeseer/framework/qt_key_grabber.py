import sys
from PyQt4 import QtCore, QtGui

class QtKeyGrabber(QtGui.QWidget):
    '''
    This class allows the user to press a combination of keys in order to
    set a shortkey.
    '''
    def __init__(self, parent=None):
        '''
        Create a minimized screen and initialize variables used in this
        class.
        '''
        QtGui.QWidget.__init__(self, None, QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowState(QtCore.Qt.WindowActive)

        self.parent = parent
        self.flag = False
        self.modifiers = {}
        self.setWindowOpacity(0.3)

    def keyPressEvent(self, event):
        other = None
        if event.key() == QtCore.Qt.Key_Shift:
            self.modifiers[QtCore.Qt.Key_Shift] = u'Shift'
        elif event.key() == QtCore.Qt.Key_Control:
            self.modifiers[QtCore.Qt.Key_Control] = u'Ctrl'
        elif event.key() == QtCore.Qt.Key_Alt:
            self.modifiers[QtCore.Qt.Key_Alt] = u'Alt'
        elif event.key() == QtCore.Qt.Key_Meta:
            self.modifiers[QtCore.Qt.Key_Meta] = u'Meta'
        else:
            other = event.text()
        if other:
            self.key_string = u'+'.join(self.modifiers.values() + [unicode(other)])
        else:
            self.key_string = u'+'.join(self.modifiers.values())
        if (self.parent.core.config.key_rec == 'Ctrl+Shift+R'):
            self.flag = True

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Shift:
            if self.modifiers.has_key(QtCore.Qt.Key_Shift):
                del self.modifiers[QtCore.Qt.Key_Shift]
        elif event.key() == QtCore.Qt.Key_Control:
            if self.modifiers.has_key(QtCore.Qt.Key_Control):
                del self.modifiers[QtCore.Qt.Key_Control]
        elif event.key() == QtCore.Qt.Key_Alt:
            if self.modifiers.has_key(QtCore.Qt.Key_Alt):
                del self.modifiers[QtCore.Qt.Key_Alt]
        elif event.key() == QtCore.Qt.Key_Meta:
            if self.modifiers.has_key(QtCore.Qt.Key_Meta):
                del self.modifiers[QtCore.Qt.Key_Meta]
        #print len(self.modifiers)
        if len(self.modifiers) == 0:
            if self.flag == True:
                self.parent.grab_rec_set(self.key_string)
            else: self.parent.grab_stop_set(self.key_string)
            self.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = QtKeyGrabber()
    main.show()
    sys.exit(app.exec_())
