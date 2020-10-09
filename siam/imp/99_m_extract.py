#!/usr/bin/env python3

filenames = ["e-q0s1_table1.dat","e-q0s3_table1.dat","e-q1s2_table1.dat","e-q2s1_table1.dat"]

for filename in filenames:
    newfilename = filename + '.m'
    newf = open( newfilename , 'w' )

    with open(filename) as f:
        for line in f:
            if line!="\n": newf.write( line.split()[1] + "\n")

    newf.close()
