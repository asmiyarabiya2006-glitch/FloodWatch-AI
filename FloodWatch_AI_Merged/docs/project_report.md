# FloodWatch AI – AI-Based Flood Prediction and Early Warning System
**Major Project Report**

Team: *<Member 1>, <Member 2>, <Member 3>, <Member 4>, A. Ganesh (Member 5)*
Institution / Department / Guide: *<fill in>*
Academic Year: *<fill in>*

> Items in `<angle brackets>` must be filled by the team. Results, metrics and screenshots must come
> from the real project run – do not invent them.

---

## 1. Abstract
Floods cause loss of life and property, and early identification of high-risk conditions can help
people prepare. FloodWatch AI is a web-based prototype that predicts flood risk (Low, Moderate, High)
from rainfall, river level, humidity and related inputs using a machine learning model. The system
is built with Python, Flask, Scikit-learn, SQLite and Chart.js, retrieves weather information through a
weather API, generates precautionary alerts and stores prediction history. The prototype reached
**<accuracy / high-risk recall from Member 1's evaluation>** on **<dataset name>**. It is intended for
academic demonstration and is not an official warning service.

## 2. Introduction
Flooding is a recurring natural hazard in many regions, including parts of India. Rising availability
of weather data and machine learning tools makes data-driven risk estimation feasible. This project
combines these into an easy-to-use web application.

## 3. Problem Statement
Flood-risk information is often scattered across sources and is hard for ordinary users to interpret
quickly. There is a need for a simple system that combines weather inputs with a trained model to
present an understandable risk level and precautionary guidance.

## 4. Objectives
1. Build an ML model that classifies flood risk into Low, Moderate and High.
2. Retrieve and process weather data from a weather API.
3. Provide a web interface for prediction, alerts and history.
4. Store predictions in a database for later review.
5. Test the full system and document actual results.

## 5. Existing System
Existing approaches include government meteorological bulletins, hydrological gauging and
dedicated forecasting platforms. *<Add 2–3 real, referenced examples, e.g. national/state agency
portals.>* Common limitations: limited personalised interpretation, complex presentation, and
little integration of ML-based risk classification for small-scale users.

## 6. Proposed System
FloodWatch AI accepts location and environmental inputs, optionally enriches them with weather API
data, predicts risk with a trained classifier, produces an alert message with precautions, saves the
result to SQLite and displays trends on a dashboard.

## 7. System Architecture
See `docs/architecture.md` for the diagram. Summary: browser frontend → Flask backend →
(ML module, weather/alert services, SQLite database).

## 8. Technologies Used
| Area | Technology | Purpose |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | User interface |
| Visualisation | Chart.js | Trend charts |
| Backend | Python, Flask | Routes and integration |
| ML | Scikit-learn, Pandas, NumPy | Model training and prediction |
| Database | SQLite | Prediction storage |
| Data source | Weather API (*<provider>*) | Weather information |
| Testing | pytest | Automated tests |
| Version control | Git, GitHub | Collaboration |

## 9. Dataset Description
*(From Member 1)*
- Dataset name and source: **<fill in – public dataset with link>**
- Number of records: **<fill in>**
- Features used: **<list the exact features>**
- Target label and class definitions: **<fill in>**
- Preprocessing: missing-value handling, encoding, train/test split **<details>**

## 10. Machine Learning Methodology
1. Data collection and cleaning
2. Feature selection
3. Train/test split (without data leakage)
4. Model training (**<Random Forest / other>**)
5. Evaluation using accuracy, precision, recall, F1-score and confusion matrix
6. Saving model as `ml/flood_model.pkl`
7. Prediction function in `ml/predict.py`

Recall for the High Risk class is emphasised because missing a dangerous event is costlier than a
false alarm.

## 11. Module Descriptions
| Module | Member | Description |
|---|---|---|
| ML Prediction | Member 1 | Preprocessing, training, evaluation, prediction |
| Frontend | Member 2 | Pages, styling, charts, form |
| Backend & Database | Member 3 | Flask routes, integration, SQLite |
| Weather & Alerts | Member 4 | Weather API, alert generation |
| Testing & Documentation | Member 5 (A. Ganesh) | Tests, integration checks, report, README, demo |

## 12. Implementation and Screenshots
*(Insert real screenshots; save them in `static/images/` or `docs/screenshots/`.)*
- Figure 1: Landing page
- Figure 2: Dashboard
- Figure 3: Prediction form
- Figure 4: Prediction result
- Figure 5: Alerts page
- Figure 6: History page
- Figure 7: Confusion matrix

## 13. Testing and Actual Results
Testing approach: unit tests (model, database), route tests (Flask test client) and manual
end-to-end integration tests. Full details are in `docs/test_results.md`.

| Test type | Tests run | Passed | Failed |
|---|---|---|---|
| Model | <actual> | <actual> | <actual> |
| Database | <actual> | <actual> | <actual> |
| Routes | <actual> | <actual> | <actual> |
| Integration (manual) | <actual> | <actual> | <actual> |

Model metrics (from Member 1): Accuracy **<>**, Precision **<>**, Recall **<>**, F1 **<>**.

## 14. Limitations
- Prototype; not an official emergency-warning service.
- Accuracy depends on dataset quality and may not generalise to all locations.
- Weather API may not provide every feature (e.g. soil moisture, river level).
- Unit/time-resolution mismatch between API data and training data must be handled carefully.
- Predictions are risk estimates, not guarantees.

## 15. Future Enhancements
- Real-time river-gauge integration
- SMS/email notifications
- Map-based risk visualisation
- Deep learning / time-series forecasting
- Multi-language support (including Tamil)
- User authentication and per-user alerts

## 16. Conclusion
FloodWatch AI demonstrates how machine learning, weather data and a web interface can be combined
into a flood-risk prediction prototype. *<Add 2–3 sentences summarising actual achieved results and
learning outcomes after testing.>*

## 17. References
*(Add only sources you actually used, e.g.)*
1. Dataset source – <title, author, link, access date>
2. Scikit-learn documentation – https://scikit-learn.org
3. Flask documentation – https://flask.palletsprojects.com
4. Chart.js documentation – https://www.chartjs.org
5. Weather API documentation – <provider link>
