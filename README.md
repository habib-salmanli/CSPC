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

