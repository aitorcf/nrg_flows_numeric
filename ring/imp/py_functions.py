#!/usr/bin/env python3

import subprocess
import os
import numpy as np
import math as mt
import cmath as ct
import matplotlib.pyplot as plt
import scipy.optimize as opt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from matplotlib.lines import Line2D


# FILES AND PARAMETERS

def write_param( **kwargs ):
    subprocess.call([ 'mv' , 'param' , 'new_param' ])
    
    param = open( 'param' , 'x' )
    new_param = open( 'new_param' , 'r' )

    for line in new_param:
        if line.strip()=='': param.write( line )
        else:
            written = False

            for key in kwargs:
                if len(line) <= len(key): continue
                if line[ : len(key) ]==key:
                    param.write( "{}={}\n".format( key , kwargs[key] ) )
                    written = True
                    break
            
            if not written:
                param.write( line )
            
    param.close()
    new_param.close()

    subprocess.call([ 'rm' , 'new_param' ])


def get_lambda( param_path ):   # returns value of lambda in param file
    param = open( param_path , 'r' ).readlines()
    for line in param:
        if line.strip()!=[]:
            if line[:6]=='Lambda':
                return float( line.strip()[7:] )


def get_tmin( param_path ): # returns value of Tmin in param file
    param = open( param_path , 'r' ).readlines()
    for line in param:
        if line.strip()!=[]:
            if line[:4]=='Tmin':
                return float( line.strip()[5:] )


def get_n( filename ): # takes the name of an eigenflow file (e.g. 'e-q1s2.dat')
                       # and returns the min number of nrg iteration present there.
    return int( open( filename , 'r' ).readlines()[0].split()[0] )


def get_N( filename ): # takes the name of an eigenflow file (e.g. 'e-q1s2.dat')
                       # and returns the max number of nrg iteration present there.
    f = open( filename , 'r' )

    for line in f:
        if line.strip()=="":
            return max_n
        max_n = int( line.split()[0] )


def get_u_gamma():
    param = open('param','r')
    for line in param:
        if line!="" and line!="\n":
            if line[0]=='U':
                U = float( line.strip()[2:] )
            elif line[:5]=='Gamma':
                GAMMA = float( line.strip()[6:] )
                param.close()
                return (U,GAMMA)

def get_nrg_scale():
    Lambda = get_lambda( 'param' )
    z = get_z()

    if get_discretization()=='Y':
        return ( 1 + Lambda**-1 ) / 2.0  *  Lambda**( 1.5 - z )

    else:
        return ( 1 - Lambda**-1 ) / mt.log( Lambda ) * Lambda**( 1.5 - z )


def get_z():
    param = open( 'param' , 'r' )

    for line in param:
        if line.strip()=='': continue
        if line.strip()[0]=='z': return float( line.strip()[2:] )

    return 1.0


def get_discretization():
    param = open( 'param' , 'r' )

    for line in param:
        if line.strip()=='': continue
        if line[:14]=='discretization':
            return line.strip()[15:]

def scale_u_gamma( U , GAMMA ):
    Lambda = get_lambda( 'param' )
    U = (  2.0  /  ( 1 + Lambda**-1 )  ) * U / 2.0
    GAMMA = (  2.0  /  ( 1 + Lambda**-1 )  )**2 * 2.0 * GAMMA / mt.pi
    return U , GAMMA


# THERMODYNAMIC CALCULATIONS (no z-averaging)

def are_equal_lambda_imp_ref(): # returns true if both have the same LAMBDA, false otherwise
    return get_lambda( 'param' )==get_lambda( '../ref/param' )


def are_equal_tmin_imp_ref(): # returns true if both have the same Tmin, false otherwise
    return get_tmin( 'param' )==get_tmin( '../ref/param' )


