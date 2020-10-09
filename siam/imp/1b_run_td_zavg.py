#!/usr/bin/env python3

import subprocess
import sys
import numpy as np
import os
import py_functions as pf


if len( sys.argv )==1:
    print( 'Argument N (number of z values) missing. Exiting.' )
    sys.exit()

N = int( sys.argv[1] )


pf.equalize_lambdas_and_tmins_imp_ref_zavg()

os.chdir( '../ref' )
subprocess.call([ '../imp/0b_run_zavg.py' , '{}'.format( N ) ])
subprocess.call([ '../imp/99_t_average.py' , '{}'.format( N ) ])
os.chdir( '../imp' )

subprocess.call([ './0b_run_zavg.py' , '{}'.format( N ) ])
subprocess.call([ './99_t_average.py' , '{}'.format( N ) ])
subprocess.call([ './99_t_subtract' ])
