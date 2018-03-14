# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-



import numpy as np
#from numpy import linalg as lg
################

from WL.BasicFunctions.cleanNeighbors import cleanNeighbors

def getFirstneighbors(neighb_table):
    pass

def getCartesianFromCoords(coords, **kwgs):
    a1_x=kwgs['a1_x']
    a1_y=kwgs['a1_y']
    #
    a2_x=kwgs['a2_x']
    a2_y=kwgs['a2_y']
    #
    q1=coords[0]
    q2=coords[1]
    x = a1_x*q1 + a2_x*q2
    y = a1_y*q1 + a2_y*q2
    return x,y    

def getIndexFromCoords(coords, **kwgs):
    N1 = kwgs['N1']
    q1 = coords[0]
    q2 = coords[1]
    idx = q2*N1 + q1
    return idx    
    
    
def getCoordsFromIndex(idx, **kwgs):
    N1 = kwgs['N1']
    q2=idx/N1
    q1=idx - q2*N1
    return q1, q2

def getDistance(deltaX, deltaY):
    distance = ( (deltaX)**2 + (deltaY)**2)**(0.5)
    return distance

              
def constructLattice(**kwgs):
    N1 = kwgs['N1']
    N2 = kwgs['N2']
    num_sites =  N1* N2
    neighbors_array = []
    for n in range(num_sites):
        neighbors_array.append(getNeighborTableGeneralized(n, **kwgs))
    return neighbors_array




def getNeighborTableGeneralized(idx, **kwgs):
    ###
    power = kwgs['power']
    a1_x=kwgs['a1_x']
    a1_y=kwgs['a1_y']
    #
    a2_x=kwgs['a2_x']
    a2_y=kwgs['a2_y']
    #
    ###
    neighbs=[]
    q1, q2 = getCoordsFromIndex(idx, **kwgs)
    #
    N1 = kwgs['N1']
    #
    N2 = kwgs['N2']
    #
    N = N1 * N2
    for i in range(0, N, 1):
        q1_n, q2_n = getCoordsFromIndex(i, **kwgs)
        ### direct        
        if q1==q1_n and q2==q2_n:
            pass
        else:
            x_n, y_n = getCartesianFromCoords(np.array([q1_n, q2_n]),
                                              **kwgs)
            # cartesian coords
            x0,y0 = getCartesianFromCoords(np.array([q1,q2]), **kwgs)
            distance = getDistance( (x_n-(x0)) , (y_n-y0) )
            ### periodic 1
            # cartesian coords
            x=x0+N2*a1_x
            y=y0+N2*a1_y
            distance10 = getDistance( (x_n-x), (y_n-y) )
            #
            x=x0-N2*a1_x
            y=y0-N2*a1_y
            distance11 = getDistance( (x_n-x), (y_n-y) )
            distance1=np.min([distance10, distance11])
            ### peridic in 2
            x=x0+N1*a2_x
            y=y0+N1*a2_y
            distance20 = getDistance( (x_n-x), (y_n-y) )
            x=x0-N1*a2_x
            y=y0-N1*a2_y
            distance21 = getDistance( (x_n-x), (y_n-y) )
            distance2=np.min([distance20, distance21])
            #### peridic in 1 and 2
            # cartesian coords
            x=x0+N1*a2_x+N2*a1_x
            y=y0+N1*a2_y+N2*a1_y
            distance300 = getDistance( (x_n-x), (y_n-y) )
            x=x0+N1*a2_x-N2*a1_x
            y=y0+N1*a2_y-N2*a1_y
            distance301 = getDistance( (x_n-x), (y_n-y) )
            x=x0-N1*a2_x+N2*a1_x
            y=y0-N1*a2_y+N2*a1_y
            distance310 = getDistance( (x_n-x), (y_n-y) )
            x=x0-N1*a2_x-N2*a1_x
            y=y0-N1*a2_y-N2*a1_y
            distance311 = getDistance( (x_n-x), (y_n-y) )
            distance3=np.min([distance300, 
                              distance310, 
                              distance301,
                              distance311])
            distance = np.min([distance, 
                               distance1,
                               distance2,
                               distance3,
                               ])
            #
            strength = 1./distance**(power)
            #
            neighbs.append([i, strength])
            if kwgs['first_neighb']==True:
                all_neighbors = cleanNeighbors(neighbs)
                neighbs=all_neighbors[0]
            ###
    return np.array(neighbs)

    