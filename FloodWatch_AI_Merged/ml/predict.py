"""Reusable prediction function for Flask integration."""
import argparse, json
from pathlib import Path
import joblib
import pandas as pd

DEFAULT_MODEL = Path(__file__).resolve().parent / "flood_model.pkl"

def load_model(model_path=DEFAULT_MODEL):
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path}. Train first: python -m ml.train_model")
    artifact = joblib.load(path)
    for key in ("model", "target", "feature_columns", "task"):
        if key not in artifact:
            raise ValueError("Model artifact is incomplete. Retrain it.")
    return artifact

def predict_one(features, model_path=DEFAULT_MODEL):
    artifact = load_model(model_path)
    expected = artifact["feature_columns"]
    missing = [c for c in expected if c not in features]
    if missing:
        raise ValueError("Missing required features: " + ", ".join(missing))
    row = pd.DataFrame([{c: features[c] for c in expected}])
    model = artifact["model"]
    label = model.predict(row)[0]
    result = {
        "prediction": str(label),
        "risk_level": str(label),
        "target": artifact["target"],
        "task": artifact["task"],
    }
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(row)[0]
        classes = model.named_steps["model"].classes_
        result["class_probabilities"] = {
            str(c): float(p) for c, p in zip(classes, probabilities)
        }
        result["probability_note"] = "Model probabilities are estimates, not calibrated real-world flood probabilities."
    return result

def main():
    p = argparse.ArgumentParser(description="Predict flood risk from a JSON feature record.")
    p.add_argument("--input", required=True, help="JSON file with the exact training feature names")
    p.add_argument("--model", default=str(DEFAULT_MODEL))
    args = p.parse_args()
    with open(args.input, encoding="utf-8") as f:
        features = json.load(f)
    print(json.dumps(predict_one(features, args.model), indent=2))

if __name__ == "__main__":
    main()
