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

from .environment   import Environment
from .volumes       import *
from .surfaces      import *
from .transformations import *



class Geometry(Environment):

    def __init__(self, **kwargs):
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

        #initialiset he position and orientations
        Environment.__init__(self)

        #initialize with a cube
        if 'volume' in kwargs.keys():
            exec("self.geometry = "+str(kwargs['volume'])+"(**kwargs)")

        elif 'surface' in kwargs.keys():
            exec("self.geometry = "+str(kwargs['surface'])+"(**kwargs)")

        else:
            self.geometry = Cube(**kwargs)

    def rotate(self, axis, angle, origin = [0,0,0]):
        '''
        ##############################################
        Rotate all points of this geometry around a 
        specified axis.
        ———————
        Input: 
        - axis ([float x 3]) rotation axis
        - angle (float) angle in degrees
        - origin ([float x 3]) rotation axis origin
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        transformation = Rotation(axis, angle, origin)

        self.geometry.applyTransformation(transformation) 

    def translate(self, vector):
        '''
        ##############################################
        Rotate all points of this geometry around a 
        specified axis.
        ———————
        Input: 
        - axis ([float x 3]) rotation axis
        - angle (float) angle in degrees
        - origin ([float x 3]) rotation axis origin
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        transformation = Translation(vector)

        self.geometry.applyTransformation(transformation) 

    def moveTo(self, position):
        '''
        ##############################################
        Rotate all points of this geometry around a 
        specified axis.
        ———————
        Input: 
        - axis ([float x 3]) rotation axis
        - angle (float) angle in degrees
        - origin ([float x 3]) rotation axis origin
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        transformation = Translation(position)

        self.geometry.applyTransformation(transformation) 

    def generateScriptGeometry(self, indentation = 0, parent = ''):
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
        output = indentation * indent + "######### GEOMETRY #########\n\n"
        output += self.geometry.generateScript(indentation, parent + "geometry.")

        return output
