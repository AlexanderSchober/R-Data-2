#  -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2017 by Alexander Schober 
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

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

import numpy as np
from scipy.optimize import least_squares
from scipy.optimize import leastsq
from scipy.sparse.linalg import spsolve

from .function_library import FunctionLibrary

class FitWorker(QThread, FunctionLibrary):
    '''
    The fit worker will be modified before fit
    and then started as the task has to be 
    performed. 
    '''
    my_event = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)
        FunctionLibrary.__init__(self)
        self.initialize()

    def run(self):
        
        self.fitter.functions = self.func_dict
        self.fitter.fit()
        self.my_event.emit()

    def initialize(self):
        '''
        This function will do all the loading of the 
        different functions locally in the class
        '''
        self.importFunctions()
        self.fitter = Fitter()

    def setXY(self, x, y):
        '''
        This function will do all the loading of the 
        different functions locally in the class
        '''
        self.fitter.x = np.asarray(x)
        self.fitter.y = np.asarray(y)

    def setParameters(self, order, precision, repetition):
        '''
        This function is aimed at setting the parameters
        that are not represented in the local function.
        '''
        self.fitter.container = [
            order,
            precision,
            repetition
            ]

class Fitter():
    '''
    This class will be initiated and run 
    to do the fit. It will hold all the 
    mathematical aspects of the fit 
    while it's parent will manage the 
    threading.
    '''
    progress_int = pyqtSignal(int)
    progress_str = pyqtSignal(str)

    def __init__(self):
        self.container = []
        self.x = []
        self.y = []
        self.functions = {}

    def fit(self):
        '''
        perform the fit
        '''
        pointer = self.container[0]

        for k in range(self.container[2]):
            for l in pointer:
                print(k,l)

    def residue(self,p,function,idx,y,x):
        '''
        This is the residual function that evaluates 
        the deference between the data
        and the fit. This function needs:
        - function: the function (Lorenzian, Linear ...) it will fit.
        - p: the parameter to evaluate
        - y: the curve to compare
        - x: the axis to feed.
        '''
        #calculate error
        err = np.sum([abs(l) for l in y - function(idx,x,p)])*self.container[1]
        
        return err

    def FetchBounds(self, para,rel_bool,rel_bound,abs_bool,abs_bound):
        '''
        A more sophisticated method was recquired 
        to check the bounds as we now compare
        the relative and absolute bounds.
        '''
 
        # reorganise if the order is wrong
        if abs_bound[0] > abs_bound[1]:
            abs_bound[0], abs_bound[1]  = abs_bound[1] , abs_bound[0]
    
        # reorganise if the order is wrong
        if rel_bound[0] > rel_bound[1]:
            rel_bound[0], rel_bound[1]  = rel_bound[1] , rel_bound[0]

        # Check if the parameters is in the bounds
        if abs_bool:
            #process
            if para < abs_bound[0]:
                para = abs_bound[0] + 0.1 * abs_bound[0]
            if para > abs_bound[1]:
                para = abs_bound[1] - 0.1 * abs_bound[1]
    
        # Compute the Bounds bound
        if rel_bool and not abs_bool:
            LowerBound = para + rel_bound[0]
            UpperBound = para + rel_bound[1]
        elif abs_bool and rel_bool:
            LowerBound = para + rel_bound[0]
            UpperBound = para + rel_bound[1]
            if LowerBound < abs_bound[0]:
                LowerBound = abs_bound[0]
            if UpperBound > abs_bound[1]:
                UpperBound = abs_bound[1]
        elif abs_bool and not rel_bool:
            LowerBound = abs_bound[0]
            UpperBound = abs_bound[1]
        else:
            return [-np.inf, np.inf], para

        return [LowerBound, UpperBound], para