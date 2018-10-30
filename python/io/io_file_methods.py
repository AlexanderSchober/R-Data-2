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


import sys
import os
import glob

def get_files_in_folder(path, extension = None):
    '''
    ##############################################
    Whatever path is set as folder the machinery
    checks first that this path is valid and then
    goes through the folder and sends back a 
    list of absolut pathss. 
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''

    #first get the absolute path
    path = os.path.abspath(path)

    #then 
    if os.path.isdir(path):

        if extension == None:

            return glob.glob(path+'/')

        else:

            return glob.glob(path+'/*'+extension)

    else: 
        return False

def get_common_substrings(path_list):
    '''
    ##############################################
    Whatever path is set as folder the machinery
    checks first that this path is valid and then
    goes through the folder and sends back a 
    list of absolut pathss. 
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''

    #first get the absolute path
    base_length = 3
    position    = 0
    substrings  = []
    run         = True
    path_list   = [element.split(os.path.sep)[-1].split('.')[0] for element in path_list]
    temp_result = ''

    #run
    while run:
        
        #are we geting out of the string length
        if position + base_length == len(path_list[0]):
            run = False
            return substrings

        #get comparison string
        string_element = path_list[0][position:position+base_length]

        #check if it exists in all 
        if substring_in_list(string_element, path_list):

            #set temporary result
            temp_result = str(string_element)

            #increase the length
            base_length += 1

        else:

            if not temp_result == '':

                #we found a result and overstepped
                substrings.append(temp_result)
                position        += base_length
                base_length     = 3
                temp_result     = ''
                
            else:
                position += 1


def substring_in_list(substring, path_list):
    '''
    ##############################################
    Check if a substring is contained within all 
    the given path elements.
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''

    #first get the absolute path
    for element in path_list:

        if not substring in element:

            return False

    return True

