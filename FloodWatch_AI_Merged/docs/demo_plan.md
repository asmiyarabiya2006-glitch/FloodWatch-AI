# FloodWatch AI – Final Demo Plan & Integration Checklist

## A. Pre-demo checklist
- [ ] Latest `main` branch pulled; app runs with `python app.py`
- [ ] `ml/flood_model.pkl` present
- [ ] Weather API key set (or sample-data mode clearly labelled)
- [ ] Database initialised; a few sample predictions saved
- [ ] `pytest tests/ -v` run and real results recorded in `docs/test_results.md`
- [ ] Screenshots captured for the report
- [ ] Browser zoom, internet and backup screenshots ready

## B. Demo flow (about 8–10 minutes)
| Step | Action | Presenter |
|---|---|---|
| 1 | Introduce project, problem and disclaimer (prototype, not official alerts) | Member 5 |
| 2 | Show architecture diagram | Member 3 |
| 3 | Open landing page and dashboard | Member 2 |
| 4 | Explain dataset, model and evaluation (confusion matrix, High Risk recall) | Member 1 |
| 5 | Enter sample values → generate prediction → show risk category | Member 2 / 3 |
| 6 | Show weather data and generated alert | Member 4 |
| 7 | Open prediction history | Member 3 |
| 8 | Show test results and limitations | Member 5 |
| 9 | Future enhancements and Q&A | All |

Sample input for demo (illustrative values only): Location = Chennai, Rainfall = 80 mm,
Water level = 3.5 m, Humidity = 85%, Soil moisture = 60%.

## C. Final integration checklist
- [ ] Routes match frontend form fields and JS endpoints
- [ ] Prediction feature names match the trained model
- [ ] Weather units match training data units
- [ ] Alerts avoid duplicates and show timestamp/location
- [ ] Stale or unavailable data is clearly labelled
- [ ] Error pages and validation messages work
- [ ] `requirements.txt` installs on a clean machine
- [ ] README instructions work from scratch
- [ ] No API keys committed to GitHub

## D. Likely viva questions (Member 5)
1. How did you test the system? (unit, route, integration, manual)
2. What happens if the weather API fails?
3. Why is recall important for the High Risk class?
4. What are the limitations of the project?
5. How did the team avoid merge conflicts? (one owner per shared file, branches)
