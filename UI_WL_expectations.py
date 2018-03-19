# -*- coding: utf-8 -*-
#

import numpy as np
import pandas as pd
import timeit
#import matplotlib.pyplot as plt
#import sys

from WL.Lattices.latticeConstructor import constructLattice

from WL.L2.getExpectation_energy import getExpectation_energy
from WL.L2.getExpectations import getExpectations
from WL.L2.getPartitionZ import getPartitionZ





##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
#################################
input_id = 1 #sys.argv[1]
print input_id



filename = 'inputs_%d.csv'%int(input_id)
INPUTS = './INPUTS/'
inputs = pd.read_csv(INPUTS+filename)

#
np.random.seed(1051)
#
#
args={}
############ Hamilt
args['J_const']= float(inputs['J_const'])   #-1.0
args['E_field']= float(inputs['E_field'])   #0.0
args['power']= float(inputs['power'])     #3.0
##########  lattice
N1=int(inputs['N1'])
N2=int(inputs['N2'])
### 
a1_x= float(inputs['a1_x'])
a1_y= float(inputs['a1_y'])
theta=np.pi/float(inputs['tetha_fraction'])
a2_x=np.cos(theta)
a2_y=np.sin(theta)
###
args['theta'] = theta
args['a1_x']=a1_x
args['a1_y']=a1_y
args['a2_x']=a2_x
args['a2_y']=a2_y
args['N1'] = N1
args['N2'] = N2
args['N_spins']=N1*N2
args['first_neighb']=inputs['first_neighb'][0]
##
##
###
start_time = timeit.default_timer()
print 'building lattice :'
neighbors_table=constructLattice(**args)
args['neighbors_table']=neighbors_table
elapsed = timeit.default_timer() - start_time
print 'time elapsed: %s '%elapsed
print '------'  
############ MC specs
args['max_cluster_size'] = int(inputs['max_cluster_size']) #1
############ callibration:
###
##log_f = 1
##f_factor= np.exp(log_f)
args['f_factor_init']=float(inputs['f_factor_init'])
##
##precision_f = 4
args['precision_f']=int(inputs['precision_f'] )#precision_f
##
##precision_E = 2
args['precision_E'] = int(inputs['precision_E'] ) #precision_E
## in %
##flatness_min = 90
args['flatness_min'] = int(inputs['flatness_min']) #flatness_min
### sub itr 
##sub_itr_number = 5000
args['sub_itr_number'] = int(inputs['sub_itr_number'])  #sub_itr_number
### max number of attempt to iterate:
##num_steps_in_one_level_random_walk=1000
args['num_steps_in_one_level_random_walk'] =  int(inputs['num_steps_in_one_level_random_walk'] ) # num_steps_in_one_level_random_walk
###################
###################
############ collection of samples:
###N_collection = 100
args['N_collection'] = int(inputs['N_collection']) # N_collection
N_collection_attempts  = int(inputs['N_collection_tollerance_factor']) * args['N_collection'] #N_collection
args['N_collection_attempts'] = N_collection_attempts
#
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
#





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



#plt.hist(energies, 100)
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
Z_Ts = []
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
    Z_Ts.append(Z_T)  
    S = expt_energy * 1./Temp + np.log(Z_T) 
    S_t.append(S)

Temp = 10000
expt_energy_inf = getExpectation_energy(energies, Temp)
Z_T_inf = getPartitionZ(energies, Temp)
S_inf = (expt_energy_inf * 1./Temp + np.log(Z_T_inf) )* 1./N
discount_inverse = np.log(2)/S_inf

S_t = np.array(S_t)*1./N * discount_inverse

##    
#fig, frame =plt.subplots(4,1, figsize=[10, 12])
#
#frame[0].plot(Temps, np.array(HeatC_expt), '-o', label = 'Hc')
#frame[0].vlines(2.63, 0, 10)
#frame[1].plot(Temps, np.array(energies_expt)*1./N, '-o', label = '<E>')
#frame[2].plot(Temps, S_t  , '-o', label = 'S')
#frame[3].plot(Temps, np.array(log_Z_Ts)  , '-o', label = 'logZ')
#
#frame[0].legend()
#frame[1].legend()
#frame[2].legend()
#frame[3].legend()

##############################################################################
##############################################################################
###################################################################
################## save outputs

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



#
HeatC_expt_df = pd.DataFrame(np.array(HeatC_expt))
HeatC_expt_df.index=Temps
HeatC_expt_df.to_csv(filename+'HeatC_expt.csv')

##
energies_expt_df = pd.DataFrame(np.array(energies_expt))
energies_expt_df.index=Temps
energies_expt_df.to_csv(filename+'energies_expt.csv')
##
S_t_df = pd.DataFrame(np.array(S_t))
S_t_df.index=Temps
S_t_df.to_csv(filename+'S_t.csv')
##
Z_Ts_df = pd.DataFrame(np.array(Z_Ts))
Z_Ts_df.index=Temps
Z_Ts_df.to_csv(filename+'Z_Ts.csv')

others= {
        'Temp_inf':Temp,
        'expt_energy_inf':expt_energy_inf,
        'Z_T_inf':Z_T_inf,
        'S_inf':S_inf,
        'discount_factor':1./(discount_inverse),        
        }

others_df = pd.DataFrame.from_dict(others, orient='index')
others_df.to_csv(filename+'others.csv')
