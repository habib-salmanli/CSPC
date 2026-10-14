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


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## PW3: Data, Distributions, Testing, and Causation

---
## PW3: Data, Distributions, Testing, and Causation

**Data:** heart.csv (Cleveland heart disease dataset, Kaggle/UCI) and chemicals_cancer.csv (synthetic).

**Shape of the variables (distributions.png):**
- age: ...
- chol: ...
- trestbps: ...
- thalach: ...

**Are they normal? (Shapiro-Wilk + Q-Q plots):**
- age: p = ..., verdict: ...
- chol: p = ..., verdict: ...
- trestbps: p = 1.5e-06, not normal.
- thalach: p = 6.6e-05, not normal.
- I also checked the Q-Q plots because Shapiro-Wilk is very sensitive with about 300 patients.

**Do heart disease patients have a different max heart rate?**
- thalach is not normal, so I used the Mann-Whitney test as the main test and a Welch t-test as a check.
- Disease group: mean 158.5 bpm (SEM 1.5, n = 165). Healthy group: mean 139.1 bpm (SEM 1.9, n = 138).
- Both tests gave p around 1e-13, so the difference is real and not chance.
- The error bars in thalach_groups.png do not overlap, which agrees with the tests.

**Do age and thalach move together?**
- Pearson r = -0.40 and Spearman rho = -0.40 (p around 1e-13).
- Older patients tend to have a lower max heart rate. The correlation is moderate and the points are spread out, so age explains only part of it.

**Chemical mystery:**
- Naive result: benzene r = ..., cadmium r = .... At face value ... looked like the cause.
- Chemicals vs pollution_index: benzene r = ..., cadmium r = ....
- With pollution_index between 40 and 60 (n = ...): benzene r = ..., cadmium r = ....
- Conclusion: ... is the real cause because its association stayed. ... only looked guilty because it follows the pollution index.
- Correlation does not mean causation: a third variable can create a fake link.

**Bonus:**
- target proportions: ... / ..., entropy = ... bits (max 1.0).
