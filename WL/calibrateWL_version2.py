# -*- coding: utf-8 -*-


#import timeit
import numpy as np

from WL.BasicFunctions.getRandomConfig import getRandomConfig


from WL.L1.getEnergyOfConfig import getEnergyOfConfig
#from DOS.WL.getIdx import getIdx
from WL.L2.one_iterateWL_version2 import one_iterationWL
from WL.L2.check_flatness import check_flatness


def callibrateWL(**args):
    ############
    N1 = args['N1']
    N2 = args['N2']
    f_factor_init = args['f_factor_init']
    precision_E = args['precision_E']
    precision_f = args['precision_f']
    flatness_min= args['flatness_min']
    N = N1 * N2
    #### ######## initializations:
    ### ex. f_factor = 2.7182
    f_factor = f_factor_init
    ### initializing the E - g_E - H(E) dynamic matrix
    E_hist_density_mtx = np.zeros([1, 3])
    # energy unknown as of now.
    E_hist_density_mtx[0, 1] = np.log(1) + np.log(f_factor)
    ##
    spin_idxs_current = [i for i in range(N)]
    ##
    config_current = getRandomConfig(N)
    ##
    E_current  = getEnergyOfConfig(config_current, **args)
    ##
    E_hist_density_mtx[0, 0] = np.round(E_current, precision_E)
    ## log(g_E) + log(f)
    E_hist_density_mtx[0, 1] += np.log(f_factor)
    ## H(E) = H(E) + 1
    E_hist_density_mtx[0, 2] += 1
    ## idx_current 
    E_idx_current  = 0
    print '================================'
    print E_hist_density_mtx
    flatness_array = []
    f_factor_array = []
#    ###################################################
    itr=0
    condition1 = (itr<= int(args['num_steps_in_one_level_random_walk']))
    condition2 = (np.round(f_factor, precision_f) > np.round(1., precision_f))
    while condition1 and condition2 :
        ###
        flatness = check_flatness(E_hist_density_mtx)
        flatness_array.append(flatness)
        f_factor_array.append(f_factor)
#        print flatness
        if flatness>flatness_min and itr!=0:
            f_factor = np.sqrt(f_factor)
            print '*****', itr,  flatness, ' %', 'f= ' , f_factor 
            E_hist_density_mtx[:, 2] =  0
        ###
        E_hist_density_mtx,\
        config_current,\
        spin_idxs_current, \
        E_current,\
        E_idx_current = one_iterationWL(f_factor,
                                        E_hist_density_mtx,
                                        config_current, 
                                        spin_idxs_current,  
                                        E_current, 
                                        E_idx_current, 
                                        N,
                                        **args)
        ###
        itr+=1
        ###
        condition1 = (itr<= int(args['num_steps_in_one_level_random_walk']))
        condition2 = (np.round(f_factor, precision_f) > np.round(1., precision_f))
        ####
    print '*****' , flatness, ' %', 'f= ' , f_factor, condition1, condition2 

    return [
            E_hist_density_mtx, 
            f_factor, 
            flatness_array,
            itr,
            f_factor_array,
            [config_current, 
             E_current,
             E_idx_current,
             spin_idxs_current,
             ]
            ]
    





#
#
#
##########################################################################           
####### test
#from DOS.FunctionsLayer1.Lattices.latticeConstructor import constructLattice
##import matplotlib.pyplot as plt
#N1=3
#N2=3
#np.random.seed(1051)
#args={}
#args['J_const']=1.0
#args['E_field']=0.0
#args['power']=3.0
##########
#a1_x= 1.0
#a1_y= 0
#theta=np.pi/3
#a2_x=np.cos(theta)
#a2_y=np.sin(theta)
###
#args['a1_x']=a1_x
#args['a1_y']=a1_y
#args['a2_x']=a2_x
#args['a2_y']=a2_y
##########
#args['N1'] = N1
#args['N2'] = N2
#args['N_spins']=N1*N2
#args['first_neighb']=True
#####
#start_time = timeit.default_timer()
#print 'building lattice :'
#neighbors_table=constructLattice(**args)
#args['neighbors_table']=neighbors_table
#elapsed = timeit.default_timer() - start_time
#print 'time elapsed: %s '%elapsed
#print '------'  
############
#args['max_cluster_size'] = 1
#N = N1 * N2
#############
#test=[1000]
#for t in test:
#    args['num_steps_in_one_level_random_walk']=t
#    ##
#    f= np.exp(1)
#    precision_f = 3
#    precision_E=2
#    flatness_min = 95
#    ##
#    args['sub_itr_number'] = 5000
#    ##
#    ## less than 2**(N1*N2) !!
##    args['N_collection'] =  200 #(N1*N2)**3/10
#    print 'N1*N2 = ', N1*N2
#    ######################
#    start_time = timeit.default_timer()
#    print 'getSample :'
#    
#    
#    
#    
#    
#    rslts=callibrateWL(f,precision_E, precision_f,flatness_min ,**args)
#    E_hist_density = rslts[0]
#    f = rslts[1]
##    collected_energies=rslts[2]
##    collected_configs = rslts[3]  
##    collected_polarizations = rslts[4]  
#    flatness_array = rslts[-3]
#    itr = rslts[-2]
#    f_array = rslts[-1]
#    print '------'
#    elapsed = timeit.default_timer() - start_time
#    print 'time elapsed: %s '%elapsed
#    print '------'
#    print ' f factor =' , f
#    ####
#    for i in range(E_hist_density.shape[0]):
#        print E_hist_density[i, :]
#    ####        
#    print check_flatness(E_hist_density), '%'
#    ####
#import matplotlib.pyplot as plt
#fig, frame =plt.subplots(3,1, figsize=[10, 12])
#
##frame[0].hist(collected_energies, 100)
#frame[1].plot(flatness_array, '-o')
#frame[1].hlines(flatness_min, 0, itr)
#frame[2].plot(f_array, '-o')
##frame[2].hlines(1, 0, itr)