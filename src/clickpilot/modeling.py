"""Synthetic-demo CatBoost training and model-bundle serialization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from clickpilot.features import (
    BASE_CATEGORICAL_COLUMNS,
    CATBOOST_CATEGORICAL_COLUMNS,
    MODEL_FEATURES,
    model_matrix,
)


def _select_threshold(y_true: np.ndarray, probability: np.ndarray) -> float:
    thresholds = np.linspace(0.02, 0.35, 100)
    scores = [f1_score(y_true, probability >= t, zero_division=0) for t in thresholds]
    return float(thresholds[int(np.argmax(scores))])


def _category_profile(frame: pd.DataFrame) -> dict[str, list[str]]:
    profile: dict[str, list[str]] = {}
    for column in BASE_CATEGORICAL_COLUMNS:
        values = frame[column].where(frame[column].notna(), "MISSING").astype(str)
        profile[column] = sorted(values.unique().tolist())
    return profile


def train_bundle(
    frame: pd.DataFrame,
    *,
    model_version: str = "demo-1.0.0",
    random_seed: int = 42,
) -> dict[str, Any]:
    if "is_click" not in frame.columns:
        raise ValueError("Training frame must contain is_click.")

    train_frame, val_frame = train_test_split(
        frame,
        test_size=0.25,
        random_state=random_seed,
        stratify=frame["is_click"],
    )

    x_train = model_matrix(train_frame)
    x_val = model_matrix(val_frame)
    y_train = train_frame["is_click"].astype(int).to_numpy()
    y_val = val_frame["is_click"].astype(int).to_numpy()

    model = CatBoostClassifier(
        iterations=90,
        depth=6,
        learning_rate=0.07,
        l2_leaf_reg=5,
        random_strength=1,
        loss_function="Logloss",
        eval_metric="AUC",
        random_seed=random_seed,
        verbose=False,
        allow_writing_files=False,
    )
    model.fit(x_train, y_train, cat_features=CATBOOST_CATEGORICAL_COLUMNS)
    probability = model.predict_proba(x_val)[:, 1]
    threshold = _select_threshold(y_val, probability)
    predicted = probability >= threshold

    metrics = {
        "roc_auc": float(roc_auc_score(y_val, probability)),
        "pr_auc": float(average_precision_score(y_val, probability)),
        "brier": float(brier_score_loss(y_val, probability)),
        "log_loss": float(log_loss(y_val, probability)),
        "precision": float(precision_score(y_val, predicted, zero_division=0)),
        "recall": float(recall_score(y_val, predicted, zero_division=0)),
        "f1": float(f1_score(y_val, predicted, zero_division=0)),
        "validation_rows": int(len(val_frame)),
    }

    # Refit on all synthetic demo rows after holding out a validation slice for QA metrics.
    x_full = model_matrix(frame)
    y_full = frame["is_click"].astype(int).to_numpy()
    final_model = CatBoostClassifier(
        iterations=90,
        depth=6,
        learning_rate=0.07,
        l2_leaf_reg=5,
        random_strength=1,
        loss_function="Logloss",
        eval_metric="AUC",
        random_seed=random_seed,
        verbose=False,
        allow_writing_files=False,
    )
    final_model.fit(x_full, y_full, cat_features=CATBOOST_CATEGORICAL_COLUMNS)

    importances = dict(
        sorted(
            zip(MODEL_FEATURES, final_model.get_feature_importance(), strict=True),
            key=lambda item: item[1],
            reverse=True,
        )
    )

    return {
        "model": final_model,
        "model_version": model_version,
        "metrics": metrics,
        "threshold": threshold,
        "demo_baseline_ctr": float(frame["is_click"].mean()),
        "training_categories": _category_profile(frame),
        "feature_importance": {k: float(v) for k, v in importances.items()},
        "training_rows": int(len(frame)),
        "random_seed": random_seed,
    }


def save_bundle(bundle: dict[str, Any], path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, output)
    return output
