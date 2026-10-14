import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("heart.csv")
cols = ["age", "chol", "trestbps", "thalach"]

for col in cols:
    stat, p = stats.shapiro(df[col])
    print(f"{col}: W={stat:.4f}, p={p:.4g}")

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, col in zip(axes.flatten(), cols):
    stats.probplot(df[col], dist="norm", plot=ax)
    ax.set_title(col)

plt.tight_layout()
plt.savefig("qqplots.png")