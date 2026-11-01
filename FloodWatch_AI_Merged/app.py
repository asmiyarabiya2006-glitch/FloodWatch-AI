from __future__ import annotations

import json
import logging
from pathlib import Path
from datetime import datetime, timezone

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from database.db import init_db, get_connection
from ml.predict import predict_one
from services.weather_service import get_weather, WeatherServiceError

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_INPUT_PATH = BASE_DIR / "ml" / "sample_input.json"

FEATURES = [
    ("EventID", "Event ID", "text"),
    ("Start Date", "Start Date (YYYY-MM-DD)", "date"),
    ("End Date", "End Date (YYYY-MM-DD)", "date"),
    ("Peak Flood Level (m)", "Peak Flood Level (m)", "number"),
    ("Peak FL Date", "Peak Flood Level Date (YYYY-MM-DD)", "date"),
    ("Num Peak FL", "Number of Peak Flood Levels", "number"),
    ("Peak Discharge Q (cumec)", "Peak Discharge (cumec)", "number"),
    ("Peak Discharge Date", "Peak Discharge Date (YYYY-MM-DD)", "date"),
    ("Flood Volume (cumec)", "Flood Volume (cumec)", "number"),
    ("Event Duration (days)", "Event Duration (days)", "number"),
    ("Time to Peak (days)", "Time to Peak (days)", "number"),
    ("Recession Time (day)", "Recession Time (days)", "number"),
]

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["JSON_SORT_KEYS"] = False
logging.basicConfig(level=logging.INFO)

init_db()


def _coerce_features(form):
    values = {}
    missing = []
    for key, label, kind in FEATURES:
        raw = (form.get(key) or "").strip()
        if not raw:
            missing.append(label)
            continue
        if kind == "number":
            try:
                number = float(raw)
            except ValueError:
                raise ValueError(f"{label} must be a valid number.")
            if number < 0:
                raise ValueError(f"{label} cannot be negative.")
            values[key] = number
        else:
            values[key] = raw
    if missing:
        raise ValueError("Please complete all model fields: " + ", ".join(missing))
    return values


def _save_prediction(location, features, result):
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO flood_data
            (location, rainfall, water_level, flood_risk, model_target, input_json)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                location,
                None,
                features.get("Peak Flood Level (m)"),
                result.get("risk_level", "Unknown"),
                result.get("target", "Flood Type"),
                json.dumps(features),
            ),
        )
        conn.commit()
    finally:
        conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM flood_data ORDER BY id DESC LIMIT 10").fetchall()
    finally:
        conn.close()
    records = [dict(row) for row in rows]
    return render_template("dashboard.html", records=records, latest=records[0] if records else None)


@app.route("/prediction", methods=["GET"])
def prediction():
    return render_template("prediction.html", features=FEATURES)


@app.route("/predict", methods=["POST"])
def predict():
    location = (request.form.get("location") or "Not specified").strip()
    try:
        features = _coerce_features(request.form)
        result = predict_one(features)
        result["location"] = location
        result["prediction_time"] = datetime.now(timezone.utc).isoformat()
        _save_prediction(location, features, result)
        return render_template("result.html", location=location, features=features, result=result)
    except (ValueError, FileNotFoundError) as exc:
        flash(str(exc), "error")
        return render_template("prediction.html", features=FEATURES, submitted=request.form), 400
    except Exception:
        app.logger.exception("Prediction failed")
        flash("The prediction could not be completed. Check the terminal and model compatibility.", "error")
        return render_template("prediction.html", features=FEATURES, submitted=request.form), 500


@app.route("/alerts")
def alerts():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM flood_data ORDER BY id DESC LIMIT 10").fetchall()
    finally:
        conn.close()
    return render_template("alerts.html", records=[dict(row) for row in rows])


@app.route("/history")
def history():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM flood_data ORDER BY id DESC").fetchall()
    finally:
        conn.close()
    return render_template("history.html", records=[dict(row) for row in rows])


@app.route("/api/dashboard")
def dashboard_api():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM flood_data ORDER BY id DESC LIMIT 50").fetchall()
    finally:
        conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/api/weather")
def weather_api():
    location = (request.args.get("location") or "").strip()
    if not location:
        return jsonify({"error": "Pass a location query parameter."}), 400
    try:
        return jsonify(get_weather(location))
    except (ValueError, WeatherServiceError) as exc:
        return jsonify({"error": str(exc)}), 502


@app.route("/api/sample-input")
def sample_input():
    try:
        return jsonify(json.loads(SAMPLE_INPUT_PATH.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError):
        return jsonify({"error": "Sample input file is missing or invalid."}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
