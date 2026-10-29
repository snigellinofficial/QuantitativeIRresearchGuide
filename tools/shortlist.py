# -*- coding: utf-8 -*-
"""把候选池切成七个议题短名单，供人工挑选。"""
import json
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "candidates_cr.json")
OUT = os.path.join(ROOT, "tools", "shortlist.md")

TIER = {
    "american political science review": "APSR",
    "american journal of political science": "AJPS",
    "the journal of politics": "JOP",
    "journal of politics": "JOP",
    "international organization": "IO",
    "international studies quarterly": "ISQ",
    "journal of conflict resolution": "JCR",
    "world politics": "WP",
    "political analysis": "PA",
    "the review of international organizations": "RIO",
    "review of international organizations": "RIO",
    "european journal of international relations": "EJIR",
    "international security": "IS",
    "journal of peace research": "JPR",
    "quarterly journal of political science": "QJPS",
    "comparative political studies": "CPS",
    "british journal of political science": "BJPS",
    "annual review of political science": "ARPS",
    "american economic review": "AER",
    "the quarterly journal of economics": "QJE",
    "quarterly journal of economics": "QJE",
    "journal of political economy": "JPE",
    "econometrica": "ECTA",
    "the review of economic studies": "REStud",
    "review of economic studies": "REStud",
    "american economic journal: applied economics": "AEJApp",
    "american economic journal: macroeconomics": "AEJMac",
    "the review of economics and statistics": "REStat",
    "review of economics and statistics": "REStat",
    "journal of development economics": "JDE",
    "journal of international economics": "JIE",
    "world development": "WD",
    "journal of economic perspectives": "JEP",
    "nature human behaviour": "NatHum",
    "proceedings of the national academy of sciences": "PNAS",
    "science": "Sci",
    "nature": "Nat",
    "review of international political economy": "RIPE",
    "conflict management and peace science": "CMPS",
    "security studies": "SecSt",
    "political science research and methods": "PSRM",
    "international interactions": "II",
    "journal of economic growth": "JEG",
    "review of international studies": "RIS",
    "european journal of political research": "EJPR",
}

BUCKETS = [
    ("G", "地理与基础设施", [
        "spatial", "geograph", "distance", "road", "railroad", "railway", "infrastructure",
        "market access", "border", "agglomerat", "city", "cities", "regional", "terrain",
        "transport", "electricity", "electrif", "port", "location", "nighttime", "gIS"]),
    ("C", "冲突与政治暴力", [
        "conflict", "civil war", "violence", "insurgen", "terror", "deter", "militar",
        "war", "peacekeep", "rebel", "insurgenc", "armed", "ceasefire", "peace agreement",
        "drone", "coercion", "repression", "protest"]),
    ("S", "制裁与经济治国", [
        "sanction", "export control", "geoeconom", "economic statecraft", "tariff",
        "trade war", "decoupl", "coercion", "restrict", "embargo", "export", "import",
        "foreign direct investment", "investment screen", "supply chain", "reserv",
        "financial", "currency", "dollar"]),
    ("I", "国际制度与援助", [
        "foreign aid", "aid ", "imf", "world bank", "conditionality", "international organization",
        "institution", "delegat", "compliance", "treaty", "alliance", "io member",
        "world trade organization", "wto", "regime", "governance", "multilateral"]),
    ("N", "网络、依赖与等级", [
        "network", "value chain", "dependen", "interdependen", "centrality", "hierarch",
        "diffusion", "spillover", "contagion", "peer", "social network", "broker",
        "topolog", "graph"]),
    ("L", "气候、迁移与灾害", [
        "climate", "weather", "temperature", "rainfall", "precipitation", "drought",
        "disaster", "migrat", "refugee", "displace", "flood", "heat", "environment",
        "adaptation", "food security"]),
    ("F", "测量、机器学习与前沿", [
        "machine learning", "satellite", "remote sensing", "nighttime", "text as data",
        "natural language", "language model", "predict", "measurement", "big data",
        "neural", "supervised", "unstructured", "image", "geocod", "automated"]),
]


def main():
    rows = json.load(open(SRC, encoding="utf-8"))
    keep = []
    for r in rows:
        v = (r.get("venue") or "").strip().lower()
        v = re.sub(r"\s+", " ", v)
        short = TIER.get(v)
        if not short:
            continue
        if r.get("type") and r["type"] != "journal-article":
            continue
        if not r.get("year"):
            continue
        r["short"] = short
        keep.append(r)

    # 去重：同一标题只留被引最高的一条
    seen = {}
    for r in keep:
        k = re.sub(r"[^a-z0-9]", "", (r["title"] or "").lower())[:70]
        if k not in seen or r["cites"] > seen[k]["cites"]:
            seen[k] = r
    keep = list(seen.values())

    # 分桶
    bucket_hits = defaultdict(list)
    for r in keep:
        blob = ((r.get("title") or "") + " " + (r.get("abstract") or "")).lower()
        best = None
        for bid, name, kws in BUCKETS:
            score = sum(1 for kw in kws if kw.lower() in blob)
            if score >= 2:
                bucket_hits[bid].append((score, r))

    lines = []
    lines.append("# 候选短名单\n")
    lines.append("共 %d 篇进入顶刊池，按议题分桶。每行格式：年份｜刊物｜引用｜作者｜标题。\n" % len(keep))

    for bid, name, kws in BUCKETS:
        items = sorted(bucket_hits[bid], key=lambda x: (-x[0], -x[1]["cites"]))[:38]
        lines.append("\n## %s %s（%d 条）\n" % (bid, name, len(items)))
        for score, r in items:
            au = (r["authors"][0].split()[-1] if r["authors"] else "?")
            lines.append("%s|%s|%s|%d|%s|%s\n" % (
                r["year"], r["short"], r["cites"], score, au, r["title"][:110]))

    # 顶刊总览：高被引前 120
    lines.append("\n## TOP 顶刊高被引总览（120 条）\n")
    top = sorted(keep, key=lambda x: -x["cites"])[:120]
    for r in top:
        au = (r["authors"][0].split()[-1] if r["authors"] else "?")
        lines.append("%s|%s|%s|%s|%s\n" % (r["year"], r["short"], r["cites"], au, r["title"][:110]))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print("tier pool", len(keep), "->", OUT)
    for bid, name, _ in BUCKETS:
        print(" ", bid, len(bucket_hits[bid]))


if __name__ == "__main__":
    main()
