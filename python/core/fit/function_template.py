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

import numpy as np

class InfoClass:
    '''
    This class is a template to be imported and 
    overwritten by the child
    '''
    
    def __init__(self):

        #######################
        #name of the function
        self.name       = 'No_name'
        self.order      = 0
        self.para_num   = 0
        
        #######################
        #parameter names
        self.para_name  = []
        self.para_unit  = []
                                       
        #######################
        #Parameter Boundaries
        self.para_bound = []

        #######################
        #Parameter Boundaries
        self.para_proc  = [None,[None]]  

class FunctionClass:
    '''
    This class is to be inherited by a proper definition. 
    Note that the only thing to be changed is the 
    self.function method.
    '''
    
    def __init__(self, info, source = None):

        self.type       = info.name
        self.info       = info
        self.paras      = list([e[1] for e in self.info.para_name])
        self.para_ini   = list([e[1] for e in self.info.para_name])
        self.para_fix   = list(self.info.para_fix_ini)
        self.calculated = False
        self.x          = []
        self.current_par= 0

        if not source == None:
            self.clone(source)


    def function(self,para):
        '''
        To be changed after inheritance
        '''

        return self.x
    
    def compute(self,x):
        '''
        This classes serves to compute and access single 
        lorentzian for given input.  In the new version 
        we introduced the asymmetric functions and therefore 
        we need to check for the asymmetry and if the asymmetry 
        is present compute it...
        '''
        self.y_bis      = self.returnData(x)
        self.x          = x
        self.y_range    = [np.min(self.y_bis),np.max(self.y_bis)]
        self.x_range    = [np.min(self.x),np.max(self.x)]
        self.calculated = True

    def returnData(self,x):
        '''
        This classes serves to compute and access single 
        lorentzian for given input.  In the new version 
        we introduced the asymmetric functions and therefore 
        we need to check for the asymmetry and if the asymmetry 
        is present compute it...
        '''
        paras = [x]
        for i in range(self.info.para_num):
            paras.append(self.paras[i])

        return self.function(paras)

    def fitWrapper(self,val):
        '''
        This function serves to return the already computed function
        This is particularly important when looping quick for
        the function constructor
        '''
        paras = [self.x]
        for element in self.paras:
            paras.append(float(element))
        paras[self.current_par + 1] = val
        return self.function(paras)

    def quickReturn(self, x):
        '''
        This function serves to return the already computed function
        This is particularly important when looping quick for
        the function constructor
        '''
        if not self.calculated:
            self.compute(x)

        return self.y_bis

    def clone(self, source):
        '''
        The current system will have the fit classes separated
        between threads, meaning that we wish to clone the content
        in the main thread over to the worker. This requires to 
        clone the content
        '''
        if not source.info.name == self.info.name:
            print('ERROR')

        self.info.order         = int(source.info.order)
        self.info.para_num      = int(source.info.para_num)
        self.info.order         = int(source.info.order)
        self.info.para_bound    = list(source.info.para_bound)
        self.info.para_proc     = list(source.info.para_proc)

        self.x              = np.array(source.x)
        self.paras          = list(source.paras)
        self.para_ini       = list(source.para_ini)
        self.para_fix       = list(source.para_fix)