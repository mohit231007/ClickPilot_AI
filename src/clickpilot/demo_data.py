"""Deterministic synthetic data for the public demo.

The original challenge dataset is intentionally not redistributed. This generator creates
schema-compatible data only to prove that the product, API, tests, and deployment work.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

PRODUCTS = list("ABCDEFGHIJ")
CAMPAIGNS = [f"C{n}" for n in range(101, 111)]
WEBPAGES = [f"W{n}" for n in range(1, 7)]
PRODUCT_CAT_1 = ["1", "2", "3", "4", "5"]
PRODUCT_CAT_2 = ["10", "11", "12", "13", "14", "15"]
USER_GROUPS = [str(n) for n in range(1, 13)]
GENDERS = ["Male", "Female"]
AGE_LEVELS = [str(n) for n in range(1, 7)]
USER_DEPTHS = ["1", "2", "3"]
CITY_INDEX = ["1", "2", "3", "4"]
VAR1 = ["0", "1"]

PRODUCT_EFFECT = {
    "J": 0.38,
    "D": 0.15,
    "H": 0.12,
    "C": 0.09,
    "E": 0.07,
    "I": 0.00,
    "A": -0.05,
    "B": -0.16,
    "F": -0.28,
    "G": -0.34,
}


def _stable_effect(value: str, scale: float) -> float:
    # Stable across Python runs; avoid built-in hash randomisation.
    code = sum((idx + 1) * ord(char) for idx, char in enumerate(value))
    return (((code % 101) / 100.0) - 0.5) * 2.0 * scale


def generate_demo_dataset(rows: int = 5000, seed: int = 42, include_target: bool = True) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    start = pd.Timestamp("2026-07-01 00:00:00")
    minute_offsets = rng.integers(0, 8 * 24 * 60, size=rows)
    datetimes = start + pd.to_timedelta(minute_offsets, unit="m")

    user_ids = rng.integers(1000, 4000, size=rows).astype(str)
    products = rng.choice(PRODUCTS, size=rows, p=[0.04,0.05,0.35,0.09,0.05,0.02,0.02,0.24,0.12,0.02])
    campaigns = rng.choice(CAMPAIGNS, size=rows)
    webpages = rng.choice(WEBPAGES, size=rows)
    pc1 = rng.choice(PRODUCT_CAT_1, size=rows)
    pc2 = rng.choice(PRODUCT_CAT_2, size=rows).astype(object)
    user_groups = rng.choice(USER_GROUPS, size=rows).astype(object)
    genders = rng.choice(GENDERS, size=rows).astype(object)
    age_levels = rng.choice(AGE_LEVELS, size=rows).astype(object)
    depths = rng.choice(USER_DEPTHS, size=rows).astype(object)
    city = rng.choice(CITY_INDEX, size=rows).astype(object)
    var1 = rng.choice(VAR1, size=rows)

    # Missingness broadly echoes the original case-study pattern without reproducing rows.
    pc2[rng.random(rows) < 0.79] = None
    city[rng.random(rows) < 0.27] = None
    low_missing = rng.random(rows) < 0.039
    for arr in (user_groups, genders, age_levels, depths):
        arr[low_missing] = None

    frame = pd.DataFrame(
        {
            "session_id": np.arange(1, rows + 1),
            "DateTime": datetimes,
            "user_id": user_ids,
            "product": products,
            "campaign_id": campaigns,
            "webpage_id": webpages,
            "product_category_1": pc1,
            "product_category_2": pc2,
            "user_group_id": user_groups,
            "gender": genders,
            "age_level": age_levels,
            "user_depth": depths,
            "city_development_index": city,
            "var_1": var1,
        }
    )

    if include_target:
        logits = np.full(rows, -2.70, dtype=float)
        logits += np.array([PRODUCT_EFFECT[p] for p in products])
        logits += np.array([_stable_effect(c, 0.18) for c in campaigns])
        logits += np.array([_stable_effect(w, 0.20) for w in webpages])
        logits += np.array([_stable_effect(u, 0.33) for u in user_ids])
        logits += (datetimes.dayofweek >= 5).astype(float) * 0.10
        logits += np.sin((datetimes.hour.to_numpy() - 8) / 24.0 * 2.0 * math.pi) * 0.12
        logits += (pd.Series(age_levels).fillna("MISSING").eq("5").to_numpy()) * 0.08
        logits += (
            pd.Series(city).fillna("MISSING").eq("4").to_numpy()
            & pd.Series(age_levels).fillna("MISSING").eq("5").to_numpy()
        ) * 0.10
        probability = 1.0 / (1.0 + np.exp(-logits))
        frame["is_click"] = rng.binomial(1, probability)

    return frame
