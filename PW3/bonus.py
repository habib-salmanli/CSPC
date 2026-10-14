import numpy as np
import pandas as pd

df = pd.read_csv("heart.csv")

for col in ["target", "sex"]:
    p = df[col].value_counts(normalize=True)
    entropy = -np.sum(p * np.log2(p))
    print(col)
    print(p)
    print(f"entropy = {entropy:.3f} bits (max = {np.log2(len(p)):.3f})")
    print()