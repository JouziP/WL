# -*- coding: utf-8 -*-


import numpy as np

def getEnergyOfConfig(sampleSpinConfig, **args):
    neighbors_table=args['neighbors_table']
    J_const =args['J_const']
    E_field =args['E_field']
    energy_total=0
#    print sampleSpinConfig.shape
    for spin_idx in range(len(sampleSpinConfig)):
        spin_neighbors=neighbors_table[spin_idx]
        ####### energy of the spin:
        S = sampleSpinConfig[spin_idx]
        spin_energy = E_field*S
        for n in range(spin_neighbors.shape[0]):
            neighb_idx=spin_neighbors[n,  0]
            strength  = spin_neighbors[n, 1]   
            S_n = sampleSpinConfig[int(neighb_idx)]
#            print S_n
            spin_energy += (J_const*(strength)) * (S*S_n)
#        print spin_energy
            
        energy_total+=spin_energy
    energy_total=energy_total/float(2)
    return energy_total
            
            
        
#    
#   ##### test
#from DOS.FunctionsLayer1.Lattices.latticeConstructor import constructLattice
#from DOS.BasicFunctions.getBinaryArray import getBinaryArray
#N1=2
#N2=2
#np.random.seed(1251)
#args={}
#args['J_const']=1.0
#args['E_field']=0.0
#args['power']=3.0
#args['a1_x']=1.0
#args['a1_y']=0.0
##
#args['a2_x']=0.0
#args['a2_y']=1.0
#
#args['N1'] = N1
#args['N2'] = N2
#args['N_spins']=N1*N2
#args['first_neighb']=True
#neighbors_tables_list = constructLattice(**args)
#neighbors_table=constructLattice(**args)
#args['neighbors_table']=neighbors_table
#
#for i in range(2**(N1*N2)):
#    config=getBinaryArray(N1*N2, i)    
#    config = [(-1)**config[i] for i in range(len(config))]
#    E = getEnergyOfConfig(config, **args)
#    print config, E