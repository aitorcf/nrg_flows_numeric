#!/usr/bin/env python3

import numpy as np
import py_functions as pf
import sys
import scipy.optimize as opt
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from matplotlib.lines import Line2D
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
    U = in_array[0]
    GAMMA = in_array[1]

    out_array = np.empty( 4 )
    
    analytic_eigenvalues = pf.compute_h0_eigenvalues_sneg_lowest( U , GAMMA )

    analytic_eigenvalues = np.append( analytic_eigenvalues[:3] , analytic_eigenvalues[4] )

    out_array = nrg_eigenvalues_step[:3] - analytic_eigenvalues[:3]

    return out_array


U_array = np.empty( int(N/2) )
GAMMA_array = np.empty( int(N/2) )

nrg_eigenvalues = np.empty( (int(N/2),6) )
nrg_eigenvalues = pf.read_h0_eigenvalues_lowest()
nrg_eigenvalues_step = np.empty( 6 )
errors = open( 'arrowplot_error.dat' , 'w' )
for n in range(0,int(N/2)):
    nrg_eigenvalues_step = nrg_eigenvalues[n,:]

    res = opt.least_squares(F,[0.15,0.5])
    U_array[n] = res.x[0]
    GAMMA_array[n] = res.x[1]

    errors.write( f"step {2*n}:\ncost = {res.cost}\noptimality = {res.optimality}\nresiduals = {res.fun}\n\n" )

errors.close()


plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots()


pf.plot_arrows( U_array , GAMMA_array , ax , fixedpoints=False , colour='black' )
print( U_array[-1] , GAMMA_array[-1] )

ax.set_title('Flow path for $ {}{:4.1e} $ and $ {}{:4.1e} $   ($D=1$ units)'.format("U=",float(U_param),'\Gamma=',float(GAMMA_param)))

if OUTFILE!=0:
    if OUTFILE=='folder':
        plt.savefig("graphs_and_data/arrowflow_and_eigenflow/u-{0:.4f}_gamma-{1:.4f}_UGdiagram.png".format(float(U_param),float(GAMMA_param)))
    elif OUTFILE=='def':
        plt.savefig("u-{0:.4f}_gamma-{1:.4f}_UGdiagram.png".format(float(U_param),float(GAMMA_param)))
    else:
        plt.savefig("{}".format(OUTFILE))
else:
    plt.show()


