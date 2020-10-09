#!/usr/bin/env python3

import subprocess


subprocess.call([ 'mv' , 'param' , 'aux_param' ])

aux_param = open( 'aux_param' , 'r' )
param = open( 'param' , 'x' )
bottom = open( 's_param_bottom.txt' , 'r' )

for line in aux_param:
    param.write( line )
aux_param.close()
subprocess.call([ 'rm' , 'aux_param' ])

for line in bottom:
    param.write( line )
bottom.close()
param.close()
