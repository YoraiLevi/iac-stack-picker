# IaC Stack Picker (2026)

An interactive map of Infrastructure-as-Code &amp; delivery tooling. Every box is one job:
**PICK ONE** slots hold interchangeable rivals; **COMBINE** slots stack together. Each tool card
shows a **popularity score** and a **sentiment score** (an *outcomes / data-points* ratio built
from GitHub metrics and 2023–2026 opinions on HN, Reddit, YouTube and blogs), plus a catalog of
recurring author concerns with source links. Pick your tools and export the stack as **SVG + JSON**.

**Live page:** enabled via GitHub Pages.

## How the scores work
- **Sentiment** = `(pos − neg) / n` mapped to 0–100, with raw `▲pos ▬neu ▼neg · n` shown on every card.
- **Popularity** = composite of GitHub stars (0.75) and 90-day commit activity (0.25),
  min-max normalized **within this survey set** (so it reads "big vs small here", not absolute install base).
  SaaS/closed tools with **no public repo show `n/a`** — we don't fabricate a number from discussion volume,
  because every tool was researched to a fixed ~20 data-point quota, making discussion count a collection
  artifact rather than an adoption signal. Their qualitative traction notes are shown instead.

Scores are indicative and method-transparent, not authoritative. Every data point links to its source.

## Data provenance and honesty
- **URLs are real, not recalled.** Every source URL was returned by an actual search during
  research; a random spot-check of 24 across all six clusters returned HTTP 200. None were constructed.
- **Community-post dates are approximate.** For Hacker News and Reddit items without an explicit
  published date, the *month* was interpolated from the post's base36/monotonic ID, calibrated against
  neighbours whose dates were stated. Those points carry `"date_approx": true` in
  `data/research/out/*.json`; treat the **year** as reliable and the **month** as an estimate. Blog,
  article and video dates are taken from explicit publication dates and are not flagged.
- **Notes are ≤15-word paraphrases**, not quoted article text.

## Data pipeline
1. `data/registry.json` — canonical tool list (frozen).
2. `data/gh_metrics.json` — GitHub metrics via one GraphQL query.
3. `data/research/out/*.json` — sentiment/concerns gathered per cluster.
4. `scripts/merge.py` — merges + computes scores into `data/tools.json` (consumed by `index.html`).

Static site, no backend, no build step. The only third-party runtime request is the Jost webfont from Google Fonts (`@import` in `index.html`, allow-listed in the page CSP); icon marks are CC0 and tool data is inlined.
