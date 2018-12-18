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
from .sample_element import SampleElement


class SampleHandler():

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

        #initialise local variable
        self.elements       = {}

        #set initial parameters
        self.initializeAttributes()

        #overwrite attributes
        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])
        
    def initializeAttributes(self):
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
        self.elements   = {}

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

        for key in self.elements.keys():

            #start the sample element creation
            output += indentation * indent + "### Adding the sample element: "+str(key)+"\n"
            output += indentation * indent + parent + "newElement(\n"
            output += (indentation + 1) * indent + "'" + str(self.elements[key].name) + "',\n"

            #check what we have to deal with
            if self.elements[key].geometry.identifier_type == 'Surface':
                output += (indentation + 1) * indent + "surface = " 

            elif self.elements[key].geometry.identifier_type == 'Volume':
                output += (indentation + 1) * indent + "volume = " 

            output += "'" + self.elements[key].geometry.type_name + "',\n"
            output += (indentation + 1) * indent + "color = np.asarray(" 
            output += str(self.elements[key].geometry.color.tolist())+ ")"

            # close it up
            output += indentation * indent + ")\n\n"

            root = parent + "elements['"+key+"']."

            output += self.elements[key].generateScript(indentation, root)

        return output

        
    def newElement(self, name = 'None', **kwargs):
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
        if name == 'None':

            name = "sample_"+len(self.elements.keys())

        self.elements[name] = SampleElement(name = name, **kwargs)

        return self.elements[name]

