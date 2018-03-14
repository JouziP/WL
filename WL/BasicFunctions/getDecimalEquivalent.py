# -*- coding: utf-8 -*-


####
def getDecimalEquivalent(config_current):
    equiv_decimal=0
    config_binarry = [(0, 1)[config_current[i]==-1] \
                      for i in range(len(config_current))]
    for i in range(len(config_binarry)):
        equiv_decimal +=(2**i)*config_binarry[i]
    return equiv_decimal, config_binarry