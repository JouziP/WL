# -*- coding: utf-8 -*-


import numpy as np


def getRandomConfig(N):
    return [int((-1)**(np.random.randint(2))) for i in range(N)]
    




####test
#N=10
#P_array = getRandomConfig(N)
#print P_array