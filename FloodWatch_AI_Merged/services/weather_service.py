"""
Weather service for FloodWatch AI.

Uses the free Open-Meteo geocoding and forecast APIs (no API key required).
Returns normalized weather fields. These values are weather observations/
forecasts, NOT direct measurements of river level or soil moisture.
"""
from __future__ import annotations

from typing import Any
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT_SECONDS = 10


class WeatherServiceError(RuntimeError):
    """Raised when location lookup or weather retrieval fails."""


def _get_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise WeatherServiceError(f"Weather service request failed: {exc}") from exc
    except ValueError as exc:
        raise WeatherServiceError("Weather service returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise WeatherServiceError("Weather service returned an unexpected response.")
    return data


def geocode_location(location: str) -> dict[str, Any]:
    """Find a location and return its name, country, latitude and longitude."""
    if not isinstance(location, str) or not location.strip():
        raise ValueError("Please enter a location.")

    data = _get_json(
        GEOCODING_URL,
        {"name": location.strip(), "count": 1, "language": "en", "format": "json"},
    )
    results = data.get("results") or []
    if not results:
        raise WeatherServiceError(f"No location found for '{location.strip()}'.")

    place = results[0]
    return {
        "name": place.get("name", location.strip()),
        "country": place.get("country", ""),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
    }


def get_weather(location: str) -> dict[str, Any]:
    """
    Retrieve current conditions and the next 24-hour precipitation forecast.

    Returns a normalized dictionary with:
      location, country, latitude, longitude, observed_at, temperature_c,
      relative_humidity_percent, precipitation_mm, wind_speed_kmh,
      next_24h_precipitation_mm, source, is_live_data.
    """
    place = geocode_location(location)
    data = _get_json(
        FORECAST_URL,
        {
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": (
                "temperature_2m,relative_humidity_2m,precipitation,"
                "wind_speed_10m"
            ),
            "hourly": "precipitation",
            "forecast_days": 2,
            "timezone": "auto",
        },
    )

    current = data.get("current") or {}
    hourly = data.get("hourly") or {}
    times = hourly.get("time") or []
    rain_values = hourly.get("precipitation") or []

    # Sum the next 24 hourly precipitation forecasts, beginning at the
    # current forecast hour when its timestamp is found.
    start_index = 0
    current_time = current.get("time")
    if current_time in times:
        start_index = times.index(current_time)
    next_24 = [
        value for value in rain_values[start_index:start_index + 24]
        if isinstance(value, (int, float))
    ]

    return {
        "location": place["name"],
        "country": place["country"],
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "observed_at": current.get("time"),
        "temperature_c": current.get("temperature_2m"),
        "relative_humidity_percent": current.get("relative_humidity_2m"),
        "precipitation_mm": current.get("precipitation"),
        "wind_speed_kmh": current.get("wind_speed_10m"),
        "next_24h_precipitation_mm": round(sum(next_24), 2) if next_24 else None,
        "source": "Open-Meteo",
        "is_live_data": True,
        "note": (
            "Weather data is not a substitute for river-gauge measurements "
            "or official flood warnings."
        ),
    }
