# Streamlit Community Cloud deployment

ClickPilot AI's public frontend is designed to run from the repository root with `app/Home.py` as the entrypoint.

## Deployment values

- Repository: `mohit231007/ClickPilot_AI`
- Branch: `main`
- Entrypoint: `app/Home.py`
- Python: 3.12

## Connect the deployed FastAPI backend

In Streamlit Community Cloud, open **Advanced settings** (or later **App settings → Secrets**) and add this root-level secret:

```toml
CLICKPILOT_API_URL = "https://<your-clickpilot-api>.onrender.com"
```

Root-level Streamlit secrets are exposed as environment variables, so the app automatically detects `CLICKPILOT_API_URL` and switches from local fallback mode to the deployed FastAPI service.

## Acceptance check

After deployment, verify:

1. the home page loads without an exception;
2. the UI identifies the backend as connected;
3. a single impression can be scored;
4. batch CSV scoring works and downloads a result;
5. scenario comparison returns baseline/proposed probabilities;
6. monitoring accepts labeled synthetic data;
7. original case-study metrics remain clearly separated from synthetic demo metrics.

Do not commit `.streamlit/secrets.toml`.
