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
from ..geometry.geometry     import Geometry 
from ..physics.physics       import Physics

class SampleElement(Geometry, Physics):
    
    def __init__(self, name = None, **kwargs):
        '''
        ##############################################
        This is a sample element ans will contain all 
        the information about its spatial shape and
        its physical properties.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #initialiset he position and orientations
        Geometry.__init__(self, **kwargs)
        Physics.__init__(self, **kwargs)

        self.name = name

    def generateScript(self, indentation = 0, root = ''):
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
        output = ""
        output += self.generateScriptGeometry(indentation, root)
        output += self.generateScriptPhysics(indentation, root)
    
        return output

