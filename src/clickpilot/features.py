"""Feature engineering for ClickPilot AI.

The transformation mirrors the original case-study logic while making it reusable for
both training and inference.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

RAW_REQUIRED_COLUMNS = [
    "DateTime",
    "user_id",
    "product",
    "campaign_id",
    "webpage_id",
    "product_category_1",
    "product_category_2",
    "user_group_id",
    "gender",
    "age_level",
    "user_depth",
    "city_development_index",
    "var_1",
]

BASE_CATEGORICAL_COLUMNS = [
    "product",
    "campaign_id",
    "webpage_id",
    "product_category_1",
    "product_category_2",
    "user_group_id",
    "gender",
    "age_level",
    "user_depth",
    "city_development_index",
    "var_1",
    "user_id",
]

DERIVED_CATEGORICAL_COLUMNS = [
    "dow",
    "is_weekend",
    "daypart",
    "user_product",
    "campaign_webpage",
    "gender_age",
]

NUMERIC_COLUMNS = ["hour", "minute"]
CATBOOST_CATEGORICAL_COLUMNS = BASE_CATEGORICAL_COLUMNS + DERIVED_CATEGORICAL_COLUMNS
MODEL_FEATURES = CATBOOST_CATEGORICAL_COLUMNS + NUMERIC_COLUMNS


def validate_columns(frame: pd.DataFrame, required: Iterable[str] = RAW_REQUIRED_COLUMNS) -> None:
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))


def add_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Create leakage-safe row-level temporal and interaction features."""

    validate_columns(frame)
    x = frame.copy()
    x["DateTime"] = pd.to_datetime(x["DateTime"], errors="coerce")
    if x["DateTime"].isna().any():
        bad = int(x["DateTime"].isna().sum())
        raise ValueError(f"DateTime contains {bad} invalid value(s).")

    x["hour"] = x["DateTime"].dt.hour.astype(float)
    x["minute"] = x["DateTime"].dt.minute.astype(float)
    x["dow"] = x["DateTime"].dt.dayofweek.astype(str)
    x["is_weekend"] = (x["DateTime"].dt.dayofweek >= 5).astype(int).astype(str)
    x["daypart"] = pd.cut(
        x["DateTime"].dt.hour,
        [-1, 5, 11, 16, 20, 23],
        labels=["night", "morning", "afternoon", "evening", "late_evening"],
    ).astype(str)

    for column in BASE_CATEGORICAL_COLUMNS:
        x[column] = x[column].where(x[column].notna(), "MISSING").astype(str)

    x["user_product"] = x["user_id"] + "|" + x["product"]
    x["campaign_webpage"] = x["campaign_id"] + "|" + x["webpage_id"]
    x["gender_age"] = x["gender"] + "|" + x["age_level"]
    return x


def model_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    return add_features(frame)[MODEL_FEATURES].copy()
