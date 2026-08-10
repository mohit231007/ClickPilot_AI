import os

from fastapi.testclient import TestClient

os.environ["CLICKPILOT_MODEL_PATH"] = "artifacts/test_api_bundle.joblib"

from api.main import app, get_bundle  # noqa: E402

get_bundle.cache_clear()
client = TestClient(app)


def test_root_landing():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "ClickPilot AI API"
    assert body["status"] == "ok"
    assert body["documentation"] == "/docs"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_contract():
    payload = {
        "DateTime": "2026-07-06T14:30:00",
        "user_id": "1500",
        "product": "J",
        "campaign_id": "C101",
        "webpage_id": "W1",
        "product_category_1": "1",
        "product_category_2": None,
        "user_group_id": "1",
        "gender": "Male",
        "age_level": "5",
        "user_depth": "2",
        "city_development_index": "4",
        "var_1": "0",
        "value_per_click": 1.5,
        "cpm_cost": 25.0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["click_probability"] <= 1
    assert body["model_version"].startswith("demo-")


def test_model_info_separates_demo_and_original_benchmark():
    response = client.get("/model-info")
    assert response.status_code == 200
    body = response.json()
    assert "public_demo_model" in body
    assert "original_case_study" in body
    assert body["original_case_study"]["training_impressions"] == 463291
