# -*- coding: utf-8 -*-
import numpy as np


def getExpectations(energies, temperature):
    E_min = np.min(energies)
    expect_energy =0 
    expect_E2 =0
    Z = 0
    for i in range(len(energies)):
        E = energies[i] 
        expect_energy += np.exp(-1./temperature * (E - E_min ) ) * (E-E_min)
        expect_E2 += np.exp(-1./temperature * (E - E_min ) ) * (E-E_min)**2
        Z += np.exp(-1./temperature * (E -E_min) )
    expect_energy = expect_energy*1./Z
    expect_E2 = expect_E2*1./Z
    return expect_energy, expect_E2, Z