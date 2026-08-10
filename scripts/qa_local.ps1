param(
    [switch]$LaunchApp,
    [switch]$LaunchApi
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
ruff check .
pytest -q
python -m compileall src api app scripts
python scripts/generate_demo_data.py --rows 1500 --output data/sample/qa_impressions.csv
python scripts/train.py --input data/sample/qa_impressions.csv --output artifacts/qa_bundle.joblib
python scripts/predict.py --input data/sample/qa_impressions.csv --model artifacts/qa_bundle.joblib --output artifacts/qa_predictions.csv

if ($LaunchApi) {
    Start-Process powershell -ArgumentList '-NoExit','-Command','& .\.venv\Scripts\Activate.ps1; uvicorn api.main:app --reload --port 8000'
}
if ($LaunchApp) {
    Start-Process powershell -ArgumentList '-NoExit','-Command','& .\.venv\Scripts\Activate.ps1; streamlit run app/Home.py'
}

Write-Host "ClickPilot AI local QA completed." -ForegroundColor Green
