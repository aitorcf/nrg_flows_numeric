#!/usr/bin/env python3

import py_functions as pf
import numpy as np
import sys
import math as mt
import matplotlib.pyplot as plt


T = [ 1 , 5 ]
E = np.linspace( 0 , 10 , 11 )

print( E )

fig, ax = plt.subplots()
plt.style.use( 'seaborn-whitegrid' )

for t in T:
    E_weighted = np.empty( len(E) )
    E_weighted[:] = [ x * mt.exp( - x / t ) for x in E ]
    print( E_weighted )
    Z = np.sum( E_weighted )
    E_weighted = E_weighted / Z

    print( E_weighted )

    ax.plot( E , E_weighted , label='T = {}'.format( t ) )
    
plt.legend()

plt.show()



