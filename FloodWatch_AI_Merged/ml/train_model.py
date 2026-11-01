"""Train a Random Forest flood-risk classifier and save evaluation artifacts."""
import argparse
import json
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from ml.preprocessing import load_dataset, detect_target, prepare_features, map_target_to_classes, split_data

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = Path(__file__).resolve().parent / "demo_flood_dataset.csv"
DEFAULT_MODEL = Path(__file__).resolve().parent / "flood_model.pkl"
DEFAULT_METRICS = Path(__file__).resolve().parent / "model_metrics.json"
DEFAULT_CM = Path(__file__).resolve().parent / "confusion_matrix.png"
DEFAULT_REPORT = Path(__file__).resolve().parent / "classification_report.txt"

def build_pipeline(X):
    numeric = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]
    transformers = []
    if numeric:
        transformers.append(("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median"))
        ]), numeric))
    if categorical:
        transformers.append(("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical))
    prep = ColumnTransformer(transformers=transformers, remainder="drop")
    model = RandomForestClassifier(
        n_estimators=300, class_weight="balanced",
        random_state=42, n_jobs=-1, min_samples_leaf=2
    )
    return Pipeline([("preprocessor", prep), ("model", model)])

def train(data_path=DEFAULT_DATA, target_name=None, model_path=DEFAULT_MODEL,
          metrics_path=DEFAULT_METRICS, confusion_path=DEFAULT_CM,
          report_path=DEFAULT_REPORT, test_size=0.2, low_cut=0.35, high_cut=0.65):
    df = load_dataset(data_path)
    target = detect_target(df, target_name)
    X, y_raw, cleaning = prepare_features(df, target)
    y, target_mapping = map_target_to_classes(y_raw, thresholds=(low_cut, high_cut))
    # Classes with too few records cannot be stratified or evaluated reliably.
    counts = y.value_counts()
    if counts.min() < 2:
        raise ValueError(f"Every class needs at least two rows. Class counts: {counts.to_dict()}")
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=test_size)
    pipeline = build_pipeline(X_train)
    pipeline.fit(X_train, y_train)
    pred = pipeline.predict(X_test)
    labels = sorted(y.unique(), key=str)
    cm = confusion_matrix(y_test, pred, labels=labels)
    metrics = {
        "dataset_path": str(Path(data_path)),
        "target_column": target,
        "target_mapping": target_mapping,
        "feature_columns": list(X.columns),
        "dropped_columns": cleaning,
        "rows_total": int(len(X)),
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "class_distribution": {str(k): int(v) for k, v in y.value_counts().items()},
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision_weighted": float(precision_score(y_test, pred, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_test, pred, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_test, pred, average="weighted", zero_division=0)),
        "per_class": classification_report(y_test, pred, labels=labels, output_dict=True, zero_division=0),
        "confusion_matrix_labels": [str(v) for v in labels],
        "confusion_matrix": cm.tolist(),
        "high_risk_recall": (
            float(recall_score(y_test, pred, labels=["High Risk"], average="micro", zero_division=0))
            if "High Risk" in labels else None
        ),
        "evaluation_note": "Held-out split only. Dataset provenance and geographic/time validation determine real-world relevance."
    }
    model_path, metrics_path, confusion_path, report_path = map(Path, [model_path, metrics_path, confusion_path, report_path])
    for path in [model_path, metrics_path, confusion_path, report_path]:
        path.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
        "model": pipeline,
        "target": target,
        "feature_columns": list(X.columns),
        "classes": [str(c) for c in pipeline.named_steps["model"].classes_],
        "target_mapping": target_mapping,
        "task": "classification",
        "dataset_path": str(data_path)
    }
    joblib.dump(artifact, model_path)
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    report = classification_report(y_test, pred, labels=labels, zero_division=0)
    report_path.write_text(report, encoding="utf-8")
    fig, ax = plt.subplots(figsize=(7, 6))
    image = ax.imshow(cm, interpolation="nearest")
    ax.set_title("FloodWatch AI — Confusion Matrix")
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    ax.set_xticks(range(len(labels)), labels=labels, rotation=25, ha="right")
    ax.set_yticks(range(len(labels)), labels=labels)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")
    fig.colorbar(image, ax=ax)
    fig.tight_layout()
    fig.savefig(confusion_path, dpi=150)
    plt.close(fig)
    print("=== FloodWatch AI classifier trained ===")
    print(f"Dataset: {data_path}\nTarget: {target}\nFeatures: {len(X.columns)}")
    print(f"Rows: {len(X)} | train: {len(X_train)} | test: {len(X_test)}")
    print(f"Model saved: {model_path}\nMetrics saved: {metrics_path}")
    print(f"Confusion matrix image: {confusion_path}\nClassification report: {report_path}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Weighted precision: {metrics['precision_weighted']:.4f}")
    print(f"Weighted recall: {metrics['recall_weighted']:.4f}")
    print(f"Weighted F1: {metrics['f1_weighted']:.4f}")
    print(f"High-risk recall: {metrics['high_risk_recall']}")
    print("WARNING: demo dataset is synthetic; use a documented dataset for final project results.")
    return artifact, metrics

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", default=str(DEFAULT_DATA))
    p.add_argument("--target", default=None)
    p.add_argument("--model-out", default=str(DEFAULT_MODEL))
    p.add_argument("--metrics-out", default=str(DEFAULT_METRICS))
    p.add_argument("--confusion-out", default=str(DEFAULT_CM))
    p.add_argument("--report-out", default=str(DEFAULT_REPORT))
    p.add_argument("--test-size", type=float, default=0.2)
    p.add_argument("--low-cut", type=float, default=0.35)
    p.add_argument("--high-cut", type=float, default=0.65)
    args = p.parse_args()
    train(args.data, args.target, args.model_out, args.metrics_out, args.confusion_out,
          args.report_out, args.test_size, args.low_cut, args.high_cut)

if __name__ == "__main__":
    main()
