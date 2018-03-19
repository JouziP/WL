# -*- coding: utf-8 -*-

##

import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt
#import sys


## Lattice constructor
from WL.Lattices.latticeConstructor import constructLattice

from WL.collect_samplesWL import collect_samples


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


###########################  Set inputs from files:
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


E_hist_density_df   = pd.read_csv(filename+'E_hist_density_mtx.csv')
flatness_array_df   = pd.read_csv(filename+'flatness_array.csv'    )
f_factor_array_df   = pd.read_csv(filename+'f_factor_array.csv'    )
config_current_df   = pd.read_csv(filename+'config_current.csv'    )
E_current_df        = pd.read_csv(filename+'E_current.csv'         )
E_idx_current_df    = pd.read_csv(filename+'E_idx_current.csv'     )
spin_idxs_current_df= pd.read_csv(filename+'spin_idxs_current.csv' )



WL_density = E_hist_density_df.values[:, 1]
config_current = config_current_df.values[:, 0]
E_idx_current = E_idx_current_df.values[:][0,0]
E_current    = E_current_df.values[0,0]
N = args['N1'] * args['N2']
spin_idxs_current = spin_idxs_current_df.values[:,0]
args['E_marks'] = E_hist_density_df.values[:, 0]


#################################################################
################## simulation to collect samples:
#
#[
#    collected_energies, 
#   collected_configs, 
#   collected_polarizations, 
#   decimal_equivs,
##]

##
start_time = timeit.default_timer()
print 'Collection :'
#
rslts = collect_samples(WL_density, 
                config_current,
                E_idx_current,
                E_current,
                N,
                spin_idxs_current, 
                **args
                )
#(filename+'collected_energies.csv'
##
elapsed = timeit.default_timer() - start_time
print 'time elapsed: %s '%elapsed


collected_energies = rslts[0]
print 'E_min=', np.min(collected_energies), 'E_max = ',np.max(collected_energies) 
print 'collected = ', len(collected_energies)
plt.hist(collected_energies, 200)
#

#
#
collected_energies = rslts[0]
collected_configs = rslts[1]
collected_polarizations = rslts[2]

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
collected_energies_df = pd.DataFrame(np.array(collected_energies))
collected_energies_df.to_csv(filename+'collected_energies.csv', index=False)
##
collected_configs_df = pd.DataFrame(np.array(collected_configs))
collected_configs_df.to_csv(filename+'collected_configs.csv', index=False)
##
collected_polarizations_df = pd.DataFrame(np.array(collected_polarizations))
collected_polarizations_df.to_csv(filename+'collected_polarizations.csv', index=False)

