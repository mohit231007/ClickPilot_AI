# ClickPilot AI live deployment status

## Public endpoints

- Live application: https://clickpilot-ai-mohit.streamlit.app/
- FastAPI service: https://clickpilot-api.onrender.com
- API documentation: https://clickpilot-api.onrender.com/docs
- Health endpoint: https://clickpilot-api.onrender.com/health
- Model metadata: https://clickpilot-api.onrender.com/model-info
- Original benchmark evidence: https://clickpilot-api.onrender.com/benchmark
- Source repository: https://github.com/mohit231007/ClickPilot_AI

## Backend

- Provider: Render
- Service: `clickpilot-api`
- Runtime: Docker
- Plan: Free
- Blueprint-managed from the repository root `render.yaml`
- Auto-deploy trigger: commits to the connected repository

The first public deployment succeeded on 2026-08-11 (IST). The initial base URL returned FastAPI's default 404 because no `/` route existed. A human-friendly root route was then added so the public API landing URL exposes the service name, status, API version, and navigation paths.

Because the backend runs on Render's free plan, it may cold-start after inactivity. The Streamlit client therefore uses a configurable HTTP timeout with a 90-second default via `CLICKPILOT_HTTP_TIMEOUT`.

## Frontend

- Provider: Streamlit Community Cloud
- Public URL: https://clickpilot-ai-mohit.streamlit.app/
- Repository: `mohit231007/ClickPilot_AI`
- Branch: `main`
- Entrypoint: `app/Home.py`
- Backend secret: `CLICKPILOT_API_URL = "https://clickpilot-api.onrender.com"`
- Cold-start timeout secret: `CLICKPILOT_HTTP_TIMEOUT = "90"`

Deployment screenshots confirm that the application loads publicly and the top-level runtime card reports **FastAPI**, showing that the frontend is configured in deployed-backend mode rather than local-package mode.

## Functional acceptance status

Completed:

- [x] Render Blueprint created and synced
- [x] Docker FastAPI service deployed
- [x] Public API URL created
- [x] Streamlit Community Cloud app deployed
- [x] Public Streamlit URL created
- [x] Streamlit configured with the Render API URL
- [x] Application loads publicly
- [x] Runtime card reports `FastAPI`
- [x] Root API landing route added
- [x] Free-tier cold-start timeout hardened
- [x] Single-impression public scoring accepted
- [x] 50-row batch ranking accepted
- [x] Ranked CSV export downloaded and validated
- [x] Baseline-versus-proposed decision simulator accepted
- [x] 1,000-row synthetic monitoring evaluation accepted
- [x] Original case-study metrics remain explicitly separated from synthetic-demo metrics

### Accepted public results

Single score with the default public-demo inputs:

- click probability: 5.00%
- propensity: Medium
- lift vs demo baseline: 0.79×
- expected value / 1K: 50.00

50-row batch:

- audit status: `valid_with_missing_categories`
- invalid datetimes: 0
- duplicate sessions: 0
- mean predicted CTR: 5.96%
- high-propensity share: 4.0%
- expected clicks / 100K: 5,958
- ranked export: 50 rows, `demo-1.0.0`, no missing output values

Scenario simulator:

- baseline probability: 5.51%
- proposed probability: 4.80%
- delta: -0.71 percentage points
- incremental expected clicks: -708 for 100K impressions
- incremental expected value: -1,062.50 under the default economic assumptions

Synthetic monitoring stream:

- rows: 1,000
- observed CTR: 6.40%
- mean predicted CTR: 5.82%
- ROC-AUC ≈ 0.5280
- PR-AUC ≈ 0.0765

These are public-demo acceptance results. They do not replace the original case-study holdout ROC-AUC 0.579538 / PR-AUC 0.078022.

See [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md) for the acceptance record.

## Operational release items

The remaining items are operational / presentation proof rather than core functional QA:

- [ ] Confirm the newest push-triggered CI run after the final documentation commits
- [ ] Confirm a deployment-smoke run after the Render-readiness polling fix
- [ ] Capture a live narrow/mobile-width visual review
- [ ] Commit polished public screenshot assets to the repository
- [ ] Add `Ad_Click_Prediction_Submission_Formatted_Mohit_Bhatnagar.pdf` under `reports/`
- [ ] Record the 20–30 second recruiter demo using `RECRUITER_DEMO.md`

GitHub repository variables for the live URLs are optional because the deployment-smoke workflow now contains the public URLs as safe defaults; variables can still override them if desired.

The product itself has passed public functional acceptance. Remaining work is release evidence and presentation packaging.
