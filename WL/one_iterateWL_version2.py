# -*- coding: utf-8 -*-
import numpy as np

from WL.L2.updateClusterWL import updateClusterWL
#from DOS.WL.getIdx_version2 import getIdx

def one_iterationWL(f_factor,
                    E_hist_density_mtx,
                    config_current, 
                    spin_idxs_current, 
                    E_current,
                    E_idx_current,
                    N,
                    precision_E,
                    **args):
    ##
    sub_itr_number = args['sub_itr_number']
    for step in range(sub_itr_number):      
        config_new,\
        spin_idxs_current,\
        E_new =  updateClusterWL(config_current, 
                                 spin_idxs_current, 
                                 E_current,
                                 N,
                                 **args)
        #
#        print 'E_new = ',  E_new
        E_idx_new=np.where(E_hist_density_mtx[:, 0]==np.round(E_new, 
                                                         precision_E) )[0]
        if len(E_idx_new)==0:
            new_row=[np.round(E_new, precision_E),
                     np.log(1) + np.log(f_factor),
                     0]
            if np.round(E_new, precision_E)>np.max(E_hist_density_mtx[:, 0]):
                #
                E_hist_density_mtx = np.vstack((E_hist_density_mtx, 
                           new_row))
            else:
                #
                E_hist_density_mtx = np.vstack((new_row,
                           E_hist_density_mtx
                           ))
                #
            E_idx_new = np.where(E_hist_density_mtx[:, 0]==np.round(E_new, 
                                                         precision_E) )[0]
                
        else:
            pass
            
        
        ## make non-Markovian decision:
        #
        log_g_E_new = E_hist_density_mtx[E_idx_new, 1]
        log_g_E_current = E_hist_density_mtx[E_idx_current, 1]
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
            E_idx_current = E_idx_new
            #### log(g_E) + log(f)
            E_hist_density_mtx[E_idx_current, 1] += +np.log(f_factor) 
            #### H(E) = H(E) + 1
            E_hist_density_mtx[E_idx_current, 2] += 1
            
        else:
            ### remain on the same manifold
            #### log(g_E) + log(f)
            E_hist_density_mtx[E_idx_current, 1] += + np.log(f_factor) 
            #### H(E) = H(E) + 1
            E_hist_density_mtx[E_idx_current, 2] += 1
            ##########
    return  E_hist_density_mtx,\
            config_current,\
            spin_idxs_current, \
            E_current,\
            E_idx_current
####                  