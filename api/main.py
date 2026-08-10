"""FastAPI inference service for ClickPilot AI."""

from __future__ import annotations

from functools import lru_cache

import pandas as pd
from fastapi import FastAPI, HTTPException

from api.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    EvaluationRequest,
    ImpressionRequest,
    PredictionResponse,
    ScenarioRequest,
)
from clickpilot.benchmark import (
    MODEL_COMPARISON,
    ORIGINAL_BASELINE_CTR,
    ORIGINAL_TEST_IMPRESSIONS,
    ORIGINAL_TRAIN_CLICKS,
    ORIGINAL_TRAIN_IMPRESSIONS,
    PERSONALIZATION_ABLATION,
    SELECTED_MODEL,
    SMOTE_EXPERIMENT,
)
from clickpilot.inference import ModelBundle, evaluate_labeled_batch, load_or_create_bundle, score_impressions
from clickpilot.simulation import compare_scenarios

app = FastAPI(
    title="ClickPilot AI API",
    version="0.1.0",
    description="Production-style CTR scoring, ranking, decision economics, and monitoring demo.",
)


@lru_cache(maxsize=1)
def get_bundle() -> ModelBundle:
    return load_or_create_bundle()


def _prediction_for(request: ImpressionRequest) -> PredictionResponse:
    bundle = get_bundle()
    frame = pd.DataFrame([request.to_record()])
    try:
        row = score_impressions(
            bundle,
            frame,
            value_per_click=request.value_per_click,
            cpm_cost=request.cpm_cost,
        ).iloc[0]
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    warnings = [item.strip() for item in str(row["warnings"]).split(",") if item.strip()]
    return PredictionResponse(
        click_probability=float(row["click_probability"]),
        predicted_click=int(row["predicted_click"]),
        propensity_band=str(row["propensity_band"]),
        lift_vs_demo_baseline=float(row["lift_vs_demo_baseline"]),
        expected_value_per_impression=float(row["expected_value_per_impression"]),
        expected_value_per_1000_impressions=float(row["expected_value_per_1000_impressions"]),
        serve_if_value_positive=bool(row["serve_if_value_positive"]),
        warnings=warnings,
        model_version=str(row["model_version"]),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "clickpilot-ai"}


@app.get("/model-info")
def model_info() -> dict:
    bundle = get_bundle()
    return {
        "public_demo_model": {
            "model_version": bundle.model_version,
            "model_type": "CatBoostClassifier",
            "training_rows": bundle.training_rows,
            "demo_baseline_ctr": bundle.demo_baseline_ctr,
            "threshold": bundle.threshold,
            "metrics": bundle.metrics,
            "feature_importance": bundle.feature_importance,
        },
        "original_case_study": {
            "training_impressions": ORIGINAL_TRAIN_IMPRESSIONS,
            "training_clicks": ORIGINAL_TRAIN_CLICKS,
            "baseline_ctr": ORIGINAL_BASELINE_CTR,
            "test_impressions": ORIGINAL_TEST_IMPRESSIONS,
            "selected_model": SELECTED_MODEL,
            "model_comparison": MODEL_COMPARISON,
            "personalization_ablation": PERSONALIZATION_ABLATION,
            "smote_experiment": SMOTE_EXPERIMENT,
        },
        "data_policy": "Public demo model is trained on deterministic synthetic data; original challenge rows are not redistributed.",
    }


@app.get("/benchmark")
def benchmark() -> dict:
    return {
        "selected_model": SELECTED_MODEL,
        "model_comparison": MODEL_COMPARISON,
        "personalization_ablation": PERSONALIZATION_ABLATION,
        "smote_experiment": SMOTE_EXPERIMENT,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: ImpressionRequest) -> PredictionResponse:
    return _prediction_for(request)


@app.post("/predict-batch", response_model=BatchPredictionResponse)
def predict_batch(request: BatchPredictionRequest) -> BatchPredictionResponse:
    if not request.impressions:
        raise HTTPException(status_code=422, detail="At least one impression is required.")
    return BatchPredictionResponse(predictions=[_prediction_for(item) for item in request.impressions])


@app.post("/compare")
def compare(request: ScenarioRequest) -> dict:
    bundle = get_bundle()
    return compare_scenarios(
        bundle,
        request.baseline.to_record(),
        request.proposed.to_record(),
        value_per_click=request.proposed.value_per_click,
        cpm_cost=request.proposed.cpm_cost,
        volume=request.volume,
    )


@app.post("/evaluate")
def evaluate(request: EvaluationRequest) -> dict:
    if not request.impressions:
        raise HTTPException(status_code=422, detail="At least one labeled impression is required.")
    records = []
    for item in request.impressions:
        payload = item.to_record()
        payload["is_click"] = item.is_click
        records.append(payload)
    try:
        return evaluate_labeled_batch(get_bundle(), pd.DataFrame(records))
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
