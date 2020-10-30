#!/usr/bin/env python3

import subprocess
import numpy as np
import matplotlib.pyplot as plt
import math as mt

# ----- #
# FILES #
# ----- #

def get_param( filename , paramname ):
    with open( filename , 'r' ) as f:
        for line in f:
            if len( line.strip() )<len( paramname ): continue
            if line.strip()[ : len(paramname) ]==paramname: 
                return float( line.strip()[ len(paramname) + 1 : ] )


def write_param( filename , paramname , paramvalue ):
    with open( filename , 'r' ) as f:
        with open( 'newparam' , 'w' ) as newparam:
            for line in f:
                if len( line.strip() )<len( paramname ): 
                    newparam.write( line )
                    continue
                if line.strip()[ : len(paramname) ]==paramname:
                    newparam.write( "{}={}\n".format( paramname , paramvalue ) )
                else:
                    newparam.write( line )
    if '../ref/' in filename:
        subprocess.call([ 'mv' , 'newparam' , '../ref/param' ])
    else:
        subprocess.call([ 'mv' , 'newparam' , 'param' ])


# -------- #
# PLOTTING #
# -------- #

def plot_mag_susc( ax , colour='tab:red' , llabel=0 , mark=None , twin=True ):
    td_data = np.loadtxt( 'td_diff' )
    mag_susc = td_data[:,1]
    temp = td_data[:,0]

    lm = np.zeros((len(temp)))
    sc = np.zeros((len(temp)))

    lm[:] = 0.25
    sc[:] = 0

    mark_every = 3 if mark!=None else None
    if llabel!=0:
        ax.plot( temp , mag_susc , label=llabel , color=colour , linewidth=2 , linestyle='-' , marker=mark , markevery=mark_every )
        ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8)
        ymax=0.5
    else:
        ax.plot( temp , mag_susc , color=colour , linewidth=2 , linestyle='-' , marker=mark , markevery=mark_every )
        ymax=0.4

    ax.plot( temp , sc , color='black' , linestyle='--' , linewidth=0.5 )
    ax.plot( temp , lm, color='black', linestyle='--' , linewidth=0.5 )

    ax.set_xticks( np.logspace( get_param( 'param' , 'Tmin' ) , 1 , 5  ) )
    ax.semilogx( base=10 )
    ax.set_xlabel( '$k_B T$' , fontsize='large' )
    ax.set_ylabel( '$k_B T \chi (T)$' , fontsize='large' )
    ax.set_xlim([ get_param( 'param' , 'Tmin' ) , 1e0 ])
    ax.set_ylim([ 0 , ymax ])

    if twin:
        par = ax.twinx()
        par.set_ylim([ 0 , ymax ])
        par.set_yticks((0,0.25))
        par.set_yticklabels(('$0$ : SC','$1/4$ : LM'))

    plt.xticks( fontsize=10 )
    plt.yticks( fontsize=10 )

    ax.tick_params( axis='both' , which='major' , labelsize='large' )

def plot_entropy( ax , llabel=0 , colour='tab:red' , mark=None , twin=True ):
    td_data = np.loadtxt( 'td_diff' )
    entropy = td_data[:,8]
    temp = td_data[:,0]

    sc = np.zeros((len(temp)))
    lm = np.zeros((len(temp)))

    lm[:] = mt.log( 2 )
    sc[:] = mt.log( 1 )

    mark_every = 3 if mark!=None else None

    if llabel!=0:
        ax.plot( temp , entropy , label=llabel , color=colour , linewidth=2 , linestyle='-' , marker=mark , markevery=mark_every )
        ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8)
        ymax=2
    else:
        ax.plot( temp , entropy , color=colour , linewidth=2 , linestyle='-' , marker=mark , markevery=mark_every )
        ymax=1
    ax.plot( temp , sc , linestyle='--' , color='black' , linewidth=0.5 )
    ax.plot( temp , lm , linestyle='--' , color='black' , linewidth=0.5 )

    ax.set_xticks( np.logspace( 10**-15 , 1 , 5 ) )
    ax.semilogx( base=10 )

    ax.set_xlabel( '$k_B T$' , fontsize='large' )
    ax.set_ylabel( '$ S/k_B (T)$' , fontsize='large' )

    ax.set_xlim([ float( get_param( 'param' , 'Tmin' ) ) , 1e0 ])

    ax.set_ylim([ 0 , ymax ])
    ax.set_yticks( np.arange( 0 , ymax , 0.2 ) )

    if twin:
        par = ax.twinx()
        par.set_ylim([ 0 , ymax ])
        par.set_yticks(( 0 , mt.log(2) ))
        par.set_yticklabels(( '$\ln(1)$ : SC' , '$\ln(2)$ : LM' ) )

    plt.xticks( fontsize=10 )
    plt.yticks( fontsize=10 )

    ax.tick_params( axis='both' , which='major' , labelsize='large' )
