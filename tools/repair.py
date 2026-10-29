# -*- coding: utf-8 -*-
"""修补核验结果：剔除预印本与图书，补齐未命中条目。"""
import difflib
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "verified.json")
V1 = os.path.join(ROOT, "catalog.json")
OUT = os.path.join(ROOT, "tools", "verified2.json")
UA = "lit-review/1.0 (mailto:research-agent@example.org)"
WS = re.compile(r"\s+")
TAGS = re.compile(r"<[^>]+>")
BAD_VENUE = ("ssrn", "repec", "book", "working", "nber", "preprint", "dissertation")

RETRY = [
    ("G", "The Economics of Urban Density", "Duranton", 2020),
    ("G", "The Economics of Urban Density", "Puga", 2020),
    ("I", "Hard and Soft Law in International Governance", "Abbott", 2000),
    ("I", "Foreign Aid and State Legitimacy", "Blair", 2021),
    ("I", "Foreign Aid and State Legitimacy: Evidence on Chinese and US Programs from a Nationwide Survey in Africa", "Blair", 2021),
    ("N", "Power Positions: International Organizations, Social Networks, and Conflict", "Hafner-Burton", 2006),
    ("L", "The Causal Effect of Environmental Catastrophe on Long-Run Human Capital Formation", "Hsiang", 2014),
    ("F", "Text as Data", "Gentzkow", 2019),
    ("M", "Bartik Instruments: What Do (and Don't Do) When You Use Them", "Goldsmith-Pinkham", 2020),
    ("M", "Civil War", "Blattman", 2010),
    ("M", "Greed and grievance in civil war", "Collier", 2004),
    ("M", "Shift-Share Designs: Theory and Inference", "Adao", 2019),
    ("M", "Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects", "Chaisemartin", 2020),
    ("C", "Economic Shocks and Conflict: Evidence from Commodity Prices", "Bazzi", 2014),
    ("C", "On the Origins of the State: Stationary Bandits and Taxation in Eastern Congo", "Sierra", 2020),
    ("S", "The Return to Protectionism", "Fajgelbaum", 2020),
    ("S", "Dominant Currency Paradigm", "Gopinath", 2020),
    ("S", "Success of economic sanctions threats: coercion, information and commitment", "Walentek", 2021),
    ("S", "The Sword and the Shield: The Economics of Targeted Sanctions", "Ahn", 2020),
    ("L", "What Do We Learn from the Weather? The New Climate-Economy Literature", "Dell", 2014),
    ("L", "The migration response to increasing temperatures", "Cattaneo", 2016),
    ("L", "Climate change, mortality, and adaptation: Evidence from annual fluctuations in weather in the US", "Deschenes", 2011),
    ("F", "Combining satellite imagery and machine learning to predict poverty", "Jean", 2016),
    ("F", "Double/debiased machine learning for treatment and structural parameters", "Chernozhukov", 2018),
    ("M", "The Colonial Origins of Comparative Development: An Empirical Investigation", "Acemoglu", 2001),
    ("G", "The Persistent Effects of Peru's Mining Mita", "Dell", 2010),
    ("G", "Pre-Colonial Ethnic Institutions and Contemporary African Development", "Michalopoulos", 2013),
    ("N", "The Diffusion of Microfinance", "Banerjee", 2013),
    ("G", "On the Geography of Global Value Chains", "Antras", 2020),
    ("F", "The changing surface of the world's roads", "Randhawa", 2026),
]


