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
from scipy.ndimage import imread

from ..gui_qt.main_window_ui import Ui_main_import_window 
from ..io.io_file_methods import getRuntimeDir


class MainWindowLayout(Ui_main_import_window):
    '''
    ##############################################
    This is the main window element that will later
    be the item managin the rest of the system. 
    Note that at a later point we will feature
    drag and drop onto this window.
    ———————
    Input: -
    ———————
    Output: -
    ———————
    status: active
    ##############################################
    '''
    def __init__(self, window):

        #set up the window
        Ui_main_import_window.__init__(self)
        self.window = window
        self.setupUi(window)

        #set up the image in the QLabel
        #self.main_label_image.
        print(getRuntimeDir())
        image = imread(os.path.join(
            getRuntimeDir(),
            'visual_ressources', 
            'R-Data_Logo.jpeg'))
        height, width, channels = image.shape
        bytesPerLine    = channels * width

        q_image         = QtGui.QImage(
            image.data, 
            width, height, 
            bytesPerLine, 
            QtGui.QImage.Format_RGB888)

        pixmap01        = QtGui.QPixmap.fromImage(q_image)
        pixmap_image    = QtGui.QPixmap(pixmap01)  
        #pixmap_image    = pixmap_image.scaledToHeight(200)
        self.main_label_image.setPixmap(pixmap_image)


