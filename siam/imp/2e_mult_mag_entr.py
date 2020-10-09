#!/usr/bin/env python3

import numpy as np
import py_functions as pf
import sys
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from matplotlib.lines import Line2D
import os
import subprocess
import math as mt

arguments = []
for arg in sys.argv[1:]:
    arguments.append(arg)

OUTFILE = 0
if np.size(arguments)>0:
    OUTFILE = arguments[0]


UG = [ np.array(elem) for elem in [ [0.01,2e-4] , [0.01,2e-3] , [2e-4,0.01] ] ]

plt.style.use('seaborn-paper')
fig = plt.figure()
ax_mag = fig.add_axes( [0.2, 0.5, 0.6, 0.48] )
ax_entr = fig.add_axes( [0.2, 0.2, 0.6, 0.30] )

linestyles = [ '-' , '--' , 'dotted' ] 

colours = mcolors.TABLEAU_COLORS
i = 0
for pair, colour , lin in zip( UG , list( colours.keys() )[1:] , linestyles ):
    param = open('param','r')
    new_param = open('new_param','w+')
    for line in param:
        if line=="" or line=="\n":
            new_param.write("\n")
        else:
            if line[0]=='U':
                new_param.write("U={}\n".format(pair[0]))
            elif line[:5]=='Gamma':
                new_param.write('Gamma={}\n'.format(pair[1]))
            else:
                new_param.write(line)
    param.close()
    new_param.close()
    subprocess.call([ 'mv' , 'new_param' , 'param' ])
    subprocess.call( './1e_run_th_fl' )
    
    N = pf.get_N( 'e-q0s1_table1.dat' )
   
    col = colours[colour]

    pf.plot_mag_susc_2( ax_mag , colour=col , llabel='$U = {:3.0e}$ , $\Gamma = {:3.0e}$'.format(pair[0],pair[1]) , llinestyle=lin ,
            labels=False )
    ax_mag.tick_params( labelsize=15 )
    ax_mag.set_xticklabels([])

    pf.plot_entropy_2( ax_entr , colour=col , llinestyle=lin , labels=False )
    ax_entr.tick_params( labelsize=15 )

ymax = 0.5
par_mag = ax_mag.twinx()
par_mag.set_ylim( ax_mag.get_ylim() )
par_mag.set_yticks((0,0.125,0.25))
par_mag.set_yticklabels(('$0$ : SC','$1/8$ : FO','$1/4$ : LM'))
par_mag.tick_params( axis='both' , which='major' , labelsize=15 )

ymax = mt.log( 4 ) + 0.2
par_entr = ax_entr.twinx()
par_entr.set_ylim( ax_entr.get_ylim() )
par_entr.set_yticks(( 0 , mt.log(2) , mt.log(4) ))
par_entr.set_yticklabels(( '$\ln(1)$ : SC' , '$\ln(2)$ : LM' , '$\ln(4)$ : FO' ) , fontsize=15 )
par_entr.tick_params( axis='both' , which='major' , labelsize=15 )

ax_mag.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 , ncol=1 , fontsize=15 )


if OUTFILE!=0:
    plt.savefig( OUTFILE )
else:
    plt.show()


