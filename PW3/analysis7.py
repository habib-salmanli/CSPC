import pandas as pd
from scipy import stats

df = pd.read_csv("chemicals_cancer.csv")
chems = ["benzene", "cadmium"]

print("=== Naive analysis (all data) ===")
for chem in chems:
    r, p = stats.pearsonr(df[chem], df["malignancy"])
    print(f"{chem} vs malignancy: r={r:.3f}, p={p:.3g}")

print("\n=== Chemicals vs pollution index ===")
for chem in chems:
    r, p = stats.pearsonr(df[chem], df["pollution_index"])
    print(f"{chem} vs pollution_index: r={r:.3f}")
r, p = stats.pearsonr(df["pollution_index"], df["malignancy"])
print(f"pollution_index vs malignancy: r={r:.3f}")

print("\n=== pollution_index between 40 and 60 ===")
sub = df[(df["pollution_index"] > 40) & (df["pollution_index"] < 60)]
print("n =", len(sub))
for chem in chems:
    r, p = stats.pearsonr(sub[chem], sub["malignancy"])
    print(f"{chem} vs malignancy: r={r:.3f}, p={p:.3g}")