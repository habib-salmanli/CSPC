# CSPC - Computer Science for Physics and Chemistry
My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup
Create the environment for a given lab:
conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc

## PW1 - Lab A: Reproducible Foundations

**What I built:**
- A reproducible conda environment, a radioactive decay simulation with tests, and a speed comparison between pure-Python and NumPy implementations.

**Speed comparison (loop vs NumPy):**
- loop  : 1.5760 s
- numpy : 0.0002 s
- speed-up: 7413.44x faster

**Tests:** all passing? yes

**Conclusion:**
- The NumPy vectorised version was thousands of times faster than the pure-Python loop, since NumPy performs the random decay calculation for all atoms at once instead of looping one by one in Python. This showed me how much overhead a Python-level loop adds for large-scale numerical work, and why libraries like NumPy are essential for scientific computing.

## PW1 - Lab B: Data, Plotting, and Automation

**What I built:**
- I compared the real decay measurements to the theoretical exponential curve using a side-by-side plot, and set up Snakemake to automatically rebuild the figure when needed.

**Result:**
- The observed data closely matches the analytical decay curve — both show the same exponential decay shape on the same axis scale.

**Snakemake pipeline:**
- The Snakefile defines a single rule that regenerates figure.png from decay_observed.csv by running plot.py, and only reruns when the input files have changed.


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## PW2 - Lab A: Motion from Tracking Data

**Mean acceleration:**
- I got a mean acceleration of -8.58 m/s². It is not exactly -9.81, but when I fitted a parabola to the position data I got -9.80, so the object really is in free fall.

**Why the acceleration is noisy:**
- The std of the acceleration was about 28.7, which is much bigger than g. The position looks smooth, but each time I take a derivative the small errors get bigger, and I did it twice.

**Integrating back:**
- When I integrated the noisy acceleration twice, I got the position back with a max difference of 0.78 m. So integration makes the noise smaller, the opposite of differentiation.


## PW2 - Lab B: Optimization in Chemistry

**Comparing the optimization methods:**
- For the easy function, all three methods agreed and gave x=3, so there was no real difference between them.
- For the harder function, the methods did not always agree. Starting from x0=0, Newton actually found a maximum instead of a minimum (I checked g'' and it was negative there), while gradient descent and SLSQP both found a real minimum. Starting from x0=2, gradient descent and Newton found the closer minimum, but SLSQP ended up at the other minimum far away. So the starting point and which method you use can both change the answer.

**Fitting the reaction rate:**
- I fitted k to the noisy data and got k≈0.26, which is close to the expected 0.25. When I plotted the fitted curve on top of the data points, it followed the data pretty well.

**Chemical equilibrium:**
- Newton's method and SLSQP both gave the same answer, x≈0.664. At that point H2 and I2 are about 0.336 mol each and HI is about 1.328 mol.

**Titration equivalence point (bonus):**
- I found the slope of the pH curve and looked for where it was biggest. It peaked at around V=... mL (öz ədədini yaz), which matches the equivalence point.
