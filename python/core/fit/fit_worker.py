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
import itertools
from scipy.optimize import least_squares
from scipy.optimize import leastsq
from scipy.sparse.linalg import spsolve

from .function_library import FunctionLibrary

class FitWorker(QtCore.QObject, FunctionLibrary):
    '''
    The fit worker will be modified before fit
    and then started as the task has to be 
    performed. 
    '''
    my_event        = pyqtSignal()
    progress_int    = pyqtSignal(int)
    progress_str    = pyqtSignal(int)
    finished        = pyqtSignal()

    def __init__(self):
        QtCore.QObject.__init__(self)
        FunctionLibrary.__init__(self)
        self.initialize()

    @QtCore.pyqtSlot()  
    def run(self):
        '''
        This is the run method of the 
        QThread class overwritten. 
        '''
        self.fitter.functions = self.func_dict
        self.fitter.fit()
        self.finished.emit()

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

class Fitter(QtCore.QObject):
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
        QtCore.QObject.__init__(self)
        self.container = []
        self.x = []
        self.y = []
        self.functions = {}

    def fit(self):
        '''
        perform the fit. Loop over all functions and all
        parameters and then check if it is fixed and if not
        proceed. 
        '''
        pointer     = self.container[0]
        keys        = [key for key in self.functions.keys()] 
        self.setProgressVal()
        i = 0

        for k, l  in itertools.product(range(self.container[2]), pointer):

            # set the progress
            self.progress_str.emit('Fitting the '+str(keys[l]) + 'functions')

            for o,m,n in itertools.product(
                range(self.functions[keys[l]][0].para_proc[0]),
                range(len(self.functions[keys[l]][2])),
                range(self.functions[keys[l]][0].para_num)):

                # set the progress
                self.progress_int.emit(self.grabProgressVal(i))
                
                #if not fixed
                if not self.functions[keys[l]][2][m].para_fix[self.functions[keys[l]][0].para_proc[1][n]]: 
                    temp_y = self.constructor(
                        ignore  = [keys[l],m],
                        data    = self.y,
                        x       = self.x)

                    self.fitFunction(
                        self.y,
                        temp_y,
                        [keys[l],m],
                        self.functions[keys[l]][0].para_proc[1][n])
                i += 1

    def setProgressVal(self):
        '''
        Prepare the progress report by setting the
        self.max_progress values
        '''
        pointer     = self.container[0]
        keys        = [key for key in self.functions.keys()] 
        self.max_progress = 0

        for k, l  in itertools.product(range(self.container[2]), pointer):
            for o,m,n in itertools.product(
                range(self.functions[keys[l]][0].para_proc[0]),
                range(len(self.functions[keys[l]][2])),
                range(self.functions[keys[l]][0].para_num)):
                self.max_progress +=1

    def grabProgressVal(self, val):
        '''
        Prepare the progress report by setting the
        self.max_progress values
        '''
        return float(val) / float(self.max_progress) * 100.


    def fitFunction(self, y, temp_y, selected, parameter):
        '''
        This is the actual fit worker. he will run
        through the leastsquare of one element.
        '''
        fit_target = self.functions[selected[0]][2][selected[1]]
        fit_target.current_par = int(parameter)
        fit_target.x = self.x
        fit_target.calculated = False

        bounds = self.fetchBounds(
            float(fit_target.paras[int(parameter)]),
            fit_target.info.para_bound[int(parameter)*2][2],
            fit_target.info.para_bound[int(parameter)*2][:2],
            fit_target.info.para_bound[(int(parameter)*2+1)][2],
            fit_target.info.para_bound[(int(parameter)*2+1)][:2])

        fit_target.paras[int(parameter)] = float(
            least_squares(
                self.residue,
                bounds[1],
                args = (
                    fit_target.fitWrapper,
                    y, 
                    temp_y),
                bounds = bounds[0],
                verbose=0).x[0])

    def residue(self,p,function,y, temp_y):
        '''
        This is the residual function that evaluates 
        the deference between the data
        and the fit. This function needs:
        - function: the function (Lorenzian, Linear ...) it will fit.
        - p: the parameter to evaluate
        - y: the curve to compare
        - x: the axis to feed.
        '''
        err = np.sum([abs(l) for l in y - (function(p) + temp_y)])*self.container[1]
        return err

    def fetchBounds(self, para, rel_bool, rel_bound, abs_bool, abs_bound):
        '''
        A more sophisticated method was recquired 
        to check the bounds as we now compare
        the relative and absolute bounds.
        '''
        pointer = [rel_bound, abs_bound]
        for i in range(2):
            for j in range(2):
                if pointer[i][j] == 'xmin':
                    pointer[i][j] = np.min(self.x)
                elif pointer[i][j] == 'ymin':
                    pointer[i][j] = np.min(self.y)
                elif pointer[i][j] == 'xmax':
                    pointer[i][j] = np.max(self.x)
                elif pointer[i][j] == 'ymax':
                    pointer[i][j] = np.max(self.y)
                elif pointer[i][j] == '-Inf':
                    pointer[i][j] = -np.inf
                elif pointer[i][j] == 'Inf':
                    pointer[i][j] = np.inf
                else:
                    pointer[i][j] = float(pointer[i][j])

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

    def constructor(self,ignore = None , data = None, x = None):
        '''
        This function will try to create the
        data minus all the functions that are not 
        currently being fitted.
        '''
        data = np.zeros(data.shape)

        for key in self.functions.keys():
            for m in range(len(self.functions[key][2])):
                if not [key,m] == ignore:
                    data = data + self.functions[key][2][m].quickReturn(x)

        return data


        
