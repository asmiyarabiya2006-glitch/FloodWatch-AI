# FloodWatch AI – System Architecture

## 1. Overview
FloodWatch AI is a three-tier web application: browser frontend, Flask backend with ML and service
modules, and an SQLite database. It is a prototype, not an official warning system.

## 2. Architecture Diagram
```
 ┌────────────────────────────┐
 │  Browser (HTML/CSS/JS,     │
 │  Chart.js)  – Member 2     │
 └─────────────┬──────────────┘
               │ HTTP (forms, JSON)
 ┌─────────────▼──────────────┐
 │  Flask app (app.py)        │  – Member 3
 │  routes, validation,       │
 │  integration               │
 └──┬──────────┬──────────┬───┘
    │          │          │
┌───▼────┐ ┌───▼──────┐ ┌─▼───────────┐
│ ML     │ │ Services │ │ Database    │
│ module │ │ weather, │ │ SQLite      │
│ M1     │ │ alerts M4│ │ db.py  M3   │
└────────┘ └────┬─────┘ └─────────────┘
                │
        ┌───────▼────────┐
        │ Weather API    │ (external)
        └────────────────┘
```

## 3. Data Flow
1. User enters information in the prediction form.
2. Flask validates the input.
3. Weather service supplies available weather data (or reports it as unavailable).
4. ML model predicts the flood-risk category.
5. Alert service prepares a warning message.
6. Database stores the prediction.
7. Dashboard / result page displays the output.

## 4. Module Responsibilities
| Module | Owner | Key files |
|---|---|---|
| ML | Member 1 | `ml/*.py`, `flood_model.pkl` |
| Frontend | Member 2 | `templates/*`, `static/*` |
| Backend + DB | Member 3 | `app.py`, `config.py`, `database/db.py` |
| Weather + Alerts | Member 4 | `services/*.py` |
| Testing + Docs | Member 5 | `tests/*`, `docs/*`, `README.md` |

## 5. Routes (to be confirmed with Member 3)
| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Landing page |
| `/dashboard` | GET | Dashboard |
| `/predict` | GET/POST | Prediction form and result |
| `/alerts` | GET | Alerts |
| `/history` | GET | Prediction history |
| `/api/dashboard` | GET | Dashboard JSON |

## 6. Database Schema (suggested)
Table `predictions`: `id`, `location`, `rainfall`, `water_level`, `risk_level`, `risk_score`, `created_at`.

## 7. External Dependencies
- Weather API provider: **<fill in: provider name, fields available, rate limits – from Member 4>**

## 8. Error Handling Strategy
- Invalid input → clear message, no server crash.
- Missing model file → friendly error.
- Weather API failure → fall back to user input; clearly label unavailable/sample data.
- Database error → logged, user-facing message shown.

## 9. Limitations
Prototype only; accuracy depends on dataset; weather API may lack some fields; not an official alert system.
