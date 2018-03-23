# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt
#import sys

## Lattice constructor
from WL.Lattices.latticeConstructor import constructLattice
from WL.Lattices.getGraphMatrix import getGraphMatrix
##
from WL.L2.getExpectations import getExpectations
from WL.L2.getEntropy import getEntropy
from WL.getDOS import getDOS
### 
from WL.calibrateWL_version2 import callibrateWL
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
#E_step = sys.argv[2] ### first input
#dE     = sys.argv[3] ### second input
##  etc.
SEED = 1021
############ Hamilt
J_const = 1
#E_field = float(E_step) * float(dE)
E_field = 0.0*J_const
E_field_type = 'random'
power = 3
##########  lattice
N1= 4
N2= 4
N = N1*N2
a1_x= 1 
a1_y=0
theta=np.pi/3
a2_x=np.cos(theta)
a2_y=np.sin(theta)
first_neighb = False
percentage_of_links_to_be_removed = 0
up_to_rank = 1
##########  MC
max_cluster_size = 1
########## callibration:
f_factor_init = 2.7182818285  ##f_factor= np.exp(log_f) ##log_f = 1
precision_f = 4 ##precision_f = 4
precision_E = 0 ##precision_E = 2
flatness_min = 90 ##flatness_min = 90
sub_itr_number  = 5000 ### sub itr  ##sub_itr_number = 5000
num_steps_in_one_level_random_walk = 1000 ##num_steps_in_one_level_random_walk=1000
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
#################################
np.random.seed(SEED)
args={}
############ Hamilt
args['J_const']= J_const
args['E_field']= E_field
args['E_field_type']=E_field_type
args['power']= power
##########  lattice
args['theta'] = theta
args['a1_x']=a1_x
args['a1_y']=a1_y
args['a2_x']=a2_x
args['a2_y']=a2_y
args['N1'] = N1
args['N2'] = N2
args['N_spins']=N1*N2
args['first_neighb']=first_neighb
args['percentage_of_links_to_be_removed']=percentage_of_links_to_be_removed
args['up_to_rank']=up_to_rank
#######################
############ MC specs
args['max_cluster_size'] = max_cluster_size
############ callibration:
args['f_factor_init']=f_factor_init
args['precision_f']=precision_f
args['precision_E'] = precision_E
args['flatness_min'] = flatness_min
args['sub_itr_number'] = sub_itr_number
args['num_steps_in_one_level_random_walk'] =  num_steps_in_one_level_random_walk
###################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###################################################################
##### log file
log_filename =\
 'logFile_N1_%d_N2_%d_theta_%2.2f_J_const_%2.5f_power_%d_nn_%s.txt'\
             %(N1,N2, 
           theta, 
           float(J_const),
           float(power),
           first_neighb,
           )
f = open(log_filename,'w')
################################################# lattice:
start_time = timeit.default_timer()
f.write('building lattice :\n')
print 'building lattice :'
##
neighbors_table=constructLattice(**args)
args['neighbors_table']=neighbors_table
args['depth']=N
G = getGraphMatrix(**args)
args['G']=G
##
#neighbors_table = linkRemover(neighbors_table, **args)
elapsed = timeit.default_timer() - start_time
################################################ find parameters:
start_time = timeit.default_timer()
print 'calibrating :'
f.write('calibrating :\n')
f.close()
##
parameters =callibrateWL(log_filename, **args)
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
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
################################## OUTPUTS

#OUTPUT = sys.argv[1]
OUTPUT = './OUTPUTS/'
###########################  save on file
filename1 =  'HAMILT_J_%2.2f_E_%2.2f_E_type_%s_power_%d_'%(
                    args['J_const'],
                    args['E_field'],
                    args['E_field_type'],
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

filename = OUTPUT+filename1 + filename2 + filename3 + filename4
#
#print filename
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
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
################################## Expectations

E_hist_density_mtx_df = pd.read_csv(filename+'E_hist_density_mtx.csv')

energies = (E_hist_density_mtx_df.values[:, 0])/args['J_const']
unormalizaed_log_E = E_hist_density_mtx_df.values[:, 1]
dos=getDOS(unormalizaed_log_E, N)

scale= 1 #1./N
energies =  energies* scale
E_min = np.min(energies)


#
###########
num_temps = 1000
dt = 0.01*scale
T_0 = 0.1*scale
Temps = [dt*i + T_0 for i in range(num_temps)]
#########
HeatC_expt=[]
energies_expt=[]
Z_Ts = []
S_t=[]
########
idx_to_measure = np.where(np.min(unormalizaed_log_E)==unormalizaed_log_E)[0]
#######
plt.bar(energies / scale, dos)
#########

for Temp in Temps:
    ### expectations = <E-E_min>, <(E-E_min)**2>, ... = < >_c
    expt_energy, expt_E2, Z_T =  getExpectations(energies, 
                                                 dos, 
                                                 Temp
                                                 )
    S = getEntropy(unormalizaed_log_E, energies, Temp, N, expt_energy+E_min)
##    ############
    HeatC_expt.append((expt_E2 - expt_energy**2)*1./Temp**2) 
    energies_expt.append(expt_energy + E_min)
    S_t.append(S)
#
print 'Residual Entropy = ', S_t[0]
#    
fig, frame =plt.subplots(1,1, figsize=[8,5])
#
#frame[0].plot(np.array(Temps)/scale, np.array(HeatC_expt), '-o', label = 'Hc')
#frame[0].vlines(2.27,0, 2*N)
#frame[1].plot(np.array(Temps)/scale, np.array(energies_expt), '-o', label = '<E>')
frame.plot(np.array(Temps)/scale, S_t  , '-o', label = 'S, N1=%d , N2=%d'%(N1, N2))
#frame[3].plot(Temps, np.array(log_Z_Ts)  , '-o', label = 'logZ')
#
frame.legend(loc='lower right')
#frame[1].legend()
#frame[2].legend()

#fig.savefig(OUTPUT+'N1_%d_N2_%d.jpg'%(N1, N2), format='jpg', dpi=100)


HeatC_expt_df = pd.DataFrame(np.array(HeatC_expt))
HeatC_expt_df.index=Temps
HeatC_expt_df.to_csv(filename+'HeatC_expt.csv')

###
energies_expt_df = pd.DataFrame(np.array(energies_expt))
energies_expt_df.index=Temps
energies_expt_df.to_csv(filename+'energies_expt.csv')
###
S_t_df = pd.DataFrame(np.array(S_t))
S_t_df.index=Temps
S_t_df.to_csv(filename+'S_t.csv')
#####
###
dos_df = pd.DataFrame(np.array(dos))
dos_df.index=energies / scale
dos_df.to_csv(filename+'dos.csv')
#####












