#!/usr/bin/env python3

import sys


if len( sys.argv )!=6:
    print( "Incorrect arguments: need O/E, Q, 2S+1, number of eigenvalues and filename" )
    sys.exit()
O_E      = sys.argv[1]
Q        = sys.argv[2]
S        = sys.argv[3]
M        = int( sys.argv[4] )
FILENAME = sys.argv[5]

annotated = open( 'annotated.dat' , 'r' )
f         = open( FILENAME , 'w' )

n = 0
eigenvalues = 0
for line in [ line.strip().split() for line in annotated ]:
    if len( line )==0: 
        f.write( "\n" )
        n += 1
        eigenvalues = 0
        continue
    if ( O_E=='E' and n%2==0 ) or ( O_E=='O' and n%2!=0 ):
        if line[1]==Q and line[2]==S and eigenvalues<M:
            print( line )
            f.write( f"{line[0]}\n" )
            eigenvalues += 1
        


annotated.close()
f.close()
