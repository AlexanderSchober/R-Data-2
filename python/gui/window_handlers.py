import sys
from PyQt5 import QtGui, QtCore

from .raw_import_window import RawWindowLayout
from .main_window import MainWindowLayout

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
        self.window_dictionary['MainWindow']    = MainWindowLayout
        self.window_dictionary['RawImport']     = RawWindowLayout
        self.active_windows = {}

        self.main_window = MainWindow()
        self.main_window.show()
        self.active_windows['MainWindow'] = self.main_window
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
            self.active_windows['RawImport'] = (
                ChildWindow(
                    self.main_window,
                    self.window_dictionary[name]))

            self.active_windows['RawImport'].show()
        
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
    '''
    ##############################################
    This class is the main window that will be 
    used as a window base. All other windows will
    be childre.
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.target = MainWindowLayout(self)

class ChildWindow(QtGui.QMainWindow):
    '''
    ##############################################
    This class will luanch and generate the child
    windows. Note that this is simply a wrapper
    that will then call the target class defining
    the arragement. 
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, parent, target):

        #set the inheritance 
        super(ChildWindow, self).__init__(parent)

        #are we linked
        self.linked = False

        #set the gui
        self.target = target(self)
        