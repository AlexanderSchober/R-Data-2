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

#############################
#personal libraries
from .sample.sample_handler             import SampleHandler
from .instrument.instrument_handler     import InstrumentHandler

from simpleplot.multi_canvas import Multi_Canvas
from PyQt5 import QtWidgets
import sys

class Measurement:

    def __init__(self, identifier = None, model = None):
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
        
        #set the handlers to null
        self.sample     = None
        self.instrument = None

        #set the measurement ID
        self.identifier = identifier

    def setSample(self):
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
        self.sample = SampleHandler()
        
    def setInstrument(self):
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
        self.instrument = InstrumentHandler()
        
    def loadModel(self, name = None, path = None):
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

        pass
        
    def generateScript(self, indentation = 0):
        '''
        ##############################################
        This method will allow the generation of a 
        script of the current structure.
        ———————
        Input (optional): -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        #set the indentation value
        indent = "\t"

        #write the output
        output  = indentation * indent + "########################################\n"
        output += indentation * indent + "############## MEASUREMENT #############\n"
        output += indentation * indent + "########################################\n"
        output += indentation * indent + "\n"
        output += indentation * indent + "########################################\n"
        output += indentation * indent + "# import dependencies here\n"
        output += indentation * indent + "import numpy as np\n" 
        output += indentation * indent + "from measurement.geometry.points import Point\n" 
        output += indentation * indent + "\n"
        output += indentation * indent + "def run(meas):"
        indentation += 1
        output += indentation * indent + "\n"
        output += indentation * indent + "\n"
        output += indentation * indent + "########################################\n"
        output += indentation * indent + "# initializing the measurement here\n"

        #set the sample
        if not self.sample == None:
            output += indentation * indent + "meas.setSample()\n" 
            output += self.sample.generateScript(
                indentation = indentation,
                parent = "meas.sample.")

        #set the instrument
        if not self.sample == None:
            output += indentation * indent + "meas.setInstrument()\n" 
            output += self.instrument.generateScript(
                indentation = indentation,
                parent = "meas.instrument.")

        #send it out
        return output


    def visualize(self):
        '''
        ##############################################
        Routine that visualizes the create sample shape
        ———————
        Input (optional): -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        ##############################################
        #set up the widget
        

        app 	    = QtWidgets.QApplication(sys.argv)
        widget      = QtWidgets.QWidget()
        mycanvas    = Multi_Canvas(
            widget,
            grid        = [[True]],
            element_types = [['3D']],
            x_ratios    = [1],
            y_ratios    = [1],
            background  = "k")

        widget.show()

        ax = mycanvas.get_subplot(0,0)

        for sam_key in meas.sample.elements.keys():

            for key in meas.sample.elements[sam_key].geometry.strucutre_surfaces.keys():
                
                ax.add_plot(
                    'Surface', 
                    meas.sample.elements[sam_key].geometry.strucutre_surfaces[key].getVertices(),
                    meas.sample.elements[sam_key].geometry.strucutre_surfaces[key].getFaces(),
                    Name    = key,
                    Color = meas.sample.elements[sam_key].geometry.strucutre_surfaces[key].color)

        ax.draw()

    
    

        sys.exit(app.exec_())

if __name__ == "__main__":

    import numpy as np

    # from pyqtgraph.opengl import shaders
    # to_use = shaders.ShaderProgram(
    #     'heightColor', 
    #     [
    #          shaders.VertexShader(
    #             """
    #             varying vec4 pos;
    #             varying vec3 normal;
    #             void main() {
    #             """+"""    
    #                 normal = normalize(gl_NormalMatrix * gl_Normal);
    #                 gl_FrontColor = gl_Color;
    #                 gl_BackColor = gl_Color;
    #                 pos = gl_Vertex;
    #                 gl_Position = ftransform();
    #             }
    #             """),
    #     shaders.FragmentShader(
    #         """
    #         uniform float colorMap[9];
    #         uniform float factor[2];
    #         varying vec4 pos;
    #         varying vec3 normal;
    #         //out vec4 gl_FragColor;   // only needed for later glsl versions
    #         //in vec4 gl_Color;
    #         void main() {
    #             vec4 color = gl_Color;
    #             color.x = colorMap[0] * ( ( pos.z - factor[1] ) * factor[0] + colorMap[1]);
    #             if (colorMap[2] != 1.0)
    #                 color.x = pow(color.x, colorMap[2]);
    #             color.x = color.x < 0. ? 0. : (color.x > 1. ? 1. : color.x);
                
    #             color.y = colorMap[3] * ( ( pos.z - factor[1] ) * factor[0] + colorMap[4]);
    #             if (colorMap[5] != 1.0)
    #                 color.y = pow(color.y, colorMap[5]);
    #             color.y = color.y < 0. ? 0. : (color.y > 1. ? 1. : color.y);
                
    #             color.z = colorMap[6] * ( ( pos.z - factor[1] ) * factor[0] + colorMap[7]) ;
    #             if (colorMap[8] != 1.0)
    #                 color.z = pow(color.z, colorMap[8]);
    #             color.z = color.z < 0. ? 0. : (color.z > 1. ? 1. : color.z);
                
    #             color.w = 1.; 

    #             gl_FragColor = color;
    #         }""")
    #         ], 
    #         uniforms={
    #             'colorMap': [0.2, 0.8, 1, 1, 0, 1, 0, 1, 1],
    #             'factor': [1/8,4]})


    meas = Measurement(identifier = '01235453210') 
    meas.setSample()
    meas.setInstrument()

    Sample_1 = meas.sample.newElement(
        'Sample_1', 
        volume  = "Cube",
        a       = 2.,
        color   = np.asarray([255,0, 0,1]),#colors.map(0.4),
        transp  = 1)
    Sample_1.geometry.buildVolume()

    Sample_2 = meas.sample.newElement(
        'Sample_2', 
        volume  = "Cylinder",
        r       = 1 * np.sqrt(2),
        height  = 1,
        color   = np.asarray([0,255, 0,1]),#colors.map(0.4),
        transp  = 1)
    Sample_2.geometry.buildVolume()
    Sample_2.translate([0,0,-1])


    Sample_3 = meas.sample.newElement(
        'Sample_3', 
        volume  = "Sphere",
        r       = 1 ,
        color   = np.asarray([0,0, 255,1]),
        transp  = 1)

    Sample_3.geometry.buildVolume()
    Sample_3.translate([0,0,1])
    Surface_3 = Sample_3.geometry.getSurface('top')

    Sample_4 = meas.sample.newElement(
        'Sample_4', 
        volume  = "Cylinder",
        r       = 0.1 * np.sqrt(2),
        height  = 2,
        color   = np.asarray([0,255, 0,1]),#colors.map(0.4),
        transp  = 1)
    Sample_4.geometry.buildVolume()
    Sample_4.translate([0,0,3])

    

    f = open('script.py', 'w')
    f.write(meas.generateScript())
    f.close()
    # import script

    # script.run(meas)
    

    meas.visualize()





