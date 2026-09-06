# Scout research brief — IaC tool sentiment/usage

For each tool in your assigned cluster, gather real-world USAGE and SENTIMENT evidence from ~2023-2026 and write it as strict JSON. GitHub star/commit metrics are already collected separately; focus on OPINION/SENTIMENT and qualitative adoption.

## Method (read-only; use web_search)
- Read your cluster's input file (path given in your task): it lists `{id,name,repo,oneliner,license}` per tool.
- For EACH tool collect 20+ sentiment DATA POINTS (aim high; report the true number found). A data point = one opinion from a real, linkable source dated ~2023-2026. Sources to mine:
  - HackerNews (search hn.algolia.com), Reddit (r/devops, r/terraform, r/kubernetes, r/ansible, r/sysadmin, plus tool-specific subs)
  - YouTube reviews/tutorials (judge from title + comment tone + view signal)
  - Dev.to / Medium / personal blogs, and "X vs Y" comparison articles
- Code each data point's stance:
  - `pos` = author recommends/praises, net-positive, would use again
  - `neu` = mixed/conditional ("great but..."), neutral tutorial, factual comparison
  - `neg` = author warns against it, frustration, migrating away, sharp criticism
- NEVER fabricate a URL. Summarize each opinion in <=15 words IN YOUR OWN WORDS (do not paste article text). If fewer than 20 found, report the true count and lower confidence.
- Distil 3-6 RECURRING author concerns per tool (criticisms that repeat), each with 1-3 supporting source URLs.

## Output
Write a JSON array (no markdown fences) to the output path in your task. Per tool object:

```
{"id","sentiment":{"pos":int,"neu":int,"neg":int,"n":int,"confidence":"high|med|low","summary":"1-2 lines",
  "data_points":[{"source":"hn|reddit|youtube|blog|article","url","date":"YYYY-MM","date_approx":true,"stance":"pos|neu|neg","note":"<=15 words"}]},
 "concerns":[{"tag":"short-slug","detail":"1 line","sources":["url"]}],
 "adopters":"notable orgs/usage signals or empty",
 "popularity_notes":"qualitative traction signals (mindshare, trend up/down)"}
```

Keep notes concise; this is evidence cataloging, not prose. Also return a 3-line summary when done.

**Note on `date_approx`:** Hacker News and Reddit posts often lack an explicit published date, so the month is interpolated from the post's base36/monotonic ID (calibrated against dated neighbours). Those points are marked `"date_approx": true` — year is reliable, month is an estimate. Blog/article/video points use explicit publication dates and omit the flag.
