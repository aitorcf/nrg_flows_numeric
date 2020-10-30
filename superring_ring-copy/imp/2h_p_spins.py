#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

OUTNAME=0
if len( sys.argv[1:] )!=0:
    OUTNAME = sys.argv[1]

plt.style.use( 'seaborn-paper' )
fig, ax = plt.subplots()
plt.grid(  b=True, which='major', color='black', linewidth='0.4' , alpha=0.3)

data = np.loadtxt( 'custom' )
t = data[:,0]
sasa = data[:,2]
sasd = data[:,3]
sasf = data[:,4]
s_imps = data[:,8]
ss = 3 * np.loadtxt('td')[:,1]
#deltass = 3 * np.loadtxt('td_diff.dat')[:,1]

ax.plot( t , sasa , label='$<S_a^2> = <S_d^2>$' , marker='d' , markersize=5 , markevery=3 )
ax.plot( t , sasd , label='$<\\vec{S}_{d} \cdot \\vec{S}_{a}>$' , marker='.' , markersize=5 , markevery=3 )
ax.plot( t , ss , label='$<S_{contr}^2>$' , marker='^' , markersize=5 , markevery=3 )
ax.plot( t , s_imps , label='$<(\\vec{S}_d+\\vec{S}_a)^2>$' , marker='v' , markersize=5 , markevery=3 )
ax.plot( t , sasf , label='$<\\vec{S}_d \cdot \\vec{S}_f>$' , marker='s' , markersize=5 , markevery=3 )


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
