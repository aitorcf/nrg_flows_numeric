#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import py_functions as pf
import subprocess


arguments = []
for argument in sys.argv[1:]:
    arguments.append( argument )
if len( arguments ) < 3:
    print( 'Incorrect arguments. O/E, Q and S are mandatory, #EIGENVALUES is optional. Exiting.' )
    sys.exit()

O_E = arguments[0]
Q = arguments[1]
S = arguments[2]

filename = '{}-q{}s{}.dat'.format( O_E , Q , S )

subprocess.call([ './99_f_extract_1sub' , O_E , Q , S ])
subprocess.call([ './99_f_fix_1sub_file.py' , filename ])

n_steps = pf.get_N( filename )

f = open( filename , 'r' )

if np.size(arguments)>3: n_eigenvalues = int(arguments[3])
else: n_eigenvalues = 6


steps = np.arange( pf.get_n( filename ) , pf.get_N( filename ) , 2 ) 
eigenvalues = np.empty( ( len(steps) , n_eigenvalues ) )

plt.style.use( 'seaborn-whitegrid' )
fig, ax = plt.subplots()

pf.plotfile( f , steps , eigenvalues , ax )
f.close()

ax.set_title( 'Lowest eigenvalues for Q={}, S={}'.format( int(Q) , (int(S)-1)/2.0 ) )

pf.label_flowplot( n_steps , n_eigenvalues , ax )

plt.show()


