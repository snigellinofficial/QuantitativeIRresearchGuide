# -*- coding: utf-8 -*-
"""用 OpenAlex 核验文献题录与引用量，输出 UTF-8 JSON。"""
import json
import os
import time
import urllib.parse
import urllib.request

TITLES = [
    "The Colonial Origins of Comparative Development: An Empirical Investigation",
    "The Persistent Effects of Peru's Mining Mita",
    "Economic Shocks and Civil Conflict: An Instrumental Variables Approach",
    "Ruggedness: The Blessing of Bad Geography in Africa",
    "Railroads and American Economic Growth: A Market Access Approach",
    "Trade Integration, Market Size, and Industrialization: Evidence from China's National Trunk Highway System",
    "Rural Roads and Local Economic Development",
    "The Permanent Effects of Transportation Revolutions in Poor Countries: Evidence from Africa",
    "The Value of Democracy: Evidence from Road Building in Kenya",
    "The Effects of Rural Electrification on Employment: New Evidence from South Africa",
    "Development Effects of Electrification: Evidence from the Topographic Placement of Hydropower Plants in Brazil",
    "Using Satellite Imagery and Machine Learning to Estimate the Livelihood Impact of Electricity Access",
    "This Mine is Mine! How Minerals Fuel Conflicts in Africa",
    "Pre-Colonial Ethnic Institutions and Contemporary African Development",
    "National Institutions and Subnational Development in Africa",
    "Regional Favoritism",
    "Ethnonationalist Triads: Assessing the Influence of Kin Groups on Civil Wars",
    "Gravity's Rainbow: A Dynamic Latent Space Model for the World Trade Network",
    "Inferential Network Analysis with Exponential Random Graph Models",
    "The Diffusion of Microfinance",
    "Measuring Economic Growth from Outer Space",
    "Combining satellite imagery and machine learning to predict poverty",
    "Machine learning and phone data can improve targeting of humanitarian aid",
    "The changing surface of the world's roads",
    "Aggregation Bias in Proxy Measurement: Nighttime Lights and Local Economic Activity",
    "PRIO-GRID: A unified spatial data structure",
    "Did Highways Cause Suburbanization?",
    "The Effect of the TseTse Fly on African Development",
    "Tourism and Economic Development: Evidence from Mexico's Coastline",
    "Horizontal Inequalities and Ethnonationalist Civil War: A Global Comparison",
    "The Economics of Density: Evidence from the Berlin Wall",
    "Ethnicity, Insurgency, and Civil War",
    "Portage and Path Dependence",
    "Roads and Trade: Evidence from the US",
]

out = []
for t in TITLES:
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(t) +
           "&per-page=3&select=title,publication_year,cited_by_count,doi,authorships,"
           "primary_location,type")
    rec = {"q": t}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mailto:research@example.org"})
            with urllib.request.urlopen(req, timeout=25) as r:
                d = json.loads(r.read().decode("utf-8"))
            res = []
            for w in d.get("results", []):
                auths = [a["author"]["display_name"] for a in w.get("authorships", [])][:6]
                src = (w.get("primary_location") or {}).get("source") or {}
                res.append({
                    "title": w.get("title"),
                    "year": w.get("publication_year"),
                    "cites": w.get("cited_by_count"),
                    "doi": w.get("doi"),
                    "venue": src.get("display_name"),
                    "authors": auths,
                })
            rec["res"] = res
            break
        except Exception as e:
            rec["err"] = repr(e)[:140]
            time.sleep(2)
    out.append(rec)
    time.sleep(0.25)

p = os.path.join(os.environ.get("TEMP", "."), "oa_out.json")
with open(p, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("wrote", p, len(out))
