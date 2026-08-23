"""
Train the PRISM-Edge on-device maternal risk model.

Data: UCI Machine Learning Repository id-863 "Maternal Health Risk Data Set"
(Ahmed et al., 2020; DOI 10.24432/C5DP5D), 1,014 patient records collected via
IoT devices at rural clinics in Bangladesh — features: Age, SystolicBP,
DiastolicBP, Blood Sugar (BS), BodyTemp, HeartRate; label: low/mid/high risk.

Exported artefact: model_weights.json — a small random forest flattened into
arrays of {feature, threshold, left, right} nodes plus leaf class vectors.
Both the Python edge agent and the browser demo evaluate the identical
arithmetic from this one file with zero ML dependencies.

Honest reporting: metrics below are from a held-out stratified split and are
quoted verbatim in README/docs. A linear baseline is trained alongside so the
choice of the forest is justified, not asserted.

Run:  python ml/train_model.py
"""

import json
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import numpy as np

HERE = Path(__file__).parent
CSV_PATH = HERE / "maternal_health_risk_uci863.csv"
OUT_PATH = HERE / "model_weights.json"
LABELS = ["low", "mid", "high"]
FEATURES = ["age", "systolic_bp", "diastolic_bp", "blood_glucose", "body_temp_f", "heart_rate"]


def load_rows():
    with open(CSV_PATH, encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        X, y = [], []
        for row in reader:
            try:
                X.append([
                    float(row["Age"]), float(row["SystolicBP"]), float(row["DiastolicBP"]),
                    float(row["BS"]), float(row["BodyTemp"]), float(row["HeartRate"]),
                ])
                label = row["RiskLevel"].strip().lower()
                y.append(LABELS.index(label.split()[0]) if " " in label else LABELS.index(label))
            except (KeyError, ValueError):
                continue  # skip malformed rows rather than guess
    return np.array(X), np.array(y)


def flatten_tree(tree):
    """sklearn tree -> parallel node arrays evaluable without sklearn."""
    t = tree.tree_
    return {
        "feature": [-1 if f < 0 else int(f) for f in t.feature],
        "threshold": [round(float(v), 6) for v in t.threshold],
        "left": [int(v) for v in t.children_left],
        "right": [int(v) for v in t.children_right],
        # value rows are class-count vectors; normalise to probabilities
        "leaf": [[round(float(c) / float(node.sum()), 6) for c in node.ravel()] for node in t.value],
    }


def main():
    X, y = load_rows()
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Linear baseline (justifies model choice in docs)
    mean, std = X_tr.mean(axis=0), X_tr.std(axis=0)
    lr = LogisticRegression(max_iter=2000).fit((X_tr - mean) / std, y_tr)
    lr_pred = lr.predict((X_te - mean) / std)

    # Portable production model
    rf = RandomForestClassifier(
        n_estimators=40, max_depth=8, random_state=42, n_jobs=-1
    ).fit(X_tr, y_tr)
    rf_pred = rf.predict(X_te)

    export = {
        "dataset": {
            "name": "UCI Maternal Health Risk (id 863)",
            "doi": "10.24432/C5DP5D",
            "n_samples": int(len(X)),
            "features": FEATURES,
            "classes": LABELS,
            "class_order_note": "leaf vectors are [p_low, p_mid, p_high]",
        },
        "forest": {
            "n_trees": 40,
            "max_depth": 8,
            "trees": [flatten_tree(est) for est in rf.estimators_],
        },
        "metrics_holdout": {
            "test_n": int(len(y_te)),
            "forest_accuracy": round(float(accuracy_score(y_te, rf_pred)), 4),
            "forest_f1_macro": round(float(f1_score(y_te, rf_pred, average="macro")), 4),
            "linear_baseline_accuracy": round(float(accuracy_score(y_te, lr_pred)), 4),
            "confusion_matrix_rows_true_low_mid_high": confusion_matrix(y_te, rf_pred).tolist(),
        },
        "trained_with": "sklearn RandomForestClassifier(n_estimators=40, max_depth=8, random_state=42); stratified 80/20 split",
        "trained_on_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    OUT_PATH.write_text(json.dumps(export), encoding="utf-8")

    print(f"samples={len(X)}")
    print(f"forest : acc={export['metrics_holdout']['forest_accuracy']:.3f} "
          f"f1m={export['metrics_holdout']['forest_f1_macro']:.3f}")
    print(f"linear : acc={export['metrics_holdout']['linear_baseline_accuracy']:.3f}")
    print("confusion (rows=true low/mid/high):")
    for row in export["metrics_holdout"]["confusion_matrix_rows_true_low_mid_high"]:
        print("   ", row)
    size_kb = OUT_PATH.stat().st_size / 1024
    print(f"exported -> {OUT_PATH.name} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    sys.exit(main())
