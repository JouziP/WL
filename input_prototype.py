
import timeit
import numpy as np

from WL.Lattices.latticeConstructor import constructLattice



np.random.seed(1051)


args={}
########### Hamilt
args['J_const']=-1.0
args['E_field']=0.0
args['power']=3.0
#########  lattice
N1=3
N2=3
## 
a1_x= 1.0
a1_y= 0
theta=np.pi/2
a2_x=np.cos(theta)
a2_y=np.sin(theta)
##
args['theta'] = theta
args['a1_x']=a1_x
args['a1_y']=a1_y
args['a2_x']=a2_x
args['a2_y']=a2_y
args['N1'] = N1
args['N2'] = N2
args['N_spins']=N1*N2
args['first_neighb']=True
#
#
##
start_time = timeit.default_timer()
print 'building lattice :'
neighbors_table=constructLattice(**args)
args['neighbors_table']=neighbors_table
elapsed = timeit.default_timer() - start_time
print 'time elapsed: %s '%elapsed
print '------'  
########### MC specs
args['max_cluster_size'] = 1
########### callibration:
##
log_f = 1
f_factor= np.exp(log_f)
args['f_factor_init']=f_factor
#
precision_f = 4
args['precision_f']=precision_f
#
precision_E = 2
args['precision_E'] = precision_E
# in %
flatness_min = 90
args['flatness_min'] =flatness_min
## sub itr 
sub_itr_number = 5000
args['sub_itr_number'] = sub_itr_number
## max number of attempt to iterate:
num_steps_in_one_level_random_walk=1000
args['num_steps_in_one_level_random_walk'] =num_steps_in_one_level_random_walk
##############################################################################
##############################################################################
########### collection of samples:
N_collection = 100
args['N_collection'] = N_collection
N_collection_attempts  = 30 * N_collection
args['N_collection_attempts'] = N_collection_attempts



