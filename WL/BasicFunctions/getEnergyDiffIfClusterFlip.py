# -*- coding: utf-8 -*-


import numpy as np


def getEnergyDiffIfClusterFlip(cluster, 
                               config_current, 
                                **args):
    neighbors_table=args['neighbors_table']
    J_const = args['J_const']
    E_field = args['E_field']
    dE=0
    for node in cluster:
        node_neighbs_table = neighbors_table[int(node)]
#        print node, node_neighbs_table
        S_node = config_current[int(node)]
        #### 
        dE+=E_field*S_node
        ####
        for row in range(len(node_neighbs_table[:, 0])):
            neighb_2_node=node_neighbs_table[row, 0]
            strength = node_neighbs_table[row, 1]
            if int(neighb_2_node) not in cluster:
                S_neighb_2_node = config_current[int(neighb_2_node)]
                dE +=  J_const * S_neighb_2_node*S_node*strength
    energy_2b_added_if_cluster_is_flipped = -2*dE
    ###
    return energy_2b_added_if_cluster_is_flipped
                


##### test 
###### test
#from DOS.FunctionsLayer1.Lattices.latticeConstructor import constructLattice
#N1=4
#N2=4
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
#args['first_neighb']=False
#neighbors_tables_list = constructLattice(**args)
#neighbors_table=constructLattice(**args)
#args['neighbors_table']=neighbors_table
#
#from DOS.BasicFunctions.getRandomConfig import getRandomConfig
#from DOS.BasicFunctions.shuffleIndxs import shuffleIndxs
#from DOS.FunctionsLayer1.getEnergyOfSpinConfig import getEnergyOfConfig
#
#N = N1 * N2
#config_current = getRandomConfig(N)
#indxs_current = [i for i in range(N)]
#indxs_new = shuffleIndxs(indxs_current, N)
#cluster = indxs_new[:1]
#print config_current
#print cluster
#E_current =getEnergyOfConfig(config_current, **args)
#print E_current
#for i in range(100):
#    dE =  getEnergyDiffIfClusterFlip(cluster, 
#                               config_current, 
#                                **args)
#    new_config = config_current
#    for i in cluster: 
#        new_config[i] = new_config[i]*-1
#    #print new_config
#    E_exact=getEnergyOfConfig(config_current, **args)
#    print np.round(E_current+ dE, 5)==np.round(E_exact,5)
#    E_current = E_current + dE
#    indxs_new = shuffleIndxs(indxs_current, N)
#    cluster = indxs_new[:1]

