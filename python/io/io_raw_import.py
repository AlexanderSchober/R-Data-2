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

class IORawHandler:
    '''
    ##############################################
    This class will be initialised and then kept
    as a manager of input output such as loading
    files from a directory and so on. 
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

        ##############################################
        #Launch measurement environment
        self.measurement = Measurement()
        self.getMeasurementString()

    def init_raw_import(self):
        '''
        ##############################################
        Initialize the import layout for multiple files
        from a directory. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.directory_path     = ''
        self.save_file_path     = ''
        self.raw_file_list      = []
        self.file_list_mask     = []
        self.file_list          = []
        self.dimension_list     = []
        self.common_str         = []
        self.visual_string      = ''
        
    def getMeasurementString(self):
        '''
        ##############################################
        Tell the measurement handler that he needs to 
        print the measurement.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.meas_string = self.measurement.generateScript()

    def set_import_directory(self, path):
        '''
        ##############################################
        This routine will allow the user to set the 
        import directory and the routine will then 
        lookf for files. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.directory_path = os.path.abspath(path)

    def set_save_file(self, path):
        '''
        ##############################################
        This routine will allow the user to set the 
        import directory and the routine will then 
        lookf for files. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.save_file_path = os.path.abspath(path)

    def scan_directory(self):
        '''
        ##############################################
        This routine will allow the user to set the 
        import directory and the routine will then 
        lookf for files. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.raw_file_list = file_methods.get_files_in_folder(
            self.directory_path, 
            extension = '.txt')

        self.file_list_mask = [True for i in self.raw_file_list]

        self.evaluate_ignore()

        return self.raw_file_list

    def evaluate_ignore(self):
        '''
        ##############################################
        This routine will evaluate which files the
        user wnats to truely keep in the end. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.file_list = []

        for i in range(len(self.raw_file_list)):
            if self.file_list_mask[i]:
                self.file_list.append(str(self.raw_file_list[i]))

    def toggle_mask(self, index, val):
        '''
        ##############################################
        This routine will allow the user to set the 
        import directory and the routine will then 
        lookf for files. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.file_list_mask[index] = val
        self.evaluate_ignore()
        self.evaluate_files()
        
    def evaluate_files(self):
        '''
        ##############################################
        Process dimensions. Will go through all the 
        files and try to determine common strings
        and then try to separate it into dimensions...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.common_str     = []
        self.dimension_list = []

        try:
            self.common_str = file_methods.get_common_substrings(self.file_list)
        except: 
            pass

        try:
            self.dimension_list = self._process_dimensions(
                self.common_str, 
                previous = self.dimension_list )
        except: 
            pass

        self.build_string()

    def build_string(self):
        '''
        ##############################################
        This method will generate a string with the 
        input being a list of strings that are
        common to all files...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        text    = ""
        colors  = [
            '#0000FF',
            '#8A2BE2',
            '#A52A2A',
            '#00008B',
            '#8B008B',
            '#228B22',
            '#FFD700'
            ]
        common_str_fix = self.common_str + ['.txt']

        for i, element in enumerate(self.common_str):
                
            #put the element
            text += "<span style='font-size:12pt; font-weight:600; color:#000000;'>"
            text += str(element)
            text += "</span>"

            if self.dimension_list[i][4]:

                #put the var
                text += "<span style='font-size:12pt; font-weight:600; color:"
                text += str(colors[i])
                text += ";'> ("
                text += self.dimension_list[i][0]
                text += ' ['
                text += self.dimension_list[i][1]
                text += '] '
                text += ") </span>"

            else:
                #put the var
                text += "<span style='font-size:12pt; font-weight:600; color:#000000;'>"
                text += self.file_list[0].split(element)[1].split(common_str_fix[i+1])[0]
                text += "</span>"

        text += "<span style='font-size:12pt; font-weight:600; color:#000000;'>"
        text += str(".txt")
        text += "</span>"

        self.visual_string = text

    def _process_dimensions(self, common_strings, previous = None):
        '''
        ##############################################
        This method will generate a string with the 
        input being a list of strings that are
        common to all files...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        dimension_list = []

        for i in range(len(common_strings)):
            #set the split elements
            pre_split = common_strings[i]

            if i + 1 == len(common_strings):

                if '.' in common_strings[i]:
                    post_split = None

                else:
                    post_split = '.txt'

            else:
                post_split = common_strings[i + 1]

            #now create the elements
            if not post_split == None:
                #try to load old set input
                try:
                    name = previous[i][0]
                    unit = previous[i][1]

                except:
                    name = "[ dim_"+str(i)+" ]"
                    unit = '-'

                #process the values
                values = []

                for item in self.file_list:
                    values.append(item.split(pre_split)[1].split(post_split)[0])

                    try: 
                        values[-1] = float(values[-1])

                    except:
                        pass

                #create hte dimension array
                dimension_list.append([
                    name,
                    unit,
                    pre_split,
                    post_split,
                    True, #is it selected
                    values,
                    sorted(values)])

        return dimension_list

    def set_dim_meta(self, index, name = 'No_Name', unit = '-'):
        '''
        ##############################################
        This method will generate a string with the 
        input being a list of strings that are
        common to all files...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.dimension_list[index][0] = name
        self.dimension_list[index][1] = unit
        self.build_string()

    def grab_data_from_file(self, index):
        '''
        ##############################################
        This method will generate a string with the 
        input being a list of strings that are
        common to all files...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #set up
        path = self.file_list[index]
        x = []
        y = []

        #open the file
        with open(path) as f:
            for element in f.readlines():
                line        = element.strip('\n')
                line_float  = list(map(float, line.split()))
                x.append(line_float[0])
                y.append(line_float[1])

        return x,y

    def process_import(self):
        '''
        ##############################################
        This function will grab all the elements and 
        actually process the import sequence.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        dimension_list = []
        for  element in self.dimension_list:
            if element[4]:
                dimension_list.append(element)
    
        file_list = self.file_list

        self.worker = IORawWorker(
            file_list,
            dimension_list, 
            self.save_file_path)

        self.worker.run()

