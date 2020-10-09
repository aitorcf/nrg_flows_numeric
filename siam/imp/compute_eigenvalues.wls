#!/usr/bin/env wolframscript
(* ::Package:: *)

<<sneg`sneg`

Import["/home/aitor/tesia/sneg/diagonalize.m"]

snegfermionoperators[d,f]
snegrealconstants[U,\[CapitalGamma]]

scale = ( 1 + 2.5^-1 ) / 2.0

eigfile=OpenWrite["m_eigenvalues.dat"]

U=ToExpression[$ScriptCommandLine[[2]]]
\[CapitalGamma]=ToExpression[$ScriptCommandLine[[3]]]

U = (  2.0  /  ( 1 + 2.5^-1 )  ) * U / 2.0
\[CapitalGamma] = (  2.0  /  ( 1 + 2.5^-1 )  )^2 * 2.0 * \[CapitalGamma] / \[Pi]

Hd=U pow[number[d[]]-1,2];
Hdf=Sqrt[\[CapitalGamma]] hop[d[],f[]];
H=Hd+Hdf;
basisops={d[],f[]};
diagSetupBasisQS[];
diagSetupHam[];
diagonalize[{}];
eigenvalues=( scale * (eig2[[All,2,1]]-Min[Flatten@eig2[[All,2,1]]]) )//N;

Do[
	eigenvalues[[i]]=Sort[ eigenvalues[[i]] ],
	{i,Length@eigenvalues}]

eigenvalues=Flatten@Table[eigenvalues[[i]],{i,Quotient[Length@eigenvalues,2],Length@eigenvalues}];

Do[
	WriteLine[ eigfile , eigenvalues[[i]] ],
	{i,Length@eigenvalues}]
	
Close[ eigfile ]
