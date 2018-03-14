# -*- coding: utf-8 -*-


import numpy as np


def shuffleIndxs(indxs_current,
                 N
                 ):
    _num_shuffling = 10
    for _n in range(_num_shuffling):
        idx_1 = np.random.randint(N)
        idx_2 = np.random.randint(N)
        tmp = indxs_current[idx_1]
        indxs_current[idx_1] =indxs_current[idx_2]
        indxs_current[idx_2]=tmp
    return indxs_current
        
    


##### test
#N = 10
#indxs_current = [i for i in range(N)]
#print indxs_current
#indxs_new = shuffleIndxs(indxs_current, N)
#print indxs_new