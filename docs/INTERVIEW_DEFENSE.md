# ClickPilot AI — Interview Defense Guide

Use this document to explain the project clearly in data-science, ML-engineering, analytics, and product interviews.

## 30-second opener

ClickPilot AI started as an ad-click prediction case study and was rebuilt as a public decision system. The modeling problem is highly imbalanced binary classification with meaningful temporal leakage risk, so I used a date-based validation design rather than random splitting. The selected CatBoost + personalization model reached 0.580 ROC-AUC and 0.078 PR-AUC on an untouched temporal holdout. I then added the engineering layer: reusable features, Streamlit, Dockerized FastAPI, batch scoring, ranking, decision economics, scenario comparison, monitoring, CI, governance, and a deterministic synthetic public demo so the original challenge rows are not redistributed.

## Why ROC-AUC and PR-AUC?

CTR is imbalanced. Accuracy can look strong while being nearly useless because the negative class dominates. ROC-AUC measures ranking quality across thresholds, while PR-AUC puts more emphasis on the positive class and is therefore especially informative when clicks are rare.

The selected original model achieved:

- ROC-AUC: **0.579538**
- PR-AUC: **0.078022**

These are modest absolute scores. The project does not hide that limitation; instead it treats the model as a ranking signal requiring monitoring, threshold management, and experimentation.

## Why temporal validation instead of a random split?

Ad systems operate forward in time. Random splitting can leak behavioral and campaign information from the future into training. The case-study validation design was:

- train: July 2–5
- tune / threshold: July 6
- untouched holdout: July 7
- unlabeled test begins July 8

This better approximates how the model would be used after deployment.

## Why CatBoost?

The dataset is dominated by categorical identifiers and interactions such as user, product, campaign, placement, and user-product combinations. CatBoost is a strong fit for mixed/categorical tabular data and reduces the need for large one-hot representations.

The comparison was:

| Model | ROC-AUC | PR-AUC |
|---|---:|---:|
| Logistic Regression | 0.525902 | 0.065134 |
| LightGBM | 0.543092 | 0.068699 |
| CatBoost + personalization | 0.579538 | 0.078022 |

Relative to Logistic Regression, the selected model improved ROC-AUC by about 10.2% and PR-AUC by about 19.8%. This is model-ranking improvement, not proven business uplift.

## What did personalization contribute?

The ablation showed:

| Feature set | ROC-AUC | PR-AUC |
|---|---:|---:|
| Base | 0.550399 | 0.072366 |
| + user_id | 0.587187 | 0.080151 |
| + user_product | 0.592973 | 0.080994 |
| + all interactions | 0.596135 | 0.081681 |

The key interview point is that user-level and interaction information improved ranking quality, but these fields can also create privacy, fairness, overfitting, and cold-start concerns. Production use therefore requires policy review, monitoring, and fallbacks for unseen users/categories.

## Why reject SMOTE?

SMOTE was tested rather than assumed to be helpful.

- no SMOTE: ~80K training rows, ROC-AUC ≈ 0.5394, PR-AUC ≈ 0.0693
- partial SMOTE: ~96.7K rows, ROC-AUC ≈ 0.5364, PR-AUC ≈ 0.0690
- full SMOTE: ~148.7K rows, ROC-AUC ≈ 0.5310, PR-AUC ≈ 0.0684

Partial SMOTE reduced false negatives but did not improve ranking metrics. Full balance increased the training sample by ~1.86× without improving AUC. The decision was therefore to avoid the extra cost and prefer class weighting / threshold management / CatBoost-native strategies.

## Why is the public demo model synthetic?

The original challenge data is not redistributed because redistribution rights are not assumed. The public app uses a deterministic, schema-compatible synthetic dataset and demo model. Original benchmark evidence is kept separately in the notebook/report and surfaced as immutable case-study metrics.

This prevents an important portfolio mistake: silently presenting synthetic public-demo metrics as though they were the original holdout results.

## What does the API architecture look like?

```text
User / recruiter
      │
      ▼
Streamlit Community Cloud
      │ HTTPS / JSON
      ▼
Dockerized FastAPI on Render
      │
      ▼
clickpilot shared Python package
      │
      ├── feature engineering
      ├── audit / schema checks
      ├── model inference
      ├── ranking / economics
      ├── scenario comparison
      └── evaluation / monitoring
```

The frontend can also fall back to the shared local package when `CLICKPILOT_API_URL` is absent, which makes local development and offline demos easier while keeping cloud inference API-backed.

## What does “value-aware” mean?

The model produces a click probability. ClickPilot then combines that probability with business assumptions such as value per click and CPM to calculate expected value. This separates prediction from decision policy.

That is important because the highest predicted CTR is not automatically the best business action if inventory cost, value per click, constraints, or exploration requirements differ.

## Is the scenario simulator causal?

No. It scores two feature configurations through the same predictive model and compares predicted outcomes. The UI explicitly says the result is a predictive what-if comparison, not a causal guarantee.

A causal answer would require experiment design or causal-inference assumptions that this model does not provide.

## How would you productionize further?

Strong next steps are:

- calibrated probabilities and reliability monitoring
- historical CTR features built with past-only / out-of-fold logic
- drift monitoring (PSI / Jensen-Shannon or equivalent)
- segment-level calibration and fairness checks
- exploration traffic rather than fully greedy serving
- champion/challenger evaluation
- experiment integration to estimate causal lift
- latency/error-rate/throughput SLOs
- feature-store integration
- model registry and artifact promotion
- SHAP or local explanations where operationally appropriate

## What would you monitor?

Model metrics:

- ROC-AUC / PR-AUC on delayed labels
- calibration / Brier score / log loss
- precision, recall and F1 at the operating threshold
- observed CTR vs predicted CTR

Data metrics:

- missingness
- unknown-category rate
- feature drift
- campaign / product / placement distribution shifts

Business metrics:

- click volume
- value per thousand impressions
- cost and revenue proxies
- segment outcomes
- exploration coverage

System metrics:

- API availability
- latency
- error rate
- cold-start behavior
- scoring throughput

## What are the biggest limitations?

1. Original holdout performance is useful but modest.
2. The public model is synthetic by design and is not the original challenge-trained production model.
3. Some high-signal identifiers can create overfitting and cold-start issues.
4. Predictive scenario differences are not causal uplift estimates.
5. A portfolio deployment does not include the traffic volume, feature store, experimentation platform, and observability stack of a real ad-serving system.

Calling out these limitations is part of the project's trust and model-governance story.

## Resume-safe claims

Safe:

- built an end-to-end CTR prediction and ranking platform
- used leakage-aware temporal validation
- selected CatBoost + personalization at 0.580 ROC-AUC / 0.078 PR-AUC on the original holdout
- deployed Streamlit + Dockerized FastAPI
- implemented single/batch inference, ranking, economics, simulation and monitoring
- personalization ablation reached ~0.596 ROC-AUC in its own experimental setup
- rejected full SMOTE after ~1.86× row expansion without AUC improvement

Avoid:

- “increased CTR by 10.2%”
- “0.596 was the final holdout ROC-AUC”
- “the scenario simulator measures causal uplift”
- “the public demo uses the confidential/original challenge model and data”
- hard demographic targeting claims
