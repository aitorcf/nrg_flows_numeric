#!/usr/bin/env python3

import subprocess
import os
import numpy as np
import math as mt
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


def equalize_lambdas_and_tmins_imp_ref(): # if lambdas or tmins are not equal, it changes them in ../ref and runs the nrg calculation there
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

def plot_mag_susc_2( ax , colour='tab:blue' , llabel=0 , llinestyle=None , labels=True ):
    td_data = np.loadtxt( 'td_diff.dat' )
    mag_susc = td_data[:,1]
    temp = td_data[:,0]

    fo = np.zeros((len(temp)))
    lm = np.zeros((len(temp)))
    sc = np.zeros((len(temp)))

    lm[:] = 0.25
    fo[:] = 0.125
    sc[:] = 0.0

    if llabel!=0:
        ax.plot( temp , mag_susc , label=llabel , color=colour , linewidth=2 , linestyle=llinestyle )
        ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 , fontsize=15 )
        ymax=0.6
    else:
        ax.plot( temp , mag_susc , color=colour , linewidth=2 , linestyle=llinestyle )
        ymax=0.3

    ax.plot( temp , lm, color='black', linestyle='--' , linewidth=0.5 )
    ax.plot( temp , fo, color='black' , linestyle='--' , linewidth=0.5 )
    ax.plot( temp , sc , color='black' , linestyle='--' , linewidth=0.5 )

    ax.semilogx( base=10 )
    ax.set_xlabel( '$k_B T$' , fontsize=15 )
    ax.set_ylabel( '$k_B T \chi (T)$' , fontsize=15 )
    ax.set_xlim([ float( get_tmin( 'param' ) ) , 1e0 ])
    ax.set_ylim([ 0 , ymax ])
    ax.set_yticks( np.arange( 0 , ymax+0.05 , 0.1 ) )
    ax.tick_params( labelsize=15 )
    ax.set_xticks( np.exp( np.arange(-15,0.5,3)  ) )

    if labels:
        par = ax.twinx()
        par.set_ylim([ 0 , ymax ])
        par.set_yticks((0,0.125,0.25))
        par.set_yticklabels(('$0$ : SC','$1/8$ : FO','$1/4$ : LM'))
        par.tick_params( labelsize=15 )

def plot_entropy_2( ax , llabel=None , colour='tab:blue' , llinestyle=None , labels=True ):
    td_data = np.loadtxt( 'td_diff.dat' )
    entropy = td_data[:,8]
    temp = td_data[:,0]

    fo = np.zeros((len(temp)))
    lm = np.zeros((len(temp)))
    sc = np.zeros((len(temp)))

    lm[:] = mt.log( 2 )
    fo[:] = mt.log( 4 )
    sc[:] = mt.log( 1 )

    if llabel!=None:
        ax.plot( temp , entropy , label=llabel , color=colour , linewidth=2 , linestyle=llinestyle )
        ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8 , fontsize=15 )
        ymax=mt.log( 4 )+0.5
    else:
        ax.plot( temp , entropy , color=colour , linewidth=2 , linestyle=llinestyle )
        ymax=mt.log( 4 ) + 0.5
    ax.plot( temp , fo , linestyle='--' , color='black' , linewidth=0.5 )
    ax.plot( temp , lm , linestyle='--' , color='black' , linewidth=0.5 )
    ax.plot( temp , sc , linestyle='--' , color='black' , linewidth=0.5 )
    
    ax.set_xticks( np.exp( np.arange(-15,0.5,3)  ) )
    ax.semilogx( base=10 )

    ax.set_xlabel( '$k_B T$' , fontsize=15 )
    ax.set_ylabel( '$ S/k_B (T)$' , fontsize=15 )

    ax.set_xlim([ float( get_tmin( 'param' ) ) , 1e0 ])

    ax.set_ylim([ 0 , ymax ])
    ax.set_yticks( np.arange( 0 , ymax , 0.5 ) )
    ax.tick_params( labelsize=15 )

    if labels:
        par = ax.twinx()
        par.set_ylim([ 0 , ymax ])
        par.set_yticks(( 0 , mt.log(2) , mt.log(4) ))
        par.set_yticklabels(( '$\ln(1)$ : SC' , '$\ln(2)$ : LM' , '$\ln(4)$ : FO' ))
        par.tick_params( labelsize=15 )


