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
#   Alexander Schober <alexander.schober@mac.com>
#
# *****************************************************************************

#############################
#personal libraroes
from .points import Point
from .transformations import *
from .operations import normal

#############################
#mathematic libraries
import numpy as np


class Surface:

    def __init__(self, **kwargs):
        '''
        ##############################################
        This is the main surface class that will
        contain all common function calls such as 
        parameter changes and processing.
        ———————
        Input: -
        ———————
        Output: -
        ———————

        status: active
        ##############################################
        '''
        self.identifier_type = 'Surface'
        self.generated      = False
        self.points         = []
        self.vertexes       = []
        self.faces          = []
        self.topography     = None
        self.border_points  = []

        self.resolution_x = 1
        self.resolution_y = 1

        #process kwargs
        if 'color' in kwargs.keys():
            self.color = kwargs['color']

        else:
            self.color = [1, 1, 1, 1]

    def changeResolution(self, resolution_x, resolution_y):
        '''
        ##############################################
        Change the resolution parameter
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y

    def getVertices(self):
        '''
        ##############################################
        Sends out the vertices for ploting in the
        desired numpy format. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        vertices = np.asarray(
            [ list(point.vec) for point in self.points ]
        )

        return vertices

    def getFaces(self):
        '''
        ##############################################
        Sends out the faces for ploting in the
        desired numpy format. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        
        return self.faces

    def applyTransformation(self, transformation):
        '''
        ##############################################
        This method will be used before processing a
        volume as the surfaces will be 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        
        #apply it to the generated points
        if self.generated:
            transformation.apply(self.border_points)
        
        #apply it to out points
        transformation.apply(self.points)


