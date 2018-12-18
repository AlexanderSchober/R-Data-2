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
from .operations    import angle, distance

#############################
#mathematic libraries
import numpy as np
import scipy.linalg as sci_lin


class Rotation:
    
    def __init__(self, axis, angle, origin = [0,0,0]):
        '''
        ##############################################
        This class we be initialised and setup to 
        allow the rotation of elements. 
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
        self.axis   = axis
        self.origin = origin
        self.angle  = np.pi * angle / 180.

        #set up the rotations
        self.rotation_m  =  sci_lin.expm(
            np.cross(np.eye(3), self.axis/sci_lin.norm(self.axis)
            * self.angle))

        #set up the translations
        self.t      = np.zeros((3,4))
        self.t_t    = np.zeros((3,4))

        np.fill_diagonal(self.t,1)
        np.fill_diagonal(self.t_t,1)

        self.t[0:3,3] = - np.asarray(origin)[:]
        self.t_t[0:3,3] = + np.asarray(origin)[:]

    def apply(self, points):
        '''
        ##############################################
        rotate the passed point element. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        for point in points:

            coordinates = point.vec.tolist()

            result = np.dot(
                self.t_t,
                list(np.dot(
                    self.rotation_m,
                    np.dot(
                        self.t,
                        coordinates+[1])
                    )
                )
                +[1])

            point.setAbsolutePosition(*list(result))

class Translation:
    
    def __init__(self, vector):
        '''
        ##############################################
        This class we be initialised and setup to 
        allow the translation of elements. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.vector     = vector
        self.t          = np.zeros((3,4))
        np.fill_diagonal(self.t,1)
        self.t[0:3,3]   = np.asarray(self.vector)[:]
        
    def apply(self, points):
        '''
        ##############################################
        translate the passed point element. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        for point in points:

            coordinates = point.vec.tolist()

            result = np.dot(self.t, coordinates+[1])

            point.setAbsolutePosition(*list(result))

class Move(Translation):
    
    def __init__(self, point_0, point_1):
        '''
        ##############################################
        Creates a translation from point 1 to 2
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        Translation.__init__(self,point_1.vec - point_0.vec)
        


class SphericalFit:
        
    def __init__(self, center = [0,0,0], radius = 1):
        '''
        ##############################################
        Here we will simply set all points on a sphere
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.center = center
        self.radius = radius
        
    def apply(self, points):
        '''
        ##############################################
        translate the passed point element. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        for point in points:

            axis        = (point.vec - self.center)
            axis        = axis / sci_lin.norm(axis)
            result      = self.center + self.radius * axis
            point.setAbsolutePosition(*list(result))

class CylinderFit:
        
    def __init__(self, center = [0,0,0], axis = [0,0,1], ref = [1,0,0]):
        '''
        ##############################################
        This is the cylinder method that will take
        all points and depending on their angle will
        extend them.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.center = center
        self.axis   = axis / sci_lin.norm(axis)
        self.ref    = ref.vec - np.dot(self.axis, ref.vec - self.center) * self.axis
        
    def apply(self, points):
        '''
        ##############################################
        translate the passed point element. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        for point in points:

            factor      = np.dot(self.axis, point.vec - self.center)
            point_bis   = point.vec - factor * self.axis
            rel_angle   = angle(self.center,  self.ref, point_bis, degrees = False)

            result = (
                self.center
                + (point_bis - self.center)
                * (1 + (np.abs(np.sin(rel_angle*2)) * (np.sqrt(2) - 1)))
                + factor * self.axis)

            point.setAbsolutePosition(*list(result))




