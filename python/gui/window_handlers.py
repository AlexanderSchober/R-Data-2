import sys
from PyQt5 import QtGui, QtCore

from .raw_import_window import RawWindow

class WindowHandler:
    '''
    ##############################################
    Initializer of the class, It will immediately call
    the first Managing instance to initialize a first
    window level. This will always be alive as it 
    contains the holder frame.
    
    The manager will also create root of the bat. 
    Tkinter build tge windows with dependance and
    root needs to be initialised from the start. 
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.window_dictionary = {}
        self.window_dictionary['RawImport'] = RawWindow
        self.active_windows = []

        self.main_window = MainWindow()
        self.main_window.show()

    def newWindow(self, name):
        '''
        ##############################################
        
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if name in self.window_dictionary.keys():
            self.active_windows.append(ChildWindow(
                self.main_window,
                self.window_dictionary[name]
            ))
            self.active_windows[-1].show()
        
    def run(self):
        '''
        ##############################################

        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        sys.exit(self.app.exec_())


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

class ChildWindow(QtGui.QMainWindow):
    def __init__(self, parent, target):

        #set the inheritance 
        super(ChildWindow, self).__init__(parent)

        #are we linked
        self.linked = False

        #set the gui
        self.target = target(self)
        