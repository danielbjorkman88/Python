# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 10:50:10 2021

@author: malyr
"""
import matplotlib.pyplot as plt
import numpy as np
import time


def generate(X, Y, phi):
    """
    Generates Z data for the points in the X, Y meshgrid and parameter phi.
    """
    R = 1 - np.sqrt(X**2 + Y**2)
    return np.cos(2 * np.pi * X + phi) * R


def generate_sphere(X, Y, phi):
    """
    """
    
    
    
    
    u, v = np.mgrid[0:2*np.pi:40j, 0:2*np.pi:40j]
    x1 = np.cos(u)*np.sin(v)*np.cos(phi)
    y1 = np.sin(u)*np.sin(v)*np.cos(phi)
    z1 = np.cos(v)
    
    return x1, y1, z1


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Make the X, Y meshgrid.
xs = np.linspace(-1, 1, 50)
ys = np.linspace(-1, 1, 50)
X, Y = np.meshgrid(xs, ys)




# Set the z axis limits so they aren't recalculated each frame.
ax.set_zlim(-1, 1)

# Begin plotting.
wframe = None
tstart = time.time()
for phi in np.linspace(0, 180. / np.pi, 100):
    # If a line collection is already remove it before drawing.
    if wframe:
        ax.collections.remove(wframe)

    # Plot the new wireframe and pause briefly before continuing.
    #Z = generate(X, Y, phi)
    #wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)
    
    x1, y1, z1 = generate_sphere(X, Y, phi)
    
    wframe = ax.plot_wireframe(x1, y1, z1, color="0.5",linewidth=0.6) #Draw grid
    #ax.plot_surface(x1, y1, z1, color="w", edgecolor="w", rcount = 500)
    
    quiver = ax.quiver(0,0,0,0,0,2)

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    
    ax.set_xlabel('$x$', fontsize=20)
    ax.set_ylabel('$y$', fontsize=20)
    ax.set_zlabel('$z$', fontsize=20)


    
    plt.pause(.001)

print('Average FPS: %f' % (100 / (time.time() - tstart)))