class IORawWorker:
    '''
    ##############################################
    This will be the threaded worker that will
    manage the file export into the default format.
    ———————
    Input: 
    - parent manager structure
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, file_list, dimension_list, path):
        '''
        ##############################################
        The init will manage all the initiali setup
        before being sent out as a thread
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.file_list      = file_list
        self.dimension_list = dimension_list
        self.state          = ''
        self.progress       = ''
        self.path           = path

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
        ##############################################
        #built a dimension array
        future_axes_values = [element[6] for element in self.dimension_list]
        future_axes_names  = [element[0] for element in self.dimension_list]
        future_axes_units  = [element[1] for element in self.dimension_list]

        ##############################################
        #scan files and create position array
        future_axes_pos    = []

        for path in self.file_list:
            try:
                future_axes_pos.append(
                    [ element[6].index(
                        float(path.split(element[2])[1].split(element[3])[0]) )
                    for element in self.dimension_list]
                )

            except:
                future_axes_pos.append(
                    [ element[6].index(
                        path.split(element[2])[1].split(element[3])[0]) 
                    for element in self.dimension_list]
                )

        ##############################################
        #read all files and create the data array
        future_data_array = []

        for path in self.file_list:
            future_data_array.append([*self._reader(path)])

        ##############################################
        #send it all out to the writer
        axis_string = self._axisWriter(
            future_axes_values,
            future_axes_names,
            future_axes_units)

        data_string = self._dataWriter(
            future_axes_pos,
            future_data_array)

        meta_string = self._metaWriter()

        ##############################################
        #write to file
        text_file = open(self.path, "w")

        text_file.write(meta_string)
        text_file.write(axis_string)
        text_file.write(data_string)    

        text_file.close()
        
    def _reader(self, path):
        '''
        ##############################################
        This method will generate a string with the 
        input being a list of strings that are
        common to all files...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #set up
        x = []
        y = []

        #open the file
        with open(path) as f:

            for element in f.readlines():

                line        = element.strip('\n')
                line_float  = list(map(float, line.split()))

                x.append(line_float[0])
                y.append(line_float[1])

        return x,y
            
    def _axisWriter(self, future_axes_values, future_axes_names, future_axes_units):
        '''
        ##############################################
        This method will generate a string with the 
        input being a list of strings that are
        common to all files...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #set up
        output = ""
        output += "#################   AXIS   ###################\n"
        ##############################################
        # write the axis informations
        for i in range(len(future_axes_names)):

            temp_list = list(
                ["**"
                + future_axes_names[i]
                + '**'
                + future_axes_units[i]+"**"]
                + future_axes_values[i])

            output += self._listToString(temp_list) + "\n"

        return output

    def _dataWriter(self,future_axes_pos,future_data_array):
        '''
        ##############################################
        This method will generate a string with the 
        input being a list of strings that are
        common to all files...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #set up
        output = ""
        output += "#################   DATA   ###################\n"
        ##############################################
        # write the data identifier informations
        output += self._listToString(future_axes_pos) + "\n"

        #grab the array length
        lengths = [len(item[0]) for item in future_data_array]

        # set the loop over the longest element
        for i in range(max(lengths)):

            #set the temporary list
            temp_list = []

            #loop over all
            for j in range(len(future_data_array)):
                try: 
                    temp_list.append(future_data_array[j][0][i])
                    temp_list.append(future_data_array[j][1][i])
                except:
                    temp_list.append("None")
                    temp_list.append("None")

            output += self._listToString(temp_list)+ "\n"

        return output

    def _metaWriter(self):
        '''
        ##############################################
        This method will generate a string with the 
        input being a list of strings that are
        common to all files...
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        output = ""
        output += "Data_file"
        output += "\n\n################# METADATA ###################\n"
        output += "This file was created on the " + str(datetime.datetime.now()) + "\n"
        #output += "The measurement ID is: " + str(self.meas_id) + "\n"
        #output += "The sample ID is: " + str(self.sam_id) + "\n"
    
        return output

    def _listToString(self,list_item):
        '''
        ##############################################
        This method returns a string from an input 
        list.
        ———————
        Input: 
        - list_item ([ints, float, str])
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        output = ""

        for item in list_item:
            output += str(item) + ","

        return output[:len(output) - 1]


        