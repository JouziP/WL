# -*- coding: utf-8 -*-

import numpy as np

def check_flatness(E_hist_density):
    n_expt = np.average(E_hist_density[:, 2])
    numE_min = np.min(E_hist_density[:, 2])
    return numE_min*1./n_expt*100
    ####