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


from .geometry.geometry     import Geometry
from .physics.physics       import Physics

class SampleObject():

    def __init__(self, **kwargs):
        '''
        ##############################################
        
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #initialise local variable
        self.elements       = {}

        #set initial parameters
        self.initializeAttributes()

        #overwrite attributes
        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])
        
    def initializeAttributes(self):
        '''
        ##############################################
         
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        self.name       = "No_name"
        self.elements   = {}

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
        indent = "    "
        output = indentation * indent + "### initializing the handler here\n"
        output += indentation * indent + "handler = SampleObject(name = '"+str(self.name)+"')\n\n"
        for key in self.elements.keys():

            #start the sample element creation
            output += indentation * indent + "### Adding the sample element: "+str(key)+"\n"
            output += indentation * indent + "handler.newSampleElement(\n"
            output += (indentation + 1) * indent + "'" + str(self.elements[key].name) + "',\n"

            #check what we have to deal with
            if self.elements[key].element.identifier_type == 'Surface':
                output += (indentation + 1) * indent + "surface = " 

            elif self.elements[key].element.identifier_type == 'Volume':
                output += (indentation + 1) * indent + "volume = " 

            output += "'" + self.elements[key].element.type_name + "',\n"
            output += (indentation + 1) * indent + "color = " 
            output += str(self.elements[key].element.color.tolist())

            # close it up
            output += indentation * indent + ")\n\n"

            root = "handler.elements['"+key+"']."

            output += self.elements[key].generateScript(indentation, root)

        return output

        

    def newSampleElement(self, name = 'None', **kwargs):
        '''
        ##############################################
        
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''
        if name == 'None':

            name = "sample_"+len(self.elements.keys())

        self.elements[name] = SampleElement(name = name, **kwargs)

class SampleElement(Geometry, Physics):

    def __init__(self, name = None, **kwargs):
        '''
        ##############################################
        This is a sample element ans will contain all 
        the information about its spatial shape and
        its physical properties.
        ———————
        Input: -
        ———————
        Output: -
        ———————
        status: active
        ##############################################
        '''

        #initialiset he position and orientations
        Geometry.__init__(self, **kwargs)
        Physics.__init__(self, **kwargs)

        self.name = name

    def generateScript(self, indentation = 0, root = ''):
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
        indent = "    "
        output = ""
        output += self.generateScriptGeometry(indentation, root)
        output += self.generateScriptPhysics(indentation, root)
    
        return output




def test_0():
    handler = SampleObject(name = 'Sample_object') 

    ##############################################
    #set up the imports
    from simpleplot.multi_canvas import Multi_Canvas
    from PyQt5 import QtWidgets
    import pyqtgraph as pg
    import numpy as np
    import sys

    ##############################################
    #set up the sample
    num=5
    color_map = [
        np.array([0., 0.33, 0.66, 1.]),
        np.array([
                [255,   0,   0, 255], 
                [  0, 255,   0, 255], 
                [  0,   0, 255, 255], 
                [255,   0,   0, 255]], 
                
                dtype=np.ubyte)]

    colors = pg.ColorMap(*color_map)
    colorTable = colors.getLookupTable(nPts = num)
    
    for i in range(num):
            
        handler.newSampleElement(
            'Sample_1_'+str(i), 
            volume  = "Parallelepiped", 
            alpha   = 45, theta = 45,
            color   = colorTable[i])

        handler.elements['Sample_1_'+str(i)].element.buildVolume()
        handler.elements['Sample_1_'+str(i)].translate([0,0,-num/2])
        handler.elements['Sample_1_'+str(i)].rotate([0,0,1], 22.5 * i + 180)
        handler.elements['Sample_1_'+str(i)].translate([0,0,i])

    for i in range(num):
    
        handler.newSampleElement(
            'Sample_2_'+str(i), 
            volume  = "Parallelepiped", 
            alpha   = 45, theta = 45,
            color   = colorTable[i])

        handler.elements['Sample_2_'+str(i)].element.buildVolume()
        handler.elements['Sample_2_'+str(i)].translate([0,0,-num/2])
        handler.elements['Sample_2_'+str(i)].rotate([0,0,1], 22.5 * i)
        handler.elements['Sample_2_'+str(i)].translate([0,0,i])


    for i in range(num):
            
        handler.newSampleElement(
            'Sample_3_'+str(i), 
            volume  = "Parallelepiped", 
            alpha   = 45, theta = 45,
            color   = colorTable[i])

        handler.elements['Sample_3_'+str(i)].element.buildVolume()
        handler.elements['Sample_3_'+str(i)].translate([0,0,-num/2])
        handler.elements['Sample_3_'+str(i)].rotate([0,0,1], 22.5 * i + 90)
        handler.elements['Sample_3_'+str(i)].translate([0,0,i])


    for i in range(num):
            
        handler.newSampleElement(
            'Sample_4_'+str(i), 
            volume  = "Parallelepiped", 
            alpha   = 45, theta = 45,
            color   = colorTable[i])


        handler.elements['Sample_4_'+str(i)].element.buildVolume()
        handler.elements['Sample_4_'+str(i)].translate([0,0,-num/2])
        handler.elements['Sample_4_'+str(i)].rotate([0,0,1], 22.5 * i - 90)
        handler.elements['Sample_4_'+str(i)].translate([0,0,i])

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
        background  = "k",
        highlightthickness = 0)

    widget.show()

    ax = mycanvas.get_subplot(0,0)
    
    for sam_key in handler.elements.keys():

        for key in handler.elements[sam_key].element.strucutre_surfaces.keys():
            
            ax.add_plot(
                'Surface', 
                handler.elements[sam_key].element.strucutre_surfaces[key].getVertices(),
                handler.elements[sam_key].element.strucutre_surfaces[key].getFaces(),
                Name    = key,
                Color = np.multiply(np.asarray(handler.elements[sam_key].element.strucutre_surfaces[key].color),1/255).tolist()+[1])
    
    ax.draw()

    sys.exit(app.exec_())


def test_1():
    handler = SampleObject(name = 'Sample_object') 

    from simpleplot.multi_canvas import Multi_Canvas
    from PyQt5 import QtWidgets
    import pyqtgraph as pg
    import numpy as np
    import sys
    num=5
    color_map = [
        np.array([0., 0.33, 0.66, 1.]),
        np.array([
                [255,   0,   0, 1], 
                [  0, 255,   0, 1], 
                [  0,   0, 255, 1], 
                [  0,   0, 255, 1]], 
                
                dtype=np.ubyte)]

    colors      = pg.ColorMap(*color_map)
    colorTable  = np.asarray(colors.getLookupTable(nPts = num))[:,:3]
    

    handler.newSampleElement(
        'Sample_1', 
        volume  = "Cuboid",
        a       = 2,
        b       = 2,
        c       = 1 ,
        alpha   = 90, theta = 90,
        color   = colors.map(0.3),
        transp  = 0.5)

    handler.elements['Sample_1'].element.buildVolume()
    handler.elements['Sample_1'].translate([-1,-1,3])

            
    handler.newSampleElement(
        'Sample_2', 
        volume  = "Cuboid",
        a       = 6,
        b       = 6,
        c       = 3,
        alpha   = 90, theta = 90,
        color   = colors.map(0.5),
        transp  = 1)

    handler.elements['Sample_2'].element.buildVolume()
    handler.elements['Sample_2'].translate([-3,-3,0])
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
    
    for sam_key in handler.elements.keys():

        for key in handler.elements[sam_key].element.strucutre_surfaces.keys():
            
            ax.add_plot(
                'Surface', 
                handler.elements[sam_key].element.strucutre_surfaces[key].getVertices(),
                handler.elements[sam_key].element.strucutre_surfaces[key].getFaces(),
                Name    = key,
                Shader = handler.elements[sam_key].element.strucutre_surfaces[key].color)
    
    ax.draw()

    sys.exit(app.exec_())

def test_2():
    handler = SampleObject(name = 'Sample_object') 

    from simpleplot.multi_canvas import Multi_Canvas
    from PyQt5 import QtWidgets
    import pyqtgraph as pg
    import numpy as np
    import sys
    import os
    from pprint import pprint
    
    
    
    color_map = [
        np.array([0., 0.15, 0.4, 0.5, 0.6, 0.75, 1.0]),
        np.array(
            [   [  0,   0, 255, 1],
                [  0,  50, 255, 1],
                [255,   0,   0, 1],
                [255,   0,   0, 1],
                [255, 255,   0, 1], 
                [255,  50,   0, 1],
                [255,   0,   0, 1]], 
                dtype=np.ubyte)]

    position = np.array([0,0.1, 0.2, 0.3, 0.4, 0.6,0.7,0.8])# 0.15, 0.4, 0.5, 0.6, 0.75, 1.0])
    col = np.array(
        [   [  0,   0,   0, 1],
            [255,   0, 255, 1],
            [  0,   0, 255, 1],
            [  0,   0,   0, 1],
            [255,   0,   0, 1],
            [255, 255,   0, 1],
            [  0, 255,   0, 1],
            [  0,   0,   0, 1]],
            
        dtype = np.ubyte)

    colors      = pg.ColorMap(position,col)
    
    
    ##############################################
    #read in the surface file
    f = open(os.getcwd()+"/sample/topotgraphy.xyz","r")
    lines = f.readlines()#512
    z = []
    for i in range(1,len(lines)):
        z.append(float(lines[i].split()[-1]))

    

    z = np.reshape(np.asarray(z),(512,512)) 
    z = (z - np.amin(z))* 1e6

    from pyqtgraph.opengl import shaders
    to_use = shaders.ShaderProgram(
        'heightColor', 
        [
             shaders.VertexShader("""
                varying vec4 pos;
                void main() {
                    gl_FrontColor = gl_Color;
                    gl_BackColor = gl_Color;
                    pos = gl_Vertex;
                    gl_Position = ftransform();
                }
            """),
        shaders.FragmentShader(
            """
            uniform float colorMap[9];
            uniform float factor;
            varying vec4 pos;
            //out vec4 gl_FragColor;   // only needed for later glsl versions
            //in vec4 gl_Color;
            void main() {
                vec4 color = gl_Color;
                color.x = colorMap[0] * (pos.z* factor + colorMap[1]);
                if (colorMap[2] != 1.0)
                    color.x = pow(color.x, colorMap[2]);
                color.x = color.x < 0. ? 0. : (color.x > 1. ? 1. : color.x);
                
                color.y = colorMap[3] * (pos.z* factor + colorMap[4]);
                if (colorMap[5] != 1.0)
                    color.y = pow(color.y, colorMap[5]);
                color.y = color.y < 0. ? 0. : (color.y > 1. ? 1. : color.y);
                
                color.z = colorMap[6] * (pos.z * factor + colorMap[7]) ;
                if (colorMap[8] != 1.0)
                    color.z = pow(color.z, colorMap[8]);
                color.z = color.z < 0. ? 0. : (color.z > 1. ? 1. : color.z);
                
                color.w = 1.;
                gl_FragColor = color;
            }""")
            ], 
            uniforms={
                'colorMap': [1, 0.5, 1, 1, 0, 1, 0, 0, 1],
                'factor': [1/np.amax(z)]})

    
    ##############################################
    #creqte the surface
    handler.newSampleElement(
        'Sample_1', 
        volume  = "Square",
        dimension   = 1)


    z_trial = np.asarray(z).flatten()
    z_trial = z_trial - np.min(z_trial)
    z_trial = z_trial/ np.max(z_trial)
    color = colors.map(z_trial)

    handler.elements['Sample_1'].element.trace()
    handler.elements['Sample_1'].element.setTopography(z, color)


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
    
    ax.add_plot(
        'Surface', 
        handler.elements["Sample_1"].element.getVertices(),
        handler.elements["Sample_1"].element.getFaces(),
        Name    = "Sample_1",
        Shader = handler.elements["Sample_1"].element.color)


    ax.draw()

    sys.exit(app.exec_())

def test_3():

    handler = SampleObject(name = 'Sample_object') 


    from simpleplot.multi_canvas import Multi_Canvas
    from PyQt5 import QtWidgets
    import pyqtgraph as pg
    import numpy as np
    import sys
    import os
    
    color_map = [
        np.array([0., 0.15, 0.4, 0.5, 0.6, 0.75, 1.0]),
        np.array(
            [   [  0,   0, 255, 1],
                [  0,  50, 255, 1],
                [255,   0,   0, 1],
                [255,   0,   0, 1],
                [255, 255,   0, 1], 
                [255,  50,   0, 1],
                [255,   0,   0, 1]], 
                dtype=np.ubyte)]

    position = np.array([0,0.1, 0.2, 0.3, 0.4, 0.6,0.7,0.8])# 0.15, 0.4, 0.5, 0.6, 0.75, 1.0])
    col = np.array(
        [   [  0,   0,   0, 1],
            [255,   0, 255, 1],
            [  0,   0, 255, 1],
            [  0,   0,   0, 1],
            [255,   0,   0, 1],
            [255, 255,   0, 1],
            [  0, 255,   0, 1],
            [  0,   0,   0, 1]],
            
        dtype = np.ubyte)

    colors      = pg.ColorMap(position,col)


    handler.newSampleElement(
        'Sample_1', 
        volume  = "Cuboid",
        a       = 2,
        b       = 2,
        c       = 0.3 ,
        alpha   = 90, theta = 90,
        color   = colors.map(0.2),
        transp  = 0.5)

    handler.elements['Sample_1'].element.buildVolume()

    ##############################################
    #read in the surface file
    # f = open(os.getcwd()+"/sample/topotgraphy.xyz","r")
    # lines = f.readlines()#512
    # z = []
    # for i in range(1,len(lines)):
    #     z.append(float(lines[i].split()[-1]))

    # z = np.reshape(np.asarray(z),(512,512)) 
    z =np.loadtxt(os.getcwd()+"/sample/Image0003.txt")
    z = z * 0.5e6

    from pyqtgraph.opengl import shaders
    to_use = shaders.ShaderProgram(
        'heightColor', 
        [
             shaders.VertexShader(
                """
                varying vec4 pos;
                varying vec3 normal;
                void main() {
                """+"""    
                    normal = normalize(gl_NormalMatrix * gl_Normal);
                    gl_FrontColor = gl_Color;
                    gl_BackColor = gl_Color;
                    pos = gl_Vertex;
                    gl_Position = ftransform();
                }
                """),
        shaders.FragmentShader(
            """
            uniform float colorMap[9];
            uniform float factor[2];
            varying vec4 pos;
            varying vec3 normal;
            //out vec4 gl_FragColor;   // only needed for later glsl versions
            //in vec4 gl_Color;
            void main() {
                vec4 color = gl_Color;
                color.x = colorMap[0] * ( ( pos.z - factor[1] ) * factor[0] + colorMap[1]);
                if (colorMap[2] != 1.0)
                    color.x = pow(color.x, colorMap[2]);
                color.x = color.x < 0. ? 0. : (color.x > 1. ? 1. : color.x);
                
                color.y = colorMap[3] * ( ( pos.z - factor[1] ) * factor[0] + colorMap[4]);
                if (colorMap[5] != 1.0)
                    color.y = pow(color.y, colorMap[5]);
                color.y = color.y < 0. ? 0. : (color.y > 1. ? 1. : color.y);
                
                color.z = colorMap[6] * ( ( pos.z - factor[1] ) * factor[0] + colorMap[7]) ;
                if (colorMap[8] != 1.0)
                    color.z = pow(color.z, colorMap[8]);
                color.z = color.z < 0. ? 0. : (color.z > 1. ? 1. : color.z);
                
                color.w = 1.;
                float s = pow(normal.x*normal.x + normal.y*normal.y, 2.);
                color.x = color.x + s * (1.0-color.x);
                color.y = color.y + s * (1.0-color.y);
                color.z = color.z + s * (1.0-color.z);
                gl_FragColor = color;
            }""")
            ], 
            uniforms={
                'colorMap': [1, 0.5, 1, 1, 0, 1, 0, 0, 1],
                'factor': [1/np.amax(z),3.3]})


    #grab top surface
    top_surface = handler.elements['Sample_1'].element.getSurface('top')
    top_surface.setTopography(z, to_use)

    handler.elements['Sample_1'].translate([-1,-1,3])

            
    handler.newSampleElement(
        'Sample_2', 
        volume  = "Cuboid",
        a       = 6.,
        b       = 6.,
        c       = 3.,
        color   = colors.map(0.4),
        transp  = 1)

    handler.elements['Sample_2'].element.buildVolume()
    handler.elements['Sample_2'].translate([-3.,-3.,0.])

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

    for sam_key in handler.elements.keys():

        for key in handler.elements[sam_key].element.strucutre_surfaces.keys():
            
            ax.add_plot(
                'Surface', 
                handler.elements[sam_key].element.strucutre_surfaces[key].getVertices(),
                handler.elements[sam_key].element.strucutre_surfaces[key].getFaces(),
                Name    = key,
                Color = handler.elements[sam_key].element.strucutre_surfaces[key].color)

    ax.draw()

    

    print(handler.generateScript())
    

    sys.exit(app.exec_())

def test_4():
    from .geometry.points import Point
    import numpy as np

    ### initializing the handler here
    handler = SampleObject(name = 'Sample_object')

    ### Adding the sample element: Sample_1
    handler.newSampleElement(
        'Sample_1',
        volume = 'Cuboid',
        color = np.asarray([0, 0, 255, 1]))

    ######### GEOMETRY #########

    points = [
        Point('Point_0',-1.0,-1.0,3.0),
        Point('Point_1',1.0,-1.0,3.0),
        Point('Point_2',-1.0,1.0,3.0),
        Point('Point_3',-1.0,-1.0,3.3),
        Point('Point_4',1.0,-1.0,3.3),
        Point('Point_5',-1.0,1.0,3.3),
        Point('Point_6',1.0,1.0,3.0),
        Point('Point_7',1.0,1.0,3.3)
        ]

    handler.elements['Sample_1'].element.initWithPoints(points)

    ######### PHYSICS #########
    ### Adding the sample element: Sample_2
    handler.newSampleElement(
        'Sample_2',
        volume = 'Cuboid',
        color = np.asarray([255, 0, 0, 1]))

    ######### GEOMETRY #########

    points = [
        Point('Point_0',-3.0,-3.0,0.0),
        Point('Point_1',3.0,-3.0,0.0),
        Point('Point_2',-3.0,3.0,0.0),
        Point('Point_3',-3.0,-3.0,3.0),
        Point('Point_4',3.0,-3.0,3.0),
        Point('Point_5',-3.0,3.0,3.0),
        Point('Point_6',3.0,3.0,0.0),
        Point('Point_7',3.0,3.0,3.0)
        ]

    handler.elements['Sample_2'].element.initWithPoints(points)

    ######### PHYSICS #########

    ##############################################
    #set up the widget
    from simpleplot.multi_canvas import Multi_Canvas
    from PyQt5 import QtWidgets
    import sys

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

    for sam_key in handler.elements.keys():

        for key in handler.elements[sam_key].element.strucutre_surfaces.keys():
            
            ax.add_plot(
                'Surface', 
                handler.elements[sam_key].element.strucutre_surfaces[key].getVertices(),
                handler.elements[sam_key].element.strucutre_surfaces[key].getFaces(),
                Name    = key,
                Color = handler.elements[sam_key].element.strucutre_surfaces[key].color)

    ax.draw()

    
    

    sys.exit(app.exec_())


if __name__ == "__main__":
    test_4()


