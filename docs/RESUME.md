# ClickPilot AI — Resume Copy

## Project links

- Live application: https://clickpilot-ai-mohit.streamlit.app/
- FastAPI / Swagger: https://clickpilot-api.onrender.com/docs
- GitHub: https://github.com/mohit231007/ClickPilot_AI

## Recommended project headline

**ClickPilot AI | End-to-End CTR Prediction & Ad Decision Intelligence Platform**  
Python · CatBoost · FastAPI · Streamlit · scikit-learn · Docker · GitHub Actions · MLOps

## Data Scientist / ML Engineer version

- Built **ClickPilot AI**, an end-to-end CTR intelligence platform on a **463K-impression / 31K-click** ad dataset; designed leakage-aware temporal validation and selected **CatBoost + personalization**, achieving **0.580 ROC-AUC / 0.078 PR-AUC** on an untouched temporal holdout and improving ROC-AUC by ~**10.2%** versus Logistic Regression.
- Publicly deployed a **Streamlit frontend + Dockerized FastAPI backend** with single/batch probability scoring, ad ranking, value-aware decision rules, scenario comparison, model versioning, synthetic public-demo isolation, and labeled-batch monitoring for ROC-AUC, PR-AUC, Brier score, log loss, precision, recall, and F1.
- Ran personalization and imbalance experiments: interaction features increased CatBoost ROC-AUC from ~**0.550 to 0.596**, while full SMOTE expanded training rows by ~**1.86×** without improving AUC; packaged the project with **pytest, Ruff, Docker, GitHub Actions, model card, security, and responsible-use guardrails**.

## Short two-bullet version

- Developed an end-to-end **CTR prediction and ad-ranking platform** using CatBoost personalization on **463K impressions**, achieving **0.580 ROC-AUC / 0.078 PR-AUC** with leakage-safe temporal validation and ~**10.2% ROC-AUC lift** over Logistic Regression.
- Publicly deployed a **Streamlit + FastAPI** system for single/batch scoring, value-aware bidding, scenario analysis, monitoring, Docker, tests, CI/CD, model governance, and synthetic public demo data.

## Marketing Analytics / Decision Science version

- Built and deployed a CTR decision-support product that ranks ad opportunities by click probability and converts predictions into expected value using **value-per-click and CPM**, supporting targeting, campaign-placement comparison, and batch prioritization.
- Identified product and personalization patterns from **463K impressions**; product J led CTR at **9.27%**, personalization increased model ranking quality to ~**0.596 ROC-AUC**, and SMOTE was rejected because it increased training cost without AUC improvement.

## Interview opener

“ClickPilot AI started as an ad-click modeling case study, but I turned it into a publicly deployed decision system. The modeling challenge was highly imbalanced classification with temporal leakage risk. I used a July-based temporal holdout, compared Logistic Regression, LightGBM and CatBoost, and selected personalized CatBoost at 0.580 ROC-AUC. Then I added the system around the model: a reusable feature package, Dockerized FastAPI backend on Render, Streamlit frontend, batch ranking, value-aware bidding, monitoring, CI, a model card, and a synthetic public demo so the original data did not need to be redistributed.”

## Claims to avoid

- Do not say the model “increased CTR by 10.2%.” The 10.2% figure is **relative ROC-AUC improvement**, not business uplift.
- Do not claim the ~0.596 ablation score is the final untouched holdout score; it comes from the separate personalization ablation setup.
- Do not call the public synthetic demo model the original trained model.
- Do not describe demographic segments as causal or as automatic exclusion rules.
- Do not say all live workflows passed acceptance QA until the public single-score, batch-ranking, simulator, and monitoring checks have been executed successfully.
