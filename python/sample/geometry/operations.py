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
#personal libraries
from .points import Point

#############################
#mathematic libraries
import numpy as np
import math
import scipy.linalg as sci_lin

def distance(point_0, point_1):
    '''
    ##############################################
    Processes the distance between two points in
    the three dimensional space.
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    #set the vecotrs
    if isinstance(point_0, Point):
        vec_0 = point_0.vec
        vec_1 = point_1.vec

    elif isinstance(point_0, np.ndarray):
        vec_0 = point_0
        vec_1 = point_1

    return np.linalg.norm(vec_1 - vec_0)

def angle(point_0, point_1, point_2, degrees = True):
    '''
    ##############################################
    Processes the angle between three points in
    the three dimensional space.
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    #set the vecotrs
    if isinstance(point_0, Point):
        vec_0 = point_1.vec - point_0.vec
        vec_1 = point_2.vec - point_0.vec

    elif isinstance(point_0, np.ndarray):
        vec_0 = point_1 - point_0
        vec_1 = point_2 - point_0

    #calculate the angle
    angle_cos = (
        np.dot(vec_0,vec_1) 
        / distance(point_0, point_1) 
        / distance(point_0, point_2) )

    angle = np.arccos(np.clip(angle_cos, -1, 1)) 

    #return degrees if necessqyr
    if degrees:
        return np.degrees(angle)
    else:
        return angle

def processBarycenter(points):
    '''
    ##############################################
    Process the barycenter of the current object
    where all the points have a mass set to 1. 
    Then go through them.
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    #set the vectors
    barycenter = np.asarray([0.,0.,0.])

    for point in points:
        barycenter += point.vec
    
    return barycenter / len(points)

def normal(points):
    '''
    ##############################################
    This method will process the normal vecotr to
    as set of three points defining a surface.
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    ##############################################
    #first we get process all values...
    if isinstance(points[0], Point):
        point_0 = points[0].vec
        point_1 = points[1].vec
        point_2 = points[2].vec

    elif isinstance(points[0], np.ndarray):
        point_0 = points[0]
        point_1 = points[1]
        point_2 = points[2]

    normal_vector = (np.cross( 
            point_1 - point_0,
            point_2 - point_0)
            / sci_lin.norm(np.cross( 
            point_1 - point_0,
            point_2 - point_0)))

    return normal_vector


def angleAroundAxis(points):
    '''
    ##############################################
    This method aims at processing the angle of 
    tzo vecotrs defined by three points around
    a common axis.
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''

    ##############################################
    #first we get process all values...
    if isinstance(points[0], Point):
        point_0 = points[0].vec
        point_1 = points[1].vec
        point_2 = points[2].vec
        point_3 = points[3].vec

    elif isinstance(points[0], np.ndarray):
        point_0 = points[0]
        point_1 = points[1]
        point_2 = points[2]
        point_3 = points[3]

    ##############################################
    #we assume that the first set 1 and 2 is the axis
    main_axis = (point_1 - point_0) / sci_lin.norm(point_1 - point_0)

    scale_0 = np.dot(
        point_2 - point_0,
        main_axis)

    scale_1 = np.dot(
        point_2 - point_0,
        main_axis)

    vec_0 = (point_2 - point_0) - scale_0 * main_axis
    vec_1 = (point_3 - point_0) - scale_1 * main_axis

    ##############################################
    #get the angle
    resulting_angle = angle(point_0, point_0 + vec_0, point_0 + vec_1)

    return main_axis, resulting_angle

