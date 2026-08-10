import math

from clickpilot.service import _payload


def test_payload_normalizes_csv_categorical_values_and_missing_data():
    record = {
        "session_id": 1,
        "DateTime": "2026-07-02 01:41:00",
        "user_id": 3784,
        "product": "D",
        "campaign_id": "C102",
        "webpage_id": "W3",
        "product_category_1": 1,
        "product_category_2": math.nan,
        "user_group_id": 11.0,
        "gender": "Female",
        "age_level": 2.0,
        "user_depth": 3.0,
        "city_development_index": 3.0,
        "var_1": 1,
        "is_click": 0,
    }

    payload = _payload(record, value_per_click=1.5, cpm_cost=25.0)

    assert payload["session_id"] == 1
    assert payload["DateTime"] == "2026-07-02 01:41:00"
    assert payload["user_id"] == "3784"
    assert payload["product_category_1"] == "1"
    assert payload["product_category_2"] is None
    assert payload["user_group_id"] == "11"
    assert payload["age_level"] == "2"
    assert payload["user_depth"] == "3"
    assert payload["city_development_index"] == "3"
    assert payload["var_1"] == "1"
    assert "is_click" not in payload
    assert payload["value_per_click"] == 1.5
    assert payload["cpm_cost"] == 25.0
