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


from ..io import io_file_methods as file_methods 
from ..measurement.measurement_handler import Measurement

import os
import datetime
import numpy as np

class IOImportHandler:
    '''
    ##############################################
    The io import handler will manage the main
    import organisation. 
    ———————
    Input: 
    - parent manager structure
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, parent = None):
        
        ##############################################
        #declare local variables
        self.parent = parent

    def setFolder(self, path):
        self.folder = path 

    def readDataFile(self, path, data_struc):  
        worker = IODataWorker(path, data_struc)  
        worker.run()

    def readSampleFile(self, path, meas_struc):  
        worker = IOMeasWorker(path, meas_struc) 
        worker.run()

class IODataWorker:
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
    def __init__(self, path, data_struc):
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
        self.path = path
        self.data_struc = data_struc

    def run(self):
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
        line_idx = self._getLines()

        self._dataReader(line_idx[2])
        self._axisReader(line_idx[1], line_idx[2])

        print(self.data_struc)

    def _getLines(self):
        '''
        ##############################################
        This routine will determine the lines at
        chich individual data is written dowm. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        with open(self.path, 'r') as f:
            for i, line in enumerate(f.readlines()):
                if 'METADATA' in line:
                    line_meta = i
                elif 'DATA' in line:
                    line_data = i
                elif 'AXIS' in line:
                    line_axis = i

        return [line_meta, line_axis, line_data]
 
    def _axisReader(self, start_line, end_line):
        '''
        ##############################################
        This routine will read through the axis
        information and try to set it in the 
        datastructure. The datastructure needs to be 
        already validated for this effect to be 
        meaningfull.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        with open(self.path, 'r') as f:
            axes_str = f.readlines()[start_line+1:end_line]

            for idx, axis_str in enumerate(axes_str):
                self.data_struc.axes.set_name(idx, name = axis_str.strip('\n').split('**')[1])
                self.data_struc.axes.set_unit(idx, unit = axis_str.strip('\n').split('**')[2])
                self.data_struc.axes.set_axis(idx, axis = [float(e) for e in axis_str.strip('\n').split('**')[3].split(',')[1:]])

    def _dataReader(self, start_line):
        '''
        ##############################################
        This routine will read in the data and then 
        send it immidiatly to the datastructures.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #read in 
        with open(self.path, 'r') as f:
            for i, line in enumerate(f):
                if i == start_line + 1:

                    #determine the indices
                    indexes = self._processIndex(line)

                    #grab the dimensionality and prepare
                    data_array = [[[],[]] for k in range(len(indexes))]

                if i > start_line + 1:

                    elements = line.split(',')

                    for j in range(len(indexes)):
                        data_array[j][0].append(float(elements[2*j]))
                        data_array[j][1].append(float(elements[2*j+1]))

        ##############################################
        #inject into datastructure
        for j in range(len(indexes)): 
            self.data_struc.add_data_object(np.asarray(data_array[j]), indexes[j])

        self.data_struc.validate()

    def _processIndex(self, line):
        '''
        ##############################################
        This routine will go through the string and 
        popuate the index array
        ———————
        Input: 
        - line is a string containing all the indexes
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        characters = [' ', '\n','\t']
        temp_str = str(line)

        for character in characters:
            temp_str = temp_str.strip(character)

        temp_array = [e.strip('[').strip(']') for e in temp_str.split('],[')]

        idx_array = []
        for element in temp_array:
            idx_array.append([int(e) for e in element.split(',')])
    
        return idx_array

    def _metaReader(self):
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
        meta_data = None
    
        return meta_data

class IOMeasWorker:
    '''
    ##############################################
    
    ———————
    Input: 
    - parent manager structure
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, path, meas_struc):
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
        self.path = path
        self.meas_structure = meas_struc

    def run(self):
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
        pass
 
    def _sampleReader(self):
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
        axis = None

        return axis

