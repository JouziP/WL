# -*- coding: utf-8 -*-
import numpy as np


def getPartitionZ(energies, unormalizaed_log_E, temperature, idx_to_measure):
    E_min = np.min(energies)
    Z = 0
    log_g_measure = unormalizaed_log_E[idx_to_measure]
    
    for i in range(len(energies)):
        E = energies[i] 
        #
        g_E = np.exp(unormalizaed_log_E[i]  - log_g_measure)
        #
        Z += g_E * np.exp(-1./temperature * (E -E_min) )
    return Z