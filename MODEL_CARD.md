# ClickPilot AI — Model Card

## Model overview

ClickPilot AI is a portfolio-grade ad click-through-rate (CTR) decision-support system. The **validated case-study model** is CatBoost with personalization and interaction features. The **public interactive demo model** is a separately trained deterministic synthetic CatBoost model used only to prove the product and deployment path without redistributing the original challenge rows.

## Validated case-study evidence

- Training data: **463,291 impressions**, **31,331 clicks**, **6.76% CTR**.
- Test data: **128,858 unlabeled impressions**.
- Validation: train July 2-5, tune/threshold July 6, untouched temporal holdout July 7.
- Selected model: **CatBoost + personalization/interactions**.
- Holdout ROC-AUC: **0.579538**.
- Holdout PR-AUC: **0.078022**.
- Holdout F1: **0.13455**.
- Personalization ablation reaches approximately **0.596 ROC-AUC** with all interaction features.

The absolute ranking metrics are modest. This is presented as an important limitation rather than hidden: short-window CTR prediction is noisy and needs continuous monitoring.

## Intended use

- Rank ad opportunities by click probability.
- Compare campaign-placement-product scenarios.
- Combine click probability with value-per-click and media cost to support bidding decisions.
- Batch-score impression opportunities and prioritize review.
- Demonstrate labeled-batch monitoring with ROC-AUC, PR-AUC, calibration-related loss, CTR, precision, recall, and F1.

## Not intended for

- Causal claims such as “changing webpage X to Y will cause the modeled CTR increase.”
- Hard exclusion of users based on demographic attributes.
- Autonomous high-stakes decisions without privacy, fairness, policy, and commercial review.
- Inventory forecasts based on CTR alone.

## Data and feature policy

The public repository must not contain the original challenge rows unless redistribution rights are explicitly confirmed. Synthetic demo data is generated from scratch with the same schema. Missing categorical values are represented as explicit `MISSING` levels. Target aggregates such as historical user CTR must be computed from past-only or out-of-fold data if added later.

## Model choice

The original analysis compared Logistic Regression, LightGBM, and CatBoost. CatBoost + personalization produced the best temporal holdout ranking metrics. A SMOTE experiment reduced false negatives at some operating points but did not improve ROC-AUC or PR-AUC and increased offline training size, so full SMOTE was rejected.

## Monitoring

Monitor at minimum:

- ROC-AUC and PR-AUC when labels arrive.
- Observed CTR vs mean predicted CTR.
- Brier score / log loss and calibration drift.
- Precision, recall, and F1 at the production operating threshold.
- Segment performance and fairness.
- Unknown-category rate and feature distribution changes.
- Feedback-loop risk caused by over-exploiting currently high-scoring ads.

## Limitations

- The original validation window is short.
- Only one weekend day is labeled in the source analysis.
- The test file is unlabeled, so final model quality is judged on the temporal holdout rather than test outcomes.
- Demographic variables can create fairness and privacy concerns.
- Synthetic live-demo metrics are not substitutes for the original case-study benchmark.

## Versioning

- `demo-1.0.0`: deterministic synthetic CatBoost used by the public app and API.
- Original case-study benchmark metrics remain immutable evidence and are displayed separately.
