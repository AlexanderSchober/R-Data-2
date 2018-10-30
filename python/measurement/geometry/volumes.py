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
from .points        import Point
from .surfaces      import *
from .operations    import distance, angle, processBarycenter, normal, angleAroundAxis
from .transformations import Translation, Rotation, SphericalFit

#############################
#mathematic libraries
import numpy as np


class Volume:

    def __init__(self, **kwargs):
        '''
        ##############################################
        This is the base class for volumes that will
        contain the routines common to all elements. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.reset()
        self.identifier_type = 'Volume'

        #process kwargs
        if 'color' in kwargs.keys():
            self.color = kwargs['color']
            
        else:
            self.color = [1, 1, 1, 1]

        #process kwargs
        if 'transp' in kwargs.keys():
            self.transp = kwargs['transp']
            
        else:
            self.transp = 1


    def reset(self):
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
        self.anchore_point      = None
        self.strucutre_surfaces = {}
        self.structure_points   = {}
        self.structure_lines    = {}
        self.raster_points      = {}
        self.surface_names      = []
        self.origin             = Point('Origin',0,0,0)

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
        output = indentation * indent + "points = [\n"

        for key in self.structure_points.keys():
            output += self.structure_points[key].generateScript(indentation + 1) + ",\n"

        output = output[:len(output) - 2]+ "\n"

        output += (indentation + 1) * indent + "]\n"
        output += (indentation + 1) * indent + "\n"

        output += (indentation) * indent + root + "initWithPoints(points)\n\n"

        return output

    def getSurface(self, name):
        '''
        ##############################################
        Grab the surface the user wants to modify
        ———————
        Input: 
        - name (str or int) name or number of the surface
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if isinstance(name, str):
            try:
                return self.strucutre_surfaces[name]

            except:
                print('This surface reference is not valid')

        elif isinstance(name, int):
            try:
                return self.strucutre_surfaces[self.surface_names[name]]

            except:
                print('This surface reference is not valid')

        else:
            print('Type of the name not valid')

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
        
        transformation.apply([self.anchore_point])
        
        for key in self.structure_points.keys():
            transformation.apply([self.structure_points[key]])

        for key in self.strucutre_surfaces.keys():
            self.strucutre_surfaces[key].applyTransformation(transformation)

    def processCorrection(self, points):
        '''
        ##############################################
        Correct the position and orientation of the 
        cube.
        ———————
        Input (optional): -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #calculate the baricenter of the given structure
        current_barycenter  = processBarycenter(
            [self.structure_points[key] 
            for key in self.structure_points.keys()])

        required_barycenter = processBarycenter(points)

        #process the transformation to move the object
        self.applyTransformation(
            Translation(required_barycenter - current_barycenter))

        ##############################################
        #process the first rotations
        barycenter = Point(
            'barycenter', 
            required_barycenter[0],
            required_barycenter[1],
            required_barycenter[2])

        condition = [(
            self.structure_points['Point_0'].vec[i] - barycenter.vec[i]) 
            == (points[0].vec[i] - barycenter.vec[i])
            for i in range(3)]

        if all(condition) :
            pass

        else:
            #process first rotation
            first_angle = angle(
                barycenter,
                self.structure_points['Point_0'],
                points[0])

            first_normal = normal([
                barycenter,
                self.structure_points['Point_0'],
                points[0]])

            tranformation = Rotation(
                first_normal,
                first_angle,
                origin = barycenter.vec )

            self.applyTransformation(tranformation)

        #############################################
        #process the second rotation
        condition = [(
            self.structure_points['Point_1'].vec[i] - barycenter.vec[i]) 
            == (points[1].vec[i] - barycenter.vec[i])
            for i in range(3)]

        if all(condition) :
    
            pass

        else:
            rotation_axis, rotation_angle = angleAroundAxis([
                points[0],
                barycenter,
                self.structure_points['Point_1'],
                points[1]])

            tranformation = Rotation(
                rotation_axis,
                rotation_angle,
                origin = barycenter.vec )

            self.applyTransformation(tranformation)
        
class Parallelepiped(Volume):
    
    def __init__(self, a = 1, b = 1, c = 1, alpha = 90., theta = 90., **kwargs):
        '''
        ##############################################
        This will be the base class for cubes and 
        cuboid objects. It will contaain all the 
        necessary informations, namely 8 points
        6 surfaces and 12 lines. 
        ———————
        Input: 
        - a (float) distance along x
        - b (float) distance along y
        - c (float) distance along z 

        - alpha (float) angle between a and b
        - theta (float) angle between b and c

        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        Volume.__init__(self, **kwargs)
        self.type_name = 'Parallelepiped'

        self.initialize()
        self.parameters = {}

        #set the dimensions
        self.parameters['a'] = a
        self.parameters['b'] = b
        self.parameters['c'] = c
        
        #set the angles
        self.parameters['alpha'] = alpha
        self.parameters['theta'] = theta


    def initialize(self):
        '''
        ##############################################
        This set the immutable parameters
        ———————
        Input (optional): -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #set the points for surfaces correspondance
        self.point_surface = (
            (4,7,5,3),
            (0,1,6,2),
            (0,3,4,1),
            (2,6,7,5),
            (0,2,5,3),
            (6,1,4,7))

        #set human surface names
        self.surface_names = (
            'top',
            'bottom',
            'front',
            'back',
            'left',
            'right')

    def initWithPoints(self, points, **kwargs):
        '''
        ##############################################
        This method supposes that the method is being
        initialised by the right points. This could be
        usefull in the event of saving the volume
        and then wanting to reread it.
        ———————
        Input (optional): -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #process the first determination of the shape

        #try to reset and then initalize
        self.reset()
        self.initialize()

        #set the dimensions
        self.parameters['a'] = round(distance(
            points[0],
            points[1]), 5)

        self.parameters['b'] = round(distance(
            points[0],
            points[2]), 5)
        self.parameters['c'] = round(distance(
            points[0],
            points[3]), 5)
        
        #set the angles
        self.parameters['alpha'] = angle(
            points[0],
            points[1],
            points[2])

        self.parameters['theta'] = angle(
            points[0],
            points[6],
            points[3])

        #build it
        self.buildVolume()

        #correct it
        self.processCorrection(points)


    def changeParameter(self, **kwargs):
        '''
        ##############################################
        change of parameters allowed in the system. 
        Note that this function will be overwritten
        by the child classes.
        ———————
        Input (optional): 
        - a (float) distance along x
        - b (float) distance along y
        - c (float) distance along z 

        - alpha (float) angle between a and b
        - theta (float) angle between b and c
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        allowed_keys = ['a', 'b', 'c', 'alpha', 'beta']

        for key in kwargs.keys():

            if key in allowed_keys:

                self.parameters[key] = kwargs[key]

            else:

                print("The parameter does not exist...")
                print("Choose between: ", *allowed_keys)

    def processVolume(self):
        '''
        ##############################################
        This method will first try to reset the 
        structures and then build all the elements. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #reset the structure
        self.reset()
        self.initialize()

        #for ease of read

        a = self.parameters['a']
        b = self.parameters['b']
        c = self.parameters['c']
        
        alpha = np.radians(self.parameters['alpha'])
        theta = np.radians(self.parameters['theta'])
        

        #create the points
        point_array = [

            #start
            [0, 0, 0],

            #first diagonal palne
            [
                a,
                0, 
                0],

            [
                np.cos(alpha) * b, 
                np.sin(alpha) * b, 
                0],
                
            [
                np.cos(alpha / 2.) * np.cos(theta) * c, 
                np.sin(alpha / 2.) * np.cos(theta) * c, 
                np.sin(theta) * c],

            #second diagonal palne
            [
                a + np.cos(alpha / 2.) * np.cos(theta) * c,
                np.sin(alpha / 2.) * np.cos(theta) * c, 
                np.sin(theta) * c],

            [
                np.cos(alpha) * b 
                + np.cos(alpha / 2.) * np.cos(theta) * c, 
                np.sin(alpha) * b
                + np.sin(alpha / 2.) * np.cos(theta) * c, 
                np.sin(theta) * c],
                
            [
                a + np.cos(alpha) * b,
                np.sin(alpha) * b, 
                0],

            #end diagonal point
            [
                a + np.cos(alpha) * b 
                + np.cos(alpha / 2.) * np.cos(theta) * c, 
                np.sin(alpha) * b
                + np.sin(alpha / 2.) * np.cos(theta) * c, 
                np.sin(theta) * c]
        ]

        point_array = list(np.around(np.array(point_array),10))

        return point_array

    def buildVolume(self):
        '''
        ##############################################
        This method will first try to reset the 
        structures and then build all the elements. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #reset the structure
        self.reset()
        self.initialize()

        #build the anchore point
        self.anchore_point = Point('Anchore', 0., 0., 0.)

        point_array = self.processVolume()

        ##############################################
        #create the points
        for i, coordinates in enumerate(point_array):

            self.structure_points['Point_'+str(i)] = Point(
                'Point_'+str(i), 
                coordinates[0],
                coordinates[1],
                coordinates[2],
                anchore = self.anchore_point)

        #build the anchore point
        barycenter = processBarycenter([self.structure_points[key] for key in self.structure_points.keys()])
        self.anchore_point = Point('Anchore', *barycenter.tolist())

        ##############################################
        #create the surfaces
        for i, point_list in enumerate(self.point_surface):

            self.strucutre_surfaces[self.surface_names[i]] = QuadSurface(
                [self.structure_points['Point_'+str(j)] for j in point_list],
                name    = self.surface_names[i],
                color   = self.color,
                transp  = self.transp)

            self.modifier(self.strucutre_surfaces[self.surface_names[i]])

        transform = Move(self.anchore_point, self.origin)
        self.applyTransformation(transform)

            
    def modifier(self, surface):
        '''
        ##############################################
        This function holds the modifier than can 
        then use the current structure of a cube
        to perform basic alterations. 

        In the present case it is not used as this is 
        a placeholder.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        
        surface.trace()

