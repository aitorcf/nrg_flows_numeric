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


arguments = []
for arg in sys.argv[1:]:
    arguments.append(arg)

OUTFILE = 0
if np.size(arguments)>0:
    OUTFILE = arguments[0]


UG = [ np.array(elem) for elem in [ [1e-2,1e-5] , [1e-2,2e-4] , [1e-2,1e-2] , [1e-4,1e-2] , [0,1e-2] ] ]

plt.style.use('seaborn-paper')
fig = plt.figure()
ax_mag = fig.add_axes( [0.1, 0.51, 0.6, 0.39] )
ax_entr = fig.add_axes( [0.1, 0.12, 0.6, 0.39] )

colours = mcolors.TABLEAU_COLORS
i = 0
for pair, colour in zip(UG,colours.keys()):
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
    subprocess.call( './1d_run_th_fl' )
    
    N = pf.get_N( 'e-q0s2_table1.dat' )
   
    col = colours[colour]

    pf.plot_mag_susc_2( ax_mag , colour=col , llabel='$U = {:3.0e}$ , $\Gamma = {:3.0e}$'.format(pair[0],pair[1]) )
    pf.plot_entropy_2( ax_entr , colour=col )   

ax_mag.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 , ncol=2 )

if OUTFILE!=0:
    plt.savefig("/graphs_and_data/arrowplots_multiple/{}".format(OUTFILE))
else:
    plt.show()


