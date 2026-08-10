# ClickPilot AI

> **Turn click probability into better ad-ranking and value-aware campaign decisions.**

[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Model](https://img.shields.io/badge/model-CatBoost-FFCC00.svg)](MODEL_CARD.md)
[![API](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](api/main.py)
[![Frontend](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](app/Home.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**ClickPilot AI** is an end-to-end CTR intelligence platform built from a real ad-click prediction case study. It combines leakage-aware temporal validation, CatBoost personalization, batch scoring, decision economics, monitoring, a Streamlit frontend, and a FastAPI backend.

The original case-study evidence and the public demo model are deliberately separated. The validated metrics below come from the supplied challenge data; the live/public demo model is trained deterministically on synthetic schema-compatible rows so the source dataset is not redistributed.

## Why this project is different

Most CTR projects end at a notebook and an AUC score. ClickPilot AI adds the product and ML-engineering layers required to make a ranking model inspectable and usable:

- score a single ad opportunity,
- rank a batch by click probability,
- convert probability into expected business value using value-per-click and CPM,
- compare baseline vs proposed targeting/placement scenarios,
- expose predictions through FastAPI,
- evaluate labeled post-deployment batches,
- keep original benchmark claims traceable to the case-study notebook/PDF,
- package tests, Docker, CI, monitoring, model-card, security, and responsible-use guidance.

## Validated original case-study result

| Model | ROC-AUC | PR-AUC | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.525902 | 0.065134 | 0.06605 | 0.64463 | 0.11982 |
| LightGBM | 0.543092 | 0.068699 | 0.06842 | 0.60759 | 0.12299 |
| **CatBoost + personalization** | **0.579538** | **0.078022** | **0.07810** | **0.48534** | **0.13455** |

Training data: **463,291 impressions**, **31,331 clicks**, **6.76% CTR**.  
Test data: **128,858 unlabeled impressions**.  
Validation: **train July 2-5 → tune/threshold July 6 → untouched temporal holdout July 7**.

Relative to the Logistic Regression baseline, the selected CatBoost model improved ROC-AUC by about **10.2%** and PR-AUC by about **19.8%**. The absolute metrics remain modest, which is a real limitation and a reason to monitor the system continuously rather than overstate model certainty.

## Personalization evidence

| Feature set | ROC-AUC | PR-AUC |
|---|---:|---:|
| Base | 0.550399 | 0.072366 |
| + user_id | 0.587187 | 0.080151 |
| + user_product | 0.592973 | 0.080994 |
| **+ all interactions** | **0.596135** | **0.081681** |

The largest gain comes from user-level information, with additional lift from user-product and campaign-placement interactions. This is a **ranking-quality** result, not a causal claim that changing a feature creates the modeled CTR increase.

## Product capabilities

### 1. Impression scorer

Enter an ad opportunity and receive:

- predicted click probability,
- propensity band,
- lift versus the synthetic demo baseline,
- expected value per impression / per 1,000 impressions,
- value-positive serve recommendation under user-entered assumptions,
- warnings for categories unseen in synthetic demo training.

### 2. Batch ranking

Upload a CSV, audit schema/date quality, score every row, rank opportunities, inspect expected CTR, and download the ranked output.

If the batch also contains `is_click`, ClickPilot computes live monitoring metrics including ROC-AUC, PR-AUC, Brier score, log loss, precision, recall, and F1.

### 3. Decision simulator

Compare a baseline and proposed ad-delivery configuration through the same model and estimate:

- probability-point change,
- relative probability change,
- incremental expected clicks for a chosen volume,
- incremental expected value under value-per-click and CPM assumptions.

The simulator is explicitly labeled **predictive, not causal**.

### 4. Model evidence

The app exposes the original model comparison, personalization ablation, SMOTE experiment, product CTR evidence, and the seven final business answers from the submitted analysis.

### 5. Monitoring & governance

The product demonstrates the post-deployment path for labeled data and documents the controls required for privacy, fairness, calibration, drift, and feedback-loop monitoring.

## Why SMOTE was rejected

Partial SMOTE reduced false negatives from **2,572 to 2,034**, but ROC-AUC and PR-AUC did not improve. Full balance expanded the benchmark training sample from **80,000 to 148,740 rows (~1.86×)** and slightly reduced F1. The project therefore keeps CatBoost/class-weight/threshold strategies as the preferred production direction instead of adding offline cost without demonstrated ranking lift.

## Architecture

```mermaid
flowchart LR
    A[Streamlit UI] -->|deployed mode| C[FastAPI]
    A -->|local fallback| B[clickpilot package]
    C --> B
    D[Synthetic demo generator] --> E[CatBoost trainer]
    E --> F[Versioned demo model bundle]
    F --> B
    B --> G[Feature engineering]
    G --> H[Click probability]
    H --> I[Ranking]
    H --> J[Value-aware decision]
    H --> K[Monitoring metrics]
    L[Original notebook + PDF] --> M[Immutable benchmark evidence]
    M --> A
    M --> C
```

## Repository layout

```text
clickpilot-ai/
├── app/                         # Streamlit decision interface
├── api/                         # FastAPI service + schemas
├── src/clickpilot/              # Feature, model, inference, audit, simulation logic
├── scripts/                     # Generate demo data, train, predict, local QA
├── tests/                       # Feature, inference and API tests
├── data/sample/                 # Synthetic public demonstration data
├── docs/                        # Architecture, deployment, LinkedIn/resume assets
├── notebooks/                   # Original analytical notebook
├── reports/                     # Polished PDF case study
├── .github/workflows/           # CI + optional deployment smoke checks
├── Dockerfile
├── docker-compose.yml
├── MODEL_CARD.md
└── pyproject.toml
```

## Quick start

```bash
git clone https://github.com/mohit231007/ClickPilot_AI.git
cd ClickPilot_AI
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

Install:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Generate demo data and train the public demo model:

```bash
python scripts/generate_demo_data.py --rows 5000
python scripts/train.py
```

Run the frontend locally (it uses the in-process package by default):

```bash
streamlit run app/Home.py
```

For a true deployed frontend/backend split, set `CLICKPILOT_API_URL` in the Streamlit environment to the public FastAPI base URL. The UI will then route scoring, comparison, and monitoring calls through the backend.

Run the API:

```bash
uvicorn api.main:app --reload --port 8000
```

Open Swagger at `http://127.0.0.1:8000/docs`.

## API example

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "DateTime": "2026-07-06T14:30:00",
    "user_id": "1500",
    "product": "J",
    "campaign_id": "C101",
    "webpage_id": "W1",
    "product_category_1": "1",
    "product_category_2": null,
    "user_group_id": "1",
    "gender": "Male",
    "age_level": "5",
    "user_depth": "2",
    "city_development_index": "4",
    "var_1": "0",
    "value_per_click": 1.5,
    "cpm_cost": 25
  }'
```

The API returns probability, propensity band, expected value, value-aware serve decision, warnings, and model version.

## Quality checks

```bash
ruff check .
pytest -q
python -m compileall src api app scripts
```

Windows full QA:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\qa_local.ps1 -LaunchApp -LaunchApi
```

## Data policy

The repository does **not** assume redistribution rights for the original challenge CSV files. Public demos and automated tests use deterministic synthetic data. To work with authorised source files locally, place them under `data/raw/`, which is ignored by Git.

## Responsible-use boundary

This is a click-propensity decision-support system. It should not be used to make unsupported causal claims or hard demographic exclusions. Historical target aggregates must be computed with past-only or out-of-fold logic. Production deployments should preserve exploration traffic, monitor segment performance/calibration/drift, and apply privacy/fairness review.

See [MODEL_CARD.md](MODEL_CARD.md) and [docs/responsible-use.md](docs/responsible-use.md).

## Portfolio assets

- [LinkedIn launch package](docs/LINKEDIN_LAUNCH.md)
- [Resume-ready project copy](docs/RESUME.md)
- [Portfolio case study](docs/PORTFOLIO_CASE_STUDY.md)
- [Architecture](docs/architecture.md)
- [Deployment guide](docs/deployment.md)
- [Original formatted report / PDF note](reports/README.md)

## Roadmap

- [x] Reusable CTR feature pipeline
- [x] CatBoost synthetic public demo model
- [x] Streamlit impression scorer
- [x] Batch ranking + CSV download
- [x] Value-aware decision economics
- [x] Scenario comparison
- [x] FastAPI prediction service
- [x] Labeled-batch monitoring metrics
- [x] Model card and responsible-use documentation
- [x] Docker + CI + smoke workflow
- [ ] Deploy permanent Streamlit URL
- [ ] Deploy public FastAPI endpoint
- [ ] Add calibration curve and reliability diagram
- [ ] Add SHAP/local explanation panel
- [ ] Add feature-store-compatible historical CTR features
- [ ] Add drift dashboard with PSI/Jensen-Shannon monitoring
- [ ] Add experiment-policy simulator for exploration traffic

## Author

**Mohit Bhatnagar** — Data Scientist

Built as an applied data-science and ML-engineering portfolio project spanning ad-tech modeling, temporal validation, personalization, decision analytics, APIs, deployment, monitoring, and responsible model communication.

## License

MIT. The license applies to this repository's code and documentation, not to third-party/source challenge datasets.
