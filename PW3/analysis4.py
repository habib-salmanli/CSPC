import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("heart.csv")

disease = df[df["target"] == 1]["thalach"]
healthy = df[df["target"] == 0]["thalach"]

print("disease: n =", len(disease), "mean =", disease.mean())
print("healthy: n =", len(healthy), "mean =", healthy.mean())


t, p_t = stats.ttest_ind(disease, healthy, equal_var=False)
print(f"Welch t-test: t={t:.3f}, p={p_t:.4g}")


u, p_u = stats.mannwhitneyu(disease, healthy)
print(f"Mann-Whitney: U={u:.1f}, p={p_u:.4g}")


means = [disease.mean(), healthy.mean()]
sems = [disease.sem(), healthy.sem()]
print("SEM disease:", sems[0], " SEM healthy:", sems[1])

plt.bar(["disease", "healthy"], means, yerr=sems, capsize=8)
plt.ylabel("mean thalach (bpm)")
plt.title("Max heart rate by group (mean ± SEM)")
plt.savefig("thalach_groups.png")