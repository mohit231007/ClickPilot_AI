# ClickPilot AI — v1.0.0 Portfolio Release Notes

## Release summary

ClickPilot AI v1.0.0 turns an ad-click prediction case study into a public CTR ranking and decision-intelligence system.

The release combines:

- leakage-aware temporal model validation,
- CatBoost personalization evidence,
- a deterministic synthetic public-demo model,
- Streamlit Community Cloud frontend,
- Dockerized FastAPI backend on Render,
- single and batch inference,
- ranked CSV export,
- value-aware decision economics,
- predictive scenario comparison,
- labeled-batch monitoring,
- model governance and responsible-use documentation,
- pytest, Ruff, GitHub Actions, Docker and deployment smoke checks.

## Public endpoints

- App: https://clickpilot-ai-mohit.streamlit.app/
- API: https://clickpilot-api.onrender.com
- Swagger: https://clickpilot-api.onrender.com/docs
- Repository: https://github.com/mohit231007/ClickPilot_AI

## Original validated case-study evidence

- 463,291 labeled impressions
- 31,331 clicks
- 6.76% CTR
- 128,858 unlabeled test impressions
- validation: July 2–5 train → July 6 tune/threshold → July 7 untouched holdout
- selected CatBoost + personalization ROC-AUC: **0.579538**
- selected model PR-AUC: **0.078022**
- relative ROC-AUC improvement vs Logistic Regression: ~**10.2%**
- relative PR-AUC improvement vs Logistic Regression: ~**19.8%**

These values remain separate from synthetic public-demo metrics.

## Personalization result

The ablation progressed from:

- base CatBoost ROC-AUC: ~0.550
- + user ID: ~0.587
- + user-product interaction: ~0.593
- + all tested interactions: ~0.596

This is ranking-quality evidence, not proof of causal CTR lift.

## SMOTE decision

Full SMOTE expanded the benchmark training sample from about 80K to about 148.7K rows (~1.86×) without improving ROC-AUC or PR-AUC. Partial SMOTE reduced false negatives at one operating point but also failed to improve ranking metrics. SMOTE was therefore rejected for the portfolio production direction.

## Public acceptance completed

### Single scoring

- probability: 5.00%
- propensity: Medium
- lift vs demo baseline: 0.79×
- expected value / 1K: 50.00
- backend: FastAPI

### Batch ranking / export

- 50 rows
- audit: `valid_with_missing_categories`
- invalid datetimes: 0
- duplicate sessions: 0
- mean predicted CTR: 5.96%
- high-propensity share: 4.0%
- expected clicks / 100K: 5,958
- ranked CSV downloaded and validated: 50 unique sessions, descending probabilities, no missing output values

### Scenario simulator

- baseline: 5.51%
- proposed: 4.80%
- delta: -0.71 percentage points
- incremental expected clicks: -708 over 100K impressions
- incremental expected value: -1,062.50 under default assumptions
- UI explicitly labels the comparison predictive rather than causal

### Monitoring

- 1,000 deterministic synthetic labeled rows
- observed CTR: 6.40%
- mean predicted CTR: 5.82%
- ROC-AUC ≈ 0.5280
- PR-AUC ≈ 0.0765
- Brier ≈ 0.05999
- log loss ≈ 0.23923

These are acceptance/demo metrics, not original holdout metrics.

## Engineering fixes made during deployment

### CI lint boundary

The preserved analytical notebook was initially included in `ruff check .`, producing false notebook-state undefined-name findings. Production CI now lints only `src api app scripts tests`, uses explicit Ruff rule families, tests Python 3.10/3.11/3.12 independently, and uses Node-24-compatible GitHub Actions v6.

### CSV → FastAPI normalization

CSV uploads introduced pandas/numpy scalar types and `NaN` values that were not valid JSON/API categorical values. The service layer now normalizes missing values to `null`, categorical numerics to canonical strings, dates to ISO strings, and numpy scalars to native Python values before HTTP serialization.

### Render deployment race

The first expanded deployment-smoke job could execute before Render finished auto-deploying the newest image. Smoke automation now polls the expected ClickPilot landing contract before running the endpoint suite and uses transient-error retries.

### Free-tier cold start

The Streamlit HTTP client uses a configurable timeout with a 90-second default so a sleeping free Render service does not immediately appear broken.

## Responsible-use boundaries

- do not claim 10.2% CTR uplift; it is relative ROC-AUC improvement
- do not present the ~0.596 personalization ablation as the final untouched holdout score
- do not describe the scenario simulator as causal inference
- do not present synthetic-demo metrics as original-case-study performance
- demographic attributes require fairness/privacy/legal review and should not be used as unsupported hard-exclusion rules

## Known limitations

- original holdout ranking quality is modest
- the public model is synthetic by design
- some high-signal identifiers introduce cold-start/overfitting/privacy concerns
- the portfolio deployment is not a high-throughput real-time ad-serving stack
- live narrow/mobile visual evidence is still a separate presentation QA item
- the formatted binary PDF and screenshot binaries still need repository attachment/upload if not already visible

## Next technical roadmap

- calibrated probabilities and reliability diagram
- SHAP/local explanations
- feature-store-compatible past-only historical CTR features
- drift dashboard (for example PSI / Jensen-Shannon)
- champion/challenger evaluation
- experiment integration for causal lift
- exploration-policy simulator
- service SLOs / latency and error-rate observability

## Release evidence

See:

- `docs/RELEASE_ACCEPTANCE.md`
- `docs/LIVE_DEPLOYMENT_STATUS.md`
- `docs/RECRUITER_DEMO.md`
- `docs/INTERVIEW_DEFENSE.md`
- `docs/LINKEDIN_LAUNCH.md`
- `docs/RESUME.md`
