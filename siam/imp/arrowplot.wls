#!/usr/bin/env wolframscript
(* ::Package:: *)

<<sneg`sneg`
<< Optimization`UnconstrainedProblems`

Import["/home/aitor/tesia/sneg/diagonalize.m"]

snegfermionoperators[d,f]
snegrealconstants[U,\[CapitalGamma]]


(* Function that computes the eigenvalues of H_0 for numerical values of the parameters *)

Heigenvalues[u_,\[Gamma]_]:=Module[{U=u,\[CapitalGamma]=\[Gamma]},
	Hd=U pow[number[d[]]-1,2];
	Hdf=Sqrt[\[CapitalGamma]] hop[d[],f[]];
	H=Hd+Hdf;
	basisops={d[],f[]};
	diagSetupBasisQS[];
	diagSetupHam[];
	diagonalize[{}];
	eigenvalues=(eig2[[All,2,1]]-Min[eig2[[All,2,1]]])//N;
	Table[eigenvalues[[i]],{i,Quotient[Length@eigenvalues,2],Length@eigenvalues}]
	]


(* Function that reads the n eigenvalues of one subspace computed by NRG for each step*)

ReadEigenvalues[f_,n_]:=Module[{alleigs,nsteps,eigs},
	alleigs=ReadList[f,RecordSeparators->" "];
	eigs={};
	nsteps=Length[alleigs]/n;
	If[n>1, 
		Do[
			eigs=Append[ eigs , Table[alleigs[[i+j*nsteps]],{j,0,n-1}] ],
		{i,1,nsteps}],
		eigs=alleigs
		];
	ToExpression@eigs
]


(* Obtain an array with all the eigenvalues computed by NRG. Store it in NRGeigenvalues *)

subspacefiles={"e-q0s1_table1.dat.m","e-q0s3_table1.dat.m","e-q1s2_table1.dat.m","e-q2s1_table1.dat.m"};

q0s1=ReadEigenvalues["e-q0s1_table1.dat.m",3];
q0s3=ReadEigenvalues["e-q0s3_table1.dat.m",1];
q1s2=ReadEigenvalues["e-q1s2_table1.dat.m",2];
q2s1=ReadEigenvalues["e-q2s1_table1.dat.m",1];

nsteps=Length@q0s3;

NRGeigenvalues={};
Do[
	NRGeigenvalues = Append[ NRGeigenvalues , q0s1[[i]]];
	NRGeigenvalues[[i]] = Append[ NRGeigenvalues[[i]] , q0s3[[i]] ];
	NRGeigenvalues[[i]] = Append[ NRGeigenvalues[[i]] , q1s2[[i]] ];
	NRGeigenvalues[[i]] = Append[ NRGeigenvalues[[i]] , q2s1[[i]] ];
	NRGeigenvalues[[i]] = Flatten[ NRGeigenvalues[[i]] ]
	,{i,nsteps}]


NRGeigenvalues=NRGeigenvalues//MatrixForm;
FindRoot[{Heigenvalues[x,y][[1]]==NRGeigenvalues[[1,1]],
	    (*Heigenvalues[x,y][[2]]==NRGeigenvalues[[1,2]],*)
	    (*Heigenvalues[x,y][[3]]==NRGeigenvalues[[1,3]],*)
	    Heigenvalues[x,y][[4]]==NRGeigenvalues[[1,4]]
	    (*Heigenvalues[x,y][[5]]==NRGeigenvalues[[1,5]],*)
	    (*Heigenvalues[x,y][[6]]==NRGeigenvalues[[1,6]]*)},
	    {{x,0.5},{y,0.5}}]