def plot_mag_susc( ax ):
    td_data = np.loadtxt( 'td_diff.dat' )
    mag_susc = td_data[:,1]
    temp = td_data[:,0]
    
    fo = np.zeros((len(temp)))
    lm = np.zeros((len(temp)))
    sc = np.zeros((len(temp)))
    lm[:] = 0.25
    fo[:] = 0.125
    sc[:] = 0.0

    ax.plot( temp , mag_susc , label='impurity magnetic susceptibility' , color='blue' , linewidth=2 , linestyle='-' )
    ax.plot( temp , lm, color='red', linestyle='--' , label="local moment" )
    ax.plot( temp , fo, color='green' , linestyle='--' , label="free orbital" )
    ax.plot( temp , sc , color='brown' , linestyle='--' , label="strong coupling" )

    ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8)

    ax.semilogx( base=10 )
    ax.set_xlabel( '$k_B T$' )
    ax.set_ylabel( '$k_B T \chi (T)$' )
    ax.set_xlim([ float( get_tmin( 'param' ) ) , 1e0 ])
    ax.set_ylim([0,0.35])


def plot_entropy( ax ):
    td_data = np.loadtxt( 'td_diff.dat' )
    entropy = td_data[:,8]
    temp = td_data[:,0]

    fo = np.zeros((len(temp)))
    lm = np.zeros((len(temp)))
    sc = np.zeros((len(temp)))
    lm[:] = mt.log( 2 )
    fo[:] = mt.log( 4 )
    sc[:] = 0

    ax.plot( temp , entropy , label='impurity entropy' , color='blue' , linewidth=2 , linestyle='-' )
    ax.plot( temp , lm , color='red', linestyle='--' , label="local moment" )
    ax.plot( temp , fo , color='green' , linestyle='--' , label="free orbital" )
    ax.plot( temp , sc , color='brown' , linestyle='--' , label="strong coupling" )

    ax.legend( loc='upper left' , frameon=True , facecolor='white' , edgecolor='white' , framealpha=0.8)

    ax.semilogx( base=10 )
    ax.set_xlabel( '$k_B T$' )
    ax.set_ylabel( '$ S/k_B (T)$' )
    ax.set_xlim([ float( get_tmin( 'param' ) ) , 1e0 ])
    ax.set_ylim([ 0 , mt.log( 5 ) ])


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
    ax.set_ylim([ -0.2 , 0.5 ])


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
                    line.set_label( kwargs['label'] )
                return
            slot = 0
            continue
        
        if slot < n_slots:
            eigenvalues[slot,eigenvalue] = line.split(' ')[1]
        slot += 1

def label_flowplot(n_steps,n_eigenvalues,ax):
    if n_steps%2==0:
        ax.set_xlabel( 'N (even)' , fontsize=15 )
        ax.set_xticks(np.arange(0,n_steps,20))
    else:
        ax.set_xlabel( 'N (odd)' , fontsize=15 )
        ax.set_xticks(np.arange(5,n_steps,20))
    ax.set_ylabel( 'E' , fontsize=15 )


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

