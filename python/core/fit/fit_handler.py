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


from .fit_worker import FitWorker
from .function_library import FunctionLibrary

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class FitHandler(QtCore.QObject, FunctionLibrary):
    '''
    This will be the main fit handler that will 
    contain all the fit properties of the current 
    environment. It is fed the environnement as a
    a data source. 

    Input is the environment containing the dataclass
    '''
    def __init__(self, env, gui = False):
        QtCore.QObject.__init__(self)
        FunctionLibrary.__init__(self)

        if not gui:
            self.openDummyApp()

        self.env = env
        self.initialize()
        self.connect()

    def openDummyApp(self):
        '''
        In the event that the app is run through the
        terminal the user still needs the QThreads
        signaling. This is why a dummy is created
        and left running until completion.        
        '''
        self.gui = False
        self.app = QtWidgets.QApplication(sys.argv)

    def initialize(self):
        '''
        Initialise the class by instating the worker 
        and setting up it's environment. 
        '''
        self.fit_worker = FitWorker()
        self.importFunctions()
        self.current_ray = 0

    def connect(self):
        '''
        Connect all relevant slots and signals to their
        method. Note that the app has to be running in
        order for this to work. 
        '''
        self.fit_worker.finished.connect(self.finishedFit)

    def preformfit(self):        
        '''
        The main fitting routine routine that is called
        as soon as all the parameters have been set.
        '''
        self.fit_worker.start()

    def finishedFit(self):
        '''
        The fitting function at the end.
        '''
        print('lol')

    def prepareFit(self):
        '''
        This function will grab all the elements from
        different subclasses and set them in the
        worker. This includes ranges properties and 
        parameters. 
        '''
        import numpy as np
        x = np.linspace(0,np.pi,100)
        y = np.sin(x)

        self.fit_worker.setXY(x, y)
        self.cloneToWorker()
        self.fit_worker.setParameters([0,1,2],1e5,5)


    def cloneToWorker(self):
        '''
        Clone the local content to the worker so he
        can proceed with the fit. This allows the 
        local component to clean.
        '''
        self.fit_worker.resetDictionary()

        self.fit_worker

        for key in self.func_dict.keys():
            for element in self.func_dict[key][2]:
                self.fit_worker.addFunction(
                    element[self.current_ray].info.name)

                
if __name__ == "__main__":
    
    worker = FitHandler(3)

    import numpy as np
    x = np.linspace(0,np.pi,100)
    y = np.sin(x)

    worker.addFunction('Sinus', rays = 10)
    # worker.addFunction('Lorenzian', rays = 10)
    # worker.addFunction('Linear', rays = 10)

    # print(worker.func_dict['Sinus'][2][0][0].function([x,1,1,1,1]))
    # print(worker.func_dict['Lorenzian'][2][0][0].function([x,1,1,1,1,1]))

    worker.prepareFit()

    # print(worker.fit_worker.func_dict['Sinus'][2][0].function([x,1,1,1,1]))
    # print(worker.fit_worker.func_dict['Linear'][2][0].function([x,1,1,1,1,1]))

    worker.fit_worker.run()
