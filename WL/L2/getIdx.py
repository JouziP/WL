# -*- coding: utf-8 -*-

import numpy as np

def getIdx(E_new, E_marks):
    min_dist  = np.abs(E_marks[0]- E_new)
    idx = 0
    for i in range(1, len(E_marks)):
        if np.abs(E_marks[i]- E_new)<min_dist:
            min_dist = np.abs(E_marks[i]- E_new)
            idx = i
    return idx