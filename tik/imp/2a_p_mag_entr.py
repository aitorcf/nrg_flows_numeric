#!/usr/bin/env python3

import sys
import py_functions as pf
import matplotlib.pyplot as plt
import numpy as np
import math as mt

J1 = pf.get_param( 'param' , 'Jkondo1' )
J2 = pf.get_param( 'param' , 'Jkondo2' )
Jad = pf.get_param( 'param' , 'Jad' )


plt.style.use( 'seaborn-paper' )
fig = plt.figure()

ax1 = fig.add_axes( [0.2, 0.55, 0.55, 0.45] )
pf.plot_mag_susc( ax1 , colour='tab:purple' , llabel="$J_1={}$, $J_2={}$, $Jad={}$".format( J1 , J2 , Jad ) )
ax1.set_xticklabels([])
ax1.set_yticks( np.arange( 0 , 1 , 0.25 ) )

ax2 = fig.add_axes( [0.2, 0.15, 0.55, 0.40] )
pf.plot_entropy( ax2 , colour='tab:orange' )
ax2.set_xticks( np.exp( np.arange( -20 , 1 , 4 ) ) )
ax2.semilogx()

ax1.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 , fontsize=15 )

plt.show()
