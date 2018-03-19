# -*- coding: utf-8 -*-
import numpy as np



def getEntropy(unormalizaed_log_E, energies, Temp, N, E_expt):
    val = 0
    for i in range(len(unormalizaed_log_E)):
        if i !=0:
            alpha=unormalizaed_log_E[i] -\
                        unormalizaed_log_E[0]
    #        print alpha
            ratio_gE_gMax = np.exp(alpha)
            val += ratio_gE_gMax*np.exp(-1./Temp * (energies[i] -energies[0]) )
#    print -1./Temp * energies[0]
#    print np.log(1+val)
    log_Z = np.log(1+val)/N+getResidualEntropy(unormalizaed_log_E, N)/N +\
    (-1./Temp * energies[0]+1./Temp *E_expt)/N
    return log_Z
###############
#m=0
#log_gMax = getEntropy(unormalizaed_log_E, energies, Temps[m], N, energies_expt[m])


def getResidualEntropy(unormalizaed_log_E, N):
    idx_g_E_max = 0
    val = 0
    for i in range(len(unormalizaed_log_E)):
        if i !=idx_g_E_max:
            alpha=unormalizaed_log_E[i] - unormalizaed_log_E[idx_g_E_max]
            ratio_gE_gMax = np.exp(alpha)
#            print np.log(ratio_gE_gMax)
            val+=ratio_gE_gMax
#            print val
    log_gMax = -np.log(1+val) + N*np.log(2)
#    print log_gMax
    return log_gMax

#m=0
#print getEntropy(unormalizaed_log_E, energies, Temps[m], N, energies_expt[m])

