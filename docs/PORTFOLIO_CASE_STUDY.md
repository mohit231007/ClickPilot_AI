# ClickPilot AI — Portfolio Case Study

## 1. Business problem

Digital advertising systems serve many impressions, but only a small share convert into clicks. A useful system must do more than output a binary label: it should rank opportunities, support value-aware decisions, compare delivery scenarios, and remain trustworthy as user, product, campaign, placement, and temporal behavior change.

The original dataset contains **463,291 labeled impressions and 31,331 clicks (6.76% CTR)** plus **128,858 unlabeled test impressions**.

## 2. Modeling challenge

The project had three core risks:

1. **Class imbalance** — accuracy can be misleading when clicks are rare.
2. **Temporal leakage** — historical CTR or target aggregates can leak future outcomes if computed across the full labeled dataset.
3. **High-cardinality personalization** — user and interaction features can help ranking, but can also overfit or create privacy/fairness issues.

## 3. Validation design

The case study used time-aware evaluation:

- train/core: July 2-5,
- tune/threshold: July 6,
- untouched holdout: July 7,
- supplied test set begins July 8.

This makes the benchmark closer to forward deployment than a random split.

## 4. Model selection

| Model | ROC-AUC | PR-AUC | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.525902 | 0.065134 | 0.06605 | 0.64463 | 0.11982 |
| LightGBM | 0.543092 | 0.068699 | 0.06842 | 0.60759 | 0.12299 |
| **CatBoost + personalization** | **0.579538** | **0.078022** | **0.07810** | **0.48534** | **0.13455** |

CatBoost was selected. Relative to Logistic Regression, its ROC-AUC improved by about **10.2%** and PR-AUC by about **19.8%**. Those are ranking-metric improvements, not demonstrated business or CTR uplift.

The absolute scores are intentionally not oversold. CTR prediction over a short window is noisy. The operational response is to monitor, calibrate, preserve exploration, and use probability/value ranking rather than claim perfect click prediction.

## 5. Personalization experiment

Ablation results:

| Feature set | ROC-AUC | PR-AUC |
|---|---:|---:|
| Base | 0.550399 | 0.072366 |
| + user_id | 0.587187 | 0.080151 |
| + user_product | 0.592973 | 0.080994 |
| + all interactions | 0.596135 | 0.081681 |

The main insight is that user and contextual affinity improve ranking quality. It does not prove that manually changing those fields causes the score difference. It also increases the need for cold-start, privacy, fairness, and overfitting controls.

## 6. Imbalance experiment

SMOTE was tested rather than assumed to be beneficial.

- No SMOTE: 80,000 rows, ROC-AUC ~0.5394, PR-AUC ~0.0693.
- Partial SMOTE: 96,681 rows, ROC-AUC ~0.5364, PR-AUC ~0.0690.
- Full balance: 148,740 rows, ROC-AUC ~0.5310, PR-AUC ~0.0684.

Partial oversampling reduced false negatives at one operating point, but ranking metrics did not improve. Full balance increased data volume by ~1.86× without AUC lift. The production direction therefore favors CatBoost/class weighting/threshold management instead of full SMOTE.

## 7. Productization

The notebook was converted into a reusable public system:

- `src/clickpilot` owns model, feature, audit, inference, simulation, and evaluation logic.
- Streamlit provides the human decision interface.
- Dockerized FastAPI on Render provides the programmatic contract.
- Synthetic public data proves the end-to-end system without redistributing original challenge rows.
- Batch outputs can be ranked and downloaded.
- Labeled batches can be evaluated using monitoring metrics.
- Docker, pytest, Ruff and GitHub Actions support reproducibility and quality checks.

Public app: https://clickpilot-ai-mohit.streamlit.app/  
API docs: https://clickpilot-api.onrender.com/docs

## 8. Decision layer

A click probability becomes more useful when tied to economics:

`expected value per impression = P(click) × value_per_click − cost_per_impression`

This allows a user to compare model ranking with campaign cost assumptions rather than rely on a fixed 0/1 threshold.

