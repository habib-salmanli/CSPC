"""
PW2 Lab B Part 3 -- fit a reaction's rate constant to measured data.

A first-order reaction decays as  C(t) = C0 * exp(-k*t).  You have noisy
concentration-vs-time measurements; find the k that best matches them.
Complete the TODOs. Run:  python kinetics.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# TODO 1: 
data = np.loadtxt("kinetics.csv", delimiter=",", skiprows=1)
t = data[:, 0]
C = data[:, 1]
C0 = C[0]


# TODO 2:
def total_error(k):
    k = k[0]  
    model = C0 * np.exp(-k * t)
    return np.sum((C - model)**2)
    

# TODO 3:
res = minimize(total_error, x0=0.5, method="SLSQP", bounds=[(0, 5)])
k_fit = res.x[0]
print("fitted k:", k_fit)


# TODO 4:
plt.scatter(t, C, label="measured")
plt.plot(t, C0 * np.exp(-k_fit * t), color="red", label=f"fit: k={k_fit:.3f}")
plt.xlabel("time")
plt.ylabel("concentration")
plt.legend()
plt.savefig("kinetics.png")
