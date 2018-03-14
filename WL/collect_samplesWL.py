# -*- coding: utf-8 -*-

#import timeit
import numpy as np

from WL.BasicFunctions.getDecimalEquivalent import getDecimalEquivalent

from WL.L2.getIdx import getIdx
from WL.L2.updateClusterWL import updateClusterWL

def collect_samples(WL_density, 
                    config_current,
                    E_idx_current,
                    E_current,
                    N,
                    spin_idxs_current, 
                    **args
                    ):
    #########
    E_marks = args['E_marks']
    N_collection = args['N_collection']
    N_attempts   = args['N_collection_attempts']
    #########
    collected_energies      = []
    collected_configs        = []
    collected_polarizations = []
    decimal_equivs = []
    ##################
    collected_energies.append(E_current)
#    collected_configs.append(config_current)
    P_current = np.sum(config_current)
    collected_polarizations.append(P_current)
    decimal_current = getDecimalEquivalent(config_current)[0]
    decimal_equivs.append(decimal_current)
    ##################
    num_attempt = 0
    while (len(decimal_equivs) < N_collection and
                num_attempt< N_attempts and\
                    len(decimal_equivs)<2**N):
        config_new,\
        spin_idxs_new,\
        E_new =  updateClusterWL(config_current, 
                                 spin_idxs_current, 
                                 E_current,
                                 N,
                                 **args)
        E_idx_new = getIdx(E_new, E_marks)
        ##
        log_g_E_new = WL_density[E_idx_new]
        log_g_E_current = WL_density[E_idx_current]
        ##
        Prob_transition = min([1, np.exp(log_g_E_current-log_g_E_new)])
        if Prob_transition==np.inf or Prob_transition==np.nan:
            print Prob_transition
            #
        r = np.random.uniform(np.round(0, 10), np.round(1, 10))
        if r<Prob_transition:
            ### make the move
            E_current  = E_new
            config_current = config_new
            E_idx_current = E_idx_new
            decimal_current  = getDecimalEquivalent(config_current)[0]
#            print decimal_current
            
            if decimal_current not in decimal_equivs:
#                print decimal_current
                collected_energies.append(E_current)
#                collected_configs.append(config_current)
                P_current = np.sum(config_current)
                collected_polarizations.append(P_current)
                decimal_equivs.append(decimal_current)
        else:
            ### remain on the same manifold
            decimal_current  = getDecimalEquivalent(config_current)[0]
            if decimal_current not in decimal_equivs:
#                print decimal_current
                collected_energies.append(E_current)
#                collected_configs.append(config_current)
                P_current = np.sum(config_current)
                collected_polarizations.append(P_current)
                decimal_equivs.append(decimal_current)
        ########
        num_attempt +=1
        #################################################
    print 'num_attempst = %d'%num_attempt
    return [
            collected_energies, 
           collected_configs, 
           collected_polarizations, 
           decimal_equivs,
           ]
    

        
#    
###### test
#from DOS.BasicFunctions.getRandomConfig import getRandomConfig
#args['E_marks'] = E_hist_density[:, 0]
#WL_density = E_hist_density[:, 1]
#args['N_collection'] = 513
#args['max_cluster_size'] = 1
#spin_idxs_current = [i for i in range(N)]
###
#config_current = getRandomConfig(N)
###
#E_current     = getEnergyOfConfig(config_current, **args)
#E_idx_current = getIdx(E_current, args['E_marks'])
##
##
#
#start_time = timeit.default_timer()
#print 'collection started:'
#rslts = collect_samples(WL_density, 
#                    config_current,
#                    E_idx_current,
#                    E_current,
#                    N,
#                    spin_idxs_current, 
#                    **args
#                    )
#elapsed = timeit.default_timer() - start_time
#print 'time elapsed: %s '%elapsed
#print '------'  
#plt.hist(rslts[0], 400)
