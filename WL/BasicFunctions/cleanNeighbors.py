import numpy as np
import pandas as pd
#
def sortNeighbors(neighbs):
   neighbs_df =  pd.DataFrame(neighbs)
   neighbs_df = neighbs_df.sort_values(1, ascending=False) 
   neighbs[:,:]= neighbs_df.values[:,:]
   return neighbs

def cleanNeighbors(neighbs):
    neighbs=sortNeighbors(np.array(neighbs) )
    length=neighbs.shape[0]
    
    
    val1=round(neighbs[0, 1], 3)
    j=0
    #
    all_neighbs=[]
    while j<length:
        val=round(neighbs[j, 1], 3)
#        print j, length
        nn=[]
        q=0
            
        while val1==val:
#            print val1, val
#            print q
            nn.append(neighbs[j+q, :])    
            q+=1
            if (j+q)<length:
                val1 = round(neighbs[j+q, 1],3)
            else:
                break
        all_neighbs.append(nn)
        j=j+q
        
        
    return all_neighbs