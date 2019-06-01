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
#   Alexander Schober <alex.schober@mac.com>
#
# *****************************************************************************

from PyQt5 import QtWidgets, QtGui, QtCore
from functools import partial

from ..gui_qt.fitcontrol_ui import Ui_fit_control_widget

class FitControlWidget(Ui_fit_control_widget):
    
    def __init__(self, parent):
        Ui_fit_control_widget.__init__(self)
        self.parent         = parent
        self.widget         = QtWidgets.QWidget() 
        self.setupUi(self.widget)
        self.connect()

    def connect(self):
        '''
        connect the actions to their respective buttons
        '''
        self.fit_button_fit.clicked.connect(self.setFit)

    def link(self, fit_handler):
        '''
        link the class that will manage the current 
        input output.
        '''
        self.fit_handler = fit_handler 
        self.fit_handler.progress_int.connect(self.setProgress)
        self.initialize()

    def initialize(self):
        '''
        This method checks if the data has been set
        in a previous instance.
        '''
        self.fit_bar_progress.setMaximum(100)
        self.fit_bar_progress.setMinimum(0)


    def setFit(self):
        '''
        Tell the system to set up the fit and 
        then run
        '''
        self.fit_handler.performFit()

    def setProgress(self, value):
        self.fit_bar_progress.setValue(value)
