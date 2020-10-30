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


def F(in_array):
    U = in_array[0]
    GAMMA = in_array[1]

    out_array = np.empty( 22 )

    analytic_eigenvalues = pf.compute_h0_eigenvalues_sneg_lowest( U , GAMMA )

    out_array = nrg_eigenvalues_step - analytic_eigenvalues

    return out_array
# --------------------------- 

arguments = []
for arg in sys.argv[1:]:
    arguments.append(arg)

OUTFILE = 0
if np.size(arguments)>0:
    OUTFILE = arguments[0]


UG_0 = np.array([0,0])
UG_1 = np.array([1e-1,1e-2])
UG_2 = np.array([1e-1,1e-1])
UG_3 = np.array([1e-2,0])
UG_4 = np.array([1e-2,1e-4])
UG_5 = np.array([1e-2,1e-3])
UG_6 = np.array([0,1e-1])

UG = [ np.array(elem) for elem in [ [1e-2,1e-5] , [1e-2,2e-4] , [1e-2,1e-2] , [1e-4,1e-2] , [0,1e-2] ] ]

plt.style.use('seaborn-paper')
fig = plt.figure()
ax = fig.add_axes([ 0.15 , 0.15 , 0.80 , 0.80 ]) 

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
   
    nrg_eigenvalues = pf.read_h0_eigenvalues_lowest()
    
    U_array = np.empty( int(N/2) )
    GAMMA_array = np.empty( int(N/2) )
    nrg_eigenvalue_step = np.empty( 6 )
    for n in range(0,int(N/2)):
        nrg_eigenvalues_step = nrg_eigenvalues[n,:]
        
        res = opt.least_squares( F , [0.3,0.3] , bounds=([-50,0],[50,50]) )
        U_array[n] = res.x[0]
        GAMMA_array[n] = res.x[1]

    col = colours[colour]

    pf.plot_arrows( U_array , GAMMA_array , ax , colour=col ,  fixedpoints=False )
        
    #ax.plot( [10000,2000] , [10000,2000] ,color=col ,\
    #    label='${}={:3.0e}$, ${}={:3.0e}$'.format('U',pair[0],'\Gamma',pair[1]))

pf.include_fixedpoints( ax )
ax.set_xlim([ -0.2 , 1.2 ])
ax.set_xticks( np.arange( 0 , 1.3 , 0.2 ) )
ax.set_ylim([ -3 , 6 ])
ax.set_yticks( np.arange( -3 , 5.5 , 1) )
ax.tick_params( labelsize=15 )


#legend = ax.legend( loc="upper right" , frameon=True , framealpha=0.8 , facecolor='white' , edgecolor='white' , fontsize=15 )


if OUTFILE!=0:
        plt.savefig("/graphs_and_data/arrowplots_multiple/{}".format(OUTFILE))
else:
    plt.show()


