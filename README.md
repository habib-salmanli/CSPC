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


--------------------------------------------------------------------------------------------------------------------------------------------------------------------

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


--------------------------------------------------------------------------------------------------------------------------------------------------------------------


## PW3: Data, Distributions, Testing, and Causation

**Data:** heart.csv (Cleveland heart disease dataset, Kaggle/UCI) and chemicals_cancer.csv (synthetic).

**Shape of the variables (distributions.png):**
- age: roughly bell-shaped, peak around 55-60, from about 29 to 77 years.
- chol: peak around 220-240 with a long tail to the right, a few very high values (one near 560).
- trestbps: peak around 120-130, skewed to the right, a few high values up to about 200.
- thalach: skewed to the left, peak around 160-170, with a tail towards low values (down to about 70).

**Are they normal? (Shapiro-Wilk + Q-Q plots):**
- age: p = 0.0058. The test says not normal, but the Q-Q plot follows the line closely and only the ends move away. With about 300 patients Shapiro-Wilk reacts to very small differences, so I call age approximately normal.
- chol: p = 5.4e-09, not normal. In the Q-Q plot a few very high values go far above the line.
- trestbps: p = 1.5e-06, not normal. The Q-Q plot is curved and the upper end goes above the line.
- thalach: p = 6.6e-05, not normal. The Q-Q plot is slightly S-shaped and the lowest points fall below the line.

**Do the two target groups have a different max heart rate?**
- thalach is not normal, so I used the Mann-Whitney test as the main test and a Welch t-test as a check.
- target=1: mean 158.5 bpm (SEM 1.5, n = 165). target=0: mean 139.1 bpm (SEM 1.9, n = 138).
- Both tests gave p around 1e-13, so the difference is real and not chance.
- In thalach_groups.png the error bars are small and the two bars are clearly separated, so the picture agrees with the tests.
- The target=1 group has the higher heart rate. This looks reversed, because patients with heart disease usually reach a lower max heart rate. The first patient in the file (age 63) has target=1 but in the original Cleveland data has no disease, and the group sizes also fit. So in this version target=1 most likely means "no disease", and the real conclusion is that patients with heart disease reach a lower max heart rate.

**Do age and thalach move together? (age_thalach.png)**
- Pearson r = -0.40 and Spearman rho = -0.40 (p around 1e-13).
- The points make a cloud going down to the right, so older patients tend to have a lower max heart rate. The cloud is wide, so age explains only part of it.

**Chemical mystery:**
- Naive result: benzene r = 0.385 and cadmium r = 0.880 with malignancy. At face value cadmium looked like the cause, much stronger than benzene.
- Looking again: cadmium is almost the same thing as the pollution index (r = 0.982), and the pollution index is strongly linked to malignancy (r = 0.895). Benzene is not linked to the pollution index (r = 0.054).
- So I kept only patients with pollution_index between 40 and 60 (n = 199) and recomputed. Benzene stayed strong (r = 0.702, p = 8e-31). Cadmium dropped a lot (r = 0.316).
- Conclusion: benzene is the real cause, because its link stayed strong when pollution was held roughly fixed. Cadmium only looked guilty because it follows the pollution index, and its link mostly disappeared once pollution was controlled.
- Correlation does not mean causation: a third variable can create a fake link.

**Bonus:**
- target proportions: 54.5% / 45.5%, entropy = 0.994 bits (max 1.0). The column is almost perfectly balanced, so it is hard to guess the category without more information.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------


## PW4: Machine Learning (Supervised and Unsupervised)

### Session A: Concrete strength

**Data:** UCI Concrete Compressive Strength (Yeh, 1998), 1030 tests. Inputs: cement, slag, ash, water, superplastic, coarse_agg, fine_agg (all kg/m3), age (days). Output: strength (MPa).

