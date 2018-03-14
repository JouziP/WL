# -*- coding: utf-8 -*-
import numpy as np


def getExpectation_energy(energies, temperature):
    E_min = np.min(energies)
    expect_energy =0 
    Z =0
    for i in range(len(energies)):
        E = energies[i] 
        expect_energy += np.exp(-1./temperature * (E - E_min ) ) * (E-E_min)
        Z += np.exp(-1./temperature * (E -E_min) )
    expect_energy = expect_energy*1./Z
    return expect_energy
