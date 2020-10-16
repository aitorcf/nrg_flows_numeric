#!/usr/bin/env wolframscript
(* ::Package:: *)

<<sneg`sneg`

Import["../../diagonalize.m"]

snegfermionoperators[d,a,f0,f1,f2]
snegrealconstants[U,\[CapitalGamma]d0,\[CapitalGamma]01]


(* Constants and parameters *)

\[CapitalLambda] = 2.5;
scale = ( 1 + \[CapitalLambda]^-1 ) / 2.0;
\[Xi] = 1; (* si sale bien el fiteo, poner el valor correcto (krishnamurthy) *) 

(* u = N[ 0.5 * scale^-1 * ToExpression@$ScriptCommandLine[[2]] , 20 ]
\[Gamma]df = N[ scale^-2 * 2 * ToExpression@$ScriptCommandLine[[3]] / \[Pi] , 20 ]
\[Gamma]ff = N[ scale^-2 * 2 * ToExpression@$ScriptCommandLine[[4]] / \[Pi] , 20 ] *)


(* Hamiltonian definition *)

Hd = U pow[ number[d[]]-1 , 2 ];
Ha = U pow[ number[a[]]-1 , 2 ];

Hd0 = Sqrt[\[CapitalGamma]d0] hop[ d[] , f0[] ];
Ha0 = Sqrt[\[CapitalGamma]d0] hop[ a[] , f0[] ];

H01 = Sqrt[\[CapitalGamma]01] hop[ f0[] , f1[] ];
H12 = \[Xi] hop[ f1[] , f2[] ];

H = Hd + Ha + Hd0 + Ha0 + H01 + H12


(* Hamiltonian matrix setup *)

basisops = { a[] , d[] , f0[] , f1[] , f2[] };
diagSetupBasisQS[];
diagSetupHam[];


(* Diagonalization *)

diagonalize[{U->1,\[CapitalGamma]d0->1,\[CapitalGamma]01->1}];


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
