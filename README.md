# IaC Stack Picker (2026)

An interactive map of Infrastructure-as-Code &amp; delivery tooling. Every box is one job:
**PICK ONE** slots hold interchangeable rivals; **COMBINE** slots stack together. Each tool card
shows a **popularity score** and a **sentiment score** (an *outcomes / data-points* ratio built
from GitHub metrics and 2023–2026 opinions on HN, Reddit, YouTube and blogs), plus a catalog of
recurring author concerns with source links. Pick your tools and export the stack as **SVG + JSON**.

**Live page:** enabled via GitHub Pages.

## How the scores work
- **Sentiment** = `(pos − neg) / n` mapped to 0–100, with raw `▲pos ▬neu ▼neg · n` shown on every card.
- **Popularity** = composite of GitHub stars, 90-day commit activity, and discussion volume,
  min-max normalized **within this survey set** (so it reads "big vs small here", not absolute install base).
  SaaS/closed tools with no public repo get a mindshare proxy from discussion volume, flagged as such.

Scores are indicative and method-transparent, not authoritative. Every data point links to its source.

## Data pipeline
1. `data/registry.json` — canonical tool list (frozen).
2. `data/gh_metrics.json` — GitHub metrics via one GraphQL query.
3. `data/research/out/*.json` — sentiment/concerns gathered per cluster.
4. `scripts/merge.py` — merges + computes scores into `data/tools.json` (consumed by `index.html`).

Static site, no backend, no build step, no runtime third-party calls (icon marks are CC0, inlined).
