# ClickPilot AI — Portfolio Case Study

## 1. Business problem

Digital advertising systems serve many impressions, but only a small share convert into clicks. A useful system must do more than output a binary label: it should rank opportunities, support bid/value decisions, and remain trustworthy when user, product, campaign, placement, and temporal behavior change.

The original dataset contains **463,291 labeled impressions and 31,331 clicks (6.76% CTR)** plus **128,858 unlabeled test impressions**.

## 2. Modeling challenge

The project had three core risks:

1. **Class imbalance** — accuracy can be misleading when clicks are rare.
2. **Temporal leakage** — historical CTR or target aggregates can leak future outcomes if computed across the full labeled dataset.
3. **High-cardinality personalization** — user and interaction features can help ranking, but can also overfit or create privacy/fairness issues.

## 3. Validation design

The case study used time-aware evaluation:

- train/core: July 2-5,
- tune/threshold: July 6,
- untouched holdout: July 7,
- supplied test set begins July 8.

This makes the benchmark closer to forward deployment than a random split.

## 4. Model selection

Three principal models were compared:

- Logistic Regression,
- LightGBM,
- CatBoost with personalization and interaction features.

CatBoost was selected with holdout **ROC-AUC 0.579538**, **PR-AUC 0.078022**, and **F1 0.13455**.

The absolute scores are intentionally not oversold. CTR prediction over a short window is noisy. The correct operational response is to monitor, calibrate, preserve exploration, and use probability/value ranking rather than claim perfect click prediction.

## 5. Personalization experiment

Ablation results:

- Base: 0.550399 ROC-AUC.
- + user_id: 0.587187.
- + user_product: 0.592973.
- + all interactions: 0.596135.

The main insight is that user and contextual affinity improve ranking quality. It does not prove that manually changing those fields causes the score difference.

## 6. Imbalance experiment

SMOTE was tested rather than assumed to be beneficial.

- No SMOTE: 80,000 rows, ROC-AUC 0.539359.
- Partial SMOTE: 96,681 rows, ROC-AUC 0.536386.
- Full balance: 148,740 rows, ROC-AUC 0.530996.

Partial oversampling reduced false negatives, but ranking metrics did not improve. Full balance increased data volume by ~1.86× and reduced F1. The production direction therefore favors CatBoost/class weighting/threshold optimization instead of full SMOTE.

## 7. Productization

The notebook was converted into a reusable system:

- `src/clickpilot` owns model logic.
- Streamlit provides a human decision interface.
- FastAPI provides a programmatic contract.
- Synthetic public data proves the end-to-end product without redistributing original rows.
- Batch outputs can be downloaded and, when labels are present, evaluated using deployment metrics.
- Docker and GitHub Actions make the runtime reproducible.

## 8. Decision layer

A click probability becomes more useful when tied to economics:

`expected value per impression = P(click) × value_per_click − cost_per_impression`

This allows a user to compare model ranking with campaign cost assumptions rather than rely on a fixed 0/1 threshold.

## 9. Monitoring and governance

CTR systems can degrade even when code does not change. ClickPilot documents monitoring for:

- ROC-AUC and PR-AUC,
- observed vs predicted CTR,
- Brier score / log loss,
- threshold precision/recall/F1,
- unseen categories and feature drift,
- segment performance and fairness,
- feedback loops caused by over-exploitation.

## 10. Portfolio value

The project demonstrates more than classification modeling. It shows:

- temporal validation,
- leakage reasoning,
- CatBoost/high-cardinality categorical handling,
- ablation testing,
- imbalanced-learning trade-offs,
- probability-to-business-value translation,
- backend API design,
- frontend product design,
- monitoring and responsible AI,
- Docker/CI/testing/documentation.

That makes it suitable for Data Scientist, Applied ML, ML Engineer, Decision Science, Marketing Analytics, and Ad-Tech portfolio positioning.
