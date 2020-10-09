#!/usr/bin/env python3

import py_functions as pf
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import subprocess
import sys
import numpy as np
from matplotlib.lines import Line2D

arguments = []
for arg in sys.argv[1:]:
    arguments.append(arg)
OUTFILE = 0
if len( arguments )>0:
    OUTFILE = arguments[0]


UG_0 = np.array([2.3,4e-2])
UG_1 = np.array([1e-1,0.0])
UG_2 = np.array([1e-2,3e-4])
UG_3 = np.array([1e-2,1e-3])
UG_4 = np.array([1e-2,2e-3])
UG_5 = np.array([1e-2,5e-3])
UG_6 = np.array([0.0,1e-2])

UG = [ [0.01,0] , [0.01,2e-4] , [0.01,2e-3] , [2e-4,0.01] , [0,0.01] ]


Lambda = pf.get_lambda( 'param' )

plt.style.use( 'seaborn-paper' )
fig = plt.figure()
ax = fig.add_axes([ 0.15 , 0.15 , 0.8 , 0.75 ])


colours = list( mcolors.TABLEAU_COLORS.values() )
i = 0
for pair, colour in zip( UG , colours ):
    pf.write_param( U=pair[0] , Gamma=pair[1] )

    subprocess.call( './1c_run_flow' )

    pf.plot_arrow_diagram( ax , colour=colour , fixedpoints=False )
    
    xtest = [11110,11111]
    ytest = [111110,111111]
    if pair[0]==0:
        ax.plot( xtest , ytest , color=colour , label='$U=0$, $\Gamma={:.1e}$'.format(pair[1]) ) 
    elif pair[1]==0:
        ax.plot( xtest , ytest , color=colour , label='$U={:.1e}$, $\Gamma=0$'.format(pair[0]) )
    else:
        ax.plot( xtest , ytest , color=colour , label='$U={:.1e}$, $\Gamma={:.1e}$'.format(pair[0],pair[1]) )

pf.include_fixedpoints( ax )

ax.tick_params( labelsize=15 )
ax.legend( loc='upper right' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 , ncol=1 , fontsize=13 )


if OUTFILE!=0:
    plt.savefig("/graphs_and_data/arrowplots_multiple/{}".format(OUTFILE))
else:
    plt.show()