The scenario simulator scores baseline and proposed configurations through the same predictive model. It is explicitly labeled **predictive, not causal**.

## 9. Public acceptance evidence

All four user-facing workflows were exercised successfully through the deployed system.

### Single scoring

- click probability: **5.00%**
- propensity band: **Medium**
- lift vs public-demo baseline: **0.79×**
- expected value / 1K: **50.00**
- runtime backend: **FastAPI**

### Batch ranking and export

Acceptance input: 50 deterministic synthetic impressions.

- audit status: `valid_with_missing_categories`
- invalid datetimes: **0**
- duplicate sessions: **0**
- mean predicted CTR: **5.96%**
- high-propensity share: **4.0%**
- expected clicks / 100K: **5,958**

The ranked output was downloaded and validated: 50 rows, 50 unique sessions, descending probabilities, `demo-1.0.0` on all rows, and no missing output values.

### Scenario comparison

- baseline probability: **5.51%**
- proposed probability: **4.80%**
- delta: **-0.71 percentage points**
- incremental expected clicks: **-708** over 100K impressions
- incremental expected value: **-1,062.50** under the default economic assumptions

### Monitoring demonstration

A 1,000-row deterministic labeled synthetic stream returned:

- observed CTR: **6.40%**
- mean predicted CTR: **5.82%**
- ROC-AUC ≈ **0.5280**
- PR-AUC ≈ **0.0765**
- Brier score ≈ **0.05999**
- log loss ≈ **0.23923**

These are **synthetic public-demo acceptance metrics**, not replacements for the original holdout metrics.

## 10. Deployment engineering lessons

Productization exposed issues that did not exist in the notebook-only workflow:

1. **CI lint boundary:** the preserved analytical notebook was initially linted as a standalone production module. CI now explicitly lints `src api app scripts tests` and evaluates Python 3.10/3.11/3.12 independently.
2. **CSV serialization:** pandas missing values and numpy scalars required normalization before JSON/FastAPI transport. The service layer now converts `NaN` to `null`, normalizes categorical IDs to strings, and converts dates/scalars to JSON-safe values.
3. **Render deployment race:** an expanded smoke job ran before Render finished auto-deploy. Smoke automation now polls the expected landing contract before executing the endpoint suite.
4. **Free-tier cold start:** the frontend HTTP timeout is configurable with a 90-second default so a sleeping Render service does not immediately appear broken.

These deployment findings are part of the project's engineering value: they demonstrate the difference between a notebook that runs and a system that can be used publicly.

## 11. Monitoring and governance

CTR systems can degrade even when code does not change. ClickPilot documents monitoring for:

- ROC-AUC and PR-AUC,
- observed vs predicted CTR,
- Brier score / log loss,
- threshold precision/recall/F1,
- unseen categories and feature drift,
- segment performance and fairness,
- feedback loops caused by over-exploitation,
- API availability, errors, latency, and cold-start behavior.

The project deliberately separates original benchmark metrics, personalization-ablation metrics, synthetic public-demo model metrics, and live synthetic acceptance metrics.

## 12. Portfolio value

The project demonstrates more than classification modeling. It shows:

- temporal validation,
- leakage reasoning,
- CatBoost/high-cardinality categorical handling,
- ablation testing,
- imbalanced-learning trade-offs,
- probability-to-business-value translation,
- backend API design,
- frontend product design,
- public deployment and acceptance testing,
- monitoring and responsible AI,
- Docker/CI/testing/documentation.

That makes it suitable for Data Scientist, Applied ML, ML Engineer, Decision Science, Marketing Analytics, and Ad-Tech portfolio positioning.

## Related release assets

- `docs/RELEASE_ACCEPTANCE.md`
- `docs/RELEASE_NOTES_v1.0.0.md`
- `docs/RECRUITER_DEMO.md`
- `docs/INTERVIEW_DEFENSE.md`
- `docs/LINKEDIN_LAUNCH.md`
- `docs/RESUME.md`
- `MODEL_CARD.md`
