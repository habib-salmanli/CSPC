import pandas as pd
from scipy import stats

df = pd.read_csv("chemicals_cancer.csv")
print(df.shape)
print(df.head())
print(df.columns.tolist())

target_col = df.columns[-1]  
print("target column:", target_col)

for chem in ["benzene", "cadmium"]:
    r, p = stats.pearsonr(df[chem], df[target_col])
    print(f"{chem} vs {target_col}: r={r:.3f}, p={p:.3g}")