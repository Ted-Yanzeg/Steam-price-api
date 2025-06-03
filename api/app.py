#!/usr/bin/env python3
"""
api/app.py – Price-prediction endpoint for paid Steam games.
"""

import os
import logging
import traceback

import joblib
import pandas as pd
from flask import Flask, request, jsonify
from numpy import expm1

# ─────────────────── Load model & helpers ────────────────────
ART   = joblib.load("model/paid_price_model.pkl")
model = ART["model"]            # sklearn Pipeline
mlb   = ART["mlb"]              # MultiLabelBinarizer

# columns that the model expects (genre dummies start with g_)
binary_cols = model.named_steps["prep"].transformers_[1][2]
genre_cols  = [c for c in binary_cols if c.startswith("g_")]

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def make_feature_df(payload: dict) -> pd.DataFrame:
    """
    Build the single-row dataframe the Ridge pipeline expects.
    Expected payload keys:
        release_year       int
        positive_ratio     float
        total_reviews      int
        is_multiplayer     0/1
        genres             list[str]
    """
    base = pd.DataFrame([{
        "release_year"  : payload["release_year"],
        "positive_ratio": payload["positive_ratio"],
        "total_reviews" : payload["total_reviews"],
        "is_multiplayer": payload["is_multiplayer"]
    }])

    g_df = pd.DataFrame(
        mlb.transform([payload["genres"]]),
        columns=[f"g_{g}" for g in mlb.classes_]
    ).reindex(columns=genre_cols, fill_value=0)

    return pd.concat([base, g_df], axis=1)


# ──────────────────────── Routes ─────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        X = make_feature_df(payload)
        log_price = float(model.predict(X)[0])
        price = round(expm1(log_price), 2)          # inverse log1p
        return jsonify({"predicted_price": price})
    except Exception as exc:
        logging.error(traceback.format_exc())
        return jsonify({"error": str(exc)}), 500


@app.route("/", methods=["GET"])
def root():
    return "Steam price API running"


# ────────────────────── Entrypoint ───────────────────────────
if __name__ == "__main__":
    # Cloud Run sets $PORT; default to 8080 for local Docker runs
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
