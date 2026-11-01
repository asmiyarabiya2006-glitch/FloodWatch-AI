# FloodWatch AI – Merged Team Project

This folder combines the deliverables from all five members into one Flask application.

## Team modules merged
- **Member 1 – Machine Learning:** `ml/` training, preprocessing, evaluation, prediction code, trained model, dataset and metrics.
- **Member 2 – Frontend:** `templates/` and `static/`; prediction form was updated to collect the exact features used by the trained model.
- **Member 3 – Backend & Database:** `app.py` routes and `database/db.py` SQLite persistence.
- **Member 4 – Weather & Alerts:** `services/weather_service.py` (Open-Meteo API) and `services/alert_service.py`.
- **Member 5 – Testing & Documentation:** `tests/` and `docs/`.

## Important integration finding
The submitted trained model does **not** use rainfall, humidity, soil moisture and water level as its input columns. The model expects 12 historical flood-event fields such as `EventID`, `Start Date`, `Peak Flood Level (m)`, `Peak Discharge Q (cumec)` and `Event Duration (days)`. Its saved target is `Flood Type`, and its classes are **Flood** and **Severe Flood**. Therefore, the merged prediction form asks for those exact 12 fields. Do not claim that the model predicts Low/Moderate/High risk from live weather inputs. The weather service is available separately at `/api/weather?location=...` and its values are not silently substituted into the ML model.

The supplied model artifact was saved with scikit-learn 1.9.1. Install the version in `requirements.txt` to reduce pickle compatibility problems. Do not open a pickle from an untrusted source.

## Run in VS Code (Windows)
1. Extract this ZIP to a simple folder, for example `C:\\FloodWatch_AI_Merged`.
2. Open that folder in VS Code: **File → Open Folder**.
3. Open **Terminal → New Terminal**.
4. Check Python:
   ```powershell
   py --version
   ```
   Use Python 3.11 or 3.12 if available. Avoid reusing an old `.venv` copied from another computer.
5. Create a fresh virtual environment:
   ```powershell
   py -3.12 -m venv .venv
   ```
   If Python 3.12 is not installed, use `py -3.11 -m venv .venv`.
6. Activate it:
   ```powershell
   .venv\\Scripts\\Activate.ps1
   ```
   If PowerShell blocks activation, run this once in that terminal:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .venv\\Scripts\\Activate.ps1
   ```
7. Upgrade pip and install packages:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```
8. Start the website:
   ```powershell
   python app.py
   ```
9. Open this address in Chrome:
   `http://127.0.0.1:5000`

Stop the server with `Ctrl + C`.

## Pages and endpoints
- `/` – Home
- `/dashboard` – Saved prediction summary
- `/prediction` – Model input form
- `/predict` – Model prediction (POST)
- `/alerts` – Model classifications and safety notes
- `/history` – SQLite history
- `/api/dashboard` – Saved predictions as JSON
- `/api/sample-input` – Member 1 sample JSON
- `/api/weather?location=Chennai` – Current/forecast weather from Open-Meteo (internet required)

## Test
```powershell
python -m pytest -q
```

## Model and safety notes
- The project is an academic prototype, not an official flood-warning service.
- The Member 1 evaluation file reports 74.29% held-out accuracy on its supplied event dataset. This is a dataset-specific result, not a guarantee of real-world accuracy.
- Weather data may not include river gauge level or soil moisture. It is displayed through a separate service and is not treated as those measurements.
- Follow official IMD and local disaster-management instructions during real flood situations.

## Retraining the model
See `ml/train_model.py --help` and `docs/dataset_and_features.md`. Retraining replaces `ml/flood_model.pkl`; keep the training and runtime scikit-learn versions aligned.
