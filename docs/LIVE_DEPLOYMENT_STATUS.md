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

## Acceptance status

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

Still required before calling the launch QA complete:

- [ ] Confirm `/health`, `/docs`, `/model-info`, and `/benchmark` after the latest Render redeploy
- [ ] Execute one live single-impression score through Streamlit
- [ ] Execute batch ranking and download the result CSV
- [ ] Execute baseline-versus-proposed decision simulation
- [ ] Execute labeled-batch monitoring
- [ ] Review narrow/mobile-width layout
- [ ] Add GitHub repository variables `CLICKPILOT_API_URL` and `CLICKPILOT_APP_URL`
- [ ] Run the scheduled/manual deployment smoke workflow
- [ ] Add a polished public screenshot/demo recording to the repository and LinkedIn launch assets

The project is now publicly deployed. The remaining gate is functional end-to-end acceptance QA, not infrastructure provisioning.
