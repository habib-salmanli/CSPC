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
