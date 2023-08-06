import numpy as np, matplotlib.pyplot as plt
from aesthetic.plot import (
    savefig, set_style, set_style_scatter, set_style_grid, format_ax
)

x = np.linspace(0,10,1000)
y = (x/100)**3 + 5*np.sin(x)

set_style()
fig, ax = plt.subplots()
ax.plot(x, y)
ax.plot(x, y+3)
ax.plot(x, y+6)
ax.set_xlabel('x')
ax.set_ylabel('y')
savefig(fig, '../results/plot_standard.png')

set_style_scatter()
fig, ax = plt.subplots()
ax.scatter(x[::50], y[::50])
ax.scatter(x[::50], y[::50]+3)
ax.scatter(x[::50], y[::50]+6)
ax.set_xlabel('x')
ax.set_ylabel('y')
savefig(fig, '../results/plot_scatter.png')

set_style_grid()
fig, ax = plt.subplots()
ax.plot(x, y)
ax.plot(x, y+3)
ax.plot(x, y+6)
ax.set_xlabel('x')
ax.set_ylabel('y')
savefig(fig, '../results/plot_grid.png')
