import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt

from WL.calibrateWL_version2 import callibrateWL


from input_prototype import args

##
start_time = timeit.default_timer()
print 'calibrating :'
#
parameters =callibrateWL(**args)
##
elapsed = timeit.default_timer() - start_time
print 'time elapsed: %s '%elapsed


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
print 'E_max = ' , np.max(E_hist_density_mtx[:, 0])

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


plt.plot(f_factor_array, '-o')

###########################    



#
#
#[
#    collected_energies, 
#   collected_configs, 
#   collected_polarizations, 
#   decimal_equivs,
##]
#
#rslts = collect_samples(WL_density, 
#                config_current,
#                E_idx_current,
#                E_current,
#                N,
#                spin_idxs_current, 
#                **args
#                )
#
#collected_energies = rslts[0]
#print 'E_min=', np.min(collected_energies), 'E_max = ',np.max(collected_energies) 
#print 'collected = ', len(collected_energies)
#plt.hist(collected_energies, 200)
#

