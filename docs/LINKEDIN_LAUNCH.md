# ClickPilot AI — LinkedIn Launch Package

## Public proof links

- Live application: https://clickpilot-ai-mohit.streamlit.app/
- FastAPI service: https://clickpilot-api.onrender.com
- API documentation: https://clickpilot-api.onrender.com/docs
- GitHub: https://github.com/mohit231007/ClickPilot_AI

## Primary launch post

Most CTR projects stop at a notebook and an AUC score. I wanted to turn one into a product a marketing or ad-tech team could actually inspect and use.

I built **ClickPilot AI** — an end-to-end click-through-rate intelligence platform for ad ranking and value-aware campaign decisions.

The original case study contains **463,291 ad impressions and 31,331 clicks (6.76% CTR)**. I used a temporal validation design — train on July 2-5, tune/threshold on July 6, and keep July 7 untouched as the holdout.

The selected **CatBoost + personalization** model achieved **0.580 ROC-AUC and 0.078 PR-AUC** on that holdout, outperforming the Logistic Regression baseline by about **10.2% on ROC-AUC and 19.8% on PR-AUC**.

The personalization ablation was also useful: the base CatBoost model was around **0.550 ROC-AUC**, while user/product/interaction features pushed the experimental score to about **0.596**.

But I did not want to publish another notebook-only project, so I productionized the case study with:

- a publicly deployed Streamlit frontend for single-impression scoring and batch ranking,
- a separately deployed Dockerized FastAPI backend,
- value-aware decision logic using click probability, value-per-click, and CPM,
- baseline-vs-proposed predictive scenario simulation,
- labeled-batch monitoring for ROC-AUC, PR-AUC, Brier score, log loss, precision, recall, and F1,
- model versioning, data-quality checks, Docker, automated tests, GitHub Actions, and responsible-use documentation,
- a deterministic synthetic public demo model so the original challenge rows are not redistributed.

I also tested SMOTE. It reduced false negatives at one operating point, but did **not** improve AUC and full balancing expanded the benchmark training sample by about **1.86×**. I rejected it rather than adding cost without demonstrated ranking lift.

Before calling the product launch-ready, I exercised the public system end-to-end: single scoring, 50-row batch ranking + CSV export, scenario comparison, and a 1,000-row synthetic monitoring stream all completed successfully through the deployed app.

The biggest lesson from this project: **production-quality data science is not just model selection. It is validation design, leakage control, decision economics, APIs, monitoring, deployment, and being explicit about what the model cannot claim.**

Live demo: **https://clickpilot-ai-mohit.streamlit.app/**  
API / Swagger: **https://clickpilot-api.onrender.com/docs**  
GitHub: **https://github.com/mohit231007/ClickPilot_AI**

I would value feedback from data scientists, ML engineers, marketing analytics, and ad-tech professionals — especially on what you would add next: calibration, SHAP explanations, feature-store aggregates, or online experimentation?

Suggested hashtags:  
`#DataScience #MachineLearning #AdTech #MarketingAnalytics #MLOps #Python #FastAPI #Streamlit`

---

## Technical first comment

Architecture details for anyone interested:

- CatBoost probability model with user/product/campaign-placement interactions
- temporal holdout instead of random validation for the original benchmark
- synthetic demo model kept separate from original case-study metrics
- public Streamlit frontend connected to a separately deployed Render FastAPI backend
- one shared Python package used by Streamlit and FastAPI
- `POST /predict`, `/predict-batch`, `/compare`, and `/evaluate`
- expected-value decision rule = `P(click) × value_per_click - cost_per_impression`
- labeled-batch monitoring includes ranking + probability quality metrics
- Docker + pytest + Ruff + GitHub Actions
- public acceptance checks completed for all four product workflows

The model card also documents the short validation window, demographic-feature risks, non-causal interpretation, and feedback-loop concerns.

Live app: https://clickpilot-ai-mohit.streamlit.app/  
Interactive API docs: https://clickpilot-api.onrender.com/docs

---

## LinkedIn Featured section copy

**ClickPilot AI — End-to-End CTR Intelligence Platform**  
Publicly deployed and acceptance-tested ad-click prediction project using CatBoost personalization, temporal validation, batch scoring/export, value-aware decision logic, FastAPI, Streamlit, Docker, CI, monitoring, and responsible-use guardrails. Original case-study holdout: ROC-AUC 0.580 / PR-AUC 0.078 on 463K impressions.

Live: https://clickpilot-ai-mohit.streamlit.app/

---

## Acceptance proof to mention only if useful

- single score: 5.00% click probability with the default public demo inputs
- batch ranking: 50 rows, 5.96% mean predicted CTR, 4.0% high-propensity share, ranked CSV export validated
- scenario simulation: 5.51% baseline vs 4.80% proposed, -708 expected clicks over 100K in the default comparison
- monitoring: 1,000-row synthetic stream, 6.40% observed CTR vs 5.82% mean predicted CTR

These are **public-demo acceptance results**, not replacements for the original case-study holdout metrics.

---

## 20–30 second demo recording script

Use [RECRUITER_DEMO.md](RECRUITER_DEMO.md) for the optimized recording sequence.

---

## LinkedIn carousel narrative

1. **From notebook to ad-tech product** — the problem and 463K-impression dataset.
2. **Leakage-safe temporal validation** — July 2-5 / July 6 / July 7.
3. **Model comparison** — Logistic vs LightGBM vs CatBoost.
4. **Why personalization mattered** — base 0.550 → interactions ~0.596 ROC-AUC.
5. **Why SMOTE lost** — fewer false negatives, no AUC improvement, higher training cost.
6. **Product architecture** — deployed Streamlit + Render FastAPI + shared Python package.
7. **Decision intelligence** — probability × value-per-click − media cost.
8. **Monitoring & responsibility** — calibration, drift, segment performance, feedback loops.
9. **Live proof** — deployed app + GitHub + public acceptance record + PDF case study.

---

## Launch sequence

- Day 0: primary launch post + screenshot or 20–30 second demo.
- Day 0: technical first comment.
- Day 1: add to Featured and Projects.
- Day 2: architecture carousel.
- Day 4: short post — why CatBoost personalization won.
- Day 7: short post — why SMOTE was rejected.
- Day 10: batch-ranking/data-quality demo.
- Day 14: monitoring/calibration lesson.
- Day 21: “what I would build next” feature-store/experimentation roadmap.

## Release note

The four public functional workflows have passed acceptance QA: single scoring, batch ranking/export, decision simulation, and monitoring. The primary LinkedIn launch claim may now truthfully describe ClickPilot AI as publicly deployed and functionally acceptance-tested. Keep synthetic demo metrics clearly separate from original case-study holdout metrics.
