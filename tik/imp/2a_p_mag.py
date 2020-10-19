#!/usr/bin/env python3

import matplotlib.pyplot as plt
import py_functions as pf


plt.style.use( 'seaborn-paper' )
fig = plt.figure()
ax = fig.add_subplot()

pf.plot_mag_susc( ax )

plt.show()
