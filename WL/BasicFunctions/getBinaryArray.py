# -*- coding: utf-8 -*-

import numpy as np


def getBinaryArray(vecLen, num):
    maxNum = 2**vecLen-1
    if num<=maxNum:
        binaryVec = []
        idx=vecLen-1
        while (num >= 2):
            m= num/2
            r = num - 2*m
            binaryVec.append(int(r));
            num = m;
            idx-=1 
        binaryVec.append(int(num));
        while len(binaryVec)<vecLen:
            binaryVec.append(int(0))
        binaryVec.reverse()
        return binaryVec
    else:
        return    
    


### testing
#vecLen=12
#num = 23
#binary = getBinaryArray(vecLen, num)
