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
from ..geometry.geometry import Geometry

#############################
#mathematic libraries
import numpy as np

class InstrumentHandler():

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
        pass

    def generateScript(self, indentation = 0, parent = ""):
        '''
        ##############################################
        This method will allow the generation of a 
        script of the current structure.
        ———————
        Input (optional): -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        indent = "    "
        output = indentation * indent + "\n"


        return output