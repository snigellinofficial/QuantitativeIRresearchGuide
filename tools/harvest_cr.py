# -*- coding: utf-8 -*-
"""用 Crossref 收割候选池。

Crossref 的 is-referenced-by-count 与 OpenAlex 的 cited_by_count 口径不同，
故全部候选统一标注来源为 Crossref，不与其他口径混用。
"""
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "candidates_cr.json")
UA = "lit-review/1.0 (mailto:research-agent@example.org)"
SEL = "DOI,title,author,container-title,issued,is-referenced-by-count,abstract,type,volume,issue"

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
    ("NATURHUM", "2397-3374", "跨学科"), ("PNAS", "0027-8424", "跨学科"),
    ("SCIENCE", "0036-8075", "跨学科"), ("NATURE", "0028-0836", "跨学科"),
]

TOPICS = [
    "economic sanctions effectiveness", "geoeconomics economic statecraft coercion",
    "weaponized interdependence network", "supply chain reshoring decoupling",
    "export controls semiconductor technology competition", "financial sanctions foreign reserves",
    "sovereign debt IMF conditionality", "foreign aid allocation donor politics",
    "alliance deterrence extended", "cyber conflict attribution",
    "drone warfare remote violence", "climate armed conflict",
    "migration refugees asylum", "trade war tariff retaliation",
    "global value chains political risk", "artificial intelligence geopolitics governance",
    "satellite imagery machine learning poverty", "energy transition geopolitics",
    "nuclear proliferation", "institutional design delegation international organization",
    "public diplomacy soft power", "investment treaties arbitration",
    "sanctions evasion ownership networks", "peacekeeping intervention effectiveness",
    "natural resources oil mining conflict", "state capacity taxation",
    "maritime territorial dispute", "foreign election interference",
    "international law compliance human rights", "currency hierarchy dollar hegemony",
    "democratic backsliding autocracy", "civil war duration peace agreement",
    "foreign direct investment political risk", "climate migration displacement",
]


def fetch(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if k == tries - 1:
                return {}
            time.sleep(2.0 + 2.0 * k)
    return {}


TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def clean(txt):
    if not txt:
        return ""
    t = TAG_RE.sub(" ", txt)
    t = html.unescape(t)
    return WS_RE.sub(" ", t).strip()[:900]


def slim(it, short, field, tag, topic=""):
    doi = (it.get("DOI") or "").lower()
    issued = ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0]
    aus = []
    for a in (it.get("author") or [])[:4]:
        nm = " ".join(x for x in [a.get("given"), a.get("family")] if x)
        if nm:
            aus.append(nm)
    ct = (it.get("container-title") or [""])
    return {
        "doi": doi,
        "title": clean((it.get("title") or ["?"])[0]),
        "year": issued,
        "cites": it.get("is-referenced-by-count", 0),
        "venue": ct[0] if ct else "",
        "volume": it.get("volume"),
        "issue": it.get("issue"),
        "authors": aus,
        "abstract": clean(it.get("abstract")),
        "type": it.get("type"),
        "venue_short": short,
        "field": field,
        "pass": tag,
        "topic_query": topic,
    }


def j_task(args):
    short, issn, field = args
    rows = []
    for tag, filt in [
        ("recent", "from-pub-date:2019-01-01"),
        ("classic", "until-pub-date:2018-12-31"),
    ]:
        rows_n = 20 if tag == "recent" else 12
        url = ("https://api.crossref.org/journals/%s/works?sort=is-referenced-by-count&order=desc"
               "&rows=%d&filter=%s,type:journal-article&select=%s"
               % (issn, rows_n, filt, urllib.parse.quote(SEL)))
        d = fetch(url)
        for it in ((d.get("message") or {}).get("items") or []):
            rows.append(slim(it, short, field, tag))
        time.sleep(0.25)
    return rows


def t_task(q):
    rows = []
    for tag, filt, rows_n in [
        ("frontier", "from-pub-date:2020-01-01,type:journal-article", 15),
        ("classic", "until-pub-date:2019-12-31,type:journal-article", 8),
    ]:
        url = ("https://api.crossref.org/works?query.bibliographic=" + urllib.parse.quote(q) +
               "&sort=is-referenced-by-count&order=desc&rows=%d&filter=%s&select=%s"
               % (rows_n, filt, urllib.parse.quote(SEL)))
        d = fetch(url)
        for it in ((d.get("message") or {}).get("items") or []):
            rows.append(slim(it, "", "议题检索", tag, topic=q))
        time.sleep(0.25)
    return rows


def main():
    jobs = []
    pool = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = []
        for j in JOURNALS:
            futs.append(ex.submit(j_task, j))
        for q in TOPICS:
            futs.append(ex.submit(t_task, q))
        for i, f in enumerate(futs):
            try:
                rows = f.result()
            except Exception as e:
                print("ERR", repr(e)[:70]); continue
            for r in rows:
                if not r["doi"] or not r["title"] or r["title"] == "?":
                    continue
                pool.setdefault(r["doi"], r)
            if i % 12 == 0:
                print("done", i, len(pool), flush=True)

    data = list(pool.values())
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    with_abs = sum(1 for d in data if d["abstract"])
    print("TOTAL", len(data), "with_abstract", with_abs, "->", OUT)


if __name__ == "__main__":
    main()
