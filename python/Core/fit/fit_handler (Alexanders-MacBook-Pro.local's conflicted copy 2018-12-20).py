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
from PyQt5.QtCore import pyqtSignal
import sys

class FitHandler(QtCore.QObject, FunctionLibrary):
    '''
    This will be the main fit handler that will 
    contain all the fit properties of the current 
    environment. It is fed the environnement as a
    a data source. 

    Input is the environment containing the dataclass
    '''
    progress_int = pyqtSignal(int)
    progress_str = pyqtSignal(str)

    def __init__(self, env, gui = False):
        QtCore.QObject.__init__(self)
        FunctionLibrary.__init__(self)

        if not gui:
            self.openDummyApp()
            self.gui = False
        else:
            self.gui = True

        self.env = env
        self.initialize()
        self.connect()

    def link(self):
        '''
        link the fit handler to some gui
        '''

    def openDummyApp(self):
        '''
        In the event that the app is run through the
        terminal the user still needs the QThreads
        signaling. This is why a dummy is created
        and left running until completion.        
        '''
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
        self.fit_worker.my_event.connect(self.finishedFit)

    def performFit(self):        
        '''
        The main fitting routine routine that is called
        as soon as all the parameters have been set.
        '''
        self.prepareFit()
        self.fit_worker.fitter.progress_int.connect(self.reportProgressInt)
        self.fit_worker.fitter.progress_str.connect(self.reportProgressStr)
        self.fit_worker.run()

    def reportProgressInt(self, percentage):
        '''
        propagate the signals for the gui
        '''
        #print(percentage, '% done')
        self.progress_int.emit(percentage)
        
    def reportProgressStr(self, message):
        '''
        propagate the signals for the gui
        '''
        #print(percentage, '% done')
        self.progress_str.emit(message)

    def finishedFit(self):
        '''
        The fitting function at the end. We can now retrieve
        the fit elements from the worker if necessary.
        '''
        self.cloneFromWorker()
        print('finished')

    def prepareFit(self):
        '''
        This function will grab all the elements from
        different subclasses and set them in the
        worker. This includes ranges properties and 
        parameters. 
        '''
        import numpy as np
        x = np.linspace(-4,5*np.pi,1000)
        y = np.sin(x) + 0.2 + 10 * 1 * 2 / ( (x - 4)**2 + 1**2) + 20 * 3 * 2 * 1 / ( (x - 7)**2 + 3**2)

        self.fit_worker.setXY(x, y)
        self.cloneToWorker()
        self.fit_worker.setParameters([0, 1,2],1e10,5)

    def cloneToWorker(self):
        '''
        Clone the local content to the worker so he
        can proceed with the fit. This allows the 
        local component to clean.
        '''
        self.fit_worker.resetDictionary()

        for key in self.func_dict.keys():
            for element in self.func_dict[key][2]:
                self.fit_worker.addFunction(
                    element[self.current_ray].info.name,
                    source = element[self.current_ray])

    def cloneFromWorker(self):
        '''
        Clone back the data from the worker to the main
        thread that will then do the visual parts.
        '''
        for key in self.func_dict.keys():
            for i, element in enumerate(self.func_dict[key][2]):
                element[self.current_ray].clone(
                    self.fit_worker.func_dict[key][2][i])


                
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    main_widow = QtWidgets.QMainWindow()
    main_widow.show()

    from ...gui.fitcontrol_widget import FitControlWidget

    widget = FitControlWidget(main_widow)
    main_widow.setCentralWidget(widget.widget)
    

    


    worker = FitHandler(3, gui = True)
    worker.addFunction('Sinus', rays = 10)
    #worker.addFunction('Linear', rays = 10)
    worker.addFunction('Lorenzian', rays = 10)
    worker.addFunction('Lorenzian', rays = 10)
    
    widget.link(worker)


    # import numpy as np
    # x = np.linspace(-4,5*np.pi,1000)
    # y = np.sin(x) + 0.2 + 10 * 1 * 2 / ( (x - 4)**2 + 1**2) + 20 * 3 * 2 * 1 / ( (x - 7)**2 + 3**2)
    # worker.addFunction('Sinus', rays = 10)
    # #worker.addFunction('Linear', rays = 10)
    # worker.addFunction('Lorenzian', rays = 10)
    # worker.addFunction('Lorenzian', rays = 10)
    # worker.func_dict['Lorenzian'][2][0][0].paras[0] = 4
    # worker.func_dict['Lorenzian'][2][1][0].paras[0] = 7

    # #worker.prepareFit()
    # #worker.fit_worker.run()
    # worker.performFit()

    # from matplotlib import pyplot as plt
    # plt.plot(x, worker.func_dict['Sinus'][2][0][0].returnData(x))
    # plt.plot(x, worker.func_dict['Lorenzian'][2][0][0].returnData(x))
    # plt.plot(x, worker.func_dict['Lorenzian'][2][1][0].returnData(x))
    # #plt.plot(x, worker.func_dict['Linear'][2][0][0].returnData(x))

    # plt.plot(x, worker.func_dict['Sinus'][2][0][0].returnData(x) + worker.func_dict['Lorenzian'][2][0][0].returnData(x) 
    # #+ worker.func_dict['Linear'][2][0][0].returnData(x)
    # +worker.func_dict['Lorenzian'][2][1][0].returnData(x)
    # )
    # plt.plot(x,y)
    # plt.show()
    # print(worker.func_dict['Lorenzian'][2][0][0].paras)
    sys.exit(app.exec_())