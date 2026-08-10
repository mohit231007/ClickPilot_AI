"""Model loading, scoring, monitoring metrics, and decision economics."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)

from clickpilot.demo_data import generate_demo_dataset
from clickpilot.features import BASE_CATEGORICAL_COLUMNS, model_matrix
from clickpilot.modeling import save_bundle, train_bundle

DEFAULT_MODEL_PATH = Path(os.getenv("CLICKPILOT_MODEL_PATH", "artifacts/clickpilot_demo_bundle.joblib"))


@dataclass
class ModelBundle:
    model: Any
    model_version: str
    metrics: dict[str, Any]
    threshold: float
    demo_baseline_ctr: float
    training_categories: dict[str, list[str]]
    feature_importance: dict[str, float]
    training_rows: int
    random_seed: int

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ModelBundle":
        return cls(
            model=payload["model"],
            model_version=str(payload.get("model_version", "unknown")),
            metrics=dict(payload.get("metrics", {})),
            threshold=float(payload.get("threshold", 0.5)),
            demo_baseline_ctr=float(payload.get("demo_baseline_ctr", 0.0)),
            training_categories=dict(payload.get("training_categories", {})),
            feature_importance=dict(payload.get("feature_importance", {})),
            training_rows=int(payload.get("training_rows", 0)),
            random_seed=int(payload.get("random_seed", 42)),
        )


def load_bundle(path: str | Path = DEFAULT_MODEL_PATH) -> ModelBundle:
    return ModelBundle.from_dict(joblib.load(path))


def load_or_create_bundle(path: str | Path = DEFAULT_MODEL_PATH) -> ModelBundle:
    model_path = Path(path)
    if model_path.exists():
        return load_bundle(model_path)
    demo = generate_demo_dataset(rows=5000, seed=42, include_target=True)
    payload = train_bundle(demo, model_version="demo-1.0.0")
    save_bundle(payload, model_path)
    return ModelBundle.from_dict(payload)


def _unseen_flags(bundle: ModelBundle, frame: pd.DataFrame) -> list[list[str]]:
    flags: list[list[str]] = []
    for _, row in frame.iterrows():
        row_flags: list[str] = []
        for column in BASE_CATEGORICAL_COLUMNS:
            if column not in frame.columns:
                continue
            value = "MISSING" if pd.isna(row[column]) else str(row[column])
            known = set(bundle.training_categories.get(column, []))
            if known and value not in known:
                row_flags.append(f"{column}_unseen_in_demo_training")
        flags.append(row_flags)
    return flags


def _band(probability: float, baseline: float) -> str:
    if baseline <= 0:
        return "Unknown"
    ratio = probability / baseline
    if ratio >= 1.35:
        return "High"
    if ratio <= 0.70:
        return "Low"
    return "Medium"


def score_impressions(
    bundle: ModelBundle,
    frame: pd.DataFrame,
    *,
    value_per_click: float = 1.0,
    cpm_cost: float = 0.0,
) -> pd.DataFrame:
    x = model_matrix(frame)
    probability = np.asarray(bundle.model.predict_proba(x)[:, 1], dtype=float)
    unseen = _unseen_flags(bundle, frame)
    cost_per_impression = float(cpm_cost) / 1000.0
    expected_value = probability * float(value_per_click) - cost_per_impression

    result = pd.DataFrame(index=frame.index)
    if "session_id" in frame.columns:
        result["session_id"] = frame["session_id"].values
    result["click_probability"] = probability
    result["predicted_click"] = (probability >= bundle.threshold).astype(int)
    result["propensity_band"] = [_band(p, bundle.demo_baseline_ctr) for p in probability]
    result["lift_vs_demo_baseline"] = np.where(
        bundle.demo_baseline_ctr > 0, probability / bundle.demo_baseline_ctr, np.nan
    )
    result["expected_value_per_impression"] = expected_value
    result["expected_value_per_1000_impressions"] = expected_value * 1000.0
    result["serve_if_value_positive"] = expected_value > 0
    result["warnings"] = [", ".join(item) for item in unseen]
    result["model_version"] = bundle.model_version
    return result.reset_index(drop=True)


def evaluate_labeled_batch(bundle: ModelBundle, frame: pd.DataFrame) -> dict[str, Any]:
    if "is_click" not in frame.columns:
        raise ValueError("Evaluation requires an is_click column.")
    y_true = pd.to_numeric(frame["is_click"], errors="raise").astype(int).to_numpy()
    probability = bundle.model.predict_proba(model_matrix(frame))[:, 1]
    predicted = probability >= bundle.threshold
    metrics: dict[str, Any] = {
        "rows": int(len(frame)),
        "observed_ctr": float(np.mean(y_true)),
        "mean_predicted_ctr": float(np.mean(probability)),
        "brier": float(brier_score_loss(y_true, probability)),
        "log_loss": float(log_loss(y_true, probability, labels=[0, 1])),
        "precision": float(precision_score(y_true, predicted, zero_division=0)),
        "recall": float(recall_score(y_true, predicted, zero_division=0)),
        "f1": float(f1_score(y_true, predicted, zero_division=0)),
        "threshold": float(bundle.threshold),
    }
    if len(np.unique(y_true)) == 2:
        metrics["roc_auc"] = float(roc_auc_score(y_true, probability))
        metrics["pr_auc"] = float(average_precision_score(y_true, probability))
    else:
        metrics["roc_auc"] = None
        metrics["pr_auc"] = None
    return metrics
