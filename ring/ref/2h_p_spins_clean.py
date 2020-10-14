#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

OUTNAME=0
if len( sys.argv[1:] )!=0:
    OUTNAME = sys.argv[1]

data = np.loadtxt( 'custom' )
t = data[:,0]
sfsf = 3 * data[:,1]

plt.style.use( 'seaborn-paper' )
fig, ax = plt.subplots()
plt.grid(  b=True, which='major', color='black', linewidth='0.4' , alpha=0.3)

ax.plot( t , sfsf , label='$<S_{band}^2>$' )

#ax.plot( t , sasa , color='tab:blue' , label='$<S_{1}^2> = <S_{2}^2>$' )
#ax.plot( t , sfsf , color='tab:orange' , label='$<S_{band}^2>$' )
#ax.plot( t , sasd , color='tab:red' , label='$<\\vec{S}_{1} \cdot \\vec{S}_{2}>$' )
#ax.plot( t , sasf , color='tab:green' , label='$ <\\vec{S}_{1} \\cdot \\vec{S}_{band}>=<\\vec{S}_{2} \\cdot \\vec{S}_{band}> $' )
#ax.plot( t , ss , color='tab:grey' , label='$<S_{tot}^2>$' )
#ax.plot( t , s_imps , color='tab:brown' , label='$<S_{imps}^2>$' )

lims = [ -0.5 , 3.0 ]

plt.semilogx( base=10 )
ax.set_ylim( lims )
ax.set_xlabel( '$k_b T$' )
ax.set_ylabel( '$ S^2 / \hbar^2 $' )

#twin = ax.twinx()
#twin.set_ylim( lims )
#twin.set_yticks([ 0.375 , 3.0/4.0 ])
#twin.set_yticklabels([ '$S_z^2=0.125$ : FO' , '$S=1/2$ : LM' ])

ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 , ncol=3 )

if OUTNAME==0: plt.show()
else: plt.savefig( OUTNAME )