def change_ref_param_lambda_tmin( Lambda , tmin ): # to be called from imp/ directory
    ref_param = open( '../ref/param' , 'r' )
    new_param = open( '../ref/new_param' , 'w' )

    for Line in ref_param:
        line = Line.strip()
        if line!=[]:
            if line[:6]=='Lambda':
                new_param.write( "Lambda={}\n".format( Lambda ) )
            elif line[:4]=='Tmin':
                new_param.write( "Tmin={}\n".format( tmin ) )
            else: new_param.write( Line )
        else: new_param.write( "\n" )

    ref_param.close()
    new_param.close()

    subprocess.call([ 'mv' , '../ref/new_param' , '../ref/param' ])


def equalize_lambdas_and_tmins_imp_ref(): 
    # If lambdas or tmins are not equal, it changes them in ../ref and runs the nrg calculation there
    
    if ( not are_equal_lambda_imp_ref() ) or ( not are_equal_tmin_imp_ref() ):

        Lambda = get_lambda( 'param' )
        tmin = get_tmin( 'param' )

        change_ref_param_lambda_tmin( Lambda , tmin )

        os.chdir( '../ref' )
        subprocess.call( './0a_run' )
        os.chdir( '../imp' )


# THERMODYNAMICS CALCULATIONS - Z-AVG

def equalize_lambdas_and_tmins_imp_ref_zavg():  # if lambdas or tmins are not equal,
                                                   # it changes them in ../ref/.
                                                   # it does not run the nrg calculation there.
    if ( not are_equal_lambda_imp_ref() ) or ( not are_equal_tmin_imp_ref() ):

        Lambda = get_lambda( 'param' )
        tmin = get_tmin( 'param' )

        change_ref_param_lambda_tmin( Lambda , tmin )


# THERMODYNAMIC PLOTS


def plot_mag_susc( ax ):
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

    ax.plot( temp , mag_susc , label='impurity magnetic susceptibility' , color='blue' , linewidth=2 , linestyle='-' )
    ax.plot( temp , ff , color='grey' , linestyle='--' , label='ferromagetic freezing' )
    ax.plot( temp , lm, color='red', linestyle='--' , label="double local moment" )
    ax.plot( temp , fo, color='green' , linestyle='--' , label="double free orbital / local moment + strong coupling" )
    ax.plot( temp , clm , color='magenta' , linestyle='--' , label='free orbital + strong coupling' )
    ax.plot( temp , cs , color='brown' , linestyle='--' , label='complete screening' )

    ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8)

    ax.semilogx( base=10 )
    ax.set_xlabel( '$k_B T$' )
    ax.set_ylabel( '$k_B T \chi (T)$' )
    ax.set_xlim([ float( get_tmin( 'param' ) ) , 1e0 ])
    ax.set_ylim([0,1.2])


def plot_mag_susc_2( ax , colour='tab:blue' , llabel=0 ):
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
    ax.set_xlim([ float( get_tmin( 'param' ) ) , 1e0 ])
    ax.set_ylim([ 0 , ymax ])

    par = ax.twinx()
    par.set_ylim([ 0 , ymax ])
    par.set_yticks((0,0.125,0.25,0.5,0.666))
    par.set_yticklabels(('$0$ : CS','$1/8$ : FO-SC','$1/4$ : PS / FO','$1/2$ : LM','$2/3$ : FF'))

    ax.tick_params( labelsize=15 )
    par.tick_params( labelsize=10 )


def plot_entropy_2( ax , llabel=0 , colour='tab:blue' ):
    td_data = np.loadtxt( 'td_diff.dat' )
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

    ax.set_xlim([ float( get_tmin( 'param' ) ) , 1e0 ])
    
    ax.set_ylim([ 0 , ymax ])
    ax.set_yticks( np.arange( 0 , ymax , 1 ) )

    par = ax.twinx()
    par.set_ylim([ 0 , ymax ])
    par.set_yticks(( 0 , mt.log(2) , mt.log(3) , mt.log(4) , mt.log(16) ))
    par.set_yticklabels(('$\ln(1)$ : CS','$\ln(2)$ : PS','$\ln(3)$ : FF','$\ln(4)$ : LM / FO-SC','$\ln(16)$ : FO'))
    
    ax.tick_params( labelsize=15 )
    par.tick_params( labelsize=10 )


