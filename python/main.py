#  -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2017 by the NSE analysis contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Alexander Schober <alexander.schober@mac.com>
#
# *****************************************************************************

#######################################
#basic imports

#system import
import sys

#operating system variables
import os

#numpyy mathematical import
import numpy

#Date and time import
import datetime

#function manipulation routines
from functools import partial

#######################################
#gui imports
import gui.window_handlers as Window_Handlers
from gui.main_window import Main_Window

class Main:
    '''
    ##############################################
    This class will manage the 
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self):


        #initalize the window manager
        self.window_handler = Window_Handlers.Main_Window_Handler(self)
    
        #initialize the specific class
        self.main_window = Main_Window(self.window_handler, self)
        
        #initialize
        self.window_handler.initialize(self.main_window)
                                
        #Set the manager to start runing Tkinter backend
        self.window_handler.run()


