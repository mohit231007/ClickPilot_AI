"""Batch-score a CSV using a ClickPilot model bundle."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from clickpilot.inference import load_or_create_bundle, score_impressions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="artifacts/ranked_predictions.csv")
    parser.add_argument("--model", default="artifacts/clickpilot_demo_bundle.joblib")
    parser.add_argument("--value-per-click", type=float, default=1.5)
    parser.add_argument("--cpm", type=float, default=25.0)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    bundle = load_or_create_bundle(args.model)
    result = score_impressions(
        bundle,
        frame,
        value_per_click=args.value_per_click,
        cpm_cost=args.cpm,
    ).sort_values("click_probability", ascending=False)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(f"Wrote {len(result):,} ranked predictions to {output}")


if __name__ == "__main__":
    main()
