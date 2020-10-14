#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

OUTFILE=0
if len( sys.argv[1:] )!=0:
    OUTFILE = sys.argv[1]

data = np.loadtxt( 'custom' )
t = data[:,0]
n_d = data[:,6]
n_f = data[:,7]

plt.style.use( 'seaborn-paper' )
fig, ax = plt.subplots()

plt.semilogx( base=10 )
ax.set_ylim([ 0.75 , 2.1 ])
ax.set_yticks( np.arange( 0.75 , 2.0 , 0.25 ) )
ax.tick_params( right= True , labelright=False )
ax.set_xlabel( '$k_b T$' )
ax.set_ylabel( '$N$' )

ax.plot( t , n_d , color='black' , label='impurity occupation' , marker='s' , markevery=5 , markersize=5 )
ax.plot( t , n_f , color='black' , label='local band occupation' , marker='d' , markevery=5 )

ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 )

if OUTFILE==0: plt.show()
else:plt.savefig( OUTFILE )
