# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt


##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
#################################


input_id = 2 #sys.argv[1]
print input_id
inputs = pd.read_csv('./INPUTS/'+'inputs_%d.csv'%input_id)


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
####
#start_time = timeit.default_timer()
#print 'building lattice :'
##neighbors_table=constructLattice(**args)
#args['neighbors_table']=neighbors_table
#elapsed = timeit.default_timer() - start_time
#print 'time elapsed: %s '%elapsed
#print '------'  
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


##########################################################################

E_hist_density_mtx = filename+'E_hist_density_mtx.csv'
collected_energies = filename+'collected_energies.csv'
HC = filename+'HeatC_expt.csv'
E_expt = filename + 'energies_expt.csv'
S = filename+ 'S_t.csv'
Z = filename + 'Z_Ts.csv'
others = filename + 'others.csv'



####
E_hist_density_mtx= pd.read_csv(E_hist_density_mtx)
collected_energies_df = pd.read_csv(collected_energies)
HC_df = pd.read_csv(HC)
S_df = pd.read_csv(S)
E_expt_df = pd.read_csv(E_expt)
others_df = pd.read_csv(others)
Z_df = pd.read_csv(Z)
#
#plt.plot(S_df.values[:,0],
#         S_df.values[:,1],
#         '-o',
#         )
#plt.vlines(2.63, 0, 6)
plt.bar(E_hist_density_mtx.values[:, 0], 
        E_hist_density_mtx.values[:, 1])



