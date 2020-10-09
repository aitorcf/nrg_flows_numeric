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


arguments = []
for arg in sys.argv[1:]:
    arguments.append(arg)
OUTFILE = 0
if np.size(arguments)>=1:
    OUTFILE = arguments[0]


plt.style.use( 'seaborn-paper' )
fig = plt.figure()
ax = fig.add_axes([ 0.15 , 0.2 , 0.8 , 0.75 ])

pf.plot_arrow_diagram( ax , fixedpoints=True )
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.tick_params( labelsize=25 )
ax.set_ylabel( '$U_{\mathrm{eff}}$' , fontsize=25 )
ax.set_xlabel( '$\Gamma_{\mathrm{eff}}$' , fontsize=25 )
ax.set_xticks([ 0 , 0.5 , 1 ])
ax.set_yticks([ 0 , 1 , 2 , 3 , 4 ])
ax.tick_params( labelsize=25 )
U_param, GAMMA_param = pf.get_u_gamma()

if OUTFILE!=0:
    if OUTFILE=='folder':
        plt.savefig("graphs_and_data/arrowflow_and_eigenflow/u-{0:.4f}_gamma-{1:.4f}_UGdiagram.png".format(float(U_param),float(GAMMA_param)))
    elif OUTFILE=='def':
        plt.savefig("u-{0:.4f}_gamma-{1:.4f}_UGdiagram.png".format(float(U_param),float(GAMMA_param)))
    else:
        plt.savefig("{}".format(OUTFILE))
else:
    plt.show()


