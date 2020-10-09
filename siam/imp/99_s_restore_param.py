#!/usr/bin/env python3

import subprocess


subprocess.call([ 'mv' , 'param' , 'aux_param' ])

aux_param = open( 'aux_param' , 'r' )
param = open( 'param' , 'x' )

for line in aux_param:
    param.write( line )
    if line.strip()!='':
        if line[:10]=='dumpgroups':
            break

param.close()
aux_param.close()

subprocess.call([ 'rm' , 'aux_param' ])
