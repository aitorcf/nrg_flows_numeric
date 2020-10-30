#!/usr/bin/env python3

import numpy as np
import sys


if len( sys.argv )==1:
    print( 'Argument N (number of z values) missing. Exiting' )
    sys.exit()

N = int( sys.argv[1] )

Z = np.linspace( 1.0/N , 1.0 , N )


z = Z[0]
dirname = 'zavg_{:.2f}/'.format( z )
td_zavg_path = dirname + 'td'
td_zavg_array = np.loadtxt( td_zavg_path )
td_array = np.empty( ( len( td_zavg_array[:,0] ) , len( td_zavg_array[0,:] ) ) )
td_array = 1.0 / N * td_zavg_array

for z in Z[1:]:
    dirname = 'zavg_{:.2f}/'.format( z )
    td_zavg_path = dirname + 'td'
    td_zavg_array = np.loadtxt( td_zavg_path )
    
    if len( td_array[:,0] ) != len( td_zavg_array[:,0] ):
        min_n = min( len( td_array[:,0] ) , len( td_zavg_array[:,0] ) )
        td_array = td_array[ :min_n , : ]
        td_zavg_array = td_zavg_array[ :min_n , : ]

    td_array = td_array + 1.0 / N * np.loadtxt( td_zavg_path )

td = open( 'td' , 'w' )
td.write( "# T\t<Sz^2>\t<Q>\t<Q^2>\t<E>\t<E^2>\tC\tF\tS\n" )
for i in range( len( td_array[:,0] ) ):
    for j in range( len( td_array[0,:] ) ):
        if j==0:
            td.write( "{:.3e}\t".format( td_array[i,j] ) )
        else:
            td.write( "{:5.3f}\t".format( td_array[i,j] ) )
    td.write( "\n" )
td.close()
