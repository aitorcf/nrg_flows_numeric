#!/usr/bin/env wolframscript
(* ::Package:: *)

<<sneg`sneg`

Import["../../diagonalize.m"]

snegfermionoperators[d,a,fe,fo]
snegrealconstants[U,\[CapitalGamma]e,Jo]


(* Constants and parameters *)

\[CapitalLambda] = 2.5;
scale = ( 1 + \[CapitalLambda]^-1 ) / 2.0;

u = 0.1
\[Gamma]e = 0.3
jo = 0.2

(* u = N[ 0.5 * scale^-1 * ToExpression@$ScriptCommandLine[[2]] , 50 ];
\[Gamma]e = N[ scale^-2 * 2 * ToExpression@$ScriptCommandLine[[3]] / \[Pi] , 50 ];
jo = N[ ToExpression@$ScriptCommandLine[[4]] , 50 ]; *)


(* Hamiltonian definition *)

Hd = U pow[ number[d[]]-1 , 2 ];
Ha = U pow[ number[a[]]-1 , 2 ];

Hrkky = Sqrt[\[CapitalGamma]e] ( hop[ d[] , fe[] ] + hop[ a[] , fe[] ]);
Hkondo = Jo Simplify[ ( spinxyz[d[]] + spinxyz[fe[]] + spinxyz[a[]] ) ~ inner ~ spinxyz[fo[]] ];

H = Hd + Ha + Hrkky + Hkondo


(* Setup for Hamiltonian diagonalization *)

basisops = { a[] , d[] , fe[] , fo[] };
diagSetupBasisQS[];
diagSetupHam[];


(* Diagonalization *)

diagonalize[{U->u,\[CapitalGamma]e->\[Gamma]e,Jo->jo}];
eig2[[All,2,1]]//MatrixForm


(* Setup of the relevant eigenvalue array *)

eigenvalues = N[ scale * (eig2[[All,2,1]]-Min[Flatten@eig2[[All,2,1]]]) , 50 ];

Do[
	eigenvalues[[i]]=Min[ eigenvalues[[i]] ],
	{i,Length@eigenvalues}]
	
eigenvalues = Flatten@Table[eigenvalues[[i]],{i,Quotient[Length@eigenvalues,2],Length@eigenvalues}];
eigenvalues = Table[ToString[eigenvalues[[i]],FortranForm],{i,Length@eigenvalues}]; 


(* Writing the eigenvalues to a file *)

eigfile=OpenWrite["m_eigenvalues_lowest.dat"]

Do[
	WriteLine[ eigfile , eigenvalues[[i]] ],
	{i,Length@eigenvalues}]
	
Close[ eigfile ]
