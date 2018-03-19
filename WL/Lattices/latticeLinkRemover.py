# -*- coding: utf-8 -*-
import numpy as np
from WL.BasicFunctions.shuffleIndxs import shuffleIndxs

def linkRemover(neighbors_array, **args):
    N_spins = len(neighbors_array)
    num_nighbors = neighbors_array[0].shape[0]
#    print N_spins
    #
    links_decimal_equivs = []
    for i in range(N_spins):
        for j in range(num_nighbors):
            links_decimal_equivs.append(i*N_spins + j)
#    print links_decimal_equivs
    num_links = len(links_decimal_equivs)
    #################################################
#    #
#    #
#    ## in percentage of total links
    percentage_of_links_to_be_removed =\
            float(args['percentage_of_links_to_be_removed'])/100.
#    print  percentage_of_links_to_be_removed
#    #
    num_links_to_be_removed = int(np.round(percentage_of_links_to_be_removed *\
                    num_links/2.))
#    print num_links_to_be_removed
#    #
#    spins_idxs = np.array([i for i in range(N_spins)])
    _shuffle = 10
    for i in range(_shuffle):
        links_decimal_equivs = shuffleIndxs(links_decimal_equivs, num_links)
    links_idxs = links_decimal_equivs
        
#    print links_idxs
    links_idxs_to_be_removed = links_idxs[:num_links_to_be_removed]
#    print links_idxs_to_be_removed
    for link_id in links_idxs_to_be_removed:
        spin_idx=link_id/N_spins
        neighb_idx = link_id - spin_idx*N_spins 
#        print [link_id, spin_idx, neighb_idx]
        neighbors_array[spin_idx][neighb_idx, 1] = 0
        # the reverse link
        neighb_spin_idx = int(neighbors_array[spin_idx][neighb_idx, 0])
#        print neighb_spin_idx, neighbors_array[neighb_spin_idx][:, 0]
        reverse_neighb_idx=np.where(neighbors_array[neighb_spin_idx][:, 0]==spin_idx)[0]
        neighbors_array[neighb_spin_idx][reverse_neighb_idx, 1] = 0
    return neighbors_array
#                     
        
    
        
    
    
    
    
    
    
    
#    
#    
#    
######################## test
#import numpy as np
#import pandas as pd
#import timeit
#
#from WL.Lattices.latticeConstructor import constructLattice
#
#input_id = 0 #sys.argv[1]
#print input_id
#
#filename = 'inputs_%d.csv'%int(input_id)
#INPUTS = '../../INPUTS/'
#inputs = pd.read_csv(INPUTS+filename)
##
#np.random.seed(1051)
##
##
#args={}
############# Hamilt
#args['J_const']= float(inputs['J_const'])   #-1.0
#args['E_field']= float(inputs['E_field'])   #0.0
#args['power']= float(inputs['power'])     #3.0
###########  lattice
#N1=int(inputs['N1'])
#N2=int(inputs['N2'])
#### 
#a1_x= float(inputs['a1_x'])
#a1_y= float(inputs['a1_y'])
#theta=np.pi/float(inputs['tetha_fraction'])
#a2_x=np.cos(theta)
#a2_y=np.sin(theta)
####
#args['theta'] = theta
#args['a1_x']=a1_x
#args['a1_y']=a1_y
#args['a2_x']=a2_x
#args['a2_y']=a2_y
#args['N1'] = N1
#args['N2'] = N2
#args['N_spins']=N1*N2
#args['first_neighb']=inputs['first_neighb'][0]
###
###
####
#start_time = timeit.default_timer()
#print 'building lattice :'
#neighbors_array=constructLattice(**args)
#elapsed = timeit.default_timer() - start_time
#
#
#args['percentage_of_links_to_be_removed']= 50
#neighbors_array_refined=linkRemover(neighbors_array, **args)
#
