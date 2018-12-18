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

import numpy as np

class Point:

    def __init__(self,name, x, y, z, orientation = None,  anchore = None):
        '''
        ##############################################
        A point in space that can be defined as its
        own or in a complete referential.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #parameter init
        self.name           = name
        self.children       = {}
        self.anchore        = anchore
        self.orientation    = [0,0,0]

        #functional init
        self.setRelativePosition(x, y, z, orientation, anchore)
        self.setAbsolutePosition(x, y, z)
        
    def __str__(self):
        '''
        ##############################################
        Returns a string to be printed when the print 
        is called onto the method. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        text  = ""
        text += self.name+" coordinates : "
        text += str(self.x_abs) +" (" + str(self.x_rel)+")"+ ", "
        text += str(self.y_abs) +" (" + str(self.y_rel)+")"+ ", "
        text += str(self.z_abs) +" (" + str(self.z_rel)+")"+ "\n"

        for key in self.children.keys():
            text += "  "+self.children[key].__str__()

        return text

    def setRelativePosition(self, x, y, z, orientation, anchore):
        '''
        ##############################################
        A point in space that can be defined as its
        own or in a complete referential.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if isinstance(anchore, Point):

            #process the positions
            self.x_rel = x + anchore.x_rel
            self.y_rel = y + anchore.x_rel
            self.z_rel = z + anchore.y_rel

            #register the point at the achore
            self.anchore.registerChild(self)
        
        else:

            #process the positions
            self.x_rel = x
            self.y_rel = y
            self.z_rel = z

    def setAbsolutePosition(self, x, y, z):
        '''
        ##############################################
        Parents will process the position of their
        children by injecting this value. This will 
        account for trnsformations such as sliding 
        and rotation. 

        One parent point will then link to the achore
        of the environement. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.vec = np.zeros((3))

        self.vec[0] = self.x_abs = x
        self.vec[1] = self.y_abs = y
        self.vec[2] = self.z_abs = z

    def registerChild(self, point):
        '''
        ##############################################
        Set the abolute position of a point 
        ———————
        Input: 
        - Point instance that is anchored on me
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.children[point.name] = point

    def generateScript(self, indentation = 0):
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
        output = indentation * indent + "Point("
        output += "'" + str(self.name)+ "',"
        output += str(self.vec[0])+ ","
        output += str(self.vec[1])+ ","
        output += str(self.vec[2])+ ")"

        return output