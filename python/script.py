########################################
############## MEASUREMENT #############
########################################

########################################
# import dependencies here
import numpy as np
from .measurement.geometry.points import Point

def run(meas):    
    
    ########################################
    # initializing the measurement here
    meas.setSample()
    
    ### Adding the sample element: Sample_1
    meas.sample.newElement(
        'Sample_1',
        volume = 'Cube',
        color = np.asarray([255, 0, 0, 1])    )

    ######### GEOMETRY #########

    points = [
        Point('Point_0',-1.0,-1.0,-1.0),
        Point('Point_1',1.0,-1.0,-1.0),
        Point('Point_2',-1.0,1.0,-1.0),
        Point('Point_3',-1.0,-1.0,1.0),
        Point('Point_4',1.0,-1.0,1.0),
        Point('Point_5',-1.0,1.0,1.0),
        Point('Point_6',1.0,1.0,-1.0),
        Point('Point_7',1.0,1.0,1.0)
        ]
        
    meas.sample.elements['Sample_1'].geometry.initWithPoints(points)

    ######### PHYSICS #########
    ### Adding the sample element: Sample_2
    meas.sample.newElement(
        'Sample_2',
        volume = 'Cylinder',
        color = np.asarray([0, 255, 0, 1])    )

    ######### GEOMETRY #########

    points = [
        Point('Point_0',-1.0,-1.0,-1.5),
        Point('Point_1',1.0,-1.0,-1.5),
        Point('Point_2',-1.0,1.0,-1.5),
        Point('Point_3',-1.0,-1.0,-0.5),
        Point('Point_4',1.0,-1.0,-0.5),
        Point('Point_5',-1.0,1.0,-0.5),
        Point('Point_6',1.0,1.0,-1.5),
        Point('Point_7',1.0,1.0,-0.5)
        ]
        
    meas.sample.elements['Sample_2'].geometry.initWithPoints(points)

    ######### PHYSICS #########
    ### Adding the sample element: Sample_3
    meas.sample.newElement(
        'Sample_3',
        volume = 'Sphere',
        color = np.asarray([0, 0, 255, 1])    )

    ######### GEOMETRY #########

    points = [
        Point('Point_0',-0.5773502692,-0.5773502692,0.4226497308),
        Point('Point_1',0.5773502692,-0.5773502692,0.4226497308),
        Point('Point_2',-0.5773502692,0.5773502692,0.4226497308),
        Point('Point_3',-0.5773502692,-0.5773502692,1.5773502692),
        Point('Point_4',0.5773502692,-0.5773502692,1.5773502692),
        Point('Point_5',-0.5773502692,0.5773502692,1.5773502692),
        Point('Point_6',0.5773502692,0.5773502692,0.4226497308),
        Point('Point_7',0.5773502692,0.5773502692,1.5773502692)
        ]
        
    meas.sample.elements['Sample_3'].geometry.initWithPoints(points)

    ######### PHYSICS #########
    ### Adding the sample element: Sample_4
    meas.sample.newElement(
        'Sample_4',
        volume = 'Cylinder',
        color = np.asarray([0, 255, 0, 1])    )

    ######### GEOMETRY #########

    points = [
        Point('Point_0',-0.1,-0.1,2.0),
        Point('Point_1',0.1,-0.1,2.0),
        Point('Point_2',-0.1,0.1,2.0),
        Point('Point_3',-0.1,-0.1,4.0),
        Point('Point_4',0.1,-0.1,4.0),
        Point('Point_5',-0.1,0.1,4.0),
        Point('Point_6',0.1,0.1,2.0),
        Point('Point_7',0.1,0.1,4.0)
        ]
        
    meas.sample.elements['Sample_4'].geometry.initWithPoints(points)

    ######### PHYSICS #########
    meas.setInstrument()
    