def get_table1_subspace(subspace,N):
    if subspace=='q0s1':
        q0s1 = np.empty( (int(N/2),3) )
        f_q0s1 = open('e-q0s1_table1.dat','r')
        count=0
        n=0
        for line in f_q0s1:
            if line=="\n" or line=="":
                count += 1
                n = 0
                continue
            if n >= int(N/2):
                continue
            q0s1[n,count] = line.split()[1]
            n += 1
        f_q0s1.close()
        return q0s1

    if subspace=='q0s3':
        q0s3 = np.empty( int(N/2) )
        f_q0s3 = open('e-q0s3_table1.dat','r')
        count=0
        n=0
        for line in f_q0s3:
            if line=="\n" or line=="":
                count += 1
                n = 0
                continue
            if n >= int(N/2):
                continue
            q0s3[n] = line.split()[1]
            n += 1
        f_q0s3.close()
        return q0s3

    if subspace=='q1s2':
        q1s2 = np.empty( (int(N/2),2) )
        f_q1s2 = open('e-q1s2_table1.dat','r')
        count=0
        n=0
        for line in f_q1s2:
            if line=="\n" or line=="":
                count += 1
                n = 0
                continue
            if n >= int(N/2):
                continue
            q1s2[n,count] = line.split()[1]
            n += 1
        f_q1s2.close()
        return q1s2

    if subspace=='q2s1':
        q2s1 = np.empty( int(N/2) )
        f_q2s1 = open( 'e-q2s1_table1.dat' , 'r' )
        count=0
        n=0
        for line in f_q2s1:
            if line=="\n" or line=="":
                count += 1
                n = 0
                continue
            if n >= int( N/2 ):
                continue
            q2s1[n] = line.split()[1]
            n += 1
        f_q2s1.close()
        return q2s1


def include_fixedpoints( ax , **kwargs ):
    colors = False
    
    lm = [ 0 , 3.148 ]
    sc = [ 0.94 , 0 ]

    if 'colors' in kwargs:
        colors = kwargs['colors']    
    if colors:
        ax.plot( 0 , 0 , marker='*' , markersize=5 , color='blue' )
        ax.plot( 0 ,2.75 , marker='*' , markersize=5 , color='red' )
        ax.plot( 0.76 , 0.0 , marker='*' , markersize=5 , color='green' )
    else:
        ax.plot( 0 , 0 , marker='*' , markersize=5 , color='black' )
        ax.plot( lm[0] , lm[1] , marker='*' , markersize=5 , color='black' )
        ax.plot( sc[0] , sc[1] , marker='*' , markersize=5 , color='black' )
    
    xlim = 1.2
    ax.set_xlim([ -0.12 , xlim ])
    ax.set_xticks( np.arange( 0 , xlim , 0.25 ) )
    ylim = 4.0
    ax.set_ylim([ -0.3 , ylim ])
    ax.set_yticks( np.arange( 0 , ylim+0.1 , 1 ) )
    
    ax.annotate( '$H_{FO}$' , ( -0.1 , -0.2 ) , fontsize=15 )
    ax.annotate( '$H_{LM}$' , ( -0.1 , lm[1]+0.08 ) , fontsize=15 )
    ax.annotate( '$H_{SC}$' , ( sc[0]+0.02 , -0.15 ) , fontsize=15 )


def plot_arrows( U_array , GAMMA_array , ax , **kwargs ):
    if 'color' in kwargs:
        plt.quiver(GAMMA_array[:-1], U_array[:-1], GAMMA_array[1:]-GAMMA_array[:-1], U_array[1:]-U_array[:-1], \
            scale_units='xy', angles='xy', scale=1, width=0.005, color=kwargs['color'])
    else:
        plt.quiver(GAMMA_array[:-1], U_array[:-1], GAMMA_array[1:]-GAMMA_array[:-1], U_array[1:]-U_array[:-1], \
            scale_units='xy', angles='xy', scale=1, width=0.005)

    xlims = [-0.025,1.5]
    xticks = np.arange( 0 , xlims[1] , 0.25)
    ylims = [-0.1,4.0]
    yticks = np.arange( 0 , ylims[1] , 1 )
    
    ax.set_xlabel( '$ \Gamma_{\mathrm{eff}} $' , fontsize=15 )
    ax.set_ylabel( '$ U_{\mathrm{eff}} $' , fontsize=15 )
    ax.set_xlim( xlims )
    ax.set_ylim( ylims )
    ax.set_xticks( xticks )
    ax.set_yticks( xlims )
    if 'fixedpoints' in kwargs and kwargs['fixedpoints']==True:
        include_fixedpoints(ax)


