import app as app_module

def client():
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()

def test_pages():
    c=client()
    for path in ["/","/dashboard","/prediction","/alerts","/history"]:
        assert c.get(path).status_code == 200

def test_dashboard_api():
    response=client().get("/api/dashboard")
    assert response.status_code == 200
    assert response.is_json

def test_sample_input():
    response=client().get("/api/sample-input")
    assert response.status_code == 200
    assert "Rainfall_mm" in response.get_json()

def test_prediction_rejects_missing_fields():
    response=client().post("/predict",data={})
    assert response.status_code == 400
