import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/concrete.csv")
print("shape:", df.shape)

print("duplicates:", df.duplicated().sum())
print("missing values:")
print(df.isna().sum())

df = df.drop_duplicates().reset_index(drop=True)
print("shape after cleaning:", df.shape)

X = df.drop(columns="strength")
y = df["strength"]

print(df.describe())

import os
os.makedirs("results", exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.scatter(df["cement"], df["strength"], alpha=0.5)
ax1.set_xlabel("cement (kg/m3)")
ax1.set_ylabel("strength (MPa)")
ax2.scatter(df["age"], df["strength"], alpha=0.5)
ax2.set_xlabel("age (days)")
ax2.set_ylabel("strength (MPa)")
plt.tight_layout()
plt.savefig("results/A2_scatter.png")



import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("train:", X_train.shape, "test:", X_test.shape)


lin = LinearRegression()
lin.fit(X_train, y_train)

print("intercept:", lin.intercept_)
for name, c in zip(X.columns, lin.coef_):
    print(f"{name}: {c:.4f}")

pred_train = lin.predict(X_train)
pred_test = lin.predict(X_test)

n, p = X_train.shape
r2_train = r2_score(y_train, pred_train)
r2_adj = 1 - (1 - r2_train) * (n - 1) / (n - p - 1)

print("train RMSE:", np.sqrt(mean_squared_error(y_train, pred_train)))
print("test RMSE:", np.sqrt(mean_squared_error(y_test, pred_test)))
print("test MAE:", mean_absolute_error(y_test, pred_test))
print("train R2:", r2_train)
print("train adj R2:", r2_adj)
print("test R2:", r2_score(y_test, pred_test))


resid = y_test - pred_test
fig, ax = plt.subplots()
ax.scatter(X_test["age"], resid, alpha=0.6)
ax.axhline(0, color="red", linestyle="--")
ax.set_xscale("log")
ax.set_xlabel("age (days, log scale)")
ax.set_ylabel("residual (MPa)")
plt.savefig("results/A4_residuals.png")


from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline

rows = []
for d in [1, 2, 3, 4]:
    poly = make_pipeline(
        PolynomialFeatures(degree=d, include_bias=False),
        StandardScaler(),
        LinearRegression())
    poly.fit(X_train, y_train)
    p = poly[0].n_output_features_
    ptr = poly.predict(X_train)
    pte = poly.predict(X_test)
    n = X_train.shape[0]
    r2tr = r2_score(y_train, ptr)
    adj = 1 - (1 - r2tr) * (n - 1) / (n - p - 1)
    rows.append({
        "degree": d, "p": p,
        "train_RMSE": np.sqrt(mean_squared_error(y_train, ptr)),
        "test_RMSE": np.sqrt(mean_squared_error(y_test, pte)),
        "train_R2": r2tr, "train_adj_R2": adj,
        "test_R2": r2_score(y_test, pte)})

poly_table = pd.DataFrame(rows)
print(poly_table.round(3).to_string(index=False))


from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_text

y_class = (df["strength"] >= 40).astype(int)
print(y_class.value_counts(normalize=True))

Xc_train, Xc_test, c_train, c_test = train_test_split(
    X, y_class, test_size=0.2, random_state=42, stratify=y_class)


ks = [1, 3, 5, 7, 15, 25, 51, 101]
knn_tr, knn_te = [], []
for k in ks:
    m = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    m.fit(Xc_train, c_train)
    knn_tr.append(m.score(Xc_train, c_train))
    knn_te.append(m.score(Xc_test, c_test))
    print(f"K={k}: train={knn_tr[-1]:.3f} test={knn_te[-1]:.3f}")

fig, ax = plt.subplots()
ax.plot(ks, knn_tr, "o-", label="train")
ax.plot(ks, knn_te, "o-", label="test")
ax.set_xscale("log")
ax.set_xlabel("K")
ax.set_ylabel("accuracy")
ax.legend()
plt.savefig("results/A6_knn.png")


K = 7
no_scale = KNeighborsClassifier(n_neighbors=K).fit(Xc_train, c_train)
print("test acc without scaler:", no_scale.score(Xc_test, c_test))


accs = []
for rs in range(5):
    a, b, c, d = train_test_split(X, y_class, test_size=0.2,
                                  random_state=rs, stratify=y_class)
    m = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=K))
    m.fit(a, c)
    accs.append(m.score(b, d))
