#!/usr/bin/env python3

import subprocess
import sys
import numpy as np
import os


if len( sys.argv )==1:
    print( 'Argument N (number of z points) missing. Exiting.' )
    sys.exit()

N = int( sys.argv[1] )
Z = np.linspace( 1.0/N , 1.0 , N )


for z in Z: # create zavg folders with param files and do td calculations inside them.
            # (no td subtraction yet --this script may be called from ../ref/, too.
    subprocess.call([ 'mkdir' , 'zavg_{:.2f}'.format( z ) ])    

    subprocess.call([ 'cp' , 'param' , 'zavg_{:.2f}/param'.format( z ) ])
    param = open( 'param' , 'r' )
    param_zavg = open( 'zavg_{:.2f}/param'.format( z ) , 'w')

    for line in param:
        param_zavg.write( line )
        if line.strip()=="discretization=Z":
            param_zavg.write( "z={:.3f}\n".format( z ) )

    param.close()
    param_zavg.close()

    os.chdir( 'zavg_{:.2f}'.format( z ) )
    subprocess.call( '../0a_run' )
    os.chdir( '..' )
