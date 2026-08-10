from pathlib import Path

from clickpilot.demo_data import generate_demo_dataset
from clickpilot.inference import evaluate_labeled_batch, load_or_create_bundle, score_impressions


def test_bundle_scores_probabilities(tmp_path: Path):
    path = tmp_path / "bundle.joblib"
    bundle = load_or_create_bundle(path)
    frame = generate_demo_dataset(rows=8, seed=8, include_target=False)
    scored = score_impressions(bundle, frame, value_per_click=2.0, cpm_cost=20.0)
    assert len(scored) == 8
    assert scored["click_probability"].between(0, 1).all()
    assert "expected_value_per_1000_impressions" in scored.columns


def test_labeled_evaluation_returns_monitoring_metrics(tmp_path: Path):
    bundle = load_or_create_bundle(tmp_path / "bundle.joblib")
    frame = generate_demo_dataset(rows=300, seed=91, include_target=True)
    metrics = evaluate_labeled_batch(bundle, frame)
    assert metrics["rows"] == 300
    assert 0 <= metrics["observed_ctr"] <= 1
    assert "brier" in metrics
