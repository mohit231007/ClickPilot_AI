# ClickPilot AI — Public Release Acceptance

This document records the public acceptance checks completed against the deployed ClickPilot AI portfolio system.

## Public system

- Streamlit: https://clickpilot-ai-mohit.streamlit.app/
- FastAPI: https://clickpilot-api.onrender.com
- Swagger: https://clickpilot-api.onrender.com/docs
- Repository: https://github.com/mohit231007/ClickPilot_AI

## Accepted workflows

### 1. Single-impression scoring

Default public-app acceptance result:

- click probability: **5.00%**
- propensity band: **Medium**
- lift vs synthetic-demo baseline: **0.79×**
- expected value / 1,000 impressions: **50.00**
- decision: **positive expected value** under the entered business assumptions
- runtime backend shown by the UI: **FastAPI**

### 2. Batch ranking and export

Acceptance input: **50 deterministic synthetic impressions**.

Data-quality audit:

- rows: **50**
- status: `valid_with_missing_categories`
- invalid datetimes: **0**
- duplicate sessions: **0**

Live ranking result:

- mean predicted CTR: **5.96%**
- high-propensity share: **4.0%**
- expected clicks / 100K: **5,958**

The ranked CSV export was downloaded and validated end-to-end:

- 50 output rows
- 50 unique session IDs
- 10 output columns
- probabilities sorted descending
- mean probability ≈ **0.05958**
- min probability ≈ **0.03347**
- max probability ≈ **0.09729**
- model version `demo-1.0.0` on all rows
- no missing output values

The same labeled synthetic batch also exercised the evaluation endpoint. Its metrics are synthetic acceptance metrics, not original case-study holdout claims.

### 3. Decision simulator

Public default scenario comparison:

- baseline probability: **5.51%**
- proposed probability: **4.80%**
- delta: **-0.71 percentage points**
- comparison volume: **100,000 impressions**
- incremental expected clicks: **-708**
- incremental expected value: **-1,062.50** with value-per-click 1.50 and CPM 25.00

The UI correctly describes this as a **predictive what-if comparison, not a causal guarantee**.

### 4. Monitoring demonstration

The Monitoring tab successfully evaluated a deterministic labeled synthetic stream of **1,000 rows**.

- observed CTR: **6.40%**
- mean predicted CTR: **5.82%**
- ROC-AUC ≈ **0.5280**
- PR-AUC ≈ **0.0765**
- Brier score ≈ **0.05999**
- log loss ≈ **0.23923**
- precision ≈ **0.0711**
- recall ≈ **0.5313**
- F1 ≈ **0.1255**

The product explicitly states that production monitoring requires real post-deployment labels, privacy-approved features, drift/calibration review, and fairness controls.

## Benchmark separation

The public demo model is intentionally synthetic and deterministic. The original validated case-study evidence remains separate:

- training impressions: **463,291**
- training clicks: **31,331**
- baseline CTR: **6.76%**
- selected CatBoost + personalization holdout ROC-AUC: **0.579538**
- holdout PR-AUC: **0.078022**

Synthetic acceptance metrics must not be presented as replacements for those original holdout metrics.

## Release interpretation

The four user-facing product workflows have passed public functional acceptance: single scoring, batch ranking/export, scenario simulation, and monitoring. The remaining release evidence is operational proof such as final CI/deployment-smoke status, narrow-width visual review, public screenshots/demo recording, and the formatted PDF artifact in `reports/`.
