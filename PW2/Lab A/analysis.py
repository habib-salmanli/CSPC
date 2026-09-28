"""
PW2 Lab A -- Motion from tracking data.

Read noisy free-fall position measurements, then:
  - differentiate once  -> velocity
  - differentiate twice -> acceleration (should be ~ constant -g, but noisy!)
  - integrate the acceleration back up -> recover velocity and position

Complete the TODOs. Run:  python analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# TODO 1:
data = np.loadtxt("freefall.csv", delimiter=",", skiprows=1)
t = data[:, 0]
y = data[:, 1]

# TODO 2: 
v = np.gradient(y, t)
a = np.gradient(v, t)


# TODO 3: 
print("mean acceleration:", a.mean())

print("mean acceleration (without edges):", a[1:-1].mean())

print("std of a:", a.std())
coef = np.polyfit(t, y, 2)
print("acceleration from parabola fit:", 2 * coef[0])

from scipy.integrate import cumulative_trapezoid


v_rec = cumulative_trapezoid(a, t, initial=0) + v[0]


y_rec = cumulative_trapezoid(v_rec, t, initial=0) + y[0]


print("max |y_rec - y|:", np.max(np.abs(y_rec - y)))


import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(8, 8))

ax1.plot(t, y)
ax1.set_ylabel("position (m)")

ax2.plot(t, v)
ax2.set_ylabel("velocity (m/s)")

ax3.plot(t, a)
ax3.axhline(-9.81, color="red", linestyle="--", label="-9.81")
ax3.set_ylabel("acceleration (m/s²)")
ax3.set_xlabel("time (s)")
ax3.legend()

plt.savefig("motion.png")
