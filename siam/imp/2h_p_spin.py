#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np



plt.style.use( 'seaborn-paper' )
fig = plt.figure()
ax = fig.add_axes( [0.22,0.22,0.72,0.73] )

ax.set_xlabel( '$k_b T$' , fontsize=25 )
ax.set_ylabel( '$S^2$' , fontsize=25 )


data = np.loadtxt( 'custom' )
t = data[:,0]
sdsd = data[:,2] 
ss = 3 * np.loadtxt( 'td_diff.dat' )[:,1]

ax.plot( t , sdsd , color='black' , label='$<S^2_{\mathrm{imp}}>$' , marker='d' , markersize=5 , markevery=3 )
ax.plot( t , ss , color='black' , label='$<S^2_{\mathrm{tot}}>$' , marker='^' , markersize=6 , markevery=3  )


lims = [ -0.05 , 1.2 ]
ticks = np.arange( 0 , 1.0 , 0.25 )

ax.set_ylim( lims )
ax.set_yticks( ticks )
ax.set_xlim([ 10**(-15) , 1 ])
ax.set_xticks([ 10**(-15) , 10**(-10) , 10**(-5) , 1 ])
ax.semilogx()
ax.tick_params( labelsize=25 )
twin = ax.twinx()
twin.set_ylim( lims )
twin.set_yticks( ticks )
twin.set_yticklabels([])
twin.set_xlim([ 10**(-15) , 1 ])
twin.set_xticks([ 10**(-15) , 10**(-10) , 10**(-5) , 1 ])

ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 , ncol=2 , fontsize=20 )

plt.show()
