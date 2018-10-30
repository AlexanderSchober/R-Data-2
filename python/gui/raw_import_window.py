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
import sys
import os

from ..gui_qt.raw_import_ui import Ui_raw_import_window
from ..gui.list_container   import ListContainer
from ..gui.python_syntax    import PythonHighlighter

from simpleplot.multi_canvas import Multi_Canvas


class Raw_Window(Ui_raw_import_window):
    '''
    ##############################################
    This class will manage the raw import 
    machinery. the UI is inherited through 
    Ui_main_window from the Qt designer anf then
    converted through pyuic5
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, window, io_handler):

        ##############################################
        #Local pointers
        Ui_raw_import_window.__init__(self)

        self.io_handler = io_handler
        self.io_handler.init_raw_import()
    
        ##############################################
        #Local pointers
        self.window = window
        self.setupUi(window)
        self.connect_methods()
        self._build_list_containers()
        self._initate_graph()
        self._set_meas()

    def _set_meas(self):
        '''
        ##############################################
        This method will connect all click events to
        the right handlers. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.syntaxHighliter = PythonHighlighter(self.meta_text_code.document())
        self.meta_text_code.setPlainText(self.io_handler.meas_string)
        self.meta_button_load.clicked.connect(self.run_code)

    def run_code(self):
        '''
        ##############################################
        This method will connect all click events to
        the right handlers. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        exec(self.meta_text_code.toPlainText())

    def _initate_graph(self):
        '''
        ##############################################
        This method will connect all click events to
        the right handlers. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.mycanvas    = Multi_Canvas(
            self.visual_widget_plot,
            grid        = [[True]],
            x_ratios    = [1],
            y_ratios    = [1],
            background  = "w",
            highlightthickness = 0)

        self.ax = self.mycanvas.get_subplot(0,0)
        self.ax.draw()  

    def connect_methods(self):
        '''
        ##############################################
        This method will connect all click events to
        the right handlers. 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        ##############################################
        #manage button clicks connect
        self.io_button_scan.clicked.connect(self.scan_folder_in)
        self.file_button_accept.clicked.connect(self.process_files)
        #self.file_button_reset.clicked.connect(self.reset_list_files)

        self.type_button_set.clicked.connect(self._set_dim)

        #set the ui for the folder select
        self.io_tool_select_in.clicked.connect(self.open_folder_in)
        self.io_tool_select_out.clicked.connect(self.open_file_out)

        self.visual_combo_selector.currentIndexChanged.connect(self._plot_file)
        self.dialog_button_process.clicked.connect(self._process_export)

        ##############################################
        #set up drag drop

    def _build_list_containers(self):
        '''
        ##############################################
        This method will manage the list elements to 
        cuild containers for them including, their name
        as a dictionary pointer, the list Qt item,
        the model, and the element list
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.list_dicitonary = {}

        list_elements = [
            ['file', self.file_list_view, True, True, self._file_changed, None],
            ['type', self.type_list_dimensions, True, True, self._dimension_changed, None],
            ['dim' , self.type_list_single_dimension, False, False, None, None]#,
            #['plot', self.plot_list_plot]
        ]

        for element in list_elements:
            
            self.list_dicitonary[element[0]] = ListContainer(element[1])

            self.list_dicitonary[element[0]].build_container(

                check = element[2],
                true  = element[3],

                clicked     = element[4],
                itemchanged = element[5])

    def open_folder_in(self):
        
        #launch the ui for the folder selection
        self.io_handler.set_import_directory(
            QtWidgets.QFileDialog.getExistingDirectory(
                self.window, 
                'Select directory'))

        #set the file in the right place
        self.io_input_in.setText(self.io_handler.directory_path)

    def open_file_out(self):

        #launch the ui for the savefile selection
        self.io_handler.set_save_file(
            QtWidgets.QFileDialog.getSaveFileName(
                self.window, 
                'Select file')[0])

        #set the file in the right place
        self.io_input_out.setText(self.io_handler.save_file_path)

    def scan_folder_in(self):
        '''
        ##############################################
        This method will scan the directory provided
        by the user and try to 
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #check for consistency
        if not self.io_handler.directory_path == self.io_input_in.text():
            self.io_handler.set_import_directory(self.io_input_in.text())
            self.io_handler.evaluate_files()

        ##############################################
        #reset the elements
        self.list_dicitonary['file'].reset_list()
        self.list_dicitonary['type'].reset_list()
        self.list_dicitonary['dim'].reset_list()

        self.type_input_name.setText('')
        self.type_input_label.setText('')
        self.type_label_path.setText(self.io_handler.visual_string)
        self.visual_combo_selector.clear()

        ##############################################
        #repopulate all
        for item in self.io_handler.scan_directory(): 

            self.list_dicitonary['file'].add_item_to_list(item)

        self.visual_combo_selector.addItems(
            [element.split(os.path.sep)[-1] for element in self.io_handler.file_list]
            )
        self.visual_combo_selector.setStyleSheet("QComboBox { combobox-popup: 0; }")

        self.process_files()

    def process_files(self):
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
        #process the file processing for dimensionality
        self.io_handler.evaluate_files()

        #grab the nicely formated string and set it
        self.type_label_path.setText(self.io_handler.visual_string)

        #build the ui element
        self._build_list_dimensions()

    def _process_export(self):
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
        self.io_handler.save_file_path = self.io_input_out.text()

        self.io_handler.process_import()

    def _build_list_dimensions(self):
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

        #add all the text items and makes them checked as well and checkable
        self.list_dicitonary['type'].reset_list()

        for item in self.io_handler.dimension_list: 

            self.list_dicitonary['type'].add_item_to_list(item[0])

        #set the select to the first row
        self.list_dicitonary['type'].dictionary['view'].setCurrentIndex(
            self.list_dicitonary['type'].dictionary['model'].index(0,0)
        )

        try:
            self._dimension_changed(self.list_dicitonary['type'].dictionary['model'].index(0,0))
        except:
            self._dimension_changed(None)

    def _dimension_changed(self, index):
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
        
        if index == None:
            self.list_dicitonary['type'].reset_list()
            self.type_input_name.setText('')
            self.type_input_label.setText('')

        else:
                
            #toggle the ignore
            if self.list_dicitonary['type'].dictionary['model'].item(index.row()).checkState() == QtCore.Qt.Checked:
                self.io_handler.dimension_list[index.row()][4] = True

            else:
                self.io_handler.dimension_list[index.row()][4] = False

            #redo the sting
            self.io_handler.build_string()

            #set the text
            self.type_label_path.setText(self.io_handler.visual_string)

            #add all the text items and makes them checked as well and checkable
            self.type_input_name.setText(self.io_handler.dimension_list[index.row()][0])
            self.type_input_label.setText(self.io_handler.dimension_list[index.row()][1])

            #add all the text items and makes them checked as well and checkable
            self.list_dicitonary['dim'].reset_list()
            
            for item in self.io_handler.dimension_list[index.row()][-1]: 

                self.list_dicitonary['dim'].add_item_to_list(str(item))

    def _file_changed(self, index):
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
        #toggle the ignore
        if self.list_dicitonary['file'].dictionary['model'].item(index.row()).checkState() == QtCore.Qt.Checked:
            check = True

        else:
            check = False
            
        #toggle the ignore
        self.io_handler.toggle_mask(
            index.row(),
            check)

        self.process_files()
        self.visual_combo_selector.clear()
        self.visual_combo_selector.addItems(
            [element.split(os.path.sep)[-1] for element in self.io_handler.file_list])
        self._plot_file(0)

    def _set_dim(self):
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
        #grab the element that is selected
        row = self.list_dicitonary['type'].dictionary['view'].selectedIndexes()[0].row()
        
        #get the parameters
        name = self.type_input_name.text()
        unit = self.type_input_label.text()

        #send the values out
        self.io_handler.set_dim_meta(row ,name = name, unit = unit)

        #refresh the views
        self.list_dicitonary['type'].dictionary['model'].item(row).setText(name)

        #set the text
        self.type_label_path.setText(self.io_handler.visual_string)

    def _plot_file(self, index):
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
        x, y = self.io_handler.grab_data_from_file(index)

        self.ax.clear()
        self.ax.add_plot(
            'Scatter',
            x,
            y,
            Thickness = 3,
            Style   = ['-','o','5'])
        self.ax.redraw()
        
    def next_tab(self):
        pass

    def previous_tab(self):
        pass


if __name__ == "__main__":

    from ..io  import io_raw_import
    from ..io  import io_data_import
    from ..data import datastructure
    
    #initialize an io_handler
    handler = io_raw_import.IORawHandler()
    
    #set up the app
    app         = QtWidgets.QApplication(sys.argv)
    window      = QtWidgets.QMainWindow()
    interface   = Raw_Window(window, handler)

    #fast input for debugging
    interface.io_input_in.setText('/Users/alexanderschober/Dropbox/software/R-DATA/Demo/DemoRawImport')
    interface.io_input_out.setText('/Users/alexanderschober/Dropbox/software/R-DATA/Demo/test.txt')
    interface.scan_folder_in()
    interface.process_files()
    interface._process_export()
    window.show()

    data = datastructure.Data_Structure()
    handler_2 = io_data_import.IOImportHandler()
    handler_2.readDataFile('/Users/alexanderschober/Dropbox/software/R-DATA/Demo/test.txt', data)



    sys.exit(app.exec_())


