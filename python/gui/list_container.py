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

from PyQt5 import QtCore, QtGui
import os

class ListContainer:

    def __init__(self, list_view):
        '''
        ##############################################
        This method will set the lsit view and wrap
        some common methods around it to allow straight
        forward manipulations.
        ———————
        Input: 
        - list view
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.list_view = list_view
        self._set_default()

    def _set_default(self):
        '''
        ##############################################
        Set the default list layout to then allow the
        user to write on top if recquired.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #intiialize the dicitonary
        self.dictionary = {}

        self.dictionary['name']  = 'List Container'
        self.dictionary['view']  = self.list_view
        self.dictionary['model'] = QtGui.QStandardItemModel(self.list_view)
        self.dictionary['items'] = []
        self.dictionary['check'] = False
        self.dictionary['true']  = False

        #methods
        self.dictionary['clicked']      = None
        self.dictionary['itemchanged']  = None

    def build_container(self, **kwargs):
        '''
        ##############################################
        Creation of the coantiner for a specific list
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        for key in kwargs.keys():
            if key in self.dictionary:
                self.dictionary[key] = kwargs[key]
            
            else:
                print('Key does not exist in this container.')

        if not self.dictionary['clicked'] == None:
            self.dictionary['view'].clicked.connect(self.dictionary['clicked'])

        if not self.dictionary['itemchanged'] == None:
            self.dictionary['model'].itemChanged.connect(self.dictionary['itemchanged'])

        #finnally initialize the list
        self.reset_list()

    def reset_list(self):
        '''
        ##############################################
        This method will reset the list
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.dictionary['view'].reset()
        self.dictionary['items'] = []
        self.dictionary['model'] = QtGui.QStandardItemModel(self.list_view)
        self.dictionary['view'].setModel(self.dictionary['model'])

    def add_item_to_list(self, item):
        '''
        ##############################################
        This method will handle the add item routine
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #add the element
        self.dictionary['items'].append([
            QtGui.QStandardItem(item.split(os.path.sep)[-1]),
            item])

        self.dictionary['items'][-1][0].setEditable( False )

        #set chekc state
        if self.dictionary['check']:
            self.dictionary['items'][-1][0].setCheckable( True )

            if self.dictionary['true']:
                self.dictionary['items'][-1][0].setCheckState( QtCore.Qt.Checked )

            else:
                self.dictionary['items'][-1][0].setCheckState( QtCore.Qt.Unchecked ) 

        #out the element
        self.dictionary['model'].appendRow(self.dictionary['items'][-1][0])