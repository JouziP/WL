# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

from WL.Lattices.latticeConstructor import constructLattice
from WL.BasicFunctions.getBinaryArray import getBinaryArray
from WL.L1.getEnergyOfSpinConfig import getEnergyOfConfig   



N1=3
N2=3
#np.random.seed(1251)
args={}
args['J_const']=1.0
args['E_field']=0.0
args['power']=3.0
##########
a1_x= 1.0
a1_y= 0
theta=np.pi/3
a2_x=np.cos(theta)
a2_y=np.sin(theta)
#
args['a1_x']=a1_x
args['a1_y']=a1_y
args['a2_x']=a2_x
args['a2_y']=a2_y
#########
#
args['N1'] = N1
args['N2'] = N2
args['N_spins']=N1*N2
args['first_neighb']=True
neighbors_tables_list = constructLattice(**args)
neighbors_table=constructLattice(**args)
args['neighbors_table']=neighbors_table

E_s = []
for i in range(2**(N1*N2)):
    config=getBinaryArray(N1*N2, i)    
    config = [(-1)**config[i] for i in range(len(config))]
    E = getEnergyOfConfig(config, **args)
    E_s.append(E)
#    print config, E
print np.min(E_s), np.max(E_s)
plt.hist(E_s, 100)




#### 4 * 4 ===> -21.1949051216 48.5294289008