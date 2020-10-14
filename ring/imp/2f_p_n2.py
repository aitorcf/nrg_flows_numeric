#!/usr/bin/env python3

import sys
import py_functions as pf
import matplotlib.pyplot as plt
import numpy as np


arguments=[]
for arg in sys.argv[1:]:
    arguments.append( arg )
OUTNAME = 0
if len(arguments)>=1:
    OUTNAME = arguments[0]


plt.style.use( 'seaborn-paper' )
fig, ax = plt.subplots()

ax.semilogx( base=10 )

data = np.loadtxt( 'custom' )
ax.plot( data[:,0] , data[:,1] )


if OUTNAME!=0:
    plt.savefig( OUTNAME )
else:
    plt.show()
