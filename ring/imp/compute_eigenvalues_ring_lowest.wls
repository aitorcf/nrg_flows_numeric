#!/usr/bin/env wolframscript
(* ::Package:: *)

<<sneg`sneg`

Import["../../diagonalize.m"]

snegfermionoperators[d,a,f]
snegrealconstants[Ud,Ua,\[CapitalGamma]d,\[CapitalGamma]a]


(* Constants and parameters *)

\[CapitalLambda] = 2.5;
scale = ( 1 + \[CapitalLambda]^-1 ) / 2.0;

ud = N[ 0.5 * scale^-1 * ToExpression@$ScriptCommandLine[[2]] , 50 ]
ua = N[ 0.5 * scale^-1 * ToExpression@$ScriptCommandLine[[3]] , 50 ]
\[Gamma]d = N[ scale^-2 * 2 * ToExpression@$ScriptCommandLine[[4]] / \[Pi] , 50 ]
\[Gamma]a = N[ scale^-2 * 2 * ToExpression@$ScriptCommandLine[[5]] / \[Pi] , 50 ]


(* Hamiltonian definition *)

Hd = Ud pow[ number[d[]]-1 , 2 ]
Ha = Ua pow[ number[a[]]-1 , 2 ]

Hdf = Sqrt[\[CapitalGamma]d] hop[ d[] , f[] ]
Haf = Sqrt[\[CapitalGamma]a] hop[ a[] , f[] ]

H = Hd + Ha + Hdf + Haf


(* Hamiltonian diagonalization *)

basisops = { a[] , d[] , f[] };
diagSetupBasisQS[];
diagSetupHam[];
diagonalize[{Ud->ud,Ua->ua,\[CapitalGamma]d->\[Gamma]d,\[CapitalGamma]a->\[Gamma]a}];


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
