#!/usr/bin/env python3
"""Merge registry + GitHub metrics + scout sentiment research into data/tools.json.

Scoring (transparent, reproducible; all relative to THIS survey set):

Popularity score 0-100:
  - Tools WITH a public repo: composite of GitHub signals
        0.60 * norm(log10 stars) + 0.15 * norm(log10 commits_90d) + 0.25 * norm(log10 sentiment_n)
    method tag = "github+buzz". Raw signals shown on the card.
  - Tools WITHOUT a public repo (SaaS/closed): mindshare proxy = norm(log10 sentiment_n)*100
    method tag = "mindshare". Flagged so the number is never mistaken for install base.

Sentiment score 0-100:
  net = (pos - neg) / n      in [-1, 1]
  score = round((net + 1) / 2 * 100)   ("outcomes / data-points" ratio, shown as pos/neu/neg + n)
  null when n == 0.
"""
import json, math, glob, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,"data")

def load(p):
    with open(p, encoding="utf-8") as f: return json.load(f)

registry=load(os.path.join(D,"registry.json"))
metrics=load(os.path.join(D,"gh_metrics.json"))

research={}
for fp in glob.glob(os.path.join(D,"research","out","*.json")):
    try:
        arr=load(fp)
    except Exception as e:
        print("WARN bad json",fp,e); continue
    for rec in arr:
        research[rec["id"]]=rec

def nlog(x): return math.log10((x or 0)+1)
def normalizer(vals):
    lo,hi=min(vals),max(vals)
    return (lambda v: 0.0 if hi==lo else (v-lo)/(hi-lo))

# collect populations for normalization
star_pop=[nlog(metrics.get(t["repo"],{}).get("stars")) for t in registry if t["repo"] and "error" not in metrics.get(t["repo"],{})]
com_pop =[nlog(metrics.get(t["repo"],{}).get("commits_90d")) for t in registry if t["repo"] and "error" not in metrics.get(t["repo"],{})]
n_pop   =[nlog((research.get(t["id"],{}).get("sentiment") or {}).get("n") or 0) for t in registry]
Ns=normalizer(star_pop or [0]); Nc=normalizer(com_pop or [0]); Nn=normalizer(n_pop or [0])

out=[]
for t in registry:
    m=metrics.get(t["repo"],{}) if t["repo"] else {}
    r=research.get(t["id"],{})
    sen=r.get("sentiment") or {}
    n=sen.get("n") or 0; pos=sen.get("pos") or 0; neg=sen.get("neg") or 0
    sscore=None; net=None
    if n:
        net=(pos-neg)/n; sscore=round((net+1)/2*100)
    # Popularity uses ONLY real GitHub signals. sentiment_n is NOT used: every tool
    # has ~20 data points by collection design, so it is a quota artifact, not adoption.
    if t["repo"] and "error" not in m and m.get("stars") is not None:
        pscore=round(100*(0.75*Ns(nlog(m.get("stars")))+0.25*Nc(nlog(m.get("commits_90d")))))
        pmethod="github"
    else:
        pscore=None            # SaaS/closed: no public-repo metric; do not fabricate one
        pmethod="saas-no-repo"
    # top distinct sources
    dps=sen.get("data_points") or []
    seen=set(); sources=[]; pros=[]; pseen=set()
    for dp in dps:
        u=dp.get("url")
        if u and u not in seen: seen.add(u); sources.append(u)
        if dp.get("stance")=="pos":
            note=(dp.get("note") or "").strip(); key=note.lower()
            if note and key not in pseen and len(pros)<5:
                pseen.add(key); pros.append({"note":note,"url":u,"source":dp.get("source")})
    sources=sources[:6]
    out.append({**{k:t[k] for k in ("id","name","stage","stage_num","slot","slot_mode","license","oneliner","brand","mono","icon","repo","docs")},
      "stage_name":t["stage_name"],
      "metrics":{"stars":m.get("stars"),"forks":m.get("forks"),"commits_90d":m.get("commits_90d"),
                 "latest_release":m.get("latest_release"),"latest_release_at":m.get("latest_release_at"),
                 "archived":m.get("archived"),"license_spdx":m.get("license")},
      "popularity":{"score":pscore,"method":pmethod,
                    "signals":{"stars":m.get("stars"),"commits_90d":m.get("commits_90d")}},
      "sentiment":{"pos":pos,"neu":sen.get("neu") or 0,"neg":neg,"n":n,"net":round(net,3) if net is not None else None,
                   "score":sscore,"confidence":sen.get("confidence"),"summary":sen.get("summary")},
      "concerns":r.get("concerns") or [],
      "adopters":r.get("adopters") or "",
      "popularity_notes":r.get("popularity_notes") or "",
      "pros":pros,
      "sources":sources,
    })

json.dump(out,open(os.path.join(D,"tools.json"),"w",encoding="utf-8"),indent=1,ensure_ascii=False)
have=sum(1 for t in out if t["sentiment"]["n"])
print(f"merged {len(out)} tools; {have} with sentiment; {sum(1 for t in out if t['popularity']['score'] is not None)} with popularity")
missing=[t["id"] for t in out if not t["sentiment"]["n"]]
if missing: print("no sentiment yet:", ", ".join(missing))