class Cuboid(Parallelepiped):
    
    def __init__(self, a = 1, b = 1, c = 1, **kwargs):
        '''
        ##############################################
        Subclass of Parallelepiped having fixed the
        angles to 0.
        ———————
        Input: 
        - a (float) distance along x
        - b (float) distance along y
        - c (float) distance along z 
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        Parallelepiped.__init__(
            self,
            a = a,
            b = b,
            c = c, 
            **kwargs)
        self.type_name = 'Cuboid'

    def changeParameter(self, **kwargs):
        '''
        ##############################################
        change of parameters allowed in the system. 
        Note that this function will be overwritten
        by the child classes.
        ———————
        Input (optional): 
        - a (float) distance along x
        - b (float) distance along y
        - c (float) distance along z 

        - alpha (float) angle between a and b
        - beta  (float) angle between b and c
        - gamma (float) angle between c and a 
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        allowed_keys = ['a', 'b', 'c']

        for key in kwargs.keys():

            if key in allowed_keys:

                self.parameters[key] = kwargs[key]

            else:

                print("The parameter does not exist...")
                print("Choose between: ", *allowed_keys)

class Cube(Cuboid):

    def __init__(self, a = 1, **kwargs):
        '''
        ##############################################
        Subclass of Parallelepiped having fixed the
        angles to 0. and the distances are all equal.
        ———————
        Input: 
        - a (float) distance along x, y, z
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        Cuboid.__init__(self, a = a, b = a , c = a, **kwargs )
        self.type_name = 'Cube'

    def changeParameter(self, **kwargs):
        '''
        ##############################################
        change of parameters allowed in the system. 
        Note that this function will be overwritten
        by the child classes.
        ———————
        Input (optional): 
        - a (float) distance along x
        - b (float) distance along y
        - c (float) distance along z 

        - alpha (float) angle between a and b
        - beta  (float) angle between b and c
        - gamma (float) angle between c and a 
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        allowed_keys = ['a']

        for key in kwargs.keys():

            if key in allowed_keys:

                self.parameters[key] = kwargs[key]

            else:

                print("The parameter does not exist...")
                print("Choose between: ", *allowed_keys)

        #do the cube thing
        self.parameters['b'] = self.parameters['a']
        self.parameters['c'] = self.parameters['a']
        