def plot_arrow_diagram( ax , colour='black' , fixedpoints=False ):
    N = get_N( 'e-q0s1_table1.dat' )
    U_param, GAMMA_param = get_u_gamma()
    Lambda = get_lambda( 'param' )

    nrg_eigenvalues = read_nrg_eigenvalues_abs()

    def F(in_array):
        U = in_array[0]
        GAMMA = in_array[1]

        analytic_eigenvalues = compute_h0_eigenvalues_abs( U , GAMMA )

        return analytic_eigenvalues - nrg_eigenvalues_step

    U_array = np.empty( int(N/2) )
    GAMMA_array = np.empty( int(N/2) )
    nrg_eigenvalues_step = np.empty( 7 )
    errors = open( 'arrowflow_errors.dat' , 'w' )
    points = open( 'arrowflow_points.dat' , 'w' )
    for n in range(0,int(N/2)):
        nrg_eigenvalues_step = nrg_eigenvalues[ n , : ]

        res = opt.least_squares( F , [0.15,0.15] , bounds=([0,0],[50,50]))
        
        U_array[n] = res.x[0]
        GAMMA_array[n] = res.x[1]
        errors.write( f"step {2*n}:\ncost = {res.cost}\noptimality = {res.optimality}\nresiduals = {res.fun}\n\n" )
        points.write( f"{U_array[n]} {GAMMA_array[n]}\n" )
    errors.close()
    points.close()

    u , g = get_u_gamma()

    plot_arrows( U_array , GAMMA_array , ax , fixedpoints=fixedpoints , color=colour )
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.tick_params( labelsize=15 )

def plot_arrow_diagram_WM( ax , colour='black' , fixedpoints=False ):
    N = get_N( 'e-q0s1_table1.dat' )
    U_param, GAMMA_param = get_u_gamma()
    Lambda = get_lambda( 'param' )

    nrg_eigenvalues = read_nrg_eigenvalues_abs()

    def F(in_array):
        U = in_array[0]
        GAMMA = in_array[1]
        
        subprocess.call([ 'wolframscript' ,  'compute_eigenvalues.wls' , f'{U}' , f'{GAMMA}' ])
        
        analytic_eigenvalues_WM = []
        with open( 'm_eigenvalues.dat' ) as f:
            for line in f:
                analytic_eigenvalues_WM.append( float( line.strip() ) )
        analytic_eigenvalues_WM = np.array( analytic_eigenvalues_WM )
        analytic_eigenvalues = compute_h0_eigenvalues_abs( U , GAMMA )
        
        print( "EIGENVALUE COMPARISON" )
        print( "Python eigenvalues:" )
        print( analytic_eigenvalues )
        print( "Mathematica eigenvalues:" )
        print( analytic_eigenvalues_WM  )
        print( "NRG eigenvalues:" )
        print( nrg_eigenvalues_step  )
        print( "\n" )
         
        return analytic_eigenvalues_WM - nrg_eigenvalues_step

    U_array = np.empty( int(N/2) )
    GAMMA_array = np.empty( int(N/2) )
    nrg_eigenvalues_step = np.empty( 7 )
    errors = open( 'arrowflow_errors.dat' , 'w' )
    points = open( 'arrowflow_points.dat' , 'w' )
    for n in range(0,int(N/2)):
        nrg_eigenvalues_step = nrg_eigenvalues[ n , : ]

        res = opt.least_squares( F , [0.15,0.15] , bounds=([0,0],[50,50]))
        
        U_array[n] = res.x[0]
        GAMMA_array[n] = res.x[1]
        errors.write( f"step {2*n}:\ncost = {res.cost}\noptimality = {res.optimality}\nresiduals = {res.fun}\n\n" )
        points.write( f"{U_array[n]} {GAMMA_array[n]}\n" )
    errors.close()
    points.close()

    u , g = get_u_gamma()

    plot_arrows( U_array , GAMMA_array , ax , fixedpoints=fixedpoints , color=colour )
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.tick_params( labelsize=15 )
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

