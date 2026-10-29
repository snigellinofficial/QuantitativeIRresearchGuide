# -*- coding: utf-8 -*-
"""串行限速版收割：遵守 OpenAlex 速率限制，断点续跑，增量落盘。"""
import json
import os
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "candidates_raw.json")
CACHE = os.path.join(ROOT, "tools", ".harvest_cache.json")
BASE = "https://api.openalex.org/works"
UA = "mailto:research-agent@example.org"
SEL = "id,doi,title,publication_year,cited_by_count,type,primary_location,authorships,abstract_inverted_index"

JOURNALS = [
    ("APSR", "0003-0554", "IR与比较政治"), ("AJPS", "0092-5853", "IR与比较政治"),
    ("JOP", "0022-3816", "IR与比较政治"), ("IO", "0020-8183", "国际组织"),
    ("ISQ", "0020-8833", "国际关系"), ("JCR", "0022-0027", "冲突研究"),
    ("WP", "0043-8871", "世界政治"), ("PA", "1047-1987", "政治方法论"),
    ("RIO", "1559-7431", "国际组织"), ("EJIR", "1354-0661", "欧洲国际关系"),
    ("IS", "0162-2889", "安全研究"), ("JPR", "0022-3433", "和平研究"),
    ("QJPS", "1554-0626", "政治学"), ("CPS", "0010-4140", "比较政治"),
    ("BJPS", "0007-1234", "政治学"), ("ARPS", "1094-2939", "政治学综述"),
    ("AER", "0002-8282", "经济学"), ("QJE", "0033-5533", "经济学"),
    ("JPE", "0022-3808", "经济学"), ("ECTA", "0012-9682", "经济学"),
    ("REStud", "0034-6527", "经济学"), ("AEJApp", "1945-7782", "应用经济学"),
    ("AEJMac", "1945-7707", "宏观经济学"), ("REStat", "0034-6535", "经济学"),
    ("JDE", "0304-3878", "发展经济学"), ("JIE", "0022-1996", "国际贸易"),
    ("WD", "0305-750X", "发展研究"), ("JEP", "0895-3309", "经济学综述"),
    ("NATURHUM", "2397-3374", "跨学科"), ("NATURE", "0028-0836", "跨学科"),
    ("SCIENCE", "0036-8075", "跨学科"), ("PNAS", "0027-8424", "跨学科"),
]

TOPICS = [
    "economic sanctions effectiveness", "geoeconomics economic statecraft coercion",
    "weaponized interdependence networks", "supply chain reshoring decoupling",
    "export controls semiconductors technology competition", "financial sanctions reserves currency",
    "sovereign debt IMF conditionality", "foreign aid allocation donor",
    "alliance deterrence extended", "cyber conflict attribution",
    "drone warfare remote violence", "climate armed conflict variability",
    "migration refugees asylum", "trade war tariff retaliation",
    "global value chains political risk", "artificial intelligence governance geopolitics",
    "satellite imagery machine learning poverty conflict", "energy transition geopolitics",
    "nuclear proliferation", "institutional design delegation international organizations",
    "public diplomacy soft power", "investment treaties arbitration",
    "sanctions evasion shell companies", "peacekeeping intervention effectiveness",
    "natural resources oil mining conflict", "state capacity taxation",
    "maritime territorial dispute", "foreign election interference information",
    "international law compliance human rights", "currency hierarchy exchange rate",
    "autocracy democracy backsliding", "civil war duration peace agreement",
]


def load_cache():
    if os.path.exists(CACHE):
        try:
            with open(CACHE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_cache(c):
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False)


def fetch(url, tries=6):
    delay = 6.0
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(delay)
                delay = min(delay * 1.8, 90.0)
                continue
            if k == tries - 1:
                return {}
            time.sleep(3.0)
        except Exception:
            if k == tries - 1:
                return {}
            time.sleep(3.0)
    return {}


def abstract_of(w):
    inv = w.get("abstract_inverted_index")
    if not inv:
        return ""
    pos = []
    for word, idxs in inv.items():
        for i in idxs:
            pos.append((i, word))
    pos.sort()
    return " ".join(wd for _, wd in pos)[:800]


def slim(w):
    src = (w.get("primary_location") or {}).get("source") or {}
    return {
        "id": (w.get("id") or "").rsplit("/", 1)[-1],
        "doi": w.get("doi"),
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "cites": w.get("cited_by_count"),
        "venue": src.get("display_name"),
        "authors": [((a.get("author") or {}).get("display_name") or "")
                    for a in w.get("authorships", [])[:4]
                    if (a.get("author") or {}).get("display_name")],
        "abstract": abstract_of(w),
        "type": w.get("type"),
    }


def query(qs, cache, key):
    if key in cache:
        return cache[key]
    url = BASE + "?" + qs + "&select=" + urllib.parse.quote(SEL) + "&mailto=research-agent@example.org"
    d = fetch(url)
    rows = [slim(w) for w in d.get("results", [])] if isinstance(d, dict) else []
    cache[key] = rows
    save_cache(cache)
    time.sleep(1.05)
    return rows


def main():
    cache = load_cache()
    pool = {}
    t0 = time.time()

    for short, issn, field in JOURNALS:
        for tag, extra in [
            ("recent", "filter=primary_location.source.issn:%s,from_publication_date:2019-01-01&sort=cited_by_count:desc&per-page=18" % issn),
            ("classic", "filter=primary_location.source.issn:%s,to_publication_date:2018-12-31&sort=cited_by_count:desc&per-page=10" % issn),
        ]:
            rows = query(extra, cache, short + "|" + tag)
            for r in rows:
                r = dict(r); r["venue_short"] = short; r["field"] = field; r["pass"] = tag
                pool.setdefault(r["id"], r)
        print("J", short, len(pool), "%.0fs" % (time.time() - t0), flush=True)

    for i, q in enumerate(TOPICS):
        qs = ("search=" + urllib.parse.quote(q) +
              "&filter=from_publication_date:2020-01-01,cited_by_count:%3E10"
              "&sort=cited_by_count:desc&per-page=14")
        rows = query(qs, cache, "T|" + q)
        for r in rows:
            r = dict(r); r["venue_short"] = (r.get("venue") or "?")[:20]
            r["field"] = "议题检索"; r["topic_query"] = q; r["pass"] = "frontier"
            pool.setdefault(r["id"], r)
        if i % 6 == 0:
            print("T", q[:28], len(pool), "%.0fs" % (time.time() - t0), flush=True)

    data = [v for v in pool.values() if v.get("title")]
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print("TOTAL", len(data), "->", OUT, "elapsed %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
