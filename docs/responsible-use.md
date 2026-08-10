# Responsible Use and Ad-Tech Guardrails

ClickPilot AI is a predictive ranking system, not a causal targeting oracle.

- Do not interpret a higher score for a demographic group as permission to exclude protected or sensitive groups.
- Prefer behavioral and contextual features where possible.
- Require legal/privacy review before using identity-linked history in real advertising systems.
- Keep exploration traffic so the system can discover changing preferences and avoid self-reinforcing feedback loops.
- Use value-aware thresholds rather than accuracy alone.
- Recompute historical CTR features from past-only windows or out-of-fold logic to prevent leakage.
- Monitor calibration and segment performance, not only ROC-AUC.
- Inventory decisions require downstream conversion, order rate, units/order, lead time, and safety stock; CTR alone is insufficient.
