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
    if '../ref/' in filename:
        subprocess.call([ 'mv' , 'newparam' , '../ref/param' ])
    else:
        subprocess.call([ 'mv' , 'newparam' , 'param' ])

# --------------- #
# THERMO PLOTTING #
# --------------- #

def plot_mag_susc( ax , colour='tab:blue' , llabel=0 ):
    td_data = np.loadtxt( 'td_diff' )
    mag_susc = td_data[:,1]
    temp = td_data[:,0]

    lm = np.zeros((len(temp)))
    cs = np.zeros((len(temp)))
    ps = np.zeros((len(temp)))
    ff = np.zeros((len(temp)))

    lm[:] = 0.5   # = 2*lo(SIAM)
    cs[:] = 0.0
    ps[:] = 0.25
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
    ax.plot( temp , ps , color='black' , linestyle='--' , linewidth=0.5 )
    ax.plot( temp , cs , color='black' , linestyle='--' , linewidth=0.5 )

    ax.semilogx( base=10 )
    ax.set_xlabel( '$k_B T$' , fontsize=15 )
    ax.set_ylabel( '$k_B T \chi (T)$' , fontsize=15 )
    ax.set_xlim([ float( get_param( 'param' , 'Tmin' ) ) , 1e0 ])
    ax.set_ylim([ 0 , ymax ])

    par = ax.twinx()
    par.set_ylim([ 0 , ymax ])
    par.set_yticks((0,0.25,0.5,0.666))
    par.set_yticklabels(('$0$ : CS','$1/4$ :FO / PS','$1/2$ : LM','$2/3$ : FF'))

    ax.tick_params( labelsize=15 )
    par.tick_params( labelsize=10 )


def plot_entropy( ax , llabel=0 , colour='tab:blue' ):
    td_data = np.loadtxt( 'td_diff' )
    entropy = td_data[:,8]
    temp = td_data[:,0]

    fo = np.zeros((len(temp)))
    lm = np.zeros((len(temp)))
    cm = np.zeros((len(temp)))
    fr = np.zeros((len(temp)))
    fc = np.zeros((len(temp)))

    lm[:] = mt.log( 4 )
    fo[:] = mt.log( 16 )
    cm[:] = mt.log( 2 )
    fr[:] = 0
    fc[:] = mt.log( 3 )

    if llabel!=0:
        ax.plot( temp , entropy , label=llabel , color=colour , linewidth=2.0 , linestyle='-' )
        ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8)
        ymax=5
    else:
        ax.plot( temp , entropy , color=colour , linewidth=2.0 , linestyle='-' )
        ymax=4
    ax.plot( temp , fo , linestyle='--' , color='black' , linewidth=0.5 )
    ax.plot( temp , lm , linestyle='--' , color='black' , linewidth=0.5 )
    ax.plot( temp , fc , linestyle='--' , color='black' , linewidth=0.5 )
    ax.plot( temp , cm , linestyle='--' , color='black' , linewidth=0.5 )
    ax.plot( temp , fr , linestyle='--' , color='black' , linewidth=0.5 )

    ax.semilogx( base=10 )

    ax.set_xlabel( '$k_B T$' , fontsize=15 )
    ax.set_ylabel( '$ S/k_B (T)$' , fontsize=15 )

    ax.set_xlim([ float( get_param( 'param' , 'Tmin' ) ) , 1e0 ])

    ax.set_ylim([ 0 , ymax ])
    ax.set_yticks( np.arange( 0 , ymax , 1 ) )

    par = ax.twinx()
    par.set_ylim([ 0 , ymax ])
    par.set_yticks(( 0 , mt.log(2) , mt.log(3) , mt.log(4) , mt.log(16) ))
    par.set_yticklabels(('$\ln(1)$ : CS','$\ln(2)$ : PS','$\ln(3)$ : FF','$\ln(4)$ : LM / FO-SC','$\ln(16)$ : FO'))

    ax.tick_params( labelsize=15 )
    par.tick_params( labelsize=10 )


# ------------------ #
# EIGENFLOW PLOTTING #
# ------------------ #

def plotfile( f , steps , eigenvalues , ax , **kwargs ):
    eigenvalue = 0
    slot = 0

    n_eigenvalues = np.size( eigenvalues[0,:] )
    n_slots = np.size( eigenvalues[:,0] )

    for line in f.readlines():

        if line=='\n' or line=='':
            if 'color' in kwargs and 'linestyle' in kwargs:
                line, = ax.plot( steps , eigenvalues[:,eigenvalue] , color=kwargs['color'] , linestyle=kwargs['linestyle'] )
            elif 'color' in kwargs:
                line, = ax.plot( steps , eigenvalues[:,eigenvalue] , color=kwargs['color'] )
            elif 'linestyle' in kwargs:
                line, = ax.plot( steps , eigenvalues[:,eigenvalue] , linestyle=kwargs['linestyle'] )
            else:
                line, = ax.plot( steps , eigenvalues[:,eigenvalue] )
            eigenvalue += 1
            if eigenvalue >= np.size( eigenvalues[0,:] ):
                if 'label' in kwargs:
                    line.set_label(kwargs['label'])
                return
            slot = 0
            continue

        if slot < n_slots:
            eigenvalues[slot,eigenvalue] = line.split(' ')[1]
        slot += 1

def label_flowplot(n_steps,n_eigenvalues,ax):
    if n_steps%2==0:
        ax.set_xlabel('N (even)')
        ax.set_xticks(np.arange(0,n_steps,10))
    else:
        ax.set_xlabel('N (odd)')
        ax.set_xticks(np.arange(5,n_steps,10))
    ax.set_ylabel('E')