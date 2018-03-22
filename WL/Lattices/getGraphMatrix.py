# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from numpy import linalg as lg

def getGraphMatrix(**args):
    neighbors_table = args['neighbors_table']
    N1 = args['N1']
    N2 = args['N2']
    depth = args['depth']
    N = N1 *N2 
    G = np.zeros([N, N])
    J_const = args['J_const']
    for i in range(N):
        neighbs= neighbors_table[i]
        for n in range(neighbs.shape[0]):
            j = int(neighbs[n, 0])
            G[i, j] = np.round(neighbs[n, 1], 5) * np.round(J_const, 5) *1./2
            
    G = np.matrix(G)
    G = getReducedG(G, depth)
    return G



def getReducedG(G, depth):
    U,D, V = lg.svd(G)

    D_df = np.zeros([len(D), 2])
    D_df[:, 1]=D[:]
    D_df[:, 0]= np.array([int(i) for i in range(len(D)) ])[:]
    D_df = pd.DataFrame(D_df)
    D_df = D_df.sort_values(by=1, ascending=False)
    indexs=np.array(D_df.values[:depth, 0], dtype=int)
    V_reduced = V[indexs, :]
    U_reduced = U[:, indexs]
    D_reduced = np.zeros([len(indexs), len(indexs)])
    for i in range(len(indexs)) : D_reduced[i,i]=D[indexs[i]]
    ##################
    for q in range(V_reduced.shape[0]):
        V_reduced[q, :]=V_reduced[q, :] * D_reduced[q,q]
        
    G_reduced = np.dot(U_reduced, V_reduced)
    
    return U_reduced, V_reduced, G_reduced



###test 
#G=getGraphMatrix(**args)