def get_nrg_scale():
    Lambda = get_lambda( 'param' )
    z = get_z()

    if get_discretization()=='Y':
        return ( 1 + Lambda**-1 ) / 2.0  *  Lambda**( 1.5 - z )

    else:
        return ( 1 - Lambda**-1 ) / mt.log( Lambda ) * Lambda**( 1.5 - z )


def compute_h0_eigenvalues_abs( U , GAMMA ):
    Lambda = get_lambda( 'param' )
    z = get_z()
    scale = ( 1 + Lambda**-1 ) / 2.0  *  Lambda**( 1.0 - z )

    U = (  2.0  /  ( 1 + Lambda**-1 )  ) * U / 2.0
    GAMMA = (  2.0  /  ( 1 + Lambda**-1 )  )**2 * 2.0 * GAMMA / mt.pi

    eigenvalues = np.empty( 7 )

    eigenvalues[0] = 0
    eigenvalues[1] = 0.5 * ( U**2 + 16*GAMMA )**0.5 + 0.5 * U
    eigenvalues[2] = ( U**2 + 16*GAMMA )**0.5
    eigenvalues[:3] = np.sort( eigenvalues[:3] )

    eigenvalues[3] = 0.5*( U**2 + 16*GAMMA )**0.5 - 0.5*U

    eigenvalues[4] = 0.5*( U**2 + 16*GAMMA )**0.5 - 0.5*( U**2 + 4*GAMMA )**0.5
    eigenvalues[5] = 0.5*( U**2 + 16*GAMMA )**0.5 + 0.5*( U**2 + 4*GAMMA )**0.5
    eigenvalues[4:6] = np.sort( eigenvalues[4:6] )

    eigenvalues[6] = 0.5*( U**2 + 16*GAMMA )**0.5 + 0.5*U

    return eigenvalues * scale


def read_nrg_eigenvalues_abs():
    N = int( get_N( 'e-q0s1_table1.dat' ) )

    eigenvalues = np.empty( ( N // 2 , 7 ) )

    eigenvalues[ : , :3 ] = np.sort( get_table1_subspace('q0s1',N) )
    eigenvalues[ : , 3 ] = get_table1_subspace('q0s3',N )
    eigenvalues[ : , 4:6 ]= np.sort( get_table1_subspace('q1s2',N) )
    eigenvalues[ : , 6 ] = get_table1_subspace('q2s1',N)

    return eigenvalues * get_nrg_scale()


def plot_arrows_colors(U_array,GAMMA_array,ax,**kwargs):
    x = GAMMA_array[:-1]
    y = U_array[:-1]
    u = GAMMA_array[1:]-GAMMA_array[:-1]
    v = U_array[1:]-U_array[:-1]
    x_scaled = x / 0.76
    y_scaled = y / 2.75
    colors = (1 - y_scaled) * np.sign(y_scaled + x/0.4 - 1)
    norm = Normalize()
    norm.autoscale(np.array([-1,1]))
    colormap = cm.brg
    plt.quiver(x, y, u, v, scale_units='xy', angles='xy', scale=1, width=0.005, color=colormap(norm(colors)))
    ax.set_xlabel('$ \Gamma_{eff} $')
    ax.set_ylabel("$ U_{eff} $")
    ax.set_xlim([-0.025,0.8])
    ax.set_ylim([-0.05,3.0])
    ax.set_xticks( np.arange(0,2.1,0.2) )
    ax.set_yticks( np.arange(0,4.1,0.5) )
    custom_lines = [Line2D([0], [0], color=colormap(0.), lw=2),
                    Line2D([0], [0], color=colormap(.5), lw=2),
                    Line2D([0], [0], color=colormap(1.), lw=2)]
    ax.legend(custom_lines, ['FO', 'LM', 'SC'], \
            loc="upper right",frameon=True,framealpha=0.7,facecolor='white',edgecolor='white')
    if 'fixedpoints' in kwargs and kwargs['fixedpoints']==True:
        include_fixedpoints(ax,colors=True)
