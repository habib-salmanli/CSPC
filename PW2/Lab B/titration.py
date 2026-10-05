"""
PW2 Lab B Part 5 (bonus) -- find a titration's equivalence point.

titration.csv holds a titration curve: pH versus the volume of base added.
The equivalence point is the volume where the pH changes fastest (the steep
jump). Numerically, that is where the SLOPE of the pH curve is largest.
Run:  python titration.py
"""
import numpy as np
import matplotlib.pyplot as plt

# TODO 1:
data = np.loadtxt("titration.csv", delimiter=",", skiprows=1)
V = data[:, 0]
pH = data[:, 1]

slope = np.gradient(pH, V)

# TODO 2:
idx = np.argmax(slope)
V_eq = V[idx]
print("equivalence point at V =", V_eq, "mL")


# TODO 3:
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.plot(V, pH)
ax1.axvline(V_eq, color="red", linestyle="--")
ax1.set_xlabel("volume base (mL)")
ax1.set_ylabel("pH")
ax1.set_title("pH curve")

ax2.plot(V, slope)
ax2.axvline(V_eq, color="red", linestyle="--")
ax2.set_xlabel("volume base (mL)")
ax2.set_ylabel("slope (dpH/dV)")
ax2.set_title("slope (peaks at equivalence)")

plt.tight_layout()
plt.savefig("titration.png")
