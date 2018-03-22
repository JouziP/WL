import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt
#import sys

## Lattice constructor
from WL.Lattices.latticeConstructor import constructLattice
from WL.Lattices.latticeLinkRemover import linkRemover
from WL.Lattices.getGraphMatrix import getGraphMatrix

### 
from WL.calibrateWL_version2 import callibrateWL

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
if 'up_to_rank' in inputs:
    args['up_to_rank']=inputs['up_to_rank'][0]
args['percentage_of_links_to_be_removed']=\
        inputs['percentage_of_links_to_be_removed'][0]
#############
##### log file
log_filename =\
 'logFile_N1_%d_N2_%d_theta_%2.2f_J_const_%d_power_%d_nn_%s_inputID_%d.txt'\
             %(N1,N2, 
           theta, 
           float(inputs['J_const']),
           float(inputs['power']),
           inputs['first_neighb'][0],
           int(input_id)
           )
           

f = open(log_filename,'w')

input_log_message = 'input_id = %d \n\n'%int(input_id)
f.write(input_log_message)
### general lattice info:
f.write('--------------------\n')
lattice_log_message= 'N1 = %d, N2 = %d, theta= %2.2f, \n'%(N1, N2, theta)
f.write(lattice_log_message)
f.write('--------------------\n\n')
#############
start_time = timeit.default_timer()
f.write('building lattice :\n')
print 'building lattice :'
##
##
neighbors_table=constructLattice(**args)
args['neighbors_table']=neighbors_table
G = getGraphMatrix(**args)
args['G']=G
##
##

#neighbors_table = linkRemover(neighbors_table, **args)
elapsed = timeit.default_timer() - start_time
#############

print 'time elapsed: %s '%elapsed
f.write('time elapsed: %s \n'%elapsed)
print '------'  
f.write('----------\n')
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
##############################################################################

start_time = timeit.default_timer()
print 'calibrating :'
f.write('calibrating :\n')
f.close()
#args['lof_file']=f
##
##
parameters =callibrateWL(log_filename, **args)
##
##
elapsed = timeit.default_timer() - start_time
print 'time elapsed: %s '%elapsed
f = open(log_filename,'a')
f.write('time elapsed: %s \n'%elapsed)
#params =>> 
#[
#            E_hist_density_mtx,   0
#            f_factor,              1
#            flatness_array,       2
#            itr,                  3
#            f_factor_array,       4
#            [config_current,      5
#             E_current,
#             E_idx_current,
#             spin_idxs_current
#             ]
#]


E_hist_density_mtx = parameters[0]
for i in range(E_hist_density_mtx.shape[0]):
    print E_hist_density_mtx[i, :]

print 'E_min = ' , np.min(E_hist_density_mtx[:, 0])
f.write('E_min = %2.2f \n'%(np.min(E_hist_density_mtx[:, 0])) )
print 'E_max = ' , np.max(E_hist_density_mtx[:, 0])
f.write('E_max = %2.2f \n'%(np.max(E_hist_density_mtx[:, 0]) ) )
f.close()
#
flatness_array = parameters[2]
f_factor_array = parameters[4]
#
last_config = parameters[5]
config_current = last_config[0]
E_current  = last_config[1]
E_idx_current = last_config[2]
spin_idxs_current= last_config[3]
N  = args['N1'] * args['N2']


###########################  save on file
filename1 =  'HAMILT_J_%d_E_%d_power_%d_'%(
                    args['J_const'],
                    args['E_field'],
                    args['power'],
                  )

filename2 =  'LATTICE_N1_%d_N2_%d_theta_%1.2f_nn_%s_links_%d_K_%d_'%(
                    args['N1'],
                    args['N2'],
                    args['theta'],
                    args['first_neighb'],
                    args['percentage_of_links_to_be_removed'],
                    args['up_to_rank'],
                  )
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
#
#
E_hist_density_mtx_df = pd.DataFrame(E_hist_density_mtx)
E_hist_density_mtx_df.to_csv(filename+'E_hist_density_mtx.csv', index=False)
##
flatness_array_df = pd.DataFrame(flatness_array)
flatness_array_df.to_csv(filename+'flatness_array.csv', index=False)
##
f_factor_array_df = pd.DataFrame(f_factor_array)
f_factor_array_df.to_csv(filename+'f_factor_array.csv', index=False)
##
config_current_df = pd.DataFrame(last_config[0])
config_current_df.to_csv(filename+'config_current.csv', index=False)
##
E_current_df = pd.DataFrame([last_config[1]])
E_current_df.to_csv(filename+'E_current.csv', index=False)
##
E_idx_current_df = pd.DataFrame([last_config[2]])
E_idx_current_df.to_csv(filename+'E_idx_current.csv', index=False)
##
spin_idxs_current_df = pd.DataFrame(last_config[3])
spin_idxs_current_df.to_csv(filename+'spin_idxs_current.csv', index=False)
##

