#!/usr/bin/env python3

import subprocess
import py_functions as pf
import sys

if len(sys.argv)==1: 
    print( "Incorrect arguments" )
    sys.exit()
arguments = sys.argv[1:]
U = float( arguments[0] )
G = float( arguments[1] )


# python part
p_eigenvalues = [ str(elem) for elem in pf.compute_h0_eigenvalues_abs( U , G ) ]
print( p_eigenvalues )

# mathematica part
subprocess.call([ "wolframscript" , "compute_eigenvalues.wls" , f"{U}" , f"{G}" ])
with open( 'm_eigenvalues.dat' ) as f:
    m_eigenvalues = []
    for line in f:
        m_eigenvalues.append( line.strip() )

# comparison
for i in range( len( p_eigenvalues ) ):
    print( p_eigenvalues[i] + "\t\t\t" + m_eigenvalues[i] )
