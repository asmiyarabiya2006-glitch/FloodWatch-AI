"""
Flood alert message helpers for FloodWatch AI.

This module interprets a risk category produced by the project's ML model.
It does not independently establish that a flood is occurring.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


ALERT_CONTENT = {
    "low": {
        "severity": "Low",
        "title": "Low flood risk",
        "message": "The model indicates low flood risk for the supplied data.",
        "actions": [
            "Continue monitoring weather updates.",
            "Follow instructions from local authorities.",
        ],
    },
    "moderate": {
        "severity": "Moderate",
        "title": "Moderate flood risk",
        "message": "The model indicates moderate flood risk. Conditions may change.",
        "actions": [
            "Monitor official weather and local authority updates.",
            "Keep essential items and important documents ready.",
            "Avoid walking or driving through floodwater.",
        ],
    },
    "high": {
        "severity": "High",
        "title": "High flood risk",
        "message": (
            "The model indicates high flood risk. Check official local alerts "
            "and follow emergency-service instructions."
        ),
        "actions": [
            "Check official warnings from local authorities immediately.",
            "Move away from rivers and flood-prone areas if advised.",
            "Do not walk, swim, or drive through floodwater.",
            "Call local emergency services if you are in immediate danger.",
        ],
    },
}


def generate_alert(
    risk_level: str,
    location: str = "Unknown location",
    prediction_time: str | None = None,
    risk_score: float | None = None,
    source: str = "FloodWatch AI model",
) -> dict[str, Any]:
    """
    Build a consistent alert dictionary from a model risk category.

    risk_level accepts low/moderate/high (case-insensitive).
    risk_score is optional and should be a probability between 0 and 1
    only if that is what the model returns.
    """
    if not isinstance(risk_level, str):
        raise ValueError("risk_level must be a string.")

    normalized = risk_level.strip().lower()
    # Accept common model label variants.
    aliases = {
        "medium": "moderate",
        "medium risk": "moderate",
        "moderate risk": "moderate",
        "low risk": "low",
        "high risk": "high",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in ALERT_CONTENT:
        raise ValueError("risk_level must be Low, Moderate, or High.")

    if risk_score is not None:
        if not isinstance(risk_score, (int, float)) or not 0 <= risk_score <= 1:
            raise ValueError("risk_score must be between 0 and 1, or None.")

    content = ALERT_CONTENT[normalized]
    return {
        "location": location.strip() if isinstance(location, str) and location.strip() else "Unknown location",
        "risk_level": content["severity"],
        "title": content["title"],
        "message": content["message"],
        "recommended_actions": list(content["actions"]),
        "risk_score": risk_score,
        "prediction_time": prediction_time or datetime.now(timezone.utc).isoformat(),
        "source": source,
        "is_official_warning": False,
        "disclaimer": (
            "This is a project-generated model alert, not an official warning. "
            "Check local authorities for verified emergency information."
        ),
    }


def generate_weather_caution(weather: dict[str, Any]) -> dict[str, Any] | None:
    """
    Create a cautious heads-up when the next-24-hour rainfall forecast is high.
    The threshold is a configurable demo threshold, not an official flood threshold.
    """
    rainfall = weather.get("next_24h_precipitation_mm")
    if not isinstance(rainfall, (int, float)):
        return None

    # Demo-only threshold; calibrate with local hydrology data before real use.
    if rainfall < 100:
        return None

    return {
        "location": weather.get("location", "Unknown location"),
        "risk_level": "Caution",
        "title": "Heavy rainfall forecast",
        "message": (
            f"The weather forecast indicates about {rainfall:.1f} mm of "
            "precipitation over the next 24 hours. This alone does not confirm flooding."
        ),
        "recommended_actions": [
            "Check official local weather and flood advisories.",
            "Avoid low-lying areas if water begins to rise.",
            "Do not enter floodwater.",
        ],
        "prediction_time": datetime.now(timezone.utc).isoformat(),
        "source": weather.get("source", "Weather service"),
        "is_official_warning": False,
        "disclaimer": (
            "The rainfall threshold is for demonstration only and is not an "
            "official or locally validated flood-warning threshold."
        ),
    }
