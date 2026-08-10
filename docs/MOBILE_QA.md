# ClickPilot AI — Narrow / Mobile QA

## Status

**Code-level responsive review: complete.**  
**Live narrow-width visual evidence: pending.**

This distinction is intentional. The public desktop app has been functionally acceptance-tested, but the current automation environment cannot render the live Streamlit page at a mobile viewport. This document records what has been reviewed in code and what must still be visually confirmed before claiming a mobile visual pass.

## Code-level review

The Streamlit UI uses responsive primitives throughout:

- `layout="wide"` with a bounded `.block-container` (`max-width: 1400px`)
- `st.columns(...)` for forms, KPI cards, proof links, simulator controls, and monitoring metrics
- `st.tabs(...)` for the five product sections
- `use_container_width=True` for important buttons and dataframes
- no fixed pixel widths on application form controls or result cards
- the hero uses padding and typography but no hard-coded viewport width
- tables use Streamlit's scrollable dataframe component rather than a fixed HTML table

These choices reduce the risk of horizontal clipping, but they do not replace a real device-width visual review.

## Live visual acceptance checklist

Recommended viewport: **390 × 844** (or a comparable modern phone width).

Confirm each item visually:

- [ ] Hero title and subtitle wrap without horizontal clipping
- [ ] GitHub / API docs / Live app proof controls remain reachable
- [ ] Original benchmark KPI cards remain readable when stacked or reflowed
- [ ] Tab navigation remains usable; horizontal tab scrolling is acceptable if provided by Streamlit
- [ ] Impression-scorer fields stack/reflow without overlapping labels or controls
- [ ] Date/time and economic inputs remain reachable
- [ ] Result metrics remain readable after scoring
- [ ] Batch uploader and data-quality metrics remain usable
- [ ] Ranked dataframe can scroll horizontally without breaking the page
- [ ] Ranked CSV download button remains accessible
- [ ] Baseline and Proposed simulator forms remain distinguishable when stacked
- [ ] Monitoring KPI cards and JSON output remain readable
- [ ] Footer does not overflow the viewport

## Pass criteria

A mobile/narrow-width pass does **not** require the desktop multi-column layout to remain multi-column. Stacking is acceptable and expected. The pass criteria are:

1. no destructive overlap,
2. no controls rendered off-screen without a way to reach them,
3. no page-level horizontal overflow that prevents normal use,
4. tables may use their own horizontal scrolling,
5. core workflows remain operable.

## If a visual issue appears

The first hardening step should be a small CSS media query in `app/Home.py`, for example reducing hero padding/font size and outer container padding below ~640px. Avoid rewriting the application around custom HTML unless Streamlit's native responsive behavior proves insufficient.

## Release claim boundary

Until a live device-width screenshot or visual inspection is captured, describe ClickPilot AI as **publicly deployed and functionally acceptance-tested**. Do not claim that mobile visual QA has passed.