def fetch(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if k == tries - 1:
                return {}
            time.sleep(2.0)
    return {}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def clean(t):
    return WS.sub(" ", html.unescape(TAGS.sub(" ", t or ""))).strip()


def best_match(title, hint, year, rows=8):
    url = ("https://api.crossref.org/works?query.bibliographic=" + urllib.parse.quote(title) +
           "&rows=%d&filter=type:journal-article"
           "&select=DOI,title,author,container-title,issued,is-referenced-by-count,volume,issue,page,type" % rows)
    d = fetch(url)
    items = ((d.get("message") or {}).get("items") or [])
    best = None
    for it in items:
        t = clean((it.get("title") or [""])[0])
        sim = difflib.SequenceMatcher(None, norm(title), norm(t)).ratio()
        fam = " ".join((a.get("family") or "") for a in (it.get("author") or [])[:3]).lower()
        bonus = 0.12 if hint.lower().replace("-", " ") in fam.replace("-", " ") else 0.0
        y = ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0]
        yb = 0.06 if (year and y and abs(int(y) - int(year)) <= 1) else 0.0
        ct = (it.get("container-title") or [""])
        ven = (ct[0] if ct else "").lower()
        vb = -0.25 if any(b in ven for b in BAD_VENUE) else 0.0
        s = sim + bonus + yb + vb
        if best is None or s > best[0]:
            best = (s, it, sim, y)
    if not best or best[2] < 0.70:
        return None
    s, it, sim, y = best
    ct = (it.get("container-title") or [""])
    au = []
    for a in (it.get("author") or [])[:5]:
        nm = " ".join(x for x in [a.get("given"), a.get("family")] if x)
        if nm:
            au.append(nm)
    return {
        "status": "ok", "sim": round(sim, 3),
        "doi": (it.get("DOI") or "").lower(),
        "title": clean((it.get("title") or [""])[0]),
        "venue": ct[0] if ct else "",
        "year": y,
        "volume": it.get("volume"), "issue": it.get("issue"), "page": it.get("page"),
        "cites": it.get("is-referenced-by-count", 0),
        "authors": au, "type": it.get("type"),
    }


def main():
    rows = json.load(open(SRC, encoding="utf-8"))
    v1 = json.load(open(V1, encoding="utf-8"))["papers"]
    v1_by_doi = {(p.get("doi") or "").lower(): p for p in v1}
    v1_by_title = {norm(p["title"]): p for p in v1}

    fixed = {}
    for r in rows:
        if r["status"] != "ok":
            continue
        ven = (r.get("venue") or "")
        title = r["title"]
        if not ven or any(b in ven.lower() for b in BAD_VENUE):
            m = best_match(title, (r.get("authors") or [""])[0].split()[-1] if r.get("authors") else "",
                           r.get("year"), rows=10)
            if m:
                m["topic"] = r["topic"]; m["q_title"] = r.get("q_title"); m["q_hint"] = r.get("q_hint")
                fixed[r["doi"]] = m
                continue
        # 若 v1 已有更权威的题录，用 v1 的卷期覆盖空值
        p1 = v1_by_doi.get(r["doi"]) or v1_by_title.get(norm(title))
        if p1:
            r.setdefault("volume", None)
            if not r.get("volume") and p1.get("volume"):
                r["volume"] = p1["volume"].strip("()").split("(")[0]
                if "(" in p1["volume"]:
                    r["issue"] = p1["volume"].split("(")[1].rstrip(")")
        fixed[r["doi"]] = r

    # 重试未命中
    for topic, title, hint, year in RETRY:
        m = best_match(title, hint, year, rows=10)
        if m:
            m["topic"] = topic; m["q_title"] = title; m["q_hint"] = hint
            m["retried"] = True
            fixed[m["doi"]] = m
            print("RETRY OK", topic, title[:44], "|", m["venue"][:38])
        else:
            print("RETRY MISS", topic, title[:54])
        time.sleep(0.24)

    # 补入 v1 中未被覆盖的条目
    v1_bucket = {
        "A": "G", "B": "G", "C": "G", "D": "C", "E": "N", "F": "F",
    }
    for p in v1:
        d = (p.get("doi") or "").lower()
        if d in fixed:
            continue
        fixed[d] = {
            "status": "ok", "sim": 1.0, "doi": d, "title": p["title"],
            "venue": p["venue"], "year": p["year"],
            "volume": (p.get("volume") or "").split("(")[0],
            "issue": (p.get("volume") or "").split("(")[1].rstrip(")") if "(" in (p.get("volume") or "") else None,
            "page": None, "cites": p.get("cites", 0),
            "authors": [a.strip() for a in p["authors"].split(",")],
            "type": "journal-article",
            "topic": v1_bucket.get(p["group"], "G"),
            "from_v1": p["id"],
        }

    out = list(fixed.values())
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print("TOTAL", len(out), Counter(r["topic"] for r in out))


if __name__ == "__main__":
    main()
