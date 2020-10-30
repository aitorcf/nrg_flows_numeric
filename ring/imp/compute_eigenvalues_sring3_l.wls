#!/usr/bin/env wolframscript
(* ::Package:: *)

mu


<<sneg`sneg`

Import["../../diagonalize.m"]

snegfermionoperators[d,a,f0,f1]
snegrealconstants[U,U,\[CapitalGamma]1,\[CapitalGamma]2]


(* Constants and parameters *)

\[CapitalLambda] = 2.5;
scale = ( 1 + \[CapitalLambda]^-1 ) / 2.0;

u = N[ 0.5 * scale^-1 * ToExpression@$ScriptCommandLine[[2]] , 50 ];
\[Gamma]1 = N[ scale^-2 * 2 * ToExpression@$ScriptCommandLine[[3]] / \[Pi] , 50 ];
\[Gamma]2 = N[ scale^-2 * 2 * ToExpression@$ScriptCommandLine[[4]] / \[Pi] , 50 ];


(* Hamiltonian definition *)

Hd = U pow[ number[d[]]-1 , 2 ];
Ha = U pow[ number[a[]]-1 , 2 ];

Hdf = Sqrt[\[CapitalGamma]1] hop[ d[] , f1[] ] + Sqrt[\[CapitalGamma]2] hop[ d[] , f2[] ];
Haf = Sqrt[\[CapitalGamma]1] hop[ a[] , f2[] ] + Sqrt[\[CapitalGamma]2] hop[ a[] , f2[] ]

H = Hd + Ha + Hdf + Haf;


(* Hamiltonian diagonalization *)

basisops = { a[] , d[] , f[] };
diagSetupBasisQS[];
diagSetupHam[];
diagonalize[{U->u,\[CapitalGamma]1->\[Gamma]1,\[CapitalGamma]2->\[Gamma]2}];


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
