# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 15:43:00 2021

@author: malyr
"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

def get_arrow(theta):
    x = 0 #np.cos(theta)
    y = 0 #np.sin(theta)
    z = 0
    u = np.sin(3*theta)
    v = np.sin(3*theta)
    w = 2
    return x,y,z,u,v,w



# draw sphere
u, v = np.mgrid[0:2*np.pi:40j, 0:2*np.pi:40j]
x1 = np.cos(u)*np.sin(v)
y1 = np.sin(u)*np.sin(v)
z1 = np.cos(v)
ax.plot_wireframe(x1, y1, z1, color="0.5",linewidth=0.6) #Draw grid
#ax.plot_wireframe(x1, y1, z1, color="w")
ax.plot_surface(x1, y1, z1, color="w", edgecolor="w", rcount = 500)



quiver = ax.quiver(*get_arrow(0))

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

ax.set_xlabel('$x$', fontsize=20)
ax.set_ylabel('$y$', fontsize=20)
ax.set_zlabel('$z$', fontsize=20)

def update(theta):
    global quiver
    quiver.remove()
    quiver = ax.quiver(*get_arrow(theta))

ani = FuncAnimation(fig, update, frames=np.linspace(0,2*np.pi,200), interval=50)
plt.show()
