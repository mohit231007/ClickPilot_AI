# Deployment Guide

## Target public architecture

```text
Browser / recruiter
       |
       v
Streamlit Community Cloud (app/Home.py)
       |
       | HTTPS/JSON via CLICKPILOT_API_URL
       v
Render FastAPI service (api.main:app)
       |
       v
clickpilot package + deterministic synthetic CatBoost demo bundle
```

The original challenge data is not required for public deployment and is not redistributed. The public runtime creates a deterministic synthetic demo model when no trusted model bundle is present.

## 1. Local

```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev]"
python scripts/generate_demo_data.py --rows 5000
python scripts/train.py
streamlit run app/Home.py
```

API:

```bash
uvicorn api.main:app --reload --port 8000
```

## 2. Docker

```bash
docker compose up --build
```

Frontend: `http://localhost:8501`  
API docs: `http://localhost:8000/docs`

## 3. Deploy the FastAPI backend on Render

The repository root contains `render.yaml`. Create a Render **Blueprint** from this GitHub repository and deploy the `clickpilot-api` service.

The Blueprint is intentionally configured as a free portfolio web service and runs:

```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

Health check:

```text
/health
```

After the first successful deploy, copy the public `https://...onrender.com` base URL. Verify `/health` and `/docs` before connecting the frontend.

> Free Render web services can sleep when idle, so the first request after inactivity can be slower. This is acceptable for a portfolio demo but not an enterprise production SLA.

## 4. Deploy the frontend on Streamlit Community Cloud

Use:

- Repository: `mohit231007/ClickPilot_AI`
- Branch: `main`
- Entrypoint: `app/Home.py`
- Python: `3.12`

The root `requirements.txt` installs both the project package and runtime dependencies so `src/clickpilot` is importable in Community Cloud.

In **Advanced settings → Secrets**, set the Render API URL as a root-level value:

```toml
CLICKPILOT_API_URL = "https://<your-clickpilot-api>.onrender.com"
```

Streamlit exposes root-level secrets as environment variables, which makes the app automatically switch from local-package fallback to FastAPI mode.

See [STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md) for the concise frontend checklist.

## 5. Live acceptance QA

Verify all of the following before publishing the LinkedIn post or adding the live URL to a resume:

1. API `/health` returns success.
2. API `/docs` loads Swagger/OpenAPI.
3. Streamlit home page loads on desktop and mobile widths.
4. Runtime backend indicator says **FastAPI**.
5. Single-impression scoring returns a probability and value-aware decision.
6. Batch CSV upload ranks rows and downloads predictions.
7. Scenario comparison returns baseline/proposed probabilities and economics.
8. Monitoring accepts a labeled synthetic batch and returns classification metrics.
9. Original benchmark metrics remain explicitly separated from synthetic public-demo metrics.
10. No challenge CSVs, secrets, local model artifacts, or `.env` files are committed.

## 6. GitHub deployment smoke monitoring

Set repository variables after both URLs are live:

```text
CLICKPILOT_API_URL=https://<api>.onrender.com
CLICKPILOT_APP_URL=https://<app>.streamlit.app
```

`.github/workflows/deployment-smoke.yml` then performs scheduled and manually triggered health checks against both public services.

## 7. Public portfolio launch

Only after live QA passes:

- add the permanent app and API URLs to the README;
- replace placeholder deployment wording in `docs/LINKEDIN_LAUNCH.md`;
- add the live app to LinkedIn Featured;
- use the final resume bullets from `docs/RESUME.md`;
- record a 20-30 second demo showing scorer → batch ranking → scenario comparison.

## Data and security policy

Do not upload the original challenge CSV files unless redistribution rights are explicitly confirmed. Do not commit Streamlit secrets, Render credentials, `.env` files, or untrusted serialized model artifacts.
