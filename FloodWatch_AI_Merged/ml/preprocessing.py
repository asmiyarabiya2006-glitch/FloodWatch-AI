"""Dataset loading, validation, target mapping, and leakage-aware splitting."""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

TARGET_CANDIDATES = [
    "FloodRisk", "flood_risk", "RiskLevel", "risk_level",
    "FloodOccurrence", "flood_occurrence", "Flood Occurred",
    "flood", "Flood", "target", "label", "FloodProbability"
]

def load_dataset(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}. Download a documented CSV and pass --data PATH."
        )
    if path.suffix.lower() != ".csv":
        raise ValueError("Dataset must be a CSV file.")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Dataset is empty.")
    df.columns = [str(c).strip() for c in df.columns]
    df = df.loc[:, ~df.columns.str.match(r"^Unnamed")]
    if df.columns.duplicated().any():
        raise ValueError("Dataset has duplicate column names.")
    return df

def detect_target(df, requested=None):
    if requested:
        if requested not in df.columns:
            raise ValueError(f"Target '{requested}' not found. Columns: {list(df.columns)}")
        return requested
    lower = {str(c).strip().lower(): c for c in df.columns}
    for candidate in TARGET_CANDIDATES:
        if candidate.lower() in lower:
            return lower[candidate.lower()]
    raise ValueError(
        "Could not detect target. Pass --target TARGET_COLUMN. "
        f"Available columns: {list(df.columns)}"
    )

def map_target_to_classes(y, mode="auto", thresholds=None):
    """Return class labels and mapping notes.

    Existing text labels are preserved. Numeric binary targets become Low/High.
    Numeric continuous FloodProbability is binned using documented default cutoffs
    (<0.35 Low, 0.35–<0.65 Moderate, >=0.65 High). These are demo thresholds,
    not official hydrological thresholds; change them to match the dataset definition.
    """
    s = y.copy()
    if mode == "regression":
        raise ValueError("This module is a classifier; choose a classification target.")
    if s.isna().any():
        raise ValueError("Target contains missing values after preprocessing.")
    if pd.api.types.is_numeric_dtype(s):
        unique = sorted(pd.unique(s))
        if len(unique) == 2:
            mapping = {unique[0]: "Low Risk", unique[1]: "High Risk"}
            return s.map(mapping), {
                "target_mapping": "binary numeric target: lower value=Low Risk, higher value=High Risk",
                "mapping": {str(k): v for k, v in mapping.items()}
            }
        if len(unique) > 10:
            if thresholds is None:
                low_cut, high_cut = 0.35, 0.65
            else:
                low_cut, high_cut = thresholds
            vals = pd.to_numeric(s, errors="coerce")
            if vals.isna().any():
                raise ValueError("Numeric target contains non-numeric values.")
            labels = pd.cut(
                vals, bins=[-float("inf"), low_cut, high_cut, float("inf")],
                labels=["Low Risk", "Moderate Risk", "High Risk"], right=False
            ).astype(str)
            return labels, {
                "target_mapping": "continuous target binned for a demo; thresholds must be validated for your dataset",
                "thresholds": {"low_upper_exclusive": low_cut, "moderate_upper_exclusive": high_cut}
            }
        mapping = {v: f"Class {v}" for v in unique}
        return s.map(mapping), {
            "target_mapping": "numeric multiclass labels converted to readable class names",
            "mapping": {str(k): v for k, v in mapping.items()}
        }
    normalized = s.astype(str).str.strip()
    known = {v.lower() for v in normalized.unique()}
    # Preserve existing Low/Moderate/High labels in a consistent display form.
    aliases = {
        "low": "Low Risk", "low risk": "Low Risk",
        "moderate": "Moderate Risk", "medium": "Moderate Risk",
        "medium risk": "Moderate Risk", "moderate risk": "Moderate Risk",
        "high": "High Risk", "high risk": "High Risk", "severe": "High Risk"
    }
    if all(v.lower() in aliases for v in normalized.unique()):
        return normalized.map(lambda v: aliases[v.lower()]), {
            "target_mapping": "existing risk labels standardized"
        }
    # Otherwise preserve the source's categorical labels without claiming risk semantics.
    return normalized, {"target_mapping": "original categorical labels preserved; interpret using dataset documentation"}

def prepare_features(df, target):
    if target not in df.columns:
        raise ValueError(f"Target '{target}' not found.")
    work = df.dropna(subset=[target]).copy()
    y = work[target]
    X = work.drop(columns=[target])
    X = X.dropna(axis=1, how="all")
    # Remove likely row IDs that can leak ordering rather than environmental signal.
    drop_cols = [c for c in X.columns if str(c).strip().lower() in {"id", "index", "row_id", "unnamed: 0"}]
    X = X.drop(columns=drop_cols, errors="ignore")
    # Remove columns with all values identical.
    constant_cols = [c for c in X.columns if X[c].nunique(dropna=True) <= 1]
    X = X.drop(columns=constant_cols, errors="ignore")
    if X.empty:
        raise ValueError("No usable feature columns remain.")
    if y.nunique() < 2:
        raise ValueError("Target must contain at least two classes.")
    return X, y, {"dropped_id_columns": drop_cols, "dropped_constant_columns": constant_cols}

def split_data(X, y, test_size=0.2, random_state=42):
    if not 0.1 <= test_size <= 0.4:
        raise ValueError("test_size must be between 0.1 and 0.4.")
    stratify = y if y.value_counts().min() >= 2 else None
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=stratify)
