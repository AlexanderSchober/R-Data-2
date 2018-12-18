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

#############################
#personal libraries


#############################
#mathematic libraries
import numpy as np



class Instrument():
    
    def __init__(self, **kwargs):
        '''
        ##############################################
        This is the main intrument class the will 
        manage general instrument logic, such as
        position, orientation.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.initialize()

    def reset(self):
        '''
        ##############################################
        In this class we will reset all the intruments
        parameter and then set them.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #finnally initialize
        self.initialize()

    def initialize(self):
        '''
        ##############################################
        In this class we will reset all the intruments
        parameter and then set them.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        pass

    def addGeometry(self):
        '''
        ##############################################
        In this class we will reset all the intruments
        parameter and then set them.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        pass

    
    def removeGeometry(self):
        '''
        ##############################################
        In this class we will reset all the intruments
        parameter and then set them.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        pass

class RamanSpectrometer(Instrument):
    
    def __init__(self, **kwargs):
        '''
        ##############################################
        This class will mange all the physical proper-
        ties of a sample. This can be surface, volume
        or tensor properties. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        Instrument.__init__(self)