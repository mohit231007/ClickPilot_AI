"""Pydantic contracts for ClickPilot AI."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ImpressionRequest(BaseModel):
    DateTime: str = "2026-07-06T14:30:00"
    user_id: str = "1500"
    product: str = "J"
    campaign_id: str = "C101"
    webpage_id: str = "W1"
    product_category_1: str = "1"
    product_category_2: str | None = None
    user_group_id: str | None = "1"
    gender: str | None = "Male"
    age_level: str | None = "5"
    user_depth: str | None = "2"
    city_development_index: str | None = "4"
    var_1: str = "0"
    session_id: int | None = None
    value_per_click: float = Field(default=1.0, ge=0)
    cpm_cost: float = Field(default=0.0, ge=0)

    def to_record(self) -> dict[str, Any]:
        payload = self.model_dump(exclude={"value_per_click", "cpm_cost"})
        return payload


class PredictionResponse(BaseModel):
    click_probability: float
    predicted_click: int
    propensity_band: str
    lift_vs_demo_baseline: float
    expected_value_per_impression: float
    expected_value_per_1000_impressions: float
    serve_if_value_positive: bool
    warnings: list[str]
    model_version: str


class BatchPredictionRequest(BaseModel):
    impressions: list[ImpressionRequest]


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]


class ScenarioRequest(BaseModel):
    baseline: ImpressionRequest
    proposed: ImpressionRequest
    volume: int = Field(default=100_000, gt=0)


class LabeledImpression(ImpressionRequest):
    is_click: int = Field(ge=0, le=1)


class EvaluationRequest(BaseModel):
    impressions: list[LabeledImpression]
