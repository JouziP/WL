# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

def sortNeighbors(neighbs):
   neighbs_df =  pd.DataFrame(neighbs)
   neighbs_df = neighbs_df.sort_values(1, ascending=False) 
   neighbs[:,:]= neighbs_df.values[:,:]
   return neighbs



def rankNeighbs(neighbs):
    #####################################
#    print neighbs
    neighbs = sortNeighbors(np.array(neighbs) )
    #################################################
    
    length_neighbs = neighbs.shape[0]
    neighbs_by_rank=[]
    idx=0 
    k=0
    while idx<length_neighbs:
        strength = neighbs[idx, 1]
        nghbs=[]
        while idx<length_neighbs and\
                np.round(neighbs[idx, 1], 5) == np.round(strength, 5):
            nghbs.append(neighbs[idx, :])
            idx+=1
            
        neighbs_by_rank.append(np.array(nghbs))
        k+=1
    return neighbs_by_rank
        
def getUpToRankNeighbs(up_to_rank, neighbs):
    neighbs_by_rank= rankNeighbs(neighbs)
    neighbs_up_to_rank = []
    ################
    if up_to_rank>=len(neighbs_by_rank):
        up_to_rank = len(neighbs_by_rank)
    ################        
    for k in range(up_to_rank):
        for i in range(neighbs_by_rank[k].shape[0]):
            neighbs_up_to_rank.append(neighbs_by_rank[k][i, :])
    return np.array(neighbs_up_to_rank)
    
    
    
    