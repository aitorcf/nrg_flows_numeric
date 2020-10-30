#!/usr/bin/env python3

import py_functions as pf
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace( 0 , 10 , 10 )
y = x 
z = x

print( x , y , z )

fig = plt.figure()
ax = fig.add_subplot( 111 , projection='3d' ) 

pf.plot_arrows_3d( x , y , z , ax )

plt.show()
