#--FUNCTION--#

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


from ..function_template import InfoClass
from ..function_template import FunctionClass

import numpy as np

class LinearInfo(InfoClass):
    '''
    This class will contain information about 
    the function, parameters and names
    '''
    def __init__(self):
        InfoClass.__init__(self)
        
        #######################
        #name of the function
        self.name = 'Linear'
        
        #how to order the functions( do not touch lorenz and linear)
        self.order = 1
        
        #number of parameters
        self.para_num   = 3
        
        #######################
        #parameter names
        self.para_name = [
            ['Position', 0],
            ['Amplitude', 0],
            ['Offset', 0]]
                                        
        #Parameter units
        self.para_unit  = [
            'cm-1',
            'Intensity',
            'Intensity']

        self.para_fix_ini   = [
            True,
            False,
            False]   
                                       
        #######################
        #Parameter Boundaries
        self.para_bound    = [
            ['-10','10', False],        # <- Relative shift min, max
            ['xmin','xmax', True],     # <- Absolute shift min, max
            
            ['-2','2', False],          # <- Relative shift min, max
            ['0.01','Inf', True],      # <- Absolute shift min, max
            
            ['-1000','1000', False],    # <- Relative shift min, max
            ['-Inf','Inf', True],         # <- Absolute shift min, max
            ]

        #######################
        #Parameter Boundaries
        self.para_proc    = [
            5,         # <- Number of iteration
            [0,1,2]]   # <- Order of Processing

class Linear(FunctionClass):
    '''
    In this class we will store the 
    cropped data used for the calculation
    this data can be modified once the class 
    is loaded to fit the needs
    '''
    
    def __init__(self, info, source = None):
        FunctionClass.__init__(self, info, source)
    
    def function(self,para):
        '''
        This is the linear function
        '''
        #function parameters
        x           = np.asarray(para[0])
        Position    = para[1]
        Factor      = para[2]
        Offset      = para[3]
    
        #process the function
        y           = ( x - Position ) * Factor + Offset
        return y
    