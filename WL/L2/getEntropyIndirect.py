# -*- coding: utf-8 -*-

import numpy as np

def getIndirectEntropy(specific_heat, E_0, Temps):
    Entropy_array=[]
#    Entropy=np.log(2)
#    Entropy_array.append(Entropy)
    for T in range(len(Temps)-1):
        dEntropy=0
        for t in range(T):
            dT = Temps[t] - Temps[t+1]
            dEntropy+=dT * specific_heat[t]/Temps[t] 
#        Entropy=np.log(2) - dEntropy + 1./Temps[0] * E_0
        Entropy=- dEntropy + np.log(2)
        Entropy_array.append(Entropy)
    return Entropy_array
