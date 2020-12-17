# A simple truth value table calculator
# Mika "AgenttiX" Mäki, 2016
# Work in progress

import numpy as np


var_count = 3

data = np.zeros((2 ** var_count, var_count + 1))


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
for i in range(var_count):
    data[:, i] = np.tile(
        np.concatenate((np.ones(2 ** (var_count - i - 1)), np.zeros(2 ** (var_count - i - 1)))),
        2**i
    )

# Calculating the truth values
for i in range(2 ** var_count):
    tval = data[i, :]

    if imp(tval[0], tval[1]) and imp(tval[0] and tval[1], tval[2]) and imp(tval[1] and tval[2], tval[0]):
        data[i, var_count] = 1

print(data)
