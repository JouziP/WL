# -*- coding: utf-8 -*-
#

import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt


from WL.collect_samplesWL import collect_samples


from input_prototype import args

from WL.L2.getExpectation_energy import getExpectation_energy
from WL.L2.getExpectation_E2 import getExpectation_E2
from WL.L2.getExpectations import getExpectations
from WL.L2.getPartitionZ import getPartitionZ

###################################################################
################## Set inputs

filename1 =  'HAMILT_J_%d_E_%d_power_%d_'%(
                    args['J_const'],
                    args['E_field'],
                    args['power'],
                  )

filename2 =  'LATTICE_N1_%d_N2_%d_theta_%1.2f_nn_%s_'%(
                    args['N1'],
                    args['N2'],
                    args['theta'],
                    args['first_neighb'],
                  )
filename3 =  'MC_clusterSize_%d_'%(
                    args['max_cluster_size'],
                  )

filename4 =  'CALLIBR_f_init_%2.2f_flatness_min_%d_sub_itr_number_%d_'%(
                    args['f_factor_init'],
                    args['flatness_min'],
                    args['sub_itr_number'],
                  )

OUTPUT = './OUTPUTS/'

filename = OUTPUT + filename1 + filename2 + filename3 + filename4


collected_energies_df     = pd.read_csv(filename+'collected_energies.csv')
collected_polarizations_df= pd.read_csv(filename+'collected_polarizations.csv')



################################################################
N = args['N1']*args['N2']

energies = collected_energies_df.values[:, 0]
E_min = np.min(energies)



plt.hist(energies, 100)
########
num_temps = 100
dt = 0.25
T_0 = 0.1
Temps = [dt*i + T_0 for i in range(num_temps)]
########
#dbeta = 0.25
#Beta_0=0.01
#num_betas = 200 # T_fin = 1/(100 * 0.01) = 1
#Betas = [dbeta*i + Beta_0 for i in range(num_betas)]
#Temps = [1./beta for beta in Betas]
########
HeatC_expt=[]
energies_expt=[]
prob_max_Temps =[]
log_Z_Ts = []
S_t=[]
for Temp in Temps:
#    expt_energy = getExpectation_energy(energies, Temp)
#    expt_E2 = getExpectation_E2(energies, Temp)
#    Z_T = getPartitionZ(energies, Temp)
    expt_energy, expt_E2, Z_T =  getExpectations(energies, Temp)
#    print [Temp , expt_energy, expt_polarization]
    ############
    HeatC_expt.append((expt_E2 - expt_energy**2)*1./Temp**2) 
    energies_expt.append(expt_energy + E_min)
    log_Z_Ts.append(Z_T)  
    S = expt_energy * 1./Temp + np.log(Z_T) 
    S_t.append(S)

Temp = 10000
expt_energy_inf = getExpectation_energy(energies, Temp)
Z_T_inf = getPartitionZ(energies, Temp)
S_inf = (expt_energy_inf * 1./Temp + np.log(Z_T_inf) )* 1./N
discount_inverse = np.log(2)/S_inf

S_t = np.array(S_t)*1./N * discount_inverse

#    
fig, frame =plt.subplots(4,1, figsize=[10, 12])

frame[0].plot(Temps, np.array(HeatC_expt), '-o', label = 'Hc')
frame[0].vlines(2.63, 0, 10)
frame[1].plot(Temps, np.array(energies_expt)*1./N, '-o', label = '<E>')
frame[2].plot(Temps, S_t  , '-o', label = 'S')
frame[3].plot(Temps, np.array(log_Z_Ts)  , '-o', label = 'logZ')

frame[0].legend()
frame[1].legend()
frame[2].legend()
frame[3].legend()

    