print("5 splits:", np.round(accs, 3), "std:", np.std(accs))


depths = [1, 2, 3, 4, 5, 6, 8, None]
t_tr, t_te = [], []
for dpt in depths:
    t = DecisionTreeClassifier(criterion="entropy", max_depth=dpt,
                               min_samples_leaf=1, random_state=0)
    t.fit(Xc_train, c_train)
    t_tr.append(t.score(Xc_train, c_train))
    t_te.append(t.score(Xc_test, c_test))
    print(f"depth={dpt}: leaves={t.get_n_leaves()} "
          f"train={t_tr[-1]:.3f} test={t_te[-1]:.3f}")

xs = [d if d is not None else 20 for d in depths]
fig, ax = plt.subplots()
ax.plot(xs, t_tr, "o-", label="train")
ax.plot(xs, t_te, "o-", label="test")
ax.set_xlabel("max_depth (None = 20)")
ax.set_ylabel("accuracy")
ax.legend()
plt.savefig("results/A6_tree.png")


best = DecisionTreeClassifier(criterion="entropy", max_depth=5, random_state=0)
best.fit(Xc_train, c_train)
print(export_text(best, feature_names=list(X.columns), max_depth=2))



from sklearn.metrics import (confusion_matrix, accuracy_score,
                             precision_score, recall_score, f1_score)

knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7))
knn.fit(Xc_train, c_train)
tree = DecisionTreeClassifier(criterion="entropy", max_depth=5, random_state=0)
tree.fit(Xc_train, c_train)

def metrics_row(name, model):
    pred = model.predict(Xc_test)
    tn, fp, fn, tp = confusion_matrix(c_test, pred).ravel()
    return {"model": name, "TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "accuracy": accuracy_score(c_test, pred),
            "precision": precision_score(c_test, pred),
            "recall": recall_score(c_test, pred),
            "f1": f1_score(c_test, pred)}

mt = pd.DataFrame([metrics_row("KNN K=7", knn),
                   metrics_row("Tree depth=5", tree)])
print(mt.round(3).to_string(index=False))
mt.to_csv("results/A_metrics.csv", index=False)


proba = knn.predict_proba(Xc_test)[:, 1]
rows = []
for t in [0.3, 0.5, 0.7, 0.9]:
    pred = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(c_test, pred).ravel()
    rows.append({"threshold": t, "TP": tp, "FP": fp, "FN": fn, "TN": tn,
                 "precision": precision_score(c_test, pred, zero_division=0),
                 "recall": recall_score(c_test, pred)})
print(pd.DataFrame(rows).round(3).to_string(index=False))



from sklearn.inspection import permutation_importance


raw_coef = lin.coef_
std_pipe = make_pipeline(StandardScaler(), LinearRegression())
std_pipe.fit(X_train, y_train)
std_coef = std_pipe[-1].coef_


tree_imp = tree.feature_importances_

pi_knn = permutation_importance(knn, Xc_test, c_test, scoring="f1",
                                n_repeats=20, random_state=0)
pi_tree = permutation_importance(tree, Xc_test, c_test, scoring="f1",
                                 n_repeats=20, random_state=0)

imp = pd.DataFrame({
    "raw_coef": raw_coef,
    "std_coef": std_coef,
    "tree_importance": tree_imp,
    "perm_knn": pi_knn.importances_mean,
    "perm_tree": pi_tree.importances_mean}, index=X.columns)
print(imp.round(3))
imp.to_csv("results/A8_importance.csv")

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, col in zip(axes, ["std_coef", "tree_importance", "perm_knn"]):
    imp[col].sort_values().plot.barh(ax=ax)
    ax.set_title(col)
plt.tight_layout()
plt.savefig("results/A8_importance.png")