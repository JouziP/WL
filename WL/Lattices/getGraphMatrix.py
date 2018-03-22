# -*- coding: utf-8 -*-

import numpy as np


def getGraphMatrix(**args):
    neighbors_table = args['neighbors_table']
    N1 = args['N1']
    N2 = args['N2']
    N = N1 *N2 
    G = np.zeros([N, N])
    J_const = args['J_const']
    for i in range(N):
        neighbs= neighbors_table[i]
        for n in range(neighbs.shape[0]):
            j = int(neighbs[n, 0])
            G[i, j] = np.round(neighbs[n, 1], 5) * np.round(J_const, 5) *1./2
    return np.matrix(G)



###test 
#G=getGraphMatrix(**args)

    