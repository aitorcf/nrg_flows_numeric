#!/usr/bin/env python3

import subprocess
import py_functions as pf
import sys
import numpy as np

if len(sys.argv)==1: 
    print( "Incorrect arguments" )
    sys.exit()
arguments = sys.argv[1:]
U = float( arguments[0] )
G = float( arguments[1] )


# python part
p_eigenvalues = pf.compute_h0_eigenvalues_abs( U , G )
print( p_eigenvalues )

# mathematica part
subprocess.call([ "wolframscript" , "compute_eigenvalues.wls" , f"{U}" , f"{G}" ])
m_eigenvalues = np.loadtxt( "m_eigenvalues.dat" )
#with open( 'm_eigenvalues.dat' ) as f:
#    m_eigenvalues = []
#    for line in f:
#        m_eigenvalues.append( float( line.strip() ) )

# comparison
print( "              Python\t\t\tMathematica" )
print( "Array types: " + str( type( p_eigenvalues ) ) + "\t\t\t" + str( type( m_eigenvalues ) ) )
print( "Element types: " + str( type( p_eigenvalues[0] ) ) + "\t\t\t" + str( type( m_eigenvalues[0] ) ) )
for i in range( len( p_eigenvalues ) ):
    print( str( p_eigenvalues[i] ) + "\t\t\t" + str( m_eigenvalues[i] ) )

diffvector = [ ( p_eigenvalue - m_eigenvalue )**2 for p_eigenvalue,m_eigenvalue in zip( p_eigenvalues , m_eigenvalues ) ]
print( "Difference squared = " + f"{ np.sum( diffvector ) }" )
