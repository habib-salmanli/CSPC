"""
PW1 Lab B -- read observed decay data and compare it to the analytical law.
Produce a 1x2 figure:  left = observed data,  right = analytical N0*exp(-lam*t),
with SHARED axes so the two shapes are directly comparable.

Complete the TODOs below. Run with:  python plot.py
"""

import numpy as np
import matplotlib.pyplot as plt

LAMBDA = 0.3     # decay constant, given

# TODO 1
data = np.loadtxt("decay_observed.csv", delimiter=",", skiprows=1)
t = data[:, 0]
observed = data[:, 1]

# TODO 2
N0 = observed[0]
analytical = N0 * np.exp(-LAMBDA * t)

# TODO 3
fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)

ax1.scatter(t, observed)
ax1.set_title("Observed data")
ax1.set_xlabel("time")
ax1.set_ylabel("count")

ax2.plot(t, analytical)
ax2.set_title("Analytical")
ax2.set_xlabel("time")
ax2.set_ylabel("count")

# TODO 4
plt.savefig("figure.png")
