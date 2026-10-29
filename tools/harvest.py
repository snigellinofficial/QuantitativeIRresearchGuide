# -*- coding: utf-8 -*-
"""从 OpenAlex 定点收割国际政治 / 发展经济学顶刊论文候选池。

两路：
  A. 按刊物 ISSN 拉取 2018 年以来的高被引论文，以及全时段经典。
  B. 按议题关键词跨库检索，捕捉 2024 年以来的前沿。
输出 consolidated JSON 到 catalog-candidates.json。
"""
import json
import os
import time
import urllib.parse
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "tools", "candidates_raw.json")

MAILTO = "mailto:research-agent@example.org"
BASE = "https://api.openalex.org/works"
SEL = ("id,doi,title,publication_year,cited_by_count,type,"
       "primary_location,authorships,abstract_inverted_index,concepts")

# ---------------------------------------------------------------- 刊物清单
# (简称, ISSN 列表, 学科)
JOURNALS = [
    ("APSR",  ["0003-0554", "1537-5943"], "IR/比较政治"),
    ("AJPS",  ["0092-5853", "1540-5907"], "IR/比较政治"),
    ("JOP",   ["0022-3816", "1468-2508"], "IR/比较政治"),
    ("IO",    ["0020-8183", "1531-5088"], "国际组织"),
    ("ISQ",   ["0020-8833", "1468-2478"], "国际关系"),
    ("JCR",   ["0022-0027", "1552-8766"], "冲突研究"),
    ("WP",    ["0043-8871", "1086-3338"], "世界政治"),
    ("PA",    ["1047-1987", "1476-4989"], "政治方法论"),
    ("RIO",   ["1559-7431", "1559-744X"], "国际组织"),
    ("EJIR",  ["1354-0661", "1460-3713"], "欧洲国际关系"),
    ("IS",    ["0162-2889", "1531-4804"], "安全研究"),
    ("JPR",   ["0022-3433", "1460-3578"], "和平研究"),
    ("QJPS",  ["1554-0626", "1554-0634"], "政治学"),
    ("CPS",   ["0010-4140", "1552-3829"], "比较政治"),
    ("BJPS",  ["0007-1234", "1469-2112"], "政治学"),
    ("AER",   ["0002-8282"], "经济学"),
    ("QJE",   ["0033-5533", "1531-4650"], "经济学"),
    ("JPE",   ["0022-3808", "1537-534X"], "经济学"),
    ("ECTA",  ["0012-9682", "1468-0262"], "经济学"),
    ("REStud",["0034-6527", "1467-937X"], "经济学"),
    ("AEJApp",["1945-7782", "1945-7790"], "应用经济学"),
    ("AEJMac",["1945-7707", "1945-7715"], "宏观经济学"),
    ("REStat",["0034-6535", "1530-9142"], "经济学"),
    ("JDE",   ["0304-3878"], "发展经济学"),
    ("JIE",   ["0022-1996"], "国际贸易"),
    ("WD",    ["0305-750X"], "发展研究"),
    ("JEP",   ["0895-3309"], "经济学综述"),
    ("ARPS",  ["1094-2939", "1545-1577"], "政治学综述"),
    ("NATURHUM", ["2397-3374"], "跨学科"),
    ("NATURE",   ["0028-0836", "1476-4687"], "跨学科"),
    ("SCIENCE",  ["0036-8075", "1095-9203"], "跨学科"),
]

# ---------------------------------------------------------------- 议题关键词
TOPICS = [
    "economic sanctions effectiveness",
    "geoeconomics economic statecraft",
    "weaponized interdependence global networks",
    "supply chain reshoring decoupling",
    "export controls semiconductor technology competition",
    "financial sanctions central bank reserves",
    "sovereign debt IMF conditionality",
    "foreign aid allocation donor politics",
    "alliance deterrence extended",
    "cyber conflict attribution",
    "drone warfare remote violence",
    "climate change armed conflict",
    "migration refugees asylum",
    "trade war tariff retaliation",
    "global value chains political risk",
    "AI artificial intelligence governance geopolitics",
    "satellite imagery machine learning conflict",
    "energy transition geopolitics",
    "nuclear proliferation",
    "IO institutional design delegation",
    "soft power public diplomacy",
    "investment treaties ISDS arbitration",
    "sanctions evasion shell companies",
    "peacekeeping intervention effectiveness",
    "natural resources oil mining conflict",
    "state capacity taxation",
    "territorial dispute maritime",
    "election foreign interference information",
    "international law compliance",
    "exchange rate currency hierarchy dollar",
]


def fetch(url, tries=5):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": MAILTO})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if k == tries - 1:
                return {"error": repr(e)[:120]}
            time.sleep(2.0 + 2.0 * k)
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
    return " ".join(wd for _, wd in pos)[:900]


def slim(w):
    src = (w.get("primary_location") or {}).get("source") or {}
    aus = []
    for a in w.get("authorships", [])[:5]:
        nm = (a.get("author") or {}).get("display_name")
        if nm:
            aus.append(nm)
    return {
        "id": (w.get("id") or "").rsplit("/", 1)[-1],
        "doi": w.get("doi"),
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "cites": w.get("cited_by_count"),
        "venue": src.get("display_name"),
        "issn": (src.get("issn_l") or ""),
        "authors": aus,
        "abstract": abstract_of(w),
        "type": w.get("type"),
    }


def collect(query_params, tag):
    url = BASE + "?" + query_params + "&select=" + urllib.parse.quote(SEL) + "&mailto=research-agent@example.org"
    d = fetch(url)
    res = d.get("results", []) if isinstance(d, dict) else []
    out = []
    for w in res:
        s = slim(w)
        s["tag"] = tag
        out.append(s)
    return out


def main():
    pool = {}

    # A. 按刊物收割：近八年高被引 + 全时段经典
    for short, issns, field in JOURNALS:
        for issn in issns:
            for tag, extra in [
                ("recent", "filter=primary_location.source.issn:%s,from_publication_date:2018-01-01&sort=cited_by_count:desc&per-page=25" % issn),
                ("classic", "filter=primary_location.source.issn:%s,to_publication_date:2017-12-31&sort=cited_by_count:desc&per-page=12" % issn),
            ]:
                rows = collect(extra, "%s:%s:%s" % (short, tag, field))
                for r in rows:
                    r["venue_short"] = short
                    r["field"] = field
                    pool.setdefault(r["id"], r)
                time.sleep(0.35)
        print("journal done", short, len(pool), flush=True)

    # B. 按议题收割：2020 年以来、被引 12 次以上
    for q in TOPICS:
        params = ("search=" + urllib.parse.quote(q) +
                  "&filter=from_publication_date:2020-01-01,cited_by_count:%3E11"
                  "&sort=cited_by_count:desc&per-page=15")
        rows = collect(params, "topic")
        for r in rows:
            r.setdefault("venue_short", (r.get("venue") or "?")[:16])
            r.setdefault("field", "议题检索")
            r["topic_query"] = q
            pool.setdefault(r["id"], r)
        time.sleep(0.35)
        print("topic done", q[:34], len(pool), flush=True)

    data = list(pool.values())
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("TOTAL", len(data), "->", OUT)


if __name__ == "__main__":
    main()
