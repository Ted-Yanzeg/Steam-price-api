#!/usr/bin/env python3
"""
train.py  – Filter out free games (price_usd == 0) and predict log(price)
"""
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from sklearn.linear_model import Ridge
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from numpy import log1p, expm1

# Path 
CSV = "data/steam_games.csv"
df = pd.read_csv(CSV)

# Keep only games with price > 0 and drop rows missing required fields
df = df.query("price_usd > 0").dropna(subset=[
    "release_year", "positive_ratio", "total_reviews",
    "is_multiplayer", "genres", "price_usd"
])

# --------- 2. Process genres column -----------
# Split the 'genres' string into a list
df["genre_list"] = df["genres"].str.split("|")
mlb = MultiLabelBinarizer()
genre_dms = pd.DataFrame(
    mlb.fit_transform(df["genre_list"]),
    columns=[f"g_{g}" for g in mlb.classes_],
    index=df.index
)
# Keep only genres that appear in at least 30 games
keep = genre_dms.columns[genre_dms.sum() >= 30]
df = pd.concat([df, genre_dms[keep]], axis=1)

# --------- 3. Construct feature matrix X and target y -----------
numeric = ["release_year", "positive_ratio", "total_reviews"]
binary = ["is_multiplayer"] + list(keep)
X = df[numeric + binary]
y = log1p(df["price_usd"])  # Log-transform price for smoother distribution

# Drop any remaining rows with NaN values
mask = X.notna().all(axis=1)
X, y = X[mask], y[mask]

# --------- 4. Build preprocessing and modeling pipeline -----------
pre = ColumnTransformer([
    ("num", StandardScaler(), numeric),
    ("bin", "passthrough", binary)
])
pipe = Pipeline([
    ("prep", pre),
    ("reg", Ridge(alpha=1.0, random_state=42))
])

# Split data into train and test sets
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# Fit the model
pipe.fit(X_tr, y_tr)
print(f"R² on paid-only test: {pipe.score(X_te, y_te):.4f}")

# --------- 5. Save the trained model and MultiLabelBinarizer -----------
os.makedirs("model", exist_ok=True)
joblib.dump({"model": pipe, "mlb": mlb}, "model/paid_price_model.pkl")
print("paid_price_model.pkl saved")