class QuadSurface(Surface):

    def __init__(self, border_points = None, height = None, width = None, **kwargs):
        '''
        ##############################################
        This class is supposed to manage the quadratic 
        surfaces. It will initialise the positions and
        then create the faces array.      

        It is supposed that the points are given in an
        ordered manner forming rectangular strucutres. 
        ———————
        Input: 
        - border_points is an array of point classes
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        Surface.__init__(self, **kwargs)

        self.type_name = 'QuadSurface'

        ##############################################
        #save the points locally
        self.logic = [
            (border_points == None),
            (height == None),
            (height == None)
            ]

        if all(self.logic):
            self.border_points = [
                Point('Point_0', 0, 0, 0),
                Point('Point_1', 1, 0, 0),
                Point('Point_2', 1, 1, 0),
                Point('Point_3', 0, 1, 0)
            ]
            self.generated = True
        
        elif not self.logic[0]:
            self.border_points = border_points
            self.generated = False

        elif self.logic[0] and not self.logic[1] and not self.logic[2]:
            self.border_points = [
                Point('Point_0', 0, 0, 0),
                Point('Point_1', width, 0, 0),
                Point('Point_2', width, height, 0),
                Point('Point_3', 0, height, 0)
            ]
            self.generated = True

        ##############################################
        #process the normal vector to process topography
        self.normal_vector = normal(self.border_points)
        
    def trace(self):
        '''
        ##############################################
        calculate points and link them to create the
        vertices.   
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #set up the system
        self.points = [
            [0,0,0]
            for i in range(
                ( self.resolution_x + 1 )
                * ( self.resolution_y + 1) ) ]

        self.faces = [
            [0,0,0]
            for i in range(
                self.resolution_x
                * self.resolution_y
                * 2)]

        ##############################################
        #fill the points
        for j in range(self.resolution_y + 1):
            for i in range(self.resolution_x + 1):

                #process intermediate
                p_0_bis = ( (self.border_points[3].vec - self.border_points[0].vec) / self.resolution_y) * j + self.border_points[0].vec
                p_1_bis = ( (self.border_points[2].vec - self.border_points[1].vec) / self.resolution_y) * j + self.border_points[1].vec
                
                p_ij = ( (p_1_bis - p_0_bis) / self.resolution_x) * i + p_0_bis

                self.points[j * (self.resolution_y + 1) + i] = Point(
                    str(j * (self.resolution_y + 1) + i),
                    p_ij[0],
                    p_ij[1],
                    p_ij[2]
                )

        ##############################################
        #set the faces
        gerade_j = True
        gerade_i = True
        for j in range(self.resolution_y):

            gerade_i = int(gerade_j)
            gerade_j = not gerade_j

            for i in range(self.resolution_x):

                if gerade_i:

                    self.faces[j * self.resolution_x * 2 + 2 * i] = [
                        (j) * (self.resolution_x + 1) + (i),
                        (j + 1) * (self.resolution_x + 1)+ (i),
                        (j) * (self.resolution_x + 1) + (i + 1)
                    ]
                
                    self.faces[j * self.resolution_x * 2 + 2 * i + 1] = [
                        (j + 1) * (self.resolution_x + 1) + (i),
                        (j + 1) * (self.resolution_x + 1) + (i + 1),
                        (j) * (self.resolution_x + 1) + (i + 1)
                    ]

                
                else:

                    self.faces[j * self.resolution_x * 2 + 2 * i] = [
                        (j) * (self.resolution_x + 1) + (i),
                        (j + 1) * (self.resolution_x + 1) + (i),
                        (j + 1) * (self.resolution_x + 1) + (i + 1)
                    ]
                
                    self.faces[j * self.resolution_x * 2 + 2 * i + 1] = [
                        (j) * (self.resolution_x + 1) + (i),
                        (j) * (self.resolution_x + 1) + (i + 1),
                        (j + 1) * (self.resolution_x + 1) + (i + 1)
                    ]

                gerade_i = not gerade_i

        ##############################################
        #apply topo
        if not isinstance(self.topography, type(None)):
            self.applyTopography()

    def setTopography(self, topography, color, x_axis = None, y_axis = None, scale = 1):
        '''
        ##############################################
        This function will allow to add a topography
        to the surface element. The topography will be
        given by an x axis and an y axis in form of 1D
        numpy array structures. The topography will be 
        given by a 2D numpy array.

        A scalling factor is given to account for
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #save topograhy locally
        self.topography = np.asarray(topography)
        self.color = color

        #change the resolution
        self.changeResolution(
            topography.shape[0] - 1,
            topography.shape[1] - 1)
        
        #retrace the points with the topography
        self.trace()

    
    def applyTopography(self):
        '''
        ##############################################
        This function applies the provided topography 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        for j in range(self.resolution_y + 1):
            for i in range(self.resolution_x + 1):

                #create tranformation
                translate = Translation(self.normal_vector * self.topography[j][i])

                translate.apply([self.points[j * (self.resolution_y + 1) + i]]) 



class Square(QuadSurface):
    
    def __init__(self, dimension = 1, **kwargs):
        '''
        ##############################################
        This is a wrapper class that will indeed 
        call the parent class made up of Quadsurface
        that inherits from surfaces.    
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        QuadSurface.__init__(self, height = dimension, width = dimension, **kwargs)
        self.type_name = 'Square'

class Rectangle(QuadSurface):
    
    def __init__(self, height = 1, width = 1, **kwargs):
        '''
        ##############################################
        This is a wrapper class that will indeed 
        call the parent class made up of Quadsurface
        that inherits from surfaces.     
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        QuadSurface.__init__(self, height = height, width = width, **kwargs)
        self.type_name = 'Rectangle'

class TriSurface(Surface):

    def __init__(self):
        '''
        ##############################################
        This class is supposed to manage the quadratic 
        surfaces. It will initialise the positions and
        then create the faces array.      
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        Surface.__init__(self)
        self.type_name = 'TriSurface'

class CylSurface(Surface):

    def __init__(self):
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
        Surface.__init__(self)
        self.type_name = 'CylSurface'

class SphereSurface(Surface):

    def __init__(self):
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
        Surface.__init__(self)
        self.type_name = 'SphereSurface'

class ConeSurface(Surface):

    def __init__(self):
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
        Surface.__init__(self)
        self.type_name = 'ConeSurface'