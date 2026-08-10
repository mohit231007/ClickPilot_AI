"""Scenario comparison utilities for ad opportunity decisions."""

from __future__ import annotations

from typing import Any

import pandas as pd

from clickpilot.inference import ModelBundle, score_impressions


def compare_scenarios(
    bundle: ModelBundle,
    baseline: dict[str, Any],
    proposed: dict[str, Any],
    *,
    value_per_click: float = 1.0,
    cpm_cost: float = 0.0,
    volume: int = 100_000,
) -> dict[str, float | str]:
    frame = pd.DataFrame([baseline, proposed])
    scores = score_impressions(
        bundle,
        frame,
        value_per_click=value_per_click,
        cpm_cost=cpm_cost,
    )
    base_p = float(scores.loc[0, "click_probability"])
    new_p = float(scores.loc[1, "click_probability"])
    base_ev = float(scores.loc[0, "expected_value_per_impression"])
    new_ev = float(scores.loc[1, "expected_value_per_impression"])
    return {
        "baseline_probability": base_p,
        "proposed_probability": new_p,
        "probability_change_points": (new_p - base_p) * 100.0,
        "relative_change": (new_p / base_p - 1.0) if base_p > 0 else 0.0,
        "incremental_expected_clicks": (new_p - base_p) * volume,
        "incremental_expected_value": (new_ev - base_ev) * volume,
        "volume": int(volume),
        "interpretation": "Predictive what-if comparison; not a causal guarantee.",
    }
