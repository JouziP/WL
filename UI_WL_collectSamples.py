# -*- coding: utf-8 -*-

##

import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt


from WL.collect_samplesWL import collect_samples


from input_prototype import args





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

