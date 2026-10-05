"""
PW2 Lab B Part 2 -- three routes to a minimum.

Compare gradient descent, Newton, and SLSQP on two functions:
  2A: f(x) = (x-3)**2 + 1          (easy, one minimum at x=3)
  2B: g(x) = x**4 - 3*x**2 + x + 5 (harder, several stationary points)
Run:  python warmup.py
"""
import numpy as np
from scipy.optimize import newton, minimize

def f(x):
    return (x - 3)**2 + 1

def fprime(x):
    return 2 * (x - 3)

def fprime2(x):
    return 2

# TODO 2A:
x = 0.0
lr = 0.1
for _ in range(100):
    x = x - lr * fprime(x)
print("gradient descent:", x)

x_newton = newton(fprime, x0=0, fprime=fprime2)
print("newton:", x_newton)

res = minimize(f, x0=0, method="SLSQP")
print("SLSQP:", res.x)



# TODO 2B:
def g(x):
    return x**4 - 3*x**2 + x + 5

def gprime(x):
    return 4*x**3 - 6*x + 1

def gprime2(x):
    return 12*x**2 - 6

for x0 in [0, 2]:
    x = x0
    lr = 0.01
    for _ in range(200):
        x = x - lr * gprime(x)
    print(f"x0={x0}, gradient descent:", x)

    x_newton = newton(gprime, x0=x0, fprime=gprime2)
    curvature = gprime2(x_newton)
    kind = "minimum" if curvature > 0 else "maximum"
    print(f"x0={x0}, newton:", x_newton, "->", kind)

    res = minimize(g, x0=x0, method="SLSQP")
    print(f"x0={x0}, SLSQP:", res.x)
