# -*- coding: utf-8 -*-



import numpy as np


def getEnergyDiffIfClusterFlip(cluster, 
                               config_current, 
                               E_current,
                                **args):
    G=args['G']
    config_new = np.copy(config_current)
    for node in cluster:
        config_new[node] = config_new[node] * -1
    config_new = np.array(config_new)
    E_new = np.dot(np.dot(config_new, G), np.transpose(config_new))[0,0]
    energy_2b_added_if_cluster_is_flipped = E_new - E_current
    ###
    return energy_2b_added_if_cluster_is_flipped
                



##########  
#import timeit
#import pandas as pd
#from WL.L1.getEnergyOfConfig import getEnergyOfConfig
#from WL.Lattices.getGraphMatrix import getGraphMatrix
#from getEnergyDiffIfClusterFlip import getEnergyDiffIfClusterFlip as getEnergyDiffIfClusterFlipOld
#from WL.BasicFunctions.getRandomConfig import getRandomConfig
#from WL.Lattices.latticeConstructor import constructLattice
#
#input_id = -1   
#print input_id
#
#
#filename = 'inputs_%d.csv'%int(input_id)
#INPUTS = '../../INPUTS/'
#inputs = pd.read_csv(INPUTS+filename)
#
##
#np.random.seed(1011)
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
##############
###### log file
#f = open('logFile_N1_%d_N2_%d_theta_%2.2f_J_const_%d_power_%d_nn_%s_inputID_%d.txt'\
#         %(N1,N2, 
#           theta, 
#           float(inputs['J_const']),
#           float(inputs['power']),
#           inputs['first_neighb'][0],
#           int(input_id)
#           )
#         ,'w')
#input_log_message = 'input_id = %d \n\n'%int(input_id)
#f.write(input_log_message)
#### general lattice info:
#f.write('--------------------\n')
#lattice_log_message= 'N1 = %d, N2 = %d, theta= %2.2f, \n'
#f.write(lattice_log_message)
#f.write('--------------------\n\n')
##############
##start_time = timeit.default_timer()
#f.write('building lattice :\n')
#print 'building lattice :'
#neighbors_table=constructLattice(**args)
##args['percentage_of_links_to_be_removed']=inputs['percentage_of_links_to_be_removed'][0]
##neighbors_table = linkRemover(neighbors_table, **args)
##elapsed = timeit.default_timer() - start_time
##############
#args['neighbors_table']=neighbors_table
#
#
#
#G=getGraphMatrix(**args)
#args['G'] = G
#N = args['N1']*args['N2']
#cluster = [0, 2, 4]
#
#
#config_current= getRandomConfig(N)
#
#start_time = timeit.default_timer()
#E_current = getEnergyOfConfig(config_current,**args)
#elapsed = timeit.default_timer() - start_time
#
#
#print E_current, 'time= ' , elapsed
#
#start_time = timeit.default_timer()
#E=np.dot(np.dot(np.array(config_current), G), np.transpose(np.array(config_current)) )[0,0]
#elapsed = timeit.default_timer() - start_time
#
#print E, 'New time= ' , elapsed
#
#
#start_time = timeit.default_timer()
#dE = getEnergyDiffIfClusterFlip(cluster, 
#                               config_current, 
#                               E,
#                                **args)
#elapsed = timeit.default_timer() - start_time
#
#print dE, 'New s Time = ' , elapsed
#
#start_time = timeit.default_timer()
#dE_old = getEnergyDiffIfClusterFlipOld(cluster, 
#                               config_current, 
#                                **args)
#elapsed = timeit.default_timer() - start_time
#
#print dE_old, 'Old s Time = ' , elapsed