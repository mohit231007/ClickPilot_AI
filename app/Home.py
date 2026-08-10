"""Streamlit decision interface for ClickPilot AI."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from clickpilot.audit import audit_impression_data
from clickpilot.benchmark import (
    FINAL_BUSINESS_ANSWERS,
    MODEL_COMPARISON,
    ORIGINAL_BASELINE_CTR,
    ORIGINAL_TEST_IMPRESSIONS,
    ORIGINAL_TRAIN_CLICKS,
    ORIGINAL_TRAIN_IMPRESSIONS,
    PERSONALIZATION_ABLATION,
    PRODUCT_PERFORMANCE,
    SELECTED_MODEL,
    SMOTE_EXPERIMENT,
    VALIDATION_DESIGN,
)
from clickpilot.demo_data import (
    AGE_LEVELS,
    CAMPAIGNS,
    CITY_INDEX,
    GENDERS,
    PRODUCT_CAT_1,
    PRODUCT_CAT_2,
    PRODUCTS,
    USER_DEPTHS,
    USER_GROUPS,
    VAR1,
    WEBPAGES,
    generate_demo_dataset,
)
from clickpilot.inference import load_or_create_bundle
from clickpilot.service import backend_mode, compare_records, evaluate_records, score_records

st.set_page_config(page_title="ClickPilot AI", page_icon="🎯", layout="wide")

st.markdown(
    """
