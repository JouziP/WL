# -*- coding: utf-8 -*-


import numpy as np

from WL.BasicFunctions.shuffleIndxs import shuffleIndxs
#from WL.L1.getEnergyDiffIfClusterFlip import getEnergyDiffIfClusterFlip
from WL.L1.getEnergyDiffIfClusterFlipV2 import getEnergyDiffIfClusterFlip

def updateClusterWL(config_current, 
                  idxs_current, 
                  E_current,
                  N,  
                  **args):
    max_cluster_size = args['max_cluster_size'] + 1
    ###
    idxs_new = shuffleIndxs(idxs_current, N)
    ###
    cluster_size  = np.random.randint(1, max_cluster_size)
    cluster = idxs_new[:cluster_size]
#    dE_2add = getEnergyDiffIfClusterFlip(cluster, config_current, **args)
    dE_2add = getEnergyDiffIfClusterFlip(cluster, 
                                         config_current, 
                                         E_current, 
                                         **args)
    E_new = E_current + dE_2add
    #
    config_new = np.copy(config_current)
    for n in cluster: config_new[n] *=-1
    #
    return config_new, idxs_new, E_new
    
    
#    
##### test 
###### test
#from DOS.FunctionsLayer1.Lattices.latticeConstructor import constructLattice
#import matplotlib.pyplot as plt
#N1=6
#N2=6
#np.random.seed(1051)
#args={}
#args['J_const']=1.0
#args['E_field']=0.0
#args['power']=3.0
#args['a1_x']=1.0
#args['a1_y']=0.0
##
#args['a2_x']=0.0
#args['a2_y']=1.0
#
#args['N1'] = N1
#args['N2'] = N2
#args['N_spins']=N1*N2
#args['first_neighb']=False
#neighbors_tables_list = constructLattice(**args)
#neighbors_table=constructLattice(**args)
#args['neighbors_table']=neighbors_table
#
#from DOS.BasicFunctions.getRandomConfig import getRandomConfig
#from DOS.FunctionsLayer1.getEnergyOfSpinConfig import getEnergyOfConfig    
#args['max_cluster_size'] = 3
#
#N = N1 * N2
#config_current = getRandomConfig(N)
#idxs_current = [i for i in range(N)]
#E_current  = getEnergyOfConfig(config_current, **args)
#E_target = -N1*N2*10
#
#print E_current
#print config_current
#print idxs_current
#
#num_E = 100.
#dE=2*E_target/num_E
#E_windows=[-E_target + dE*i for i in range(int(num_E))]
#print E_current, E_windows[0]
#E_currents=[]
#for E_w in E_windows:
#    for i in range(300):
#        config_current,\
#        idxs_current,\
#        E_current,\
#        dE_2add= updateCluster(config_current, 
#                             idxs_current, 
#                             E_current,
#                             E_w,
#                             N,  **args)
##        print E_current
#    E_currents.append(E_current)
#    
#    
#print np.min(E_currents), np.max(E_currents)