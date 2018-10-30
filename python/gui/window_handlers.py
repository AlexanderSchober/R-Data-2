import sys
from PyQt5 import QtGui, QtCore


class MainWindowHandler:
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

    def __init__(self, Initializer_Class):
        
        #Link the topmost managing class
        self.Initializer_Class = Initializer_Class
        
        #Create the Manager Pointer List
        self.Managers   = []


    def initialize(self, build_class):
        '''
        ##############################################
        Initialize the application environement by 
        setting the the app and then setting its 
        variables. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.app = QtGui.QApplication(sys.argv)

