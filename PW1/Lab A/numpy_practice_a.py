# WORKED EXAMPLE:

import numpy as np

temperature_c = np.array([18.4, 19.1, 20.0, 21.3, 22.1])
print(temperature_c)
print(temperature_c.shape)
print(temperature_c.dtype)


# TODO 1:

time_s = np.arange(0, 11, 2)
print(time_s)


# TODO 2:

wavelength_nm = np.linspace(400, 700, 8)
print(wavelength_nm)


# TODO 3:

concentrations = np.array([
    [0.10, 0.20, 0.30, 0.40],
    [0.15, 0.25, 0.35, 0.45]
])

print(concentrations.shape)
print(concentrations.dtype)
print(concentrations.size)
