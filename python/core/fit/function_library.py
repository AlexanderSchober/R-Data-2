#  -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2017 by Alexander Schober 
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


from ..io.io_file_methods import getFileNames
import os


class FunctionLibrary:
    '''
    It turns out that the function library is needed in 
    different places and therefore should be set as an 
    external class which can be imported and then run.
    '''

    def importFunctions(self):
        '''
        This function will import all the fit elements
        locally to have them available in the thread.
        '''

        ########################
        # grab the paths in the folder and select who is a function 
        # definition file
        path_array  = [
            os.path.dirname(os.path.realpath(__file__)),
            'functions']
        path            = os.path.join(*path_array)
        path_array      = getFileNames(path, '.py')
        temp_path       = []
        temp_class_name = []

        for path in path_array:
            with open(path, 'r') as f:
                first_line = f.readline()
                if len(first_line.split( '--FUNCTION--')) > 1:
                    temp_path.append(path)
    
        self.num_func = len(temp_path)
    
        for path in temp_path:
            lines = [line.rstrip('\n') for line in open(path)]
            for line in lines:
                if len(line.split('class')) > 1:
                    if len(line.split('class')[1].split('(')) > 1:
                        temp_class_name.append(
                            line.split('class')[1].split('(')[0])

        ########################
        #Process the import
        for i in range(0, self.num_func):
            name = os.path.split(temp_path[i])[1]
            exec('from .functions.'+name.split('.py')[0]+' import '+temp_class_name[2*i]+','+temp_class_name[2*i+1])

        ########################
        #set it all up
        self.func_ptrs      = [None] * self.num_func
        self.func_inf_ptrs  = [None] * self.num_func
        self.class_ptrs     = [None] * self.num_func
        self.func_order     = [None] * self.num_func
        
        for i in range(0,self.num_func):
            self.func_ptrs[i] = []
            exec('self.func_inf_ptrs[i] = '+temp_class_name[2*i]+'()')
            exec('self.class_ptrs[i] = '+temp_class_name[2*i+1])
            self.func_order[i] = self.func_inf_ptrs[i].order

        ########################
        #Order them
        self.func_ptrs        = [
            x for _,x in sorted(zip(
                self.func_order,
                self.func_ptrs ))]

        self.func_inf_ptrs   = [
            x for _,x in sorted(zip(
                self.func_order,
                self.func_inf_ptrs ))]

        self.class_ptrs            = [
            x for _,x in sorted(zip(
                self.func_order,
                self.class_ptrs ))]

        self.resetDictionary()

    def addFunction(self, name, rays = 1, source = None):
        '''
        Add a initiated function to the functions in
        the dictionary associated to the name
        '''

        if rays == 1:
            self.func_dict[name][2].append(
                self.func_dict[name][1](
                    self.func_dict[name][0],
                    source = source))
        else:
            self.func_dict[name][2].append([
                self.func_dict[name][1](
                    self.func_dict[name][0],
                    source = source)
                for ray in range(rays)])

    def resetDictionary(self):
        '''
        Set the dictionary of all functions and
        their constructors.
        '''
        self.func_dict = {}
        for i in range(0,self.num_func): 
            self.func_dict[self.func_inf_ptrs[i].name] = [
                self.func_inf_ptrs[i],
                self.class_ptrs[i],
                self.func_ptrs[i]]