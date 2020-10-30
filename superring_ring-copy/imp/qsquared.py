import matplotlib.pyplot as plt
import numpy as np

plt.style.use( 'seaborn-paper' )

data = np.loadtxt( 'custom' )
plt.plot( data[:,0] , data[:,1] )
plt.show()
