# -*- coding: utf-8 -*-
#import numpy as np
#import pandas as pd
#import timeit
#import matplotlib.pyplot as plt
#
#from WL.Lattices.latticeConstructor import constructLattice
#from rankNeighbs import getUpToRankNeighbs
#np.random.seed(1051)
##
##
#args={}
############# Hamilt
#args['J_const']= -1.0
#args['E_field']= 0.0
#args['power']= 3.0
###########  lattice
#N1=8
#N2=8
#### 
#a1_x= 1
#a1_y= 0
#theta=np.pi/3
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
#args['first_neighb']=False
###
##############
##############
#neighbors_table=constructLattice(**args)
#
#
#
##args['percentage_of_links_to_be_removed']=inputs['percentage_of_links_to_be_removed'][0]
##neighbors_table = linkRemover(neighbors_table, **args)
#
#
##
#
#def sortNeighbors(neighbs):
#   neighbs_df =  pd.DataFrame(neighbs)
#   neighbs_df = neighbs_df.sort_values(1, ascending=False) 
#   neighbs[:,:]= neighbs_df.values[:,:]
#   return neighbs
#
#
######################################
#spin_idx = 0
#neighbs = neighbors_table[0]
#
#
#length_neighbs = neighbs.shape[0]
##for i in range(length_neighbs):
##    print neighbs[i, :]
##print '==================='
#neighbs=getUpToRankNeighbs(4, neighbs)
##for i in range(len(neighbs)):
##    print neighbs[i, :]
##################################################
##
##length_neighbs = neighbs.shape[0]
##neighbs_by_rank=[]
##idx=0 
##k=0
##while idx<length_neighbs:
##    strength = neighbs[idx, 1]
##    nghbs=[]
##    while idx<length_neighbs and\
##            np.round(neighbs[idx, 1], 5) == np.round(strength, 5):
##        nghbs.append(neighbs[idx, :])
##        idx+=1
##        
##    neighbs_by_rank.append(np.array(nghbs))
##    k+=1
##
##for i in range(len(neighbs_by_rank)):
##    for j in range(neighbs_by_rank[i].shape[0]):
##        print neighbs_by_rank[i][j, :]
##    print '======'
##
##print '-------'
##print '-------'
##print '-------'
##for i in range(length_neighbs):
##    print neighbs[i, :]
##
##   
#
#    
#
#
