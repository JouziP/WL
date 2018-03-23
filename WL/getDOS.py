# -*- coding: utf-8 -*-
import numpy as np


def getDOS(unormalizaed_log_E, N):
    log_dos=[]
    for E in range(len(unormalizaed_log_E)):
        sum_part = 1
        for E_prime in range(len(unormalizaed_log_E)):
            if E!=E_prime:
                alpha=unormalizaed_log_E[E_prime] - unormalizaed_log_E[E]
                g_Eprime_over_g_E = np.exp(alpha)
                sum_part+= g_Eprime_over_g_E
        log_dos.append(N*np.log(2) - np.log(sum_part))
    return np.array(log_dos)
        


#test 
#
#dos=getDOS(unormalizaed_log_E, N)
#
#import matplotlib.pyplot as plt

#plt.bar(energies/ scale, dos)