"""Display evaluation metrics saved by train_model.py."""
import argparse, json
from pathlib import Path

DEFAULT_METRICS = Path(__file__).resolve().parent / "model_metrics.json"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS))
    args = parser.parse_args()
    path = Path(args.metrics)
    if not path.exists():
        raise SystemExit("Metrics not found. Run: python -m ml.train_model")
    data = json.loads(path.read_text(encoding="utf-8"))
    print("=== FloodWatch AI evaluation ===")
    for key in ["dataset_path", "target_column", "rows_total", "training_rows", "test_rows",
                "accuracy", "precision_weighted", "recall_weighted", "f1_weighted", "high_risk_recall"]:
        print(f"{key}: {data.get(key)}")
    print("\nPer-class metrics:")
    for cls, scores in data.get("per_class", {}).items():
        if isinstance(scores, dict) and "precision" in scores:
            print(f"{cls}: precision={scores['precision']:.3f}, recall={scores['recall']:.3f}, f1={scores['f1-score']:.3f}, support={scores['support']}")
    print("\nConfusion matrix labels:", data.get("confusion_matrix_labels"))
    for row in data.get("confusion_matrix", []):
        print(row)
    print("\nNote:", data.get("evaluation_note"))

if __name__ == "__main__":
    main()