def plot_entropy( ax ):
    td_data = np.loadtxt( 'td_diff.dat' )
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

    ax.plot( temp , entropy , label='impurity entropy' , color='blue' , linewidth=2 , linestyle='-' )
    ax.plot( temp , fo , color='green' , linestyle='--' , label="double free orbital" )
    ax.plot( temp , lm , color='red', linestyle='--' , label="double local moment / free orbital + strong coupling" )
    ax.plot( temp , fc , color='grey' , linestyle='--' , label="ferromagnetic freezing" )
    ax.plot( temp , cm , color='brown' , linestyle='--' , label="local moment + strong coupling" )
    ax.plot( temp , fr , color='magenta' , linestyle='--' , label="complete screening" )

    ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8)

    ax.semilogx( base=10 )
    
    ax.set_xlabel( '$k_B T$' )
    ax.set_ylabel( '$ S/k_B (T)$' )
    
    ax.set_xlim([ float( get_tmin( 'param' ) ) , 1e0 ])
    ax.set_ylim([ 0 , 5 ])

    

def plot_heat_capacity( ax ):
    td_data = np.loadtxt( 'td_diff.dat' )
    c = td_data[:,6]
    temp = td_data[:,0]

    ax.plot( temp , c , label='impurity heat capacity' , color='blue' , linewidth=2 , linestyle='-' )

    ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8)

    ax.semilogx( base=10 )
    ax.set_xlabel( '$k_B T$' )
    ax.set_ylabel( '$C/k_B (T)$' )
    ax.set_xlim([ float( get_tmin( 'param' ) ) , 1e0 ])
    ax.set_ylim([ -0.2 , 1.0 ])


# EIGENFLOW PLOTS

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


# SPECTRAL PLOT

def plot_spectral( ax ):
    data = np.loadtxt( 'spec_FDM_dens_A_d-A_d.dat' )

    a = data[ : , 1 ]
    omega = data[ : , 0 ]

    ax.plot( omega , a , color='magenta' , linestyle='-' )
    
    ax.set_ylabel( "$A(\omega) D$" )
    ax.set_xlabel( "$\omega / D$" )

    ax.set_xlim([ -0.1 , 0.1 ])

    ax.set_title( 'Spectral function' )


# ARROWFLOW PLOT

def read_h0_eigenvalues():
    N = get_N( 'e-q0s2_table1.dat' )
    eigenvalues = np.empty( (int(N/2)+1 , 22) )
    datas = ["e-q0s2_table1.dat","e-q0s4_table1.dat","e-q1s1_table1.dat","e-q1s3_table1.dat","e-q2s2_table1.dat","e-q3s1_table1.dat"]

    eig_number = 0
    for filename in datas:
        f = open(filename,'r')

        for line in f:
            if line=="" or line=="\n":
                eig_number += 1
                continue
            n = int( int(line.split(" ")[0]) / 2 )
            eigenvalues[n,eig_number] = float( line.split()[1] )

        f.close()

    return eigenvalues

def read_h0_eigenvalues_lowest2():
    full_eigens = read_h0_eigenvalues()
    eigenvalues = np.empty( ( len(full_eigens[:,0]) , 10 ) )
    
    eigenvalues[ : , :2 ] = full_eigens[ : , :2  ]
    eigenvalues[ : ,  2 ] = full_eigens[ : ,  8  ]
    eigenvalues[ : , 3:5] = full_eigens[ : , 9:11]
    eigenvalues[ : , 5:7] = full_eigens[ : ,15:17]
    eigenvalues[ : , 7:9] = full_eigens[ : ,18:20]
    eigenvalues[ : , 9  ] = full_eigens[ : , 21  ]
    return np.array( eigenvalues )

