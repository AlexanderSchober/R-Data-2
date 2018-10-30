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


#######################################
#gui imports
from .io.io_handler         import IOHandler
from .data.datastructure    import Data_Structure
from .measurement.measurement_handler import Measurement

class EnvironmentHandler:
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
    def __init__(self):
        self.environments = {}

    def addEnv(self, name = 'No Name'):
        self.environments[name] = Environment(name)
        self.setCurrentEnv(name)

    def setCurrentEnv(self, name):
        self.current_env = self.environments[name]

    def getCurrentEnv(self):
        return self.current_env

class Environment:
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
    def __init__(self, name):
        self.name   = name
        self.io     = IOHandler()
        self.data   = Data_Structure()
        self.meas   = Measurement()
        
        
