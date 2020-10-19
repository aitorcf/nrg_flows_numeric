#!/usr/bin/env python3

import py_functions as pf
import os
import subprocess
import sys

N_NODES
if len( sys.argv[1:] ) >= 1:
    N_NODES = sys.argv[1]

if pf.get_param( 'param' , 'Tmin' )!=pf.get_param( '../ref/param' , 'Tmin' ) or pf.get_param( 'param' , 'Lambda' )!=pf.get_param( '../ref/param' , 'Lambda' ):
    pf.write_param( '../ref/param' , 'Tmin' , pf.get_param( 'param' , 'Tmin' ) )
    pf.write_param( '../ref/param' , 'Lambda' , pf.get_param( 'param' , 'Lambda' ) )
    os.chdir( '../ref/' )
    subprocess.call([ 'nrginit' , '&&' , 'nrgrun' ])
    os.chdir( '../imp/' )

subprocess.call([ 'nrginit' ])
subprocess.call([ 'mpirun' , '-np' , str( N_NODES ) ,  'nrgrun' ])
subprocess.call([ './99_t_subtract' ])

