# -*- coding: utf-8 -*-
import numpy as np


def getExpectation_E2(energies,  temperature):
    E_min = np.min(energies)
#    E_min = 0
    expect_E2 =0 
    Z =0
    for i in range(len(energies)):
        E = energies[i] 
        expect_E2 += np.exp(-1./temperature * (E - E_min ) ) * (E-E_min)**2
#        print np.exp(-1./temperature * (E - E_min ) )
        Z += np.exp(-1./temperature * (E -E_min) )
    expect_E2 = expect_E2*1./Z
    return expect_E2