**Cleaning:**
- 25 duplicate rows and 0 missing values. I removed the duplicates, so 1005 rows are left.
- A duplicated row is a problem because one copy can land in the training set and the other in the test set. The model then sees a test row during training, and the test score looks better than it really is.
- In describe(), coarse_agg and fine_agg are in the hundreds, while superplastic is only a few units. So the scales are very different and scaling is needed later.
- strength vs cement: strength goes up when cement goes up, but the points are very spread out (for example at 300 kg/m3 strength is anywhere between 10 and 80 MPa), because the other ingredients and the age also matter.
- strength vs age: the samples were tested at only a few ages (1, 3, 7, 14, 28, 56, 90, 100, 180, 270, 360 days). Strength is low at the first days and goes up fast until about 30-100 days, then it grows much more slowly. So the curve is not a straight line.

**Split:** 80/20 with random_state=42, so 804 training rows and 201 test rows.

**Linear regression:**
strength = -23.39 + 0.1167 cement + 0.0981 slag + 0.0846 ash - 0.1314 water + 0.3315 superplastic + 0.0155 coarse_agg + 0.0206 fine_agg + 0.1106 age
(MPa per kg/m3 for the ingredients, MPa per day for age)

| train RMSE | test RMSE | test MAE | train R2 | train adj R2 | test R2 |
|---|---|---|---|---|---|
| 10.00 | 11.19 | 8.90 | 0.610 | 0.606 | 0.580 |

- Residuals vs age (A4_residuals.png): the points are not randomly spread around zero. At young ages (3-7 days) the residuals are mostly negative (down to about -25 MPa), so the model predicts too much strength. Around 28-90 days they are mostly positive (up to about +35), so the model predicts too little. At the oldest ages (about 360 days) they are negative again. This is a curved pattern.
- A systematic pattern in the residuals means the model is missing some structure, here the curved effect of age, so a straight line is not enough. Train and test errors are close, so this is underfitting, not overfitting.

**Polynomial regression:**

| degree | p | train RMSE | test RMSE | train R2 | train adj R2 | test R2 |
|---|---|---|---|---|---|---|
| 1 | 8 | 10.00 | 11.19 | 0.610 | 0.606 | 0.580 |
| 2 | 44 | 6.99 | 8.31 | 0.809 | 0.798 | 0.769 |
| 3 | 164 | 4.40 | 5.95 | 0.925 | 0.905 | 0.881 |
| 4 | 494 | 2.33 | 39.41 | 0.979 | 0.945 | -4.206 |

- I would choose degree 3, because it has the lowest test error.
- At degree 4 there are 494 features for only 804 training rows, so the model memorises the training data. Train error is small, but test R2 is negative, which is worse than just predicting the mean.
- Adjusted R2 alone does not protect from this: at degree 4 it is still 0.945. Only the separate test set shows the problem.

**Classification (strength >= 40 MPa):** 64% of the mixes do not reach 40 MPa and 36% do, so I used stratify.

KNN sweep (scaled):

| K | 1 | 3 | 5 | 7 | 15 | 25 | 51 | 101 |
|---|---|---|---|---|---|---|---|---|
| train | 0.998 | 0.934 | 0.907 | 0.893 | 0.848 | 0.841 | 0.805 | 0.757 |
| test | 0.831 | 0.801 | 0.816 | 0.836 | 0.826 | 0.806 | 0.781 | 0.736 |

- I chose K=7. K=1 memorises the training data, and K=51 or more underfits.
- At K=5, test accuracy without scaler is 0.806 and with scaler is 0.816.
- Five different splits (K=5) gave 0.801, 0.866, 0.861, 0.861, 0.836, with std about 0.024. The spread is bigger than the scaler difference (0.01) and the differences between K=5, 7 and 15, so those differences are not meaningful. Only the extreme K values are clearly worse.

Decision tree sweep:

| max_depth | 1 | 2 | 3 | 4 | 5 | 6 | 8 | None |
|---|---|---|---|---|---|---|---|---|
| leaves | 2 | 4 | 8 | 16 | 26 | 38 | 61 | 80 |
| train | 0.755 | 0.755 | 0.840 | 0.869 | 0.889 | 0.930 | 0.973 | 0.998 |
| test | 0.701 | 0.701 | 0.796 | 0.826 | 0.846 | 0.841 | 0.856 | 0.881 |

