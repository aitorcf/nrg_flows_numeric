#!/usr/bin/env python3

import sys
import py_functions as pf
import matplotlib.pyplot as plt


arguments=[]
for arg in sys.argv[1:]:
    arguments.append( arg )
OUTNAME = 0
if len(arguments)>=1:
    OUTNAME = arguments[0]


plt.style.use( 'seaborn-whitegrid' )
fig, ax = plt.subplots()

pf.plot_mag_susc( ax )


if OUTNAME!=0:
    plt.savefig( OUTNAME )
else:
    plt.show()
