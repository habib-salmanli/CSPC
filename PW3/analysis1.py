import pandas as pd


df = pd.read_csv("heart.csv")


print("shape:", df.shape)
print(df.head())


cont = df[["age", "chol", "trestbps", "thalach"]]
print(cont.describe())
