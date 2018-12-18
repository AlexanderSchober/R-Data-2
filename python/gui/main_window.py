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


from PyQt5 import QtWidgets, QtGui, QtCore

from ..gui_qt.main_window_ui import Ui_RData 


class MainWindowLayout(Ui_RData):
    '''
    This is the main window element that will later
    be the item managin the rest of the system. 
    Note that at a later point we will feature
    drag and drop onto this window.
    '''
    def __init__(self, window, window_manager):

        #set up the window
        Ui_RData.__init__(self)
        self.window = window
        self.window_manager = window_manager
        self.setupUi(window)
        self.initialize()
        self.connect()
        # self.revertAllButtons()
        # self.selectButton(0)
        # self.hideActivity()

    def connect(self):
        '''
        connect the actions to their respective buttons
        '''

        # #button actions
        # self.env_button.clicked.connect(self.refreshChecked)
        # self.data_button.clicked.connect(self.refreshChecked)
        # self.script_button.clicked.connect(self.refreshChecked)
        # self.save_button.clicked.connect(self.refreshChecked)

        # #Menu actions
        # self.actionAddEnv.triggered.connect(
        #     partial(self.actionDispatcher, 0, self.widgetClasses[0].addEnvironment))
        # self.actionRemoveEnv.triggered.connect(
        #     partial(self.actionDispatcher, 0, self.widgetClasses[0].deleteEnvironment))

        # self.actionAdd_element.triggered.connect(
        #     partial(self.actionDispatcher, 1, self.widgetClasses[1].addElement))
        # self.actionRemove_element.triggered.connect(
        #     partial(self.actionDispatcher, 1, self.widgetClasses[1].removeElement))
        # self.actionGenerate.triggered.connect(
        #     partial(self.actionDispatcher, 1, self.widgetClasses[1].generateDataset))
        # self.actionSave_to_file.triggered.connect(
        #     partial(self.actionDispatcher, 1, self.widgetClasses[1].save))
        # self.actionLoad_from_file.triggered.connect(
        #     partial(self.actionDispatcher, 1, self.widgetClasses[1].load))

        # self.actionSaveScript.triggered.connect(
        #     partial(self.actionDispatcher, 2, self.widgetClasses[2].saveScripts))
        # self.actionLoadScript.triggered.connect(
        #     partial(self.actionDispatcher, 2, self.widgetClasses[2].loadScripts))
        # self.actionImport.triggered.connect(
        #     partial(self.actionDispatcher, 2, partial(self.widgetClasses[2].run,0)))
        # self.actionPhase.triggered.connect(
        #     partial(self.actionDispatcher, 2, partial(self.widgetClasses[2].run,1)))
        # self.actionReduction.triggered.connect(
        #     partial(self.actionDispatcher, 2, partial(self.widgetClasses[2].run,2)))
        # self.actionVisual.triggered.connect(
        #     partial(self.actionDispatcher, 2, partial(self.widgetClasses[2].run,3)))
        # self.actionAll.triggered.connect(
        #     partial(self.actionDispatcher, 2, self.widgetClasses[2].runAll))

        # self.actionLoad_Session.triggered.connect(
        #     partial(self.actionDispatcher, 3, partial(self.widgetClasses[3].getLoadPath, True)))
        # self.actionSave_Session.triggered.connect(
        #     partial(self.actionDispatcher, 3, partial(self.widgetClasses[3].getSavePath, True)))

    def actionDispatcher(self,index, method = None):
        '''
        This will dispatch the actions to the right 
        function but still try to check if the page is
        the right one.
        '''
        # if not self.stack.currentIndex() == index:
        #     if index == 0:
        #         self.refreshChecked(0)
        #     if index == 1:
        #         if not self.widgetClasses[1].io_core == self.handler.current_env.io:
        #             self.widgetClasses[1].link(self.handler.current_env.io)
        #         self.refreshChecked(1)
        #     elif index == 2:
        #         if not self.widgetClasses[2].env == self.handler.current_env:
        #             self.widgetClasses[2].link(self.handler.current_env)
        #         self.refreshChecked(2)
        #     elif index == 3:
        #         self.refreshChecked(3)

        # if not method == None:
        #     method()

    def link(self, handler):
        '''
        link the class that will manage the current 
        input output.
        Input: meta_class is the metadata class from the io
        '''
        # self.setActivity(
        #     'Linking',0,3)
        
        # self.setProgress('Linking handler',0)
        # self.handler = handler 

        # self.setProgress('Linking script view',1)
        # self.widgetClasses[0].link(self.handler)

        # self.setProgress('Linking script view',3)
        # self.widgetClasses[3].link(self.handler)

        # self.fadeActivity()
        
    def initialize(self):
        '''
        This method checks if the data has been set
        in a previous instance.
        '''
        self.stack = QtWidgets.QStackedWidget()

        self.widgetClasses = []
        # self.widgetClasses = [
        #     PageEnvWidget(self.stack, self),
        #     PageDataWidget(self.stack, self),
        #     PageScriptWidget(self.stack, self),
        #     PageIOWidget(self.stack, self)]

        # self.stack.addWidget(self.widgetClasses[1].local_widget)

        for element in self.widgetClasses:
            self.stack.addWidget(element.local_widget)

        self.main_layout.addWidget(self.stack)
