#!/usr/bin/env wolframscript
(* ::Package:: *)

<<sneg`sneg`

Import["../../diagonalize.m"]

snegfermionoperators[d,a,f]
snegrealconstants[U,\[CapitalGamma]d,\[CapitalGamma]a]


(* Constants and parameters *)

\[CapitalLambda] = 2.5;
scale = ( 1 + \[CapitalLambda]^-1 ) / 2.0;

u = scale^-1 * N@ToExpression@$ScriptCommandLine[[2]]
\[Gamma]d = scale^-2 * N@2 * ToExpression@$ScriptCommandLine[[3]] / \[Pi]
\[Gamma]a = scale^-2 * 2 * N@ToExpression@$ScriptCommandLine[[4]] / \[Pi] 


(* Hamiltonian definition *)

Hd = U pow[ number[d[]]-1 , 2 ]
Ha = U pow[ number[a[]]-1 , 2 ]

Hdf = Sqrt[\[CapitalGamma]d] hop[ d[] , f[] ]
Haf = Sqrt[\[CapitalGamma]a] hop[ a[] , f[] ]

H = Hd + Ha + Hdf + Haf


(* Hamiltonian diagonalization *)

basisops = { a[] , d[] , f[] };
diagSetupBasisQS[];
diagSetupHam[];
diagonalize[{U->u,\[CapitalGamma]d->\[Gamma]d,\[CapitalGamma]a->\[Gamma]a}];


(* Setup of the relevant eigenvalue array *)

eigenvalues = N[ scale * (eig2[[All,2,1]]-Min[Flatten@eig2[[All,2,1]]]) ];

Do[
	eigenvalues[[i]]=Sort[ eigenvalues[[i]] ],
	{i,Length@eigenvalues}]
	
eigenvalues = Flatten@Table[eigenvalues[[i]],{i,Quotient[Length@eigenvalues,2],Length@eigenvalues}];
eigenvalues = Table[ToString[eigenvalues[[i]],FortranForm],{i,Length@eigenvalues}]; 


(* Writing the eigenvalues to a file *)

eigfile=OpenWrite["m_eigenvalues.dat"]

Do[
	WriteLine[ eigfile , eigenvalues[[i]] ],
	{i,Length@eigenvalues}]
	
Close[ eigfile ]




