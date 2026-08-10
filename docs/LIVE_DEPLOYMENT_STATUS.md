# ClickPilot AI live deployment status

## Backend

- Provider: Render
- Service: `clickpilot-api`
- Public URL: `https://clickpilot-api.onrender.com`
- Runtime: Docker
- Plan: Free
- Health endpoint: `/health`
- API docs: `/docs`
- Model metadata: `/model-info`
- Original benchmark evidence: `/benchmark`

The first public deployment succeeded on 2026-08-11 (IST). The initial base URL returned FastAPI's default 404 because no `/` route existed. A human-friendly landing route was then added so the root URL exposes the service name, status, API version, and navigation paths.

## Frontend

Pending Streamlit Community Cloud deployment.

Expected coordinates:

- Repository: `mohit231007/ClickPilot_AI`
- Branch: `main`
- Entrypoint: `app/Home.py`
- Secret: `CLICKPILOT_API_URL = "https://clickpilot-api.onrender.com"`

## Release gate

Do not call the project fully live on LinkedIn/resume until the Streamlit frontend is deployed and the end-to-end API-backed workflows pass acceptance QA.
