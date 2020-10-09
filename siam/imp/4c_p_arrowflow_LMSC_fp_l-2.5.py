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
ax = fig.add_axes([ 0.15 , 0.2 , 0.8 , 0.7 ])

pf.plot_arrow_diagram( ax , fixedpoints=True )
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.tick_params( labelsize=25 )
ax.set_xlabel( '$\Gamma_{\mathrm{eff}}$' , fontsize=25 )
ax.set_ylabel( '$U_{\mathrm{eff}}$' , fontsize=25 )
ax.tick_params( labelsize=25 )
ax.set_xticks([ 0 , 0.5 , 1.0 ])

x1 = 0.0181
y1 = 3.0535
malda = -4.056

x2 = x1 + 0.2
y2 = y1 + malda*( x2- x1 )
ax.plot( [x1,x2] , [y1,y2] , color='black' , linestyle='--' , linewidth=1 )


J = np.arange( 0 , 1 , 0.05 )
c = y1 + x1 
X = c * J / ( 1 + J )
Y = c / ( 1 + J )

#ax.plot( X , Y , linestyle=':' , color='black' )

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


