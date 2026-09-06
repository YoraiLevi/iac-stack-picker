#!/usr/bin/env python3
"""Generate CONCERNS.md from data/tools.json — a human-readable catalog of the
recurring author concerns per tool, grouped by pipeline stage, with source links
and each tool's popularity/sentiment scores for context."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tools = json.load(open(os.path.join(ROOT, "data", "tools.json")))

STAGE_ORDER = ["provision", "orchestrate", "configure", "deliver", "reconcile"]
STAGE_TITLE = {
    "provision": "1 · Provision",
    "orchestrate": "2 · Orchestrate & Govern",
    "configure": "3 · Configure · Images · Secrets",
    "deliver": "4 · Deliver · CI/CD",
    "reconcile": "5 · Reconcile · GitOps",
}
HEALTH = {"open": "open", "bsl": "source-available (BSL)", "comm": "commercial", "fade": "fading/EOL"}

lines = []
lines.append("# Author Concerns Catalog — IaC & Delivery Tools (2026)\n")
lines.append("Recurring criticisms and risks raised by practitioners across HackerNews, Reddit, "
             "YouTube, and blogs (2023-2026), distilled per tool with source links. Each tool also "
             "shows its popularity and sentiment scores (see the live picker and data/tools.json "
             "for the underlying data points).\n")
lines.append("> Scores are indicative and method-transparent, not authoritative. Sentiment = "
             "`(pos - neg)/n` mapped to 0-100; popularity is normalized within this survey set.\n")

by_stage = {}
for t in tools:
    by_stage.setdefault(t["stage"], []).append(t)

for s in STAGE_ORDER:
    group = sorted(by_stage.get(s, []), key=lambda t: (t["slot"], t["name"]))
    if not group:
        continue
    lines.append(f"\n## {STAGE_TITLE.get(s, s)}\n")
    for t in group:
        sen = t.get("sentiment", {}) or {}
        pop = t.get("popularity", {}) or {}
        pscore = pop.get("score")
        sscore = sen.get("score")
        badge = (f"popularity {pscore if pscore is not None else '-'}/100 - "
                 f"sentiment {sscore if sscore is not None else '-'}/100 "
                 f"(+{sen.get('pos',0)} ~{sen.get('neu',0)} -{sen.get('neg',0)} - n={sen.get('n',0)}"
                 f"{', ' + sen['confidence'] if sen.get('confidence') else ''})")
        lines.append(f"### {t['name']}\n")
        lines.append(f"*{HEALTH.get(t['license'], t['license'])} - {t['slot']} - {badge}*\n")
        if sen.get("summary"):
            lines.append(f"{sen['summary']}\n")
        concerns = t.get("concerns") or []
        if concerns:
            for c in concerns:
                srcs = c.get("sources") or []
                links = " ".join(f"[[{i+1}]]({u})" for i, u in enumerate(srcs[:3]))
                lines.append(f"- **{c.get('tag','concern')}** - {c.get('detail','').rstrip('.')}. {links}".rstrip())
        else:
            lines.append("- _No concerns catalogued (thin sentiment sample)._")
        lines.append("")

out = os.path.join(ROOT, "CONCERNS.md")
open(out, "w", encoding="utf-8").write("\n".join(lines))
n_concerns = sum(len(t.get("concerns") or []) for t in tools)
print(f"wrote CONCERNS.md - {len(tools)} tools, {n_concerns} concerns")
