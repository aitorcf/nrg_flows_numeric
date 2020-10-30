#!/usr/bin/env python3

import numpy as np

matrix_ref = np.loadtxt( '../ref/td' )
matrix_imp = np.loadtxt( 'td' )
matrix_diff = matrix_imp - matrix_ref
matrix_diff[ : , 0 ] = matrix_imp[ : , 0 ]

with open( 'td_diff' , 'w' ) as td_diff:
    td_diff.write( "# T\t\t<Sz^2>\t<Q>\t<Q^2>\t<E>\t<E^2>\tC\tF\tS\n" ) 
    for i in range( len( matrix_diff[:,0] ) ):
        for j in range( len( matrix_diff[i,:] ) ):
            if j==( len( matrix_diff[i,:] ) - 1 ):
                td_diff.write( "{:.4f}\n".format(matrix_diff[i,j]) )
            elif j==0:
                td_diff.write( "{:.2e}\t".format(matrix_diff[i,j]) )
            else:
                td_diff.write( "{:.4f}\t".format(matrix_diff[i,j]) )
