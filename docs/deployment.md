# Deployment Guide

## Local

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

## Docker

```bash
docker compose up --build
```

Frontend: `http://localhost:8501`  
API docs: `http://localhost:8000/docs`

## Public portfolio deployment

Recommended setup mirrors the proven InfluenceLift pattern:

- Streamlit Community Cloud for `app/Home.py`.
- A container host for FastAPI. Configure the Streamlit secret/environment variable `CLICKPILOT_API_URL` to that API base URL so the deployed frontend uses the backend rather than the local fallback.
- GitHub Actions for lint/test/compile checks.
- Repository variables `CLICKPILOT_APP_URL` and `CLICKPILOT_API_URL` to activate the scheduled deployment smoke workflow.

Do not upload the original challenge CSV files to the public repository unless redistribution rights are confirmed.
