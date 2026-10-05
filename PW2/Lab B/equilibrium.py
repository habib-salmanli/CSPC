"""
PW2 Lab B Part 4 -- chemical equilibrium via the equilibrium constant K.

Reaction  H2 + I2 <=> 2 HI, starting from 1 mol H2 and 1 mol I2.
As the reaction proceeds by an extent x:  H2 = 1-x,  I2 = 1-x,  HI = 2x.
At equilibrium the composition satisfies the equilibrium constant
        K = [HI]^2 / ([H2][I2]) = (2x)^2 / ((1-x)(1-x)).
Given K, find the extent x. Solve it TWO ways and compare.
Run:  python equilibrium.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton, minimize

K = 15.6
a = b = 1.0

def k_imbalance(x):
    return (2*x)**2 / ((1-x)*(1-x)) - K
    
    
# TODO 1:
x_newton = newton(k_imbalance, x0=0.5)
print("newton x:", x_newton)


# TODO 2:
res = minimize(lambda x: k_imbalance(x[0])**2, x0=[0.5], method="SLSQP", bounds=[(0, 0.999)])
x_slsqp = res.x[0]
print("SLSQP x:", x_slsqp)


# TODO 3:
x_eq = x_newton
n_H2 = 1 - x_eq
n_I2 = 1 - x_eq
n_HI = 2 * x_eq
print(f"H2={n_H2:.3f}, I2={n_I2:.3f}, HI={n_HI:.3f}")


# TODO 4: 
x_range = np.linspace(0, 0.99, 200)
plt.plot(x_range, 1 - x_range, label="H2")
plt.plot(x_range, 1 - x_range, label="I2", linestyle="--")
plt.plot(x_range, 2 * x_range, label="HI")
plt.axvline(x_eq, color="red", linestyle=":", label=f"equilibrium x={x_eq:.3f}")
plt.xlabel("extent of reaction (x)")
plt.ylabel("moles")
plt.legend()
plt.savefig("equilibrium.png")
