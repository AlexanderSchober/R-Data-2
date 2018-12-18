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


from .gui.window_handlers import WindowHandler
from .core.environment import EnvironmentHandler

class Main:
    '''
    ##############################################
    This class is the root class in our system.
    It will just launch the instances and then
    manage them accordingly. 
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self):
        self.initCore()
        self.initGUI()
        self.connectAll()

        self.window_handler.run()

    def initCore(self):
        self.env_handler = EnvironmentHandler()

    def initGUI(self):
        self.window_handler = WindowHandler(self.env_handler)

    def connectAll(self):
        target = self.window_handler.main_window.target
        target.actionNew_environment.triggered.connect(self.addEnv)
        target.actionConvert_dataset.triggered.connect(self.launchRawImport)

    def addEnv(self, name = 'No Name'):
        self.env_hanler.addEnv(name = name)

    def launchRawImport(self):
        self.env_hanler.current_env.io.setupRawImporter()
        self.window_handler.newWindow('RawImport')
        self.window_handler.active_windows['RawImport'].target.linkCore(
            self.env_hanler.current_env.io.target)
        


if __name__ == "__main__":

    manager = Main()
    manager.addEnv()
    manager.launchRawImport()
    manager.window_handler.run()

    
    # #initialize an io_handler
    # handler = io_raw_import.IORawHandler()
    
    # #set up the app
    # app         = QtWidgets.QApplication(sys.argv)
    # window      = QtWidgets.QMainWindow()
    # interface   = Raw_Window(window, handler)

    # #fast input for debugging
    # interface.io_input_in.setText('/Users/alexanderschober/Dropbox/software/R-DATA/Demo/DemoRawImport')
    # interface.io_input_out.setText('/Users/alexanderschober/Dropbox/software/R-DATA/Demo/test.txt')
    # interface.scan_folder_in()
    # interface.process_files()
    # interface._process_export()
    # window.show()

    # data = datastructure.Data_Structure()
    # handler_2 = io_data_import.IOImportHandler()
    # handler_2.readDataFile('/Users/alexanderschober/Dropbox/software/R-DATA/Demo/test.txt', data)



    # sys.exit(app.exec_())