- The gap between train and test grows as the tree grows (about 0.04 at depth 4-5, about 0.12 at depth 8 and None).
- I chose depth 5. The unlimited tree has the best test accuracy (0.881) but 80 leaves, which nobody can read. With depth 5 I lose about 3.5 points of test accuracy but get a tree with 26 leaves that is much less overfitted.
- Root question: "age <= 42 days?". Then cement, water and superplastic. This makes physical sense: concrete gets stronger with age, with more cement and with less water.

**Metrics (test set):**

| model | TP | FP | FN | TN | accuracy | precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|
| KNN K=7 | 54 | 15 | 18 | 114 | 0.836 | 0.783 | 0.750 | 0.766 |
| Tree depth 5 | 58 | 17 | 14 | 112 | 0.846 | 0.773 | 0.806 | 0.789 |

The two models are about equal, since the differences are smaller than the split spread.

- The dangerous mistake is FP: the model says the concrete reaches 40 MPa but it does not. Weak concrete would be used in a building. Precision controls this. FN only wastes good concrete.

Thresholds (KNN):

| threshold | TP | FP | FN | TN | precision | recall |
|---|---|---|---|---|---|---|
| 0.3 | 61 | 23 | 11 | 106 | 0.726 | 0.847 |
| 0.5 | 54 | 15 | 18 | 114 | 0.783 | 0.750 |
| 0.7 | 39 | 11 | 33 | 118 | 0.780 | 0.542 |
| 0.9 | 18 | 1 | 54 | 128 | 0.947 | 0.250 |

- I chose threshold 0.9 because safety matters most: FP goes from 15 to 1 and precision is 0.947.
- The price is that recall drops from 0.75 to 0.25, so the model rejects most of the good concrete. In real life a lab test would still be needed.

**Feature importance:**

| | raw coef | std coef | tree importance | perm KNN | perm tree |
|---|---|---|---|---|---|
| cement | 0.117 | 12.119 | 0.253 | 0.165 | 0.170 |
| slag | 0.098 | 8.437 | 0.036 | 0.055 | 0.009 |
| ash | 0.085 | 5.440 | 0.037 | 0.016 | 0.000 |
| water | -0.131 | -2.828 | 0.095 | 0.068 | 0.012 |
| superplastic | 0.331 | 1.971 | 0.164 | 0.066 | 0.188 |
| coarse_agg | 0.016 | 1.199 | 0.011 | 0.038 | 0.002 |
| fine_agg | 0.021 | 1.670 | 0.091 | 0.081 | 0.072 |
| age | 0.111 | 6.895 | 0.313 | 0.176 | 0.165 |

- Raw coefficients have different units, so they cannot be compared. superplastic looks the biggest (0.33) only because it takes small numbers. After standardising, cement (12.1), slag (8.4) and age (6.9) are the top ones.
- The methods mostly agree that age and cement are the most important (tree importance and KNN permutation). They disagree on slag, which is high in the standardised coefficients but low in the others.
- This fits what engineers say: age and cement matter a lot, and water has a negative coefficient (more water, weaker concrete). water and cement work together as a ratio, but the model sees them separately.
- High importance does not mean that changing the ingredient would change the strength. Importance only shows what the model uses for prediction, like in PW3 (correlation is not causation). Ingredients are also mixed together, so they are linked to each other.

### Session B: Wine chemistry

**Data:** UCI Wine data (Forina et al.), 178 wines from the same region of Italy, 3 cultivars, 13 chemical measurements (alcohol, malic acid, ash, alcalinity of ash, magnesium, phenols, flavanoids, colour, hue, OD280/OD315, proline, ...). I did not use the cultivars until the end.
- Biggest ranges: proline (278-1680, std 314.9) and magnesium (70-162, std 14.3). Smallest: nonflavanoid_phenols (0.13-0.66, std 0.12) and hue (std 0.23).

