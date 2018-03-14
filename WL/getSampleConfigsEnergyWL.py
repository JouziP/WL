# -*- coding: utf-8 -*-


import timeit
import numpy as np

from WL.BasicFunctions.getRandomConfig import getRandomConfig


from WL.L1.getEnergyOfSpinConfig import getEnergyOfConfig  

from WL.L2.getIdx import getIdx
from WL.L2.one_iterateWL import one_iterationWL
from WL.L2.check_flatness import check_flatness
from WL.L2.collect_samplesWL import collect_samples

def getSampleConfigsEnergysWL(f_factor_init,precision, **args):
    N1 = args['N1']
    N2 = args['N2']
    N = N1 * N2
    ### ex. f_factor = 2.7182
    f_factor = f_factor_init
    #### ######## initializations:
    E_hist_density = np.zeros([len(args['E_marks']), 3])
    E_hist_density[:, 0] = args['E_marks']
    ### log(g_E)
    E_hist_density[:, 1] = np.log(1) + np.log(f_factor)
    ### H(E)
    E_hist_density[:, 2] = 0
    #### ######## init configs:
    idxs_current = [i for i in range(N)]
    config_current = getRandomConfig(N)
    E_current  = getEnergyOfConfig(config_current, **args)
    idx_current = getIdx(E_current, E_marks)
    #### log(g_E) + log(f)
    E_hist_density[idx_current, 1] += np.log(f_factor) 
    #### H(E) = H(E) + 1
    E_hist_density[idx_current, 2] += 1
#    ###################################################
    itr=0
    condition1 = (itr<= int(args['num_steps_in_one_level_random_walk']))
    condition2 = (np.round(f_factor, precision) > np.round(1., precision))
    while condition1 and condition2 :
        ###
        flatness = check_flatness(E_hist_density)
#        print '**' , flatness, ' %', 'f= ' , f_factor 
        if flatness<10 and itr!=0:
            f_factor = np.sqrt(f_factor)
            print '*****' ,itr,  flatness, ' %', 'f= ' , f_factor 
            E_hist_density[:, 2] =0
        ###
        E_hist_density,\
        config_current,\
        idxs_current, \
        E_current,\
        idx_current = one_iterationWL(f_factor, E_hist_density, 
                  config_current,  idxs_current,  E_current,idx_current,  N,
                   **args)
        ###
        itr+=1
        ###
        condition1 = (itr<= int(args['num_steps_in_one_level_random_walk']))
        condition2 = (np.round(f_factor, precision) > np.round(1., precision))
        ####
    print '*****' , flatness, ' %', 'f= ' , f_factor, condition1, condition2 
    ########  collection:
    WL_density = E_hist_density[:, 1]
    ##
    collected_energies,\
    collected_configs,\
    collected_polarizations = collect_samples(WL_density, config_current,
                                                idx_current, E_current, N,
                                                idxs_current, **args
                                                )
    
    return E_hist_density, f_factor, collected_energies,\
                collected_configs,  collected_polarizations
    


#########################################################################           
###### test
from DOS.FunctionsLayer1.Lattices.latticeConstructor import constructLattice
#import matplotlib.pyplot as plt
N1=10
N2=10
np.random.seed(1051)
args={}
args['J_const']=1.0
args['E_field']=0.0
args['power']=3.0
#########
a1_x= 1.0
a1_y= 0
theta=np.pi/3
a2_x=np.cos(theta)
a2_y=np.sin(theta)
##
args['a1_x']=a1_x
args['a1_y']=a1_y
args['a2_x']=a2_x
args['a2_y']=a2_y
#########
args['N1'] = N1
args['N2'] = N2
args['N_spins']=N1*N2
args['first_neighb']=True
####
start_time = timeit.default_timer()
print 'building lattice :'
neighbors_table=constructLattice(**args)
args['neighbors_table']=neighbors_table
elapsed = timeit.default_timer() - start_time
print 'time elapsed: %s '%elapsed
print '------'  
###########
args['max_cluster_size'] = 1
N = N1 * N2
############
test=[1000]
for t in test:
    args['num_steps_in_one_level_random_walk']=t
    ##
    f= np.exp(1)
    precision = 6
    ##
    args['sub_itr_number'] = 5000
    ##
    args['E_lower_bound'] =-1.5*N1*N2
    args['E_upper_bound'] =+1.5*N1*N2
    ##
    #######################
    E_lower_bound = args['E_lower_bound']
    E_upper_bound = args['E_upper_bound']
    E_marks=[
#            E_lower_bound, 
            E_lower_bound/2.,
            E_lower_bound/5.5, 
#            E_lower_bound/2.5,  
#            0,
#            E_upper_bound/1.5 , 
#            E_upper_bound/5.5 ,             
#            E_upper_bound/1. , 
#            E_upper_bound
             ]
    args['E_marks'] = E_marks
    ## less than 2**(N1*N2) !!
    args['N_collection'] =  100000
    print 'N1*N2 = ', N1*N2
    print E_marks
    ######################
    start_time = timeit.default_timer()
    print 'getSample :'
    E_hist_density, f, collected_energies,\
        collected_configs,  collected_polarizations=\
                    getSampleConfigsEnergysWL(f,precision ,**args)
    print '------'
    elapsed = timeit.default_timer() - start_time
    print 'time elapsed: %s '%elapsed
    print '------'
    print ' f factor =' , f
    ####
    for i in range(E_hist_density.shape[0]):
        print E_hist_density[i, :]
    ####        
    print check_flatness(E_hist_density), '%'
    ####
import matplotlib.pyplot as plt
plt.hist(collected_energies, 100)
print np.min(collected_energies), np.max(collected_energies)
#
#    
#
#
##import matplotlib.pyplot as plt
##plt.hist(energys_collected, 200)
##plt.hist(collected_E_exact_calculation, len(collected_E_exact_calculation))