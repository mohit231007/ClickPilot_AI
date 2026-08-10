import pytest

from clickpilot.demo_data import generate_demo_dataset
from clickpilot.features import add_features, model_matrix


def test_feature_engineering_creates_interactions():
    frame = generate_demo_dataset(rows=5, seed=1, include_target=True)
    transformed = add_features(frame)
    assert {
        "hour",
        "minute",
        "dow",
        "is_weekend",
        "daypart",
        "user_product",
        "campaign_webpage",
        "gender_age",
    }.issubset(transformed.columns)
    assert len(model_matrix(frame)) == 5


def test_invalid_datetime_fails_fast():
    frame = generate_demo_dataset(rows=2, seed=2, include_target=True)
    frame.loc[0, "DateTime"] = "not-a-date"
    with pytest.raises(ValueError, match="DateTime contains"):
        add_features(frame)