**PCA on raw data:** PC1 carries 99.81% of the variance and its loading is 0.9998 on proline, all others are below 0.02. PCA does not rescale, and proline has by far the biggest numbers, so PC1 is just the proline axis. I would not accept it as the main chemical difference. It is an effect of units, not chemistry.

**PCA on scaled data:**
- Explained variance: 0.362, 0.192, 0.111, 0.071, 0.066, 0.049, 0.042, 0.027, 0.022, 0.019, 0.017, 0.013, 0.008. Cumulative: 0.362, 0.554, 0.665, 0.736, 0.802, 0.851, 0.893, 0.920, ...
- 8 components are needed for 90%. PC1 + PC2 keep 55.4%.
- PC1: positive for flavanoids (0.42), total phenols (0.40), OD280 (0.38), proanthocyanins (0.31). Negative for nonflavanoid phenols (-0.30), malic acid (-0.25), alcalinity of ash (-0.24). So PC1 is about how rich the wine is in phenols and flavanoids.
- PC2: positive for colour intensity (0.53), alcohol (0.48), proline (0.37). Negative for hue (-0.28). So PC2 is about colour and alcohol.
- In the single-colour PC1-PC2 plot I see about 3 groups.

**K-Means:**
- (a) With n_init=1 and random_state 0 to 7 the inertia is between 1277.9 and 1282.5. The values differ because the random starting centres differ and the algorithm can stop in a different local minimum. n_init=10 runs 10 starts and keeps the lowest inertia.
- (b) Inertia for k=1..10: 2314, 1659, 1278, 1181, 1110, 1044, 996, 945, 913, 865. The elbow is at k=3, because after that the curve becomes flat. We cannot choose k by lowest inertia because it always decreases when k grows (it would be 0 with k=178).

**Clusters (k=3), sizes 65 / 51 / 62:**
- Cluster 0: low alcohol (12.25), pale colour (colour intensity 2.97), low proline (510). Light wines.
- Cluster 1: lots of malic acid (3.31), very low flavanoids (0.82) and OD280 (1.70), darkest colour (7.23), lowest hue (0.69). Sour, dark wines with few phenols.
- Cluster 2: highest alcohol (13.68), flavanoids (3.00), OD280 (3.16) and proline (1100). Strong wines rich in phenols and proline.

**The reveal (agreement with the real cultivars):**

| version | agreement |
|---|---|
| scaled data | 0.966 |
| raw data | 0.702 |
| first 2 PCs of scaled data | 0.966 |

- Raw is bad because K-Means uses distances, and on raw data proline dominates the distance (as in the raw PCA). The other 12 measurements hardly count.
- Scaled is good because all 13 measurements count equally.
- The first 2 PCs give the same 0.966. They keep only 55% of the variance, but the structure that separates the cultivars is in this plane (phenols on PC1, colour and alcohol on PC2).
- K-Means never saw the cultivars, but it put 172 of 178 wines in the right group. So the three grape varieties really have different chemistry.

### Snakemake (B7)

Snakefile with 4 rules: all, fetch, session_a, session_b. One command to reproduce all of PW4:

    snakemake --cores 1

1. snakemake -n prints the plan without running anything. When everything is already built it says "Nothing to be done".
2. I deleted data/ and results/ and ran snakemake --cores 1. It ran all 4 steps in order: fetch, session_a, session_b, all.
3. I ran the same command again. It said "Nothing to be done", because all output files exist and none of the inputs is newer than its output.
4. I changed K in sessionA.py and ran again. Only session_a and all ran. session_a reran because sessionA.py is one of its inputs and is newer than the output. session_b did not rerun because sessionB.py did not change. fetch did not rerun because data/concrete.csv exists and fetch has no inputs, so it can never be out of date. (After this test I changed K back to 7 and ran again so the results match this README.)
