# -*- coding: utf-8 -*-
#
'''
last update March 19th 2018. 
'''

import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt
#import sys

from WL.Lattices.latticeConstructor import constructLattice

from WL.L2.getExpectation_energy import getExpectation_energy
from WL.L2.getExpectations import getExpectations
from WL.L2.getPartitionZ import getPartitionZ
from WL.L2.getEntropyIndirect import getIndirectEntropy
from WL.L2.getEntropy import getEntropy




##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
#################################
input_id = 0 #sys.argv[1]
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
args['percentage_of_links_to_be_removed']=inputs['percentage_of_links_to_be_removed'][0]
args['up_to_rank']=inputs['up_to_rank']
#######################
print 'lattice specs:'
print 'N1= ' , N1, 'N2= ', N2,\
     'tetha_fraction= ', inputs['tetha_fraction'][0],\
     'J= ', inputs['J_const'][0]
##
###
start_time = timeit.default_timer()
#print 'building lattice :'
#neighbors_table=constructLattice(**args)
#args['neighbors_table']=neighbors_table
elapsed = timeit.default_timer() - start_time
#print 'time elapsed: %s '%elapsed
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

filename1 =  'HAMILT_J_%2.2f_E_%d_power_%d_'%(
                    args['J_const'],
                    args['E_field'],
                    args['power'],
                  )
#filename1 =  'HAMILT_J_%d_E_%d_power_%d_'%(
#                    args['J_const'],
#                    args['E_field'],
#                    args['power'],
#                  )
#filename2 =  'LATTICE_N1_%d_N2_%d_theta_%1.2f_nn_%s_'%(
#                    args['N1'],
#                    args['N2'],
#                    args['theta'],
#                    args['first_neighb'],
##                    args['percentage_of_links_to_be_removed']
#                  )
filename2 =  'LATTICE_N1_%d_N2_%d_theta_%1.2f_nn_%s_links_%d_K_%d_'%(
                    args['N1'],
                    args['N2'],
                    args['theta'],
                    args['first_neighb'],
                    args['percentage_of_links_to_be_removed'],
                    args['up_to_rank'],
                  )
#filename2 =  'LATTICE_N1_%d_N2_%d_theta_%1.2f_nn_%s_links_%d_'%(
#                    args['N1'],
#                    args['N2'],
#                    args['theta'],
#                    args['first_neighb'],
#                    args['percentage_of_links_to_be_removed']
#                  )
filename3 =  'MC_clusterSize_%d_'%(
                    args['max_cluster_size'],
                  )

filename4 =  'CALLIBR_f_init_%2.2f_flatness_min_%d_sub_itr_number_%d_f_pcisn_%d_'%(
                    args['f_factor_init'],
                    args['flatness_min'],
                    args['sub_itr_number'],
                    args['precision_f'],
                  )

OUTPUT = './OUTPUTS/'

filename = OUTPUT + filename1 + filename2 + filename3 + filename4


E_hist_density_mtx_df     = pd.read_csv(filename+'E_hist_density_mtx.csv')

################################################################
N = args['N1']*args['N2']

energies = (E_hist_density_mtx_df.values[:, 0])/args['J_const']
unormalizaed_log_E = E_hist_density_mtx_df.values[:, 1]

scale= 1 #1./N
energies =  energies* scale
E_min = np.min(energies)


#
###########
#num_temps = 1000
#dt = 0.01*scale
#T_0 = 0.05*scale
#Temps = [dt*i + T_0 for i in range(num_temps)]
#########
#HeatC_expt=[]
#energies_expt=[]
#Z_Ts = []
#S_t=[]
########
idx_to_measure = np.where(np.min(unormalizaed_log_E)==unormalizaed_log_E)[0]
########
plt.bar(energies / scale,
        unormalizaed_log_E-unormalizaed_log_E[idx_to_measure])
#########
#
#for Temp in Temps:
#    ### expectations = <E-E_min>, <(E-E_min)**2>, ... = < >_c
#    expt_energy, expt_E2, Z_T =  getExpectations(energies, 
#                                                 unormalizaed_log_E, 
#                                                 Temp, 
#                                                 idx_to_measure)
#    S = getEntropy(unormalizaed_log_E, energies, Temp, N, expt_energy+E_min)
##    ############
#    HeatC_expt.append((expt_E2 - expt_energy**2)*1./Temp**2) 
#    energies_expt.append(expt_energy + E_min)
#    S_t.append(S)
#
#print 'Residual Entropy = ', S_t[0]
#    
#fig, frame =plt.subplots(1,1, figsize=[8,5])
###
##frame[0].plot(np.array(Temps)/scale, np.array(HeatC_expt), '-o', label = 'Hc')
##frame[0].vlines(2.27,0, 2*N)
##frame[1].plot(np.array(Temps)/scale, np.array(energies_expt), '-o', label = '<E>')
#frame.plot(np.array(Temps)/scale, S_t  , '-o', label = 'S, N1=%d , N2=%d'%(N1, N2))
###frame[3].plot(Temps, np.array(log_Z_Ts)  , '-o', label = 'logZ')
###
#frame.legend(loc='lower right')
##frame[1].legend()
##frame[2].legend()
#
#fig.savefig(OUTPUT+'N1_%d_N2_%d.jpg'%(N1, N2), format='jpg', dpi=100)
#
###frame[3].legend()
##
################################################################################
################################################################################
#####################################################################
#################### save outputs
##
##filename1 =  'HAMILT_J_%d_E_%d_power_%d_'%(
##                    args['J_const'],
##                    args['E_field'],
##                    args['power'],
##                  )
##filename2 =  'LATTICE_N1_%d_N2_%d_theta_%1.2f_nn_%s_links_%d'%(
##                    args['N1'],
##                    args['N2'],
##                    args['theta'],
##                    args['first_neighb'],
##                    args['percentage_of_links_to_be_removed']
##                  )
##filename3 =  'MC_clusterSize_%d_'%(
##                    args['max_cluster_size'],
##                  )
##
##filename4 =  'CALLIBR_f_init_%2.2f_flatness_min_%d_sub_itr_number_%d_f_pcisn_%d_'%(
##                    args['f_factor_init'],
##                    args['flatness_min'],
##                    args['sub_itr_number'],
##                    args['precision_f'],
##                  )
##
##OUTPUT = './OUTPUTS/'
##
##filename = OUTPUT + filename1 + filename2 + filename3 + filename4
##
##
##
###
##HeatC_expt_df = pd.DataFrame(np.array(HeatC_expt))
##HeatC_expt_df.index=Temps
##HeatC_expt_df.to_csv(filename+'HeatC_expt.csv')
##
####
##energies_expt_df = pd.DataFrame(np.array(energies_expt))
##energies_expt_df.index=Temps
##energies_expt_df.to_csv(filename+'energies_expt.csv')
####
##S_t_df = pd.DataFrame(np.array(S_t))
##S_t_df.index=Temps
##S_t_df.to_csv(filename+'S_t.csv')
####
##Z_Ts_df = pd.DataFrame(np.array(Z_Ts))
##Z_Ts_df.index=Temps
##Z_Ts_df.to_csv(filename+'Z_Ts.csv')
##
##others= {
##        'Temp_inf':Temp,
##        'expt_energy_inf':expt_energy_inf,
##        'Z_T_inf':Z_T_inf,
##        'S_inf':S_inf,
##        'discount_factor':1./(discount_inverse),        
##        }
##
##others_df = pd.DataFrame.from_dict(others, orient='index')
##others_df.to_csv(filename+'others.csv')
