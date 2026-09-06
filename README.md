# IaC Stack Picker (2026)

An interactive map of Infrastructure-as-Code &amp; delivery tooling. Every box is one job:
**PICK ONE** slots hold interchangeable rivals; **COMBINE** slots stack together. Each tool card
shows exact **GitHub stars** and a **favorable / total** sentiment count built from 2023–2026 opinions
on HN, Reddit, YouTube and blogs, plus a license chip, a lifecycle marker, and a catalog of recurring
author concerns with source links. Pick your tools and export the stack as **SVG + JSON**.

**Live page:** enabled via GitHub Pages.

## How the scores work
- **Sentiment:** the card shows the raw pair `pos / n` (favorable takes out of the total sampled), with `▲pos ▬neu ▼neg · n` beneath it. The sentiment bar fills to `pos / n`. A composite `(pos − neg) / n` mapped to 0–100 lives in `tools.json` only and is never the displayed number.
- **Popularity:** the card shows exact **GitHub stars**. The bar fills relative to the most-starred tool in this set on a log scale (stars only, so bar and number agree). SaaS/closed tools with **no public repo show `n/a`** rather than a fabricated number, since every tool was researched to a fixed ~20 data-point quota that makes discussion count a collection artifact, not adoption. Their qualitative traction notes are shown instead. A GitHub-only composite (`0.75·stars + 0.25·commits_90d`, min-max normalized within the set) lives in `tools.json` as `popularity.score`.
- **License vs lifecycle are separate.** The license chip always states open / source-available (BSL) / proprietary. A distinct **Fading / EOL** chip marks tools losing momentum or archived (Chef, Puppet, Salt, Terrascan), so every card states open-vs-paid on its own, never hidden behind a lifecycle label.

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
