import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("heart.csv")

r, p_r = stats.pearsonr(df["age"], df["thalach"])
rho, p_s = stats.spearmanr(df["age"], df["thalach"])
print(f"Pearson:  r={r:.3f}, p={p_r:.4g}")
print(f"Spearman: rho={rho:.3f}, p={p_s:.4g}")

plt.scatter(df["age"], df["thalach"], alpha=0.6)
plt.xlabel("age (years)")
plt.ylabel("max heart rate thalach (bpm)")
plt.title("age vs thalach")
plt.savefig("age_thalach.png")