<style>
.block-container {padding-top: 1.3rem; padding-bottom: 2rem; max-width: 1400px;}
.hero {padding: 1.5rem 1.7rem; border-radius: 18px; background: linear-gradient(120deg,#0d1b2a,#16324f); color:#fff; margin-bottom:1rem;}
.hero h1 {margin:0; font-size:2.55rem;}
.hero p {margin:0.4rem 0 0 0; color:#dbe9f4; font-size:1.05rem;}
.kicker {font-size:.8rem; letter-spacing:.11rem; text-transform:uppercase; color:#5eead4; font-weight:700;}
.small-note {font-size:.88rem; color:#64748b;}
[data-testid="stMetric"] {border:1px solid rgba(148,163,184,.25); border-radius:14px; padding:12px;}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def bundle():
    return load_or_create_bundle()


@st.cache_data
def demo_batch(rows: int = 80, seed: int = 7, labels: bool = True):
    return generate_demo_dataset(rows=rows, seed=seed, include_target=labels)


model = bundle()

st.markdown(
    """
<div class="hero">
  <div class="kicker">Ad-tech · classification · decision intelligence</div>
  <h1>ClickPilot AI</h1>
  <p>Score ad impressions, rank click propensity, compare targeting scenarios, and translate CTR probabilities into value-aware decisions.</p>
</div>
""",
    unsafe_allow_html=True,
)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Original impressions", f"{ORIGINAL_TRAIN_IMPRESSIONS:,}")
col2.metric("Original CTR", f"{ORIGINAL_BASELINE_CTR:.2%}")
col3.metric("Holdout ROC-AUC", "0.580")
col4.metric("Holdout PR-AUC", "0.078")
col5.metric("Runtime backend", backend_mode())

st.info(
    "Original benchmark metrics come from the supplied CTR case study. The public interactive scorer uses a deterministic synthetic CatBoost demo model so the challenge data is not redistributed."
)

scorer_tab, batch_tab, simulator_tab, evidence_tab, monitoring_tab = st.tabs(
    ["🎯 Impression scorer", "📦 Batch ranking", "🧪 Decision simulator", "📚 Model & evidence", "📡 Monitoring"]
)


def build_record(prefix: str, *, default_product: str = "J", default_campaign: str = "C101", default_webpage: str = "W1"):
    left, middle, right = st.columns(3)
    with left:
        user_id = st.text_input(f"{prefix} user ID", value="1500", key=f"{prefix}_user")
        product = st.selectbox(f"{prefix} product", PRODUCTS, index=PRODUCTS.index(default_product), key=f"{prefix}_product")
        campaign = st.selectbox(f"{prefix} campaign", CAMPAIGNS, index=CAMPAIGNS.index(default_campaign), key=f"{prefix}_campaign")
        webpage = st.selectbox(f"{prefix} webpage", WEBPAGES, index=WEBPAGES.index(default_webpage), key=f"{prefix}_webpage")
    with middle:
        pc1 = st.selectbox(f"{prefix} product category 1", PRODUCT_CAT_1, key=f"{prefix}_pc1")
        pc2 = st.selectbox(f"{prefix} product category 2", ["MISSING"] + PRODUCT_CAT_2, key=f"{prefix}_pc2")
        gender = st.selectbox(f"{prefix} gender", ["MISSING"] + GENDERS, index=1, key=f"{prefix}_gender")
        age = st.selectbox(f"{prefix} age level", ["MISSING"] + AGE_LEVELS, index=5, key=f"{prefix}_age")
    with right:
        group = st.selectbox(f"{prefix} user group", ["MISSING"] + USER_GROUPS, index=1, key=f"{prefix}_group")
        depth = st.selectbox(f"{prefix} user depth", ["MISSING"] + USER_DEPTHS, index=2, key=f"{prefix}_depth")
        city = st.selectbox(f"{prefix} city development index", ["MISSING"] + CITY_INDEX, index=4, key=f"{prefix}_city")
        var1 = st.selectbox(f"{prefix} var_1", VAR1, key=f"{prefix}_var1")

    dt_col, minute_col = st.columns(2)
    with dt_col:
        event_date = st.date_input(f"{prefix} impression date", value=datetime(2026, 7, 6).date(), key=f"{prefix}_date")
    with minute_col:
        event_time = st.time_input(f"{prefix} impression time", value=datetime(2026, 7, 6, 14, 30).time(), key=f"{prefix}_time")

    def optional(value: str):
        return None if value == "MISSING" else value

    return {
        "DateTime": pd.Timestamp.combine(event_date, event_time),
        "user_id": user_id,
        "product": product,
        "campaign_id": campaign,
        "webpage_id": webpage,
        "product_category_1": pc1,
        "product_category_2": optional(pc2),
        "user_group_id": optional(group),
        "gender": optional(gender),
        "age_level": optional(age),
        "user_depth": optional(depth),
        "city_development_index": optional(city),
        "var_1": var1,
    }


with scorer_tab:
    st.markdown("### Score one ad opportunity")
    st.caption("The probability is produced by the synthetic public-demo model; use the original benchmark only for validated case-study claims.")
    record = build_record("Scorer")
    econ1, econ2 = st.columns(2)
    with econ1:
        value_per_click = st.number_input("Business value per click", min_value=0.0, value=1.50, step=0.10)
    with econ2:
        cpm_cost = st.number_input("Media cost per 1,000 impressions (CPM)", min_value=0.0, value=25.0, step=1.0)

    if st.button("Score impression", type="primary", use_container_width=True):
        result = score_records(
            model,
            pd.DataFrame([record]),
            value_per_click=value_per_click,
            cpm_cost=cpm_cost,
        ).iloc[0]
        a, b, c, d = st.columns(4)
        a.metric("Click probability", f"{result['click_probability']:.2%}")
        b.metric("Propensity band", result["propensity_band"])
        c.metric("Lift vs demo baseline", f"{result['lift_vs_demo_baseline']:.2f}×")
        d.metric("Expected value / 1K", f"{result['expected_value_per_1000_impressions']:.2f}")
        if result["serve_if_value_positive"]:
            st.success("Value-aware decision: positive expected value under the entered click value and CPM assumptions.")
        else:
            st.warning("Value-aware decision: negative expected value under the entered click value and CPM assumptions.")
        if result["warnings"]:
            st.warning("Model familiarity warning: " + result["warnings"])
        st.caption("This is a predictive ranking/value calculation, not a causal claim that changing a field will create the modeled uplift.")

with batch_tab:
    st.markdown("### Rank a batch of ad opportunities")
    sample = demo_batch(rows=50, seed=11, labels=True)
    st.download_button(
        "Download synthetic sample CSV",
        sample.to_csv(index=False).encode("utf-8"),
        file_name="clickpilot_synthetic_impressions.csv",
        mime="text/csv",
    )
    uploaded = st.file_uploader("Upload impression CSV", type=["csv"])
    if uploaded is None:
        st.caption("Use the downloadable synthetic sample to test the full batch workflow.")
    else:
        frame = pd.read_csv(uploaded)
        report = audit_impression_data(frame)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Rows", f"{len(frame):,}")
        m2.metric("Audit status", report.status.replace("_", " ").title())
        m3.metric("Invalid datetimes", report.invalid_datetime_count)
        m4.metric("Duplicate sessions", report.duplicate_session_count)
        with st.expander("Data-quality audit"):
            st.json(report.to_dict())

        if report.missing_required_columns or report.invalid_datetime_count:
            st.error("Fix the schema/date errors before scoring the batch.")
        else:
            scored = score_records(model, frame, value_per_click=1.5, cpm_cost=25.0)
            if "session_id" in frame.columns and "session_id" not in scored.columns:
                scored.insert(0, "session_id", frame["session_id"])
            scored = scored.sort_values("click_probability", ascending=False)
            b1, b2, b3 = st.columns(3)
            b1.metric("Mean predicted CTR", f"{scored['click_probability'].mean():.2%}")
            b2.metric("High-propensity share", f"{(scored['propensity_band'] == 'High').mean():.1%}")
            b3.metric("Expected clicks / 100K", f"{scored['click_probability'].mean() * 100_000:,.0f}")
            st.dataframe(scored.head(100), use_container_width=True)
            st.download_button(
                "Download ranked predictions",
                scored.to_csv(index=False).encode("utf-8"),
                file_name="clickpilot_ranked_predictions.csv",
                mime="text/csv",
                use_container_width=True,
            )
            if "is_click" in frame.columns:
                st.markdown("#### Labeled-batch evaluation")
                st.json(evaluate_records(model, frame))

with simulator_tab:
    st.markdown("### Compare two ad-delivery scenarios")
    st.caption("The simulator runs both scenarios through the same model and reports the change in predicted probability. It does not estimate causal treatment effects.")
    st.markdown("#### Baseline")
    baseline = build_record("Baseline", default_product="C", default_campaign="C101", default_webpage="W1")
    st.markdown("#### Proposed")
    proposed = build_record("Proposed", default_product="J", default_campaign="C105", default_webpage="W3")
    x, y, z = st.columns(3)
    with x:
        sim_value = st.number_input("Scenario value per click", min_value=0.0, value=1.50, step=0.10)
    with y:
        sim_cpm = st.number_input("Scenario CPM", min_value=0.0, value=25.0, step=1.0)
    with z:
        sim_volume = st.number_input("Comparison volume", min_value=1_000, max_value=10_000_000, value=100_000, step=10_000)

    if st.button("Compare scenarios", use_container_width=True):
        comparison = compare_records(
            model,
            baseline,
            proposed,
            value_per_click=sim_value,
            cpm_cost=sim_cpm,
            volume=int(sim_volume),
        )
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Baseline probability", f"{comparison['baseline_probability']:.2%}")
        s2.metric("Proposed probability", f"{comparison['proposed_probability']:.2%}")
        s3.metric("Probability delta", f"{comparison['probability_change_points']:+.2f} pp")
        s4.metric("Incremental expected clicks", f"{comparison['incremental_expected_clicks']:+,.0f}")
        st.metric("Incremental expected value", f"{comparison['incremental_expected_value']:+,.2f}")
        st.caption(comparison["interpretation"])

with evidence_tab:
    st.markdown("### Original case-study evidence")
    st.write(f"**Selected model:** {SELECTED_MODEL}")
    st.write(f"**Validation design:** {VALIDATION_DESIGN}")
    st.dataframe(pd.DataFrame(MODEL_COMPARISON), hide_index=True, use_container_width=True)

    st.markdown("#### Personalization ablation")
    st.dataframe(pd.DataFrame(PERSONALIZATION_ABLATION), hide_index=True, use_container_width=True)
    st.caption("Personalization improves ranking quality; it should not be described as mechanically causing higher CTR.")

    st.markdown("#### SMOTE experiment")
    st.dataframe(pd.DataFrame(SMOTE_EXPERIMENT), hide_index=True, use_container_width=True)
    st.caption("Partial SMOTE reduced false negatives, but AUC did not improve. Full balance expanded training rows by ~1.86×, so SMOTE was not selected.")

    st.markdown("#### Product evidence")
    product_df = pd.DataFrame(PRODUCT_PERFORMANCE)
    product_df["ctr"] = product_df["ctr"].map(lambda x: f"{x:.2%}")
    st.dataframe(product_df, hide_index=True, use_container_width=True)

    with st.expander("Seven final business answers"):
        for idx, answer in enumerate(FINAL_BUSINESS_ANSWERS, start=1):
            st.markdown(f"**{idx}.** {answer}")

    st.markdown("### Public demo model metadata")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Version", model.model_version)
    q2.metric("Synthetic training rows", f"{model.training_rows:,}")
    q3.metric("Demo ROC-AUC", f"{model.metrics.get('roc_auc', 0):.3f}")
    q4.metric("Demo PR-AUC", f"{model.metrics.get('pr_auc', 0):.3f}")
    importance = pd.DataFrame(
        [{"feature": k, "importance": v} for k, v in model.feature_importance.items()]
    ).head(15)
    st.bar_chart(importance.set_index("feature"))

with monitoring_tab:
    st.markdown("### Monitoring and governance demonstration")
    st.write(
        "A deployed CTR model should be monitored on ranking quality, calibration, observed CTR, feature drift, segment performance, and feedback-loop risk. This tab evaluates a deterministic labeled synthetic stream to prove the monitoring path."
    )
    stream = demo_batch(rows=1000, seed=99, labels=True)
    metrics = evaluate_records(model, stream)
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Synthetic stream ROC-AUC", f"{metrics['roc_auc']:.3f}" if metrics['roc_auc'] is not None else "N/A")
    r2.metric("Synthetic stream PR-AUC", f"{metrics['pr_auc']:.3f}" if metrics['pr_auc'] is not None else "N/A")
    r3.metric("Observed CTR", f"{metrics['observed_ctr']:.2%}")
    r4.metric("Mean predicted CTR", f"{metrics['mean_predicted_ctr']:.2%}")
    st.json(metrics)
    st.warning(
        "Production monitoring must use real post-deployment labels and privacy-approved features. Demographic fields should be reviewed for fairness and never used as hard exclusion rules without policy/legal review."
    )

st.divider()
st.caption(
    f"ClickPilot AI · original case study: {ORIGINAL_TRAIN_IMPRESSIONS:,} impressions / {ORIGINAL_TRAIN_CLICKS:,} clicks · public demo model: {model.model_version}"
)