class Sphere(Cube):

    def __init__(self, r = 1, **kwargs):
        '''
        ##############################################
        The sphere will be based ont a modification of 
        the cube shape.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        Cube.__init__(self, a = 2 * r / np.sqrt(3), **kwargs)

        self.parameters['r'] = r

        self.type_name = 'Sphere'

    def modifier(self, surface):
        '''
        ##############################################
        This function holds the modifier than can 
        then use the current structure of a cube
        to perform basic alterations. 

        In the present case it is not used as this is 
        a placeholder.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        # process the resolution
        if surface.resolution_x < 4:
            surface.resolution_x = 4

        if surface.resolution_y < 4:
            surface.resolution_y = 4

        ##############################################
        # trace the points
        surface.trace()

        ##############################################
        # set the tranformation
        tranformation = SphericalFit(
            center = processBarycenter(
                [
                    self.structure_points[key] 
                    for key in self.structure_points.keys()
                    ]),
            radius = self.parameters['r'])

        surface.applyTransformation(tranformation)


        
class Cylinder(Cuboid):
    
    def __init__(self, r = 1, height = 1, **kwargs):
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
        Cuboid.__init__(
            self, 
            a = 2 * r / np.sqrt(2),
            b = 2 * r / np.sqrt(2),
            c = height,
            **kwargs)

        self.type_name = 'Cylinder'
        self.parameters['r']        = r
        self.parameters['height']   = height

    def modifier(self, surface):
        '''
        ##############################################
        This function holds the modifier than can 
        then use the current structure of a cube
        to perform basic alterations. 

        In the present case it is not used as this is 
        a placeholder.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        # process the resolution
        if surface.resolution_x < 4:
            surface.resolution_x = 4

        if surface.resolution_y < 4:
            surface.resolution_y = 4

        ##############################################
        # trace the points
        surface.trace()

        ##############################################
        # prepare the transformation
        center  = processBarycenter([
                self.structure_points[key] 
                for key in self.structure_points.keys()])

        reference = surface.border_points[0]

        axis    = (
            self.structure_points['Point_3'].vec 
            - self.structure_points['Point_0'].vec) 


        ##############################################
        # set the tranformation
        tranformation = CylinderFit(
            center = center,
            axis   = axis, 
            ref    = reference)

        surface.applyTransformation(tranformation)