#!/usr/bin/env wolframscript
(* ::Package:: *)

<<sneg`sneg`

Import["../../diagonalize.m"]

snegfermionoperators[d,a,f]
snegrealconstants[U,RKKY,J]


(* Constants and parameters *)

\[CapitalLambda] = 2.5;
scale = ( 1 + \[CapitalLambda]^-1 ) / 2.0;

(* u = N[ 0.5 * scale^-1 * ToExpression@$ScriptCommandLine[[2]] , 20 ]
\[Gamma]df = N[ scale^-2 * 2 * ToExpression@$ScriptCommandLine[[3]] / \[Pi] , 20 ]
\[Gamma]ff = N[ scale^-2 * 2 * ToExpression@$ScriptCommandLine[[4]] / \[Pi] , 20 ] *)


(* Hamiltonian definition *)

Hd = U pow[ number[d[]]-1 , 2 ];
Ha = U pow[ number[a[]]-1 , 2 ];

Had = RKKY spinspin[ d[] , a[] ];

Hk = J Simplify[ ( spinxyz[d[]] + spinxyz[a[]] ) ~ inner ~ spinxyz[f[]] ];

H = Hd + Ha + Had + Hk


(* Hamiltonian matrix setup *)

basisops = { a[] , d[] , f[] };
diagSetupBasisQS[];
diagSetupHam[];


(* Diagonalization *)

diagonalize[{U->U,RKKY->RKKY,J->J}];
eig2[[All,1]]
eig2[[All,2,1]]//MatrixForm



