"""Generate schema-compatible synthetic public demo data."""

from __future__ import annotations

import argparse
from pathlib import Path

from clickpilot.demo_data import generate_demo_dataset


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="data/sample/synthetic_impressions.csv")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame = generate_demo_dataset(rows=args.rows, seed=args.seed, include_target=True)
    frame.to_csv(output, index=False)
    print(f"Wrote {len(frame):,} synthetic rows to {output}")


if __name__ == "__main__":
    main()
