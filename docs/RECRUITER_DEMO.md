# ClickPilot AI — 20–30 Second Recruiter Demo

## Goal

Show that ClickPilot AI is not just a notebook: it is a publicly deployed decision system with model evidence, an API backend, batch scoring, scenario analysis, and monitoring.

## Recommended recording sequence

### 0–4 seconds — product + proof

Open the live app at https://clickpilot-ai-mohit.streamlit.app/ and hold on the top section.

Make sure the frame shows:

- ClickPilot AI hero
- 463,291 original impressions
- 6.76% original CTR
- 0.580 holdout ROC-AUC
- 0.078 holdout PR-AUC
- `Runtime backend: FastAPI`
- GitHub / API docs buttons

Suggested voiceover/caption:

> ClickPilot AI turns a CTR modeling case study into a deployed ad-ranking and decision-intelligence product.

### 4–10 seconds — single scoring

Open **Impression scorer** and click **Score impression** with defaults.

Show the probability, propensity band, expected value, and value-aware decision.

Suggested caption:

> Single-impression scoring converts click probability into ranking and business-value signals.

### 10–17 seconds — batch ranking

Open **Batch ranking** with the synthetic sample already uploaded. Scroll directly to the ranked table and KPI cards.

Show:

- Mean predicted CTR
- High-propensity share
- Expected clicks / 100K
- ranked probabilities
- Download ranked predictions

Suggested caption:

> Batch inference audits input quality, ranks opportunities, and exports scored decisions.

### 17–23 seconds — scenario intelligence

Open **Decision simulator** and show an already-computed comparison.

Suggested caption:

> A predictive what-if simulator compares delivery scenarios without presenting the result as causal uplift.

### 23–28 seconds — monitoring + close

Open **Monitoring** and briefly show ROC-AUC, PR-AUC, observed CTR, and mean predicted CTR.

End on the app header or GitHub button.

Suggested caption:

> Monitoring, governance, Dockerized FastAPI, CI, and a synthetic public demo complete the production-style layer.

## Recording rules

- Record at 1080p if possible.
- Keep browser zoom around 90–100%.
- Hide bookmarks/personal tabs if visible.
- Do not spend recording time filling fields; pre-load each state first.
- Keep the mouse movement slow and deliberate.
- Avoid claiming that the synthetic demo metrics are the original model's holdout performance.
- Avoid saying the simulator measures causal lift.
- Keep the finished clip under ~30 seconds for LinkedIn Featured / post media.

## Suggested title overlay

**ClickPilot AI — CTR Prediction → Ranking → Decision Economics → Monitoring**

## Suggested end card

**Live app:** clickpilot-ai-mohit.streamlit.app  
**GitHub:** github.com/mohit231007/ClickPilot_AI
