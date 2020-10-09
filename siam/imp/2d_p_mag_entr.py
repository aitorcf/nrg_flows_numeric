#!/usr/bin/env python3

import sys
import py_functions as pf
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


arguments=[]
for arg in sys.argv[1:]:
    arguments.append( arg )
OUTNAME = 0
if len(arguments)>=1:
    OUTNAME = arguments[0]


plt.style.use( 'seaborn-paper' )
fig = plt.figure()

#colour = list( mcolors.TABLEAU_COLORS.values() )[0]
colour = 'black'

ax1 = fig.add_axes( [0.2, 0.55, 0.6, 0.43] )
pf.plot_mag_susc_2( ax1 , colour=colour , llabel=f'$U = {pf.get_u_gamma()[0]}$, $\Gamma = {pf.get_u_gamma()[1]}$' )
ax1.set_xticklabels([])
ax1.tick_params( axis='both' , which='major' , labelsize=15 )

ax2 = fig.add_axes( [0.2, 0.2, 0.6, 0.35] )
pf.plot_entropy_2( ax2 , colour=colour )
plt.xticks( fontsize=15 )
plt.yticks( fontsize=15 )
ax2.tick_params( axis='both' , which='major' , labelsize=15 )

ax1.legend( loc='upper left' , frameon=True , framealpha=0.7 , facecolor='white' , edgecolor='white' , fontsize=15 )


if OUTNAME!=0:
    plt.savefig( OUTNAME )
else:
    plt.show()
