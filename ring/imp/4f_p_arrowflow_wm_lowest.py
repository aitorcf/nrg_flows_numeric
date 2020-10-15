#!/usr/bin/env python3

import numpy as np
import py_functions as pf
import sys
import scipy.optimize as opt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as mt
import subprocess 


N = pf.get_N('e-q0s2_table1.dat')

f = open( '4d_arrowflow.dat' , 'w' )

def F(in_array):
    Ud = "{:.50f}".format( in_array[0] )
    Ua = "{:.50f}".format( in_array[1] )
    Gd = "{:.50f}".format( in_array[2] )
    Ga = "{:.50f}".format( in_array[3] )

    #if not float(Gd)+0.0001 > float(Ga): return 1000*np.ones(6)
    
    print( f"#####\nUd = {Ud}\nUa = {Ua}\nGd = {Gd}\nGa = {Ga}\n#####" )

    subprocess.call([ 'wolframscript' , 'compute_eigenvalues_ring_lowest.wls' , f"{Ud}" , f"{Ua}" , f"{Gd}" , f"{Ga}" ])
    analytic_eigenvalues = np.loadtxt( 'm_eigenvalues_lowest.dat' )

    out_array = nrg_eigenvalues_step - analytic_eigenvalues

    return out_array


Ud_array = np.empty( int(N/2) )
Ua_array = np.empty( int(N/2) )
Gd_array = np.empty( int(N/2) )
Ga_array = np.empty( int(N/2) )

nrg_eigenvalues = np.empty( ( int(N/2) , 6 ) )
nrg_eigenvalues = pf.read_h0_eigenvalues_lowest()
nrg_eigenvalues_step = np.empty( 6 )
for n in range(0,int(N/2)):
    nrg_eigenvalues_step = nrg_eigenvalues[ n , : ]

    res = opt.least_squares( F , [0.15,0.15,0.15,0.15] , bounds=([0,0,0,0],[10,10,10,10]) );
    Ud_array[n] = res.x[0]
    Ua_array[n] = res.x[1]
    Gd_array[n] = res.x[2]
    Ga_array[n] = res.x[3]
    
    print( res , file=f )
    print( res )
    print( f"#####\nUd = {res.x[0]}\nUa = {res.x[1]}\nGd = {res.x[2]}\nGa = {res.x[3]}\n#####" , file=f ) 
    print( "\n\n------------------------\n\n" , file=f )

f.close()

#plt.style.use('seaborn-paper')
#fig = plt.figure()
#ax = fig.gca( projection='3d' )

#pf.plot_arrows_3d( Ud_array , Ua_array , Gd_array , Ga_array , ax , fixedpoints=False )

#plt.show()


