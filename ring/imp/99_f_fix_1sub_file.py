#!/usr/bin/env python3

import sys
import subprocess


if len( sys.argv )==1:
    print( 'Missing argument: FILENAME. Exiting.' )
    sys.exit()

FILENAME = sys.argv[1]

subprocess.call([ 'cp' , FILENAME , '{}_new'.format( FILENAME ) ])

f_new = open( '{}_new'.format( FILENAME ) , 'r' )
f = open( FILENAME , 'w' )

max_starting_n = 0
now = True
for line in f_new:
    if now:
        now = False
        n = int( line.strip().split()[0] )
        if n > max_starting_n:
            max_starting_n = n
    if line.strip()=="":
        now = True
        if n > max_starting_n: 
            max_starting_n = n

f_new.seek( 0 )

for line in f_new:
    if line.strip()!="":
        if int( line.strip().split()[0] ) >= max_starting_n:
            f.write( line )
    else: f.write( line )

f.close()
f_new.close()

subprocess.call([ 'rm' , '{}_new'.format( FILENAME ) ])

