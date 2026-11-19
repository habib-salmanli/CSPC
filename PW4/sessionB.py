import pandas as pd
from sklearn.datasets import load_wine

wine = load_wine(as_frame=True)
X = wine.data
cultivar = wine.target  
 
print(X.shape)
print(X.describe().T[["mean", "std", "min", "max"]].round(2))


from sklearn.decomposition import PCA

pca_raw = PCA()
pca_raw.fit(X)

print("explained variance ratio (raw):")
print(pca_raw.explained_variance_ratio_.round(4))

load1 = pd.Series(pca_raw.components_[0], index=X.columns)
print("PC1 loadings (raw), sorted:")
print(load1.sort_values(key=abs, ascending=False).round(4))


import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler

os.makedirs("results", exist_ok=True)

scaler = StandardScaler()
Z = scaler.fit_transform(X)
print("Z mean:", Z.mean(axis=0).round(3))
print("Z std:", Z.std(axis=0).round(3))

pca = PCA()
pca.fit(Z)
evr = pca.explained_variance_ratio_
cum = np.cumsum(evr)
print("explained variance ratio:", evr.round(3))
print("cumulative:", cum.round(3))
print("components for 90%:", np.argmax(cum >= 0.9) + 1)
print("PC1+PC2 keep:", cum[1].round(3))


fig, ax = plt.subplots()
ax.bar(range(1, 14), evr, label="each")
ax.plot(range(1, 14), cum, "o-", color="red", label="cumulative")
ax.axhline(0.9, linestyle="--", color="gray")
ax.set_xlabel("component")
ax.set_ylabel("explained variance ratio")
ax.legend()
plt.savefig("results/B3_scree.png")


load = pd.DataFrame(pca.components_[:2].T, index=X.columns, columns=["PC1", "PC2"])
print("PC1 sorted:")
print(load["PC1"].sort_values().round(3))
print("PC2 sorted:")
print(load["PC2"].sort_values().round(3))


scores = pca.transform(Z)
fig, ax = plt.subplots()
ax.scatter(scores[:, 0], scores[:, 1], alpha=0.7)
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
plt.savefig("results/B3_pc1pc2.png")


from sklearn.cluster import KMeans

for rs in range(8):
    km1 = KMeans(n_clusters=3, init="k-means++", n_init=1, random_state=rs)
    km1.fit(Z)
    print(rs, round(km1.inertia_, 3))

ks = range(1, 11)
inertias = []
for k in ks:
    kmk = KMeans(n_clusters=k, init="k-means++", n_init=10, max_iter=300, random_state=0)
    kmk.fit(Z)
    inertias.append(kmk.inertia_)
    print(k, round(kmk.inertia_, 2))

fig, ax = plt.subplots()
ax.plot(list(ks), inertias, "o-")
ax.set_xlabel("k")
ax.set_ylabel("inertia")
plt.savefig("results/B4_elbow.png")

km = KMeans(n_clusters=3, init="k-means++", n_init=10, max_iter=300, random_state=0)
km.fit(Z)
print("sizes:", np.bincount(km.labels_))

centers = pd.DataFrame(scaler.inverse_transform(km.cluster_centers_), columns=X.columns)
print(centers.round(2).T)

fig, ax = plt.subplots()
ax.scatter(scores[:, 0], scores[:, 1], c=km.labels_, alpha=0.7)
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
plt.savefig("results/B5_clusters.png")


def agreement(labels):
    table = pd.crosstab(cultivar, labels)
    return table, table.max(axis=0).sum() / len(cultivar)

km_scaled = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=0).fit(Z)
km_raw = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=0).fit(X)
km_pc = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=0).fit(scores[:, :2])

t1, a1 = agreement(km_scaled.labels_)
t2, a2 = agreement(km_raw.labels_)
t3, a3 = agreement(km_pc.labels_)

print("scaled crosstab:")
print(t1)
print("raw crosstab:")
print(t2)
print("PC1-PC2 crosstab:")
print(t3)

agree = pd.DataFrame({
    "version": ["scaled data", "raw data", "first 2 PCs of scaled data"],
    "agreement": [a1, a2, a3]})
print(agree.round(3).to_string(index=False))
agree.to_csv("results/B_agreement.csv", index=False)