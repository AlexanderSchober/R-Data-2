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

from .sample_object     import SampleObject
from .geometry.environment       import Environment

class SampleHandler:

    def __init__(self):
        '''
        ##############################################
        The sample manager is a standalone package
        that can be used to generate sample structure.
        This goes for physical properties as much as
        form and shape. The sample will be built of
        subset of samples which can be brought together
        through a smart geometry manager. 

        This procedure should also allow easier
        management of the simulation of Raman 
        experiments.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        
        self.samples = {}
        
    def newSample(self, name = None):
        '''
        ##############################################
        add 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        if name == None:

            name = "sample_"+len(self.samples.keys())

        self.samples[name] = SampleObject()
        


if __name__ == "__main__":
    
    handler = SampleObject(name = 'Sample_object') 
    #handler.newSample('hey')

    print(handler.name)

