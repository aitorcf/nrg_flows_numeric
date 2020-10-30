#!/usr/bin/env python3

import sys
import py_functions as pf
import matplotlib.pyplot as plt
import numpy as np
import math as mt

U = pf.get_param( 'param' , 'U' )
G = pf.get_param( 'param' , 'Gamma' )

plt.style.use( 'seaborn-paper' )
fig = plt.figure()

ax1 = fig.add_axes( [0.2, 0.55, 0.55, 0.45] )
pf.plot_mag_susc( ax1 , colour='tab:purple' , llabel=f"$U={U}$, $\Gamma={G}$" )
ax1.set_xticklabels([])
ax1.set_yticks( np.arange( 0 , 1 , 0.25 ) )

ax2 = fig.add_axes( [0.2, 0.15, 0.55, 0.40] )
pf.plot_entropy( ax2 , colour='tab:orange' )
ax2.set_yticks( np.arange( 0 , 4 , 1 ) )
ax2.set_xticks( np.exp( np.arange( -20 , 1 , 4 ) ) )
ax2.semilogx()

ax1.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 , fontsize=15 )

plt.show()
