# -*- coding: utf-8 -*-
import numpy as np

from WL.L2.updateClusterWL import updateClusterWL
from WL.L2.getIdx import getIdx

def one_iterationWL(f_factor,
                  E_hist_density,
                  config_current, 
                  idxs_current, 
                  E_current,
                  idx_current,
                  N,
                  **args):
    ##
    E_marks = args['E_marks']
    sub_itr_number= args['sub_itr_number']
    for step in range(sub_itr_number):      
        config_new,\
        idxs_new,\
        E_new =  updateClusterWL(config_current, 
                                   idxs_current, 
                                   E_current,
                                   N,
                                   **args)
        ## decision:
        idx_new = getIdx(E_new, E_marks)
        #
        log_g_E_new = E_hist_density[idx_new, 1]
        log_g_E_current = E_hist_density[idx_current, 1]
        #
        Prob_transition = min([1, np.exp(log_g_E_current-log_g_E_new)])
        if Prob_transition==np.inf or Prob_transition==np.nan:
            print Prob_transition
        #
        r = np.random.uniform()
        if r<Prob_transition:
            ### make the move
            E_current  = E_new
            config_current = config_new
            idx_current = idx_new
            #### log(g_E) + log(f)
            E_hist_density[idx_current, 1] += +np.log(f_factor) 
            #### H(E) = H(E) + 1
            E_hist_density[idx_current, 2] += 1
            
        else:
            ### remain on the same manifold
            #### log(g_E) + log(f)
            E_hist_density[idx_current, 1] += + np.log(f_factor) 
            #### H(E) = H(E) + 1
            E_hist_density[idx_current, 2] += 1
            ##########
    return  E_hist_density,\
            config_current,\
            idxs_current, \
            E_current,\
            idx_current
####                  