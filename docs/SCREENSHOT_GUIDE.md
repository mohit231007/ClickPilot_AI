# ClickPilot AI — Portfolio Screenshot Guide

The public application has already been captured during live acceptance testing. This guide standardizes which frames should be committed to the repository and used on LinkedIn / resume portfolio surfaces.

## Recommended repository paths

Create `docs/assets/` and use these names:

| File | What it should show | Recommended use |
|---|---|---|
| `clickpilot-overview.png` | Hero, proof links, original benchmark KPI cards, `Runtime backend: FastAPI` | README hero / LinkedIn Featured |
| `clickpilot-single-score.png` | Single-score result cards + value-aware decision | Recruiter demo / case study |
| `clickpilot-batch-ranking.png` | Batch KPI cards + ranked probability table | README / carousel |
| `clickpilot-batch-audit.png` | 50-row audit with valid-with-missing-categories, 0 invalid dates, 0 duplicate sessions | Data-quality evidence |
| `clickpilot-simulator.png` | 5.51% baseline vs 4.80% proposed + -708 clicks / -1,062.50 value | Decision-intelligence evidence |
| `clickpilot-monitoring.png` | Monitoring KPI cards for the 1,000-row synthetic stream | Governance / MLOps evidence |

## Best README image order

Use at most three images in the main README to avoid making it feel like a screenshot dump:

1. `clickpilot-overview.png`
2. `clickpilot-batch-ranking.png`
3. `clickpilot-simulator.png`

Link the remaining frames from the portfolio case study or `docs/RELEASE_ACCEPTANCE.md`.

## Suggested captions

### Overview

**Public ClickPilot AI deployment — Streamlit frontend connected to the Dockerized FastAPI backend, with original case-study metrics kept separate from the synthetic demo model.**

### Batch ranking

**Live 50-row batch ranking: 5.96% mean predicted CTR, 4.0% high-propensity share and downloadable ranked output after schema/date auditing.**

### Simulator

**Predictive scenario comparison: the default proposed configuration scores 0.71 percentage points below baseline, translating to -708 expected clicks over 100K impressions under the selected assumptions. This is not a causal uplift estimate.**

### Monitoring

**Synthetic post-deployment monitoring path: ranking, probability-quality and calibration-related metrics are evaluated on labeled demo traffic; production monitoring would require real delayed labels and privacy-approved features.**

## Screenshot hygiene

Before committing or publishing a frame:

- crop browser chrome when it adds no proof value
- avoid exposing unrelated tabs, bookmarks, account details, emails or local paths
- keep the ClickPilot brand header or tab name visible when possible
- do not crop away the `Runtime backend: FastAPI` proof on the overview image
- do not present synthetic monitoring metrics without a visible/adjacent demo disclaimer
- use PNG for crisp UI captures; JPEG is acceptable for social media where file size matters
- preserve readable text at normal GitHub/LinkedIn widths

## Current binary-upload limitation

The connected GitHub text-content tools can update Markdown/code but do not provide a safe direct path for committing the local PNG/PDF binaries in this session. The screenshots should therefore be uploaded through GitHub's web interface or normal Git tooling under `docs/assets/` using the names above.

This is a packaging limitation only; the public functional acceptance evidence is recorded in `docs/RELEASE_ACCEPTANCE.md`.
