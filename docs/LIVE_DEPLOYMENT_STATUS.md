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

The first public deployment succeeded on 2026-08-11 (IST). The initial base URL returned FastAPI's default 404 because no `/` route existed. A human-friendly root route was later added in source, but deployment readiness must not depend on that cosmetic landing route.

The authoritative deployment-readiness contract is `GET /health`, which returns the ClickPilot service health response and is also the endpoint configured as Render's `healthCheckPath`. Deployment smoke now polls `/health` until the expected contract is available; the `/` landing route is checked only as informational portfolio polish.

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
- [x] Free-tier cold-start timeout hardened
- [x] Single-impression public scoring accepted
- [x] 50-row batch ranking accepted
- [x] Ranked CSV export downloaded and validated
- [x] Baseline-versus-proposed decision simulator accepted
- [x] 1,000-row synthetic monitoring evaluation accepted
- [x] Original case-study metrics remain explicitly separated from synthetic-demo metrics
- [x] Latest observed CI run is green
- [x] Deployment smoke #7 is green after switching readiness to `/health`

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

## Deployment-smoke history

Deployment smoke #6 ran for roughly the entire previous 20 × 15-second polling window and failed before downstream endpoint checks because the gate was still waiting for the optional `/` landing route. Commit `bd050fa` changed readiness to the authoritative `/health` contract and kept the landing route informational.

Deployment smoke #7 then completed successfully in **1m09s**, confirming the corrected readiness design and the full live smoke sequence.

## Operational release items

Engineering / operations gates are now complete. Remaining work is presentation proof:

- [ ] Capture a live narrow/mobile-width visual review — see [MOBILE_QA.md](MOBILE_QA.md)
- [ ] Commit polished public screenshot assets — see [SCREENSHOT_GUIDE.md](SCREENSHOT_GUIDE.md)
- [ ] Add `Ad_Click_Prediction_Submission_Formatted_Mohit_Bhatnagar.pdf` under `reports/`
- [ ] Record the 20–30 second recruiter demo using [RECRUITER_DEMO.md](RECRUITER_DEMO.md)

GitHub repository variables for the live URLs are optional because the deployment-smoke workflow contains the public URLs as safe defaults; variables can still override them if desired.

The product has passed public functional acceptance, CI, and live deployment smoke. Remaining work is presentation packaging only.
