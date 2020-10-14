#!/usr/bin/env python3

import numpy as np
import py_functions as pf
import sys
import scipy.optimize as opt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as mt
import subprocess 

arguments = []
for arg in sys.argv[1:]:
    arguments.append(arg)
OUTFILE = 0
if np.size(arguments)>=1:
    OUTFILE = arguments[1]


N = pf.get_N('e-q0s2_table1.dat')
U_param, GAMMA_param = pf.get_u_gamma()


def F(in_array):
    U = "{:f}".format( in_array[0] )
    Gd = "{:f}".format( in_array[1] )
    Ga = "{:f}".format( in_array[2] )

    if not Gd > Ga: Gd , Ga = ( Ga , Gd )
    
    subprocess.call([ 'wolframscript' , 'compute_eigenvalues_ring.wls' , f"{U}" , f"{Gd}" , f"{Ga}" ])
    analytic_eigenvalues = np.loadtxt( 'm_eigenvalues.dat' )

    out_array = nrg_eigenvalues_step - analytic_eigenvalues
    print( out_array )

    return out_array


U_array = np.empty( int(N/2) )
Gd_array = np.empty( int(N/2) )
Ga_array = np.empty( int(N/2) )

nrg_eigenvalues = np.empty( ( int(N/2) , 22 ) )
nrg_eigenvalues = pf.read_h0_eigenvalues()
nrg_eigenvalues_step = np.empty( 22 )
for n in range(0,int(N/2)):
    nrg_eigenvalues_step = nrg_eigenvalues[ n , : ]

    res = opt.least_squares( F , [0.15,0.15,0.15] )
    U_array[n] = res.x[0]
    Gd_array[n] = res.x[1]
    Ga_array[n] = res.x[2]

plt.style.use('seaborn-paper')
fig = plt.figure()
ax = fig.add_subplot( 111 , projection='3d' )


pf.plot_arrows_3d( U_array , Gd_array , Ga_array , ax , fixedpoints=False )


plt.show()


