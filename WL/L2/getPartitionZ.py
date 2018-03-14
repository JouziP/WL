# -*- coding: utf-8 -*-
import numpy as np


def getPartitionZ(energies, temperature):
    E_min = np.min(energies)
    Z =0
    for i in range(len(energies)):
        E = energies[i] 
        Z += np.exp(-1./temperature * (E -E_min) )
    return Z