def read_h0_eigenvalues_lowest():
    # Por cada subespacio, lee el autovalor más bajo de cada iteración.
    # Con todos ellos forma la lista que devuelve como output.

    N = get_N( 'e-q0s2_table1.dat' )
    eigenvalues = np.empty( (int(N/2)+1,6) )
    datas = ["e-q0s2_table1.dat","e-q0s4_table1.dat","e-q1s1_table1.dat","e-q1s3_table1.dat","e-q2s2_table1.dat","e-q3s1_table1.dat"]

    eigenvalues[:,:] = 100

    for ( filename , i ) in zip( datas , range(6) ):
        f = open(filename,'r')

        for line in f:
            if line=="" or line=="\n":
                continue
            n = int( int(line.split(" ")[0]) / 2 )
            if i < len( eigenvalues[n,:] ):
                if float( line.split()[1] ) < eigenvalues[n,i]:
                    eigenvalues[n,i] = float( line.split()[1] )

        f.close()

    return eigenvalues * get_nrg_scale()

def compute_h0_eigenvalues_sneg( u , g ):
    Lambda = get_lambda( 'param' )
    z = get_z()
    scale = ( 1 + Lambda**-1 ) / 2.0  *  Lambda**( 1.0 - z )

    u , g = scale_u_gamma( u , g )
    g = mt.abs( g )

    eigs = np.empty(22)

    eigs[0] = u
    eigs[1] = 0.5 * ( u - ( u**2 + 8*g )**0.5 )
    eigs[2] = 0.5 * ( 3*u - ( u**2 + 8*g )**0.5 )
    eigs[3] = 0.5 * ( u + ( u**2 + 8*g )**0.5 )
    eigs[4] = 0.5 * ( 3*u + ( u**2 + 8*g )**0.5 )
    eig5 = -1/6*(u**2 + 8*g)*(-1j*ct.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - 6*g*u \
            + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) \
            - 1/2*(u**3 - (u**2 - 4*g)*u - 6*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 \
            - 28*g**2*u**2 - 512/3*g**3))**(1/3)*(1j*mt.sqrt(3) + 1) + u
    eigs[5] = eig5.real
    eig6 = -1/6*(u**2 + 8*g)*(1j*ct.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - 6*g*u + \
            1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) - \
            1/2*(u**3 - (u**2 - 4*g)*u - 6*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - \
            28*g**2*u**2 - 512/3*g**3))**(1/3)*(-1j*ct.sqrt(3) + 1) + u
    eigs[6] = eig6.real
    eig7 = u + 1/3*(u**2 + 8*g)/(u**3 - (u**2 - 4*g)*u - 6*g*u + 1/3*ct.sqrt(-1/3*u**6 - \
            8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) + (u**3 - (u**2 - 4*g)*u - 6*g*u \
            + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3)
    eigs[7] = eig7.real

    eigs[8] = 0

    eigs[9] = 2 * u
    eigs[10] = 0.5 * ( 3*u - ( u**2 + 8*g )**0.5 )
    eigs[11] = 0.5 * ( 3*u + ( u**2 + 8*g )**0.5 )
    eig12 = -1/6*(u**2 + 8*g)*(-1j*mt.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - \
            2*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - \
            512/3*g**3))**(1/3) - 1/2*(u**3 - (u**2 - 4*g)*u - 2*g*u + \
            1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3)*(1j*ct.sqrt(3) + 1) + u
    eigs[12] = eig12.real
    eig13 = -1/6*(u**2 + 8*g)*(1j*mt.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - 2*g*u + \
            1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) - \
            1/2*(u**3 - (u**2 - 4*g)*u - 2*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - \
            28*g**2*u**2 - 512/3*g**3))**(1/3)*(-1j*mt.sqrt(3) + 1) + u
    eigs[13] = eig13.real
    eig14 = u + 1/3*(u**2 + 8*g)/(u**3 - (u**2 - 4*g)*u - 2*g*u + 1/3*ct.sqrt(-1/3*u**6 \
            - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) + (u**3 - (u**2 - 4*g)*u - \
            2*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3)
    eigs[14] = eig14.real

    eigs[15] = u
    eigs[16] = 0.5 * ( u - ( u**2 + 8*g )**0.5 )
    eigs[17] = 0.5 * ( u + ( u**2 + 8*g )**0.5 )

    eigs[18] = u
    eigs[19] = 0.5 * ( 3*u - ( u**2 + 8*g )**0.5 )
    eigs[20] = 0.5 * ( 3*u + ( u**2 + 8*g )**0.5 )

    eigs[21] = 2*u

    return ( eigs - eigs.min() ) * scale


def compute_h0_eigenvalues_sneg_lowest( u , g ):
    Lambda = get_lambda( 'param' )
    z = get_z()
    scale = ( 1 + Lambda**-1 ) / 2.0  *  Lambda**( 1.0 - z )

    u , g = scale_u_gamma( u , g )

    eigs = np.empty(22)
    lowest_eigs = np.empty(6)

    eigs[0] = u
    eigs[1] = 0.5 * ( u - ( u**2 + 8*g )**0.5 )
    eigs[2] = 0.5 * ( 3*u - ( u**2 + 8*g )**0.5 )
    eigs[3] = 0.5 * ( u + ( u**2 + 8*g )**0.5 )
    eigs[4] = 0.5 * ( 3*u + ( u**2 + 8*g )**0.5 )
    eig5 = -1/6*(u**2 + 8*g)*(-1j*ct.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - 6*g*u \
            + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) \
            - 1/2*(u**3 - (u**2 - 4*g)*u - 6*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 \
            - 28*g**2*u**2 - 512/3*g**3))**(1/3)*(1j*mt.sqrt(3) + 1) + u
    eigs[5] = eig5.real
    eig6 = -1/6*(u**2 + 8*g)*(1j*ct.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - 6*g*u + \
            1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) - \
            1/2*(u**3 - (u**2 - 4*g)*u - 6*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - \
            28*g**2*u**2 - 512/3*g**3))**(1/3)*(-1j*ct.sqrt(3) + 1) + u
    eigs[6] = eig6.real
    eig7 = u + 1/3*(u**2 + 8*g)/(u**3 - (u**2 - 4*g)*u - 6*g*u + 1/3*ct.sqrt(-1/3*u**6 - \
            8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) + (u**3 - (u**2 - 4*g)*u - 6*g*u \
            + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3)
    eigs[7] = eig7.real
    lowest_eigs[0] = np.amin( eigs[:8] )

    eigs[8] = 0
    lowest_eigs[1] = 0

    eigs[9] = 2 * u
    eigs[10] = 0.5 * ( 3*u - ( u**2 + 8*g )**0.5 )
    eigs[11] = 0.5 * ( 3*u + ( u**2 + 8*g )**0.5 )
    eig12 = -1/6*(u**2 + 8*g)*(-1j*mt.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - \
            2*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - \
            512/3*g**3))**(1/3) - 1/2*(u**3 - (u**2 - 4*g)*u - 2*g*u + \
            1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3)*(1j*ct.sqrt(3) + 1) + u
    eigs[12] = eig12.real
    eig13 = -1/6*(u**2 + 8*g)*(1j*mt.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - 2*g*u + \
            1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) - \
            1/2*(u**3 - (u**2 - 4*g)*u - 2*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - \
            28*g**2*u**2 - 512/3*g**3))**(1/3)*(-1j*mt.sqrt(3) + 1) + u
    eigs[13] = eig13.real
    eig14 = u + 1/3*(u**2 + 8*g)/(u**3 - (u**2 - 4*g)*u - 2*g*u + 1/3*ct.sqrt(-1/3*u**6 \
            - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) + (u**3 - (u**2 - 4*g)*u - \
            2*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3)
    eigs[14] = eig14.real
    lowest_eigs[2] = np.amin( eigs[9:15] )

    eigs[15] = u
    eigs[16] = 0.5 * ( u - ( u**2 + 8*g )**0.5 )
    eigs[17] = 0.5 * ( u + ( u**2 + 8*g )**0.5 )
    lowest_eigs[3] = np.amin( eigs[15:18] )

    eigs[18] = u
    eigs[19] = 0.5 * ( 3*u - ( u**2 + 8*g )**0.5 )
    eigs[20] = 0.5 * ( 3*u + ( u**2 + 8*g )**0.5 )
    lowest_eigs[4] = np.amin( eigs[18:21] )

    eigs[21] = 2*u
    lowest_eigs[5] = eigs[21]

    return ( lowest_eigs - eigs.min() ) * scale



def compute_h0_eigenvalues_siam( U , GAMMA ):
    Lambda = get_lambda( 'param' )
    z = get_z()
    scale = ( 1 + Lambda**-1 ) / 2.0  *  Lambda**( 1.0 - z )

    U = (  2.0  /  ( 1 + Lambda**-1 )  ) * U / 2.0
    GAMMA = (  2.0  /  ( 1 + Lambda**-1 )  )**2 * 2.0 * GAMMA / mt.pi

    eigenvalues = np.empty( 7 )
    eigs = np.empty( 4 )

    eigenvalues[0] = 0
    eigenvalues[1] = 0.5 * ( U**2 + 16*GAMMA )**0.5 + 0.5 * U
    eigenvalues[2] = ( U**2 + 16*GAMMA )**0.5
    eigenvalues[:3] = np.sort( eigenvalues[:3] )
    eigs[0] = np.min( eigenvalues[:3] )

    eigenvalues[3] = 0.5*( U**2 + 16*GAMMA )**0.5 - 0.5*U
    eigs[1] = eigenvalues[3]

    eigenvalues[4] = 0.5*( U**2 + 16*GAMMA )**0.5 - 0.5*( U**2 + 4*GAMMA )**0.5
    eigenvalues[5] = 0.5*( U**2 + 16*GAMMA )**0.5 + 0.5*( U**2 + 4*GAMMA )**0.5
    eigenvalues[4:6] = np.sort( eigenvalues[4:6] )
    eigs[2] = np.min( eigenvalues[4:6] )

    eigenvalues[6] = 0.5*( U**2 + 16*GAMMA )**0.5 + 0.5*U
    eigs[3] = eigenvalues[6]

    return eigs * scale

def compute_h0_eigenvalues_sneg_lowest2( u , g ):
    Lambda = get_lambda( 'param' )
    z = get_z()
    scale = ( 1 + Lambda**-1 ) / 2.0  *  Lambda**( 1.0 - z )

    u , g = scale_u_gamma( u , g )

    eigs = np.empty(22)

    eigs[0] = u
    eigs[1] = 0.5 * ( u - ( u**2 + 8*g )**0.5 )
    eigs[2] = 0.5 * ( 3*u - ( u**2 + 8*g )**0.5 )
    eigs[3] = 0.5 * ( u + ( u**2 + 8*g )**0.5 )
    eigs[4] = 0.5 * ( 3*u + ( u**2 + 8*g )**0.5 )
    eig5 = -1/6*(u**2 + 8*g)*(-1j*ct.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - 6*g*u \
            + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) \
            - 1/2*(u**3 - (u**2 - 4*g)*u - 6*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 \
            - 28*g**2*u**2 - 512/3*g**3))**(1/3)*(1j*mt.sqrt(3) + 1) + u
    eigs[5] = eig5.real
    eig6 = -1/6*(u**2 + 8*g)*(1j*ct.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - 6*g*u + \
            1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) - \
            1/2*(u**3 - (u**2 - 4*g)*u - 6*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - \
            28*g**2*u**2 - 512/3*g**3))**(1/3)*(-1j*ct.sqrt(3) + 1) + u
    eigs[6] = eig6.real
    eig7 = u + 1/3*(u**2 + 8*g)/(u**3 - (u**2 - 4*g)*u - 6*g*u + 1/3*ct.sqrt(-1/3*u**6 - \
            8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) + (u**3 - (u**2 - 4*g)*u - 6*g*u \
            + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3)
    eigs[7] = eig7.real

    eigs[8] = 0

    eigs[9] = 2 * u
    eigs[10] = 0.5 * ( 3*u - ( u**2 + 8*g )**0.5 )
    eigs[11] = 0.5 * ( 3*u + ( u**2 + 8*g )**0.5 )
    eig12 = -1/6*(u**2 + 8*g)*(-1j*mt.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - \
            2*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - \
            512/3*g**3))**(1/3) - 1/2*(u**3 - (u**2 - 4*g)*u - 2*g*u + \
            1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3)*(1j*ct.sqrt(3) + 1) + u
    eigs[12] = eig12.real
    eig13 = -1/6*(u**2 + 8*g)*(1j*mt.sqrt(3) + 1)/(u**3 - (u**2 - 4*g)*u - 2*g*u + \
            1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) - \
            1/2*(u**3 - (u**2 - 4*g)*u - 2*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - \
            28*g**2*u**2 - 512/3*g**3))**(1/3)*(-1j*mt.sqrt(3) + 1) + u
    eigs[13] = eig13.real
    eig14 = u + 1/3*(u**2 + 8*g)/(u**3 - (u**2 - 4*g)*u - 2*g*u + 1/3*ct.sqrt(-1/3*u**6 \
            - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3) + (u**3 - (u**2 - 4*g)*u - \
            2*g*u + 1/3*ct.sqrt(-1/3*u**6 - 8*g*u**4 - 28*g**2*u**2 - 512/3*g**3))**(1/3)
    eigs[14] = eig14.real

    eigs[15] = u
    eigs[16] = 0.5 * ( u - ( u**2 + 8*g )**0.5 )
    eigs[17] = 0.5 * ( u + ( u**2 + 8*g )**0.5 )

    eigs[18] = u
    eigs[19] = 0.5 * ( 3*u - ( u**2 + 8*g )**0.5 )
    eigs[20] = 0.5 * ( 3*u + ( u**2 + 8*g )**0.5 )

    eigs[21] = 2*u
    
    lowest2 = np.empty( 10 )
    lowest2[0] = np.sort( eigs[:8] )[0]
    lowest2[1] = np.sort( eigs[:8] )[1]
    lowest2[2] = eigs[8]
    lowest2[3] = np.sort( eigs[9:15] )[0]
    lowest2[4] = np.sort( eigs[9:15] )[1]
    lowest2[5] = np.sort( eigs[15:18] )[0]
    lowest2[6] = np.sort( eigs[15:18] )[1]
    lowest2[7] = np.sort( eigs[18:21] )[0]
    lowest2[8] = np.sort( eigs[18:21] )[1]
    lowest2[9] = eigs[21]

    return ( lowest2 - eigs.min() ) * scale


def plot_arrows( U_array , GAMMA_array , ax , colour='tab:blue' , fixedpoints=False , multi=False ):
    plt.quiver(GAMMA_array[:-1], U_array[:-1], GAMMA_array[1:]-GAMMA_array[:-1], U_array[1:]-U_array[:-1], \
        scale_units='xy', angles='xy', scale=1, width=0.005, color=colour)
    
    ax.set_xlabel( '$ \Gamma_{eff} $' , fontsize=15 )
    ax.set_ylabel('$ U_{eff} $' , fontsize=15 )
    ax.tick_params( labelsize=15 )

    x_lim = 1.6 if multi else 1.3
    y_lim = 7.0
    
    ax.set_xlim([-0.025,x_lim])
    ax.set_ylim([-0.1,y_lim])
    
    ax.set_xticks( np.arange( 0 , x_lim+0.1 , 0.2 ) )
    ax.set_yticks( np.arange( -3.0 , y_lim+0.1 , 1 ) )
    
    if fixedpoints: include_fixedpoints( ax , multi=multi )

def include_fixedpoints( ax , multi=False ):
    fo = [ 0 , 0 ]
    ps = [ 0.94 , 2.38 ]
    ff = [ 0.3 , 4.7 ]
    fosc = [ 0.47 , 0 ]
    cs = [ 0.94 , -2.4 ]
    lm = [ 0 , 3.15 ]

    ms = 5
    
    ax.plot( fo[0] , fo[1] , marker='+' , markersize=ms , color='black' )
    ax.plot( ps[0] , ps[1] , marker='x' , markersize=ms , color='black' )
    ax.plot( ff[0] , ff[1] , marker='2' , markersize=ms , color='black' )
    ax.plot( fosc[0] , fosc[1] , marker='3' , markersize=ms , color='black' )
    ax.plot( cs[0] , cs[1] , marker='x' , markersize=ms , color='black' )
    ax.plot( lm[0] , lm[1] , marker='1' , markersize=ms , color='black' )

    ax.annotate( '$H_{FO}$' , ( -0.15 , -0.3 ) , fontsize=15 )
    ax.annotate( '$H_{PS}$' , ( ps[0]+0.05 , ps[1]+0.05 ) , fontsize=15 )
    ax.annotate( '$H_{FF}$' , ( ff[0] , ff[1]+0.1 ) , fontsize=15 )
    ax.annotate( '$H_{FO-SC}$' , ( 0.6 , fosc[1]-0.1 ) , fontsize=15 )
    ax.annotate( '$H_{CS}$' , ( cs[0]+0.1 , cs[1]-0.3 ) , fontsize=15 )
    ax.annotate( '$H_{LM}$' , ( lm[0]-0.15 , lm[1]+0.1 ) , fontsize=15 )

    x_lim = 1.6 if multi else 1.3
    y_lim = 5.5

    ax.set_xlim([ -0.15 , x_lim ])
    ax.set_ylim([ -3.0 , y_lim ])


def include_fixedpoints_siam( ax , multi=False ):
    fo = [ 0 , 0 ]
    ff = [ 0.42 , 2 ]
    ps = [ 0.87 , 0 ]
    fosc = [ 0.34 , -2 ]
    cs = [ 0.94 , -2.4 ]
    lm = [ 0 , 3.15 ]

    ms = 5
    
    #ax.plot( fo[0] , fo[1] , marker='+' , markersize=ms , color='black' )
    #ax.plot( ps[0] , ps[1] , marker='x' , markersize=ms , color='black' )
    #ax.plot( ff[0] , ff[1] , marker='2' , markersize=ms , color='black' )
    #ax.plot( fosc[0] , fosc[1] , marker='3' , markersize=ms , color='black' )
    #ax.plot( cs[0] , cs[1] , marker='x' , markersize=ms , color='black' )
    #ax.plot( lm[0] , lm[1] , marker='1' , markersize=ms , color='black' )

    ax.annotate( '$H_{FO}$' , ( -0.1 , -0.3 ) )
    ax.annotate( '$H_{PS}$' , ( 0.97 , ps[1]+0.08 ) )
    ax.annotate( '$H_{FF}$' , ( ff[0] , ff[1]+0.1 ) )
    ax.annotate( '$H_{FO-SC}$' , ( 0.55 , fosc[1]-0.6 ) )
    #ax.annotate( '$H_{CS}$' , ( cs[0] , cs[1]-0.3 ) )
    ax.annotate( '$H_{LM}$' , ( lm[0]-0.1 , lm[1]+0.1 ) )

    x_lim = 1 
    y_lim = 5 if multi else 4

    ax.set_xlim([ -0.15 , x_lim ])
    ax.set_ylim([ -8.0 , y_lim ])
