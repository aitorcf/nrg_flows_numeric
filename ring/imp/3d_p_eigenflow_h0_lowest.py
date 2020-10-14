#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import py_functions as pf
import matplotlib.colors as mcolors


arguments = []
for arg in sys.argv[1:]:
    arguments.append(arg)

OUTNAME = 0
if len(arguments) > 0:
    OUTNAME = arguments[0] 


plt.style.use('seaborn-paper')
fig, ax = plt.subplots()
plt.grid(  b=True, which='major', color='black', linewidth='0.4' , alpha=0.3)


nrg = pf.read_h0_eigenvalues_lowest()
N = np.arange( 0 , pf.get_N( 'e-q0s2_table1.dat' ) , 2 )

ax.plot( N , nrg[:-1,0] , label='Q=0, S=1/2' )
ax.plot( N , nrg[:-1,1] , label='Q=0, S=3/2' )
ax.plot( N , nrg[:-1,2] , label='Q=1, S=0' )
ax.plot( N , nrg[:-1,3] , label='Q=1, S=1' )
ax.plot( N , nrg[:-1,4] , label='Q=2, S=1/2' )
ax.plot( N , nrg[:-1,5] , label='Q=3, S=0' )


ax.set_ylim([ -0.1 , 6.5 ])
ax.set_yticks( np.arange( 0 , 7 , 1 ) )
ax.legend(loc='upper left',frameon=True,framealpha=0.7,facecolor='white',edgecolor='white')

if OUTNAME!=0:
    plt.savefig(OUTNAME)
else:
    plt.show()
