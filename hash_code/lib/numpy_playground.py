import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x = y = np.linspace(-10, 10, 100)

X, Y = np.meshgrid(x, y)

R = np.sqrt(X ** 2 + Y ** 2)
Z = np.sin(R)

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis')
fig.show()
