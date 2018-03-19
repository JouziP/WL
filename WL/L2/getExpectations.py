# -*- coding: utf-8 -*-
import numpy as np


def getExpectations(energies, unormalizaed_log_E, temperature, idx_to_measure):
    E_min = np.min(energies)
#    E_min = 0
    expect_energy =0 
    expect_E2 =0
    Z = 0
    log_g_measure = unormalizaed_log_E[idx_to_measure]
    
    for i in range(len(energies)):
        E = energies[i] 
        #
        g_E = np.exp(unormalizaed_log_E[i]  - log_g_measure)
        #
        expect_energy += g_E * np.exp(-1./temperature * (E - E_min ) ) * (E-E_min)
        expect_E2 += g_E * np.exp(-1./temperature * (E - E_min ) ) * (E-E_min)**2
#        print [E, g_E, np.exp(-1./temperature * (E - E_min ) ), 
#               expect_energy**2 , 
#               expect_E2]
        Z += g_E * np.exp(-1./temperature * (E -E_min) )
    expect_energy = expect_energy*1./Z
    expect_E2 = expect_E2*1./Z
    return expect_energy, expect_E2, Z