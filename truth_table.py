# A simple truth value table calculator
# Mika "AgenttiX" Mäki, 2016
# Work in progress

import numpy as np


varcount = 3

data = np.zeros((2**varcount,varcount+1))

# Implication
def imp(a, b):
    if a:
        if b:
            return True
        else:
            return False
    else:
        return True

# Generating truth values for the table
for i in range(varcount):
    data[:,i] = np.tile( np.concatenate((np.ones(2**(varcount-i-1)), np.zeros(2**(varcount-i-1)))), 2**i)

# Calculating the truth values
for i in range(2**varcount):
    tval = data[i,:]

    if( imp(tval[0], tval[1]) and imp(tval[0] and tval[1], tval[2]) and imp(tval[1] and tval[2], tval[0])):
        data[i,varcount] = 1

print(data)
