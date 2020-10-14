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

    out_array = np.empty( 4 )

    analytic_eigenvalues = pf.compute_h0_eigenvalues_siam( U , GAMMA )

    out_array = np.append( nrg_eigenvalues_step[:3] , nrg_eigenvalues_step[4] ) - analytic_eigenvalues

    return out_array
# --------------------------- 

arguments = []
for arg in sys.argv[1:]:
    arguments.append(arg)

OUTFILE = 0
if np.size(arguments)>0:
    OUTFILE = arguments[0]

UG = [ np.array(elem) for elem in [ [1e-2,1e-5] , [1e-2,2e-4] , [1e-2,5e-4] , [1e-2,5e-3] , [1e-2,1e-3] , [1e-2,2e-3],
                                    [2e-3,1e-2] ,
                                    [1e-4,1e-2] , [0,0.01] ] ]
plt.style.use('seaborn-paper')
fig, ax = plt.subplots()
#plt.grid( b=True, which='major', color='black', linewidth='0.4' , alpha=0.3)

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
        
        res = opt.least_squares( F , [0.3,0.7]  )
        U_array[n] = res.x[0]
        GAMMA_array[n] = res.x[1]

    col = colours[colour]

    pf.plot_arrows( U_array , GAMMA_array , ax , colour='black' ,  fixedpoints=False )
        
    #ax.plot(GAMMA_array,U_array,color=col, linewidth=0 ,\
    #    label='${}={:3.0e}$, ${}={:3.0e}$'.format('U',pair[0],'\Gamma',pair[1]))

pf.include_fixedpoints_siam( ax , multi=True )

ax.set_yticks( np.arange(-9,8,1) )

legend = ax.legend(loc="upper right",frameon=True,framealpha=0.7,facecolor='white',edgecolor='white')
for handle in legend.legendHandles:
    handle.set_linewidth(3.0)


if OUTFILE!=0:
        plt.savefig("/graphs_and_data/arrowplots_multiple/{}".format(OUTFILE))
else:
    plt.show()


