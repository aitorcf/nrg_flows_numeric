#!/usr/bin/env python3

import subprocess
import numpy as np
import matplotlib.pyplot as plt


# ----- #
# FILES #
# ----- #

def get_param( filename , paramname ):
    with open( filename , 'r' ) as f:
        for line in f:
            if len( line.strip() )<len( paramname ): continue
            if line.strip()[ : len(paramname) ]==paramname: 
                return line.strip()[ len(paramname) + 1 : ]


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
    subprocess.call([ 'mv' , 'newparam' , 'param' ])

# -------- #
# PLOTTING #
# -------- #

def plot_mag_susc( ax , colour='tab:blue' , llabel=0 ):
    td_data = np.loadtxt( 'td_diff.dat' )
    mag_susc = td_data[:,1]
    temp = td_data[:,0]

    fo = np.zeros((len(temp)))
    lm = np.zeros((len(temp)))
    cs = np.zeros((len(temp)))
    clm = np.zeros((len(temp)))
    ff = np.zeros((len(temp)))

    lm[:] = 0.5   # = 2*lo(SIAM)
    fo[:] = 0.25  # = 2*fo(SIAM)
    cs[:] = 0.0
    clm[:] = 0.125
    ff[:] = 0.666

    if llabel!=0:
        ax.plot( temp , mag_susc , label=llabel , color=colour , linewidth=2.0 , linestyle='-' )
        ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8)
        ymax=0.9
    else:
        ax.plot( temp , mag_susc , color=colour , linewidth=2.0 , linestyle='-' )
        ymax=0.8

    ax.plot( temp , ff , color='black' , linestyle='--' , linewidth=0.5 )
    ax.plot( temp , lm, color='black', linestyle='--' , linewidth=0.5 )
    ax.plot( temp , fo, color='black' , linestyle='--' , linewidth=0.5 )
    ax.plot( temp , clm , color='black' , linestyle='--' , linewidth=0.5 )
    ax.plot( temp , cs , color='black' , linestyle='--' , linewidth=0.5 )


    ax.semilogx( base=10 )
    ax.set_xlabel( '$k_B T$' , fontsize=15 )
    ax.set_ylabel( '$k_B T \chi (T)$' , fontsize=15 )
    ax.set_xlim([ float( get_param( 'param' , 'Tmin' ) ) , 1e0 ])
    ax.set_ylim([ 0 , ymax ])

    par = ax.twinx()
    par.set_ylim([ 0 , ymax ])
    par.set_yticks((0,0.125,0.25,0.5,0.666))
    par.set_yticklabels(('$0$ : CS','$1/8$ : FO-SC','$1/4$ : PS / FO','$1/2$ : LM','$2/3$ : FF'))

    ax.tick_params( labelsize=15 )
    par.tick_params( labelsize=10 )
