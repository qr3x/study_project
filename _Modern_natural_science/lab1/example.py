#!/usr/bin/env python
# coding: utf-8

# In[10]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# In[11]:


def pendula(freq):
    def rhs(t, X):
        x, y = X
        return [y, -freq * freq * x]
    return rhs

def saddleNodePlane(mu):
    def rhs(t, X):
        x, y = X
        return [mu - x**2, -2*y]
    return rhs


# In[20]:


def eq_quiver(rhs, limits, N = 16):
    xlims, ylims = limits
    xs = np.linspace(xlims[0], xlims[1], N)
    ys = np.linspace(ylims[0], ylims[1], N)
    U = np.zeros((N, N))
    V = np.zeros((N, N))
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            vfield = rhs(0.0, [x, y])
            u, v = vfield
            U[i][j] = u
            V[i][j] = v
    return xs, ys, U, V

def plotOnPlane(rhs, limits):
    plt.close()
    xlims, ylims = limits
    plt.xlim([xlims[0],xlims[1]])
    plt.ylim([ylims[0],ylims[1]])
    xs, ys, U, V = eq_quiver(rhs, limits)
    plt.quiver(xs, ys, U, V, alpha = 0.6)
    
def plotTraj(rhs, times, point):
    sol = solve_ivp(rhs, times, point, method = 'RK45', rtol=1e-12)
    xs, ys = sol.y
    plt.plot(xs, ys, 'b-')
    


# In[28]:


freq = 0.75
rhs = pendula(freq)
plotOnPlane(rhs, [(-2.,2.0), (-2.,2.0)])
plotTraj(rhs, [0., 40.], (0.0, 1.0))
plotTraj(rhs, [0., 40.], (0.0, 0.5))
plotTraj(rhs, [0., 40.], (0.0, 1.5))
plotTraj(rhs, [0., 40.], (0.01, 0.0))


# In[ ]:




