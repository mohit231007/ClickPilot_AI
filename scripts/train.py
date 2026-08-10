"""Train and serialize the deterministic synthetic demo model."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from clickpilot.modeling import save_bundle, train_bundle


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample/synthetic_impressions.csv")
    parser.add_argument("--output", default="artifacts/clickpilot_demo_bundle.joblib")
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    payload = train_bundle(frame, model_version="demo-1.0.0")
    output = save_bundle(payload, Path(args.output))
    print(f"Saved model bundle to {output}")
    print(payload["metrics"])


if __name__ == "__main__":
    main()
