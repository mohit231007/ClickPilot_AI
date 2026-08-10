"""Validated benchmark facts from the original CTR case study.

These constants intentionally stay separate from the synthetic public-demo model.
"""

from __future__ import annotations

ORIGINAL_TRAIN_IMPRESSIONS = 463_291
ORIGINAL_TRAIN_CLICKS = 31_331
ORIGINAL_BASELINE_CTR = 0.0676
ORIGINAL_TEST_IMPRESSIONS = 128_858

VALIDATION_DESIGN = (
    "Train on July 2-5, tune/threshold on July 6, and evaluate once on the "
    "untouched July 7 temporal holdout."
)

MODEL_COMPARISON = [
    {
        "model": "Logistic Regression",
        "roc_auc": 0.525902,
        "pr_auc": 0.065134,
        "precision": 0.06605,
        "recall": 0.64463,
        "f1": 0.11982,
    },
    {
        "model": "LightGBM",
        "roc_auc": 0.543092,
        "pr_auc": 0.068699,
        "precision": 0.06842,
        "recall": 0.60759,
        "f1": 0.12299,
    },
    {
        "model": "CatBoost + personalization",
        "roc_auc": 0.579538,
        "pr_auc": 0.078022,
        "precision": 0.07810,
        "recall": 0.48534,
        "f1": 0.13455,
    },
]

PERSONALIZATION_ABLATION = [
    {"feature_set": "Base", "roc_auc": 0.550399, "pr_auc": 0.072366},
    {"feature_set": "+ user_id", "roc_auc": 0.587187, "pr_auc": 0.080151},
    {"feature_set": "+ user_product", "roc_auc": 0.592973, "pr_auc": 0.080994},
    {"feature_set": "+ all interactions", "roc_auc": 0.596135, "pr_auc": 0.081681},
]

SMOTE_EXPERIMENT = [
    {
        "variant": "No SMOTE",
        "rows": 80_000,
        "positive_rate": 0.070375,
        "roc_auc": 0.539359,
        "pr_auc": 0.069267,
        "recall": 0.41559,
        "f1": 0.12019,
        "false_negatives": 2572,
        "offline_seconds": 0.41,
    },
    {
        "variant": "SMOTE 0.30",
        "rows": 96_681,
        "positive_rate": 0.230769,
        "roc_auc": 0.536386,
        "pr_auc": 0.069029,
        "recall": 0.53783,
        "f1": 0.12066,
        "false_negatives": 2034,
        "offline_seconds": 6.31,
    },
    {
        "variant": "SMOTE 1.00",
        "rows": 148_740,
        "positive_rate": 0.5,
        "roc_auc": 0.530996,
        "pr_auc": 0.068437,
        "recall": 0.52761,
        "f1": 0.11768,
        "false_negatives": 2079,
        "offline_seconds": 13.29,
    },
]

PRODUCT_PERFORMANCE = [
    {"product": "J", "impressions": 9698, "clicks": 899, "ctr": 0.0927},
    {"product": "D", "impressions": 41064, "clicks": 2949, "ctr": 0.0718},
    {"product": "H", "impressions": 109574, "clicks": 7654, "ctr": 0.0699},
    {"product": "C", "impressions": 163501, "clicks": 11306, "ctr": 0.0691},
    {"product": "E", "impressions": 21452, "clicks": 1474, "ctr": 0.0687},
    {"product": "I", "impressions": 63711, "clicks": 4079, "ctr": 0.0640},
    {"product": "A", "impressions": 15391, "clicks": 953, "ctr": 0.0619},
    {"product": "B", "impressions": 22479, "clicks": 1238, "ctr": 0.0551},
    {"product": "F", "impressions": 7007, "clicks": 344, "ctr": 0.0491},
    {"product": "G", "impressions": 9414, "clicks": 435, "ctr": 0.0462},
]

FINAL_BUSINESS_ANSWERS = [
    "Weekend CTR is 7.33% vs 6.65% weekday (+10.2% relative), but only one weekend day is labeled; validate across more weeks before changing bids.",
    "Product J is best by CTR (9.27%); D/H/C follow. G (4.62%) and F (4.91%) are weakest. C leads absolute clicks due to volume.",
    "Personalization helps ranking quality: ROC-AUC rises from ~0.550 base to ~0.593 after user-product personalization and ~0.596 with all interactions.",
    "Key drivers are user identity/history, webpage placement, campaign-webpage interaction, campaign, day-of-week, and product category.",
    "SMOTE reduces false negatives but does not improve AUC here and materially increases offline training size, so it is not selected for production.",
    "Use smoothed historical product CTR as a demand feature, then convert expected impressions -> clicks -> orders -> units and incorporate lead time and safety stock.",
    "Highest robust profiles include Male / age level 5 / city index 4 (~8.66%) and Female / age level 5 / city index 4 (~8.47%); use them as controlled bid modifiers, not hard exclusions.",
]

SELECTED_MODEL = "CatBoost + personalization/interactions"
