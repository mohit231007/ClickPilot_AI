"""Backend service abstraction for the Streamlit frontend.

When CLICKPILOT_API_URL is set, the frontend uses the deployed FastAPI service.
Without it, the app falls back to the shared in-process package for local/offline demos.
"""

from __future__ import annotations

import os
from typing import Any

import httpx
import pandas as pd

from clickpilot.inference import ModelBundle, evaluate_labeled_batch, score_impressions
from clickpilot.simulation import compare_scenarios


def api_url() -> str | None:
    value = os.getenv("CLICKPILOT_API_URL", "").strip().rstrip("/")
    return value or None


def backend_mode() -> str:
    return "FastAPI" if api_url() else "Local package"


def _payload(record: dict[str, Any], value_per_click: float, cpm_cost: float) -> dict[str, Any]:
    payload = dict(record)
    dt = payload.get("DateTime")
    if isinstance(dt, pd.Timestamp):
        payload["DateTime"] = dt.isoformat()
    payload["value_per_click"] = float(value_per_click)
    payload["cpm_cost"] = float(cpm_cost)
    return payload


def score_records(
    bundle: ModelBundle,
    frame: pd.DataFrame,
    *,
    value_per_click: float,
    cpm_cost: float,
) -> pd.DataFrame:
    endpoint = api_url()
    if not endpoint:
        return score_impressions(
            bundle,
            frame,
            value_per_click=value_per_click,
            cpm_cost=cpm_cost,
        )

    requests = [
        _payload(record, value_per_click, cpm_cost)
        for record in frame.to_dict(orient="records")
    ]
    with httpx.Client(timeout=30.0) as client:
        response = client.post(f"{endpoint}/predict-batch", json={"impressions": requests})
        response.raise_for_status()
    output = pd.DataFrame(response.json()["predictions"])
    if "session_id" in frame.columns:
        output.insert(0, "session_id", frame["session_id"].values)
    return output


def compare_records(
    bundle: ModelBundle,
    baseline: dict[str, Any],
    proposed: dict[str, Any],
    *,
    value_per_click: float,
    cpm_cost: float,
    volume: int,
) -> dict[str, Any]:
    endpoint = api_url()
    if not endpoint:
        return compare_scenarios(
            bundle,
            baseline,
            proposed,
            value_per_click=value_per_click,
            cpm_cost=cpm_cost,
            volume=volume,
        )
    payload = {
        "baseline": _payload(baseline, value_per_click, cpm_cost),
        "proposed": _payload(proposed, value_per_click, cpm_cost),
        "volume": int(volume),
    }
    with httpx.Client(timeout=30.0) as client:
        response = client.post(f"{endpoint}/compare", json=payload)
        response.raise_for_status()
    return response.json()


def evaluate_records(bundle: ModelBundle, frame: pd.DataFrame) -> dict[str, Any]:
    endpoint = api_url()
    if not endpoint:
        return evaluate_labeled_batch(bundle, frame)

    records = []
    for record in frame.to_dict(orient="records"):
        click = int(record.pop("is_click"))
        payload = _payload(record, 1.0, 0.0)
        payload["is_click"] = click
        records.append(payload)
    with httpx.Client(timeout=30.0) as client:
        response = client.post(f"{endpoint}/evaluate", json={"impressions": records})
        response.raise_for_status()
    return response